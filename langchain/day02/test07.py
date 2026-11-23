from typing import Any, Dict, List, Tuple

from pymilvus import MilvusClient, AnnSearchRequest, RRFRanker
from FlagEmbedding import BGEM3FlagModel
from langchain.chat_models import init_chat_model

COLLECTION_NAME = "test_collection"

def get_milvus_client(uri:str = "http://localhost:19530",token:str = ""):
	return MilvusClient(uri=uri,token=token)


def get_bge_m3_model():
    return BGEM3FlagModel(model_name_or_path="../../assets/models/bge-m3",use_fp16=False, devices="cpu", batch_size=2)

def encode_query(model,query:str) -> Tuple[List[float],Dict[int,float]]:
    all_embeddings = model.encode([query], return_dense=True, return_sparse=True)
    dense_vecs = all_embeddings["dense_vecs"][0]
    spare_vecs = all_embeddings["lexical_weights"][0]
    return dense_vecs,spare_vecs

def print_hits(title: str, hits: List[dict]):
    print("\n" + "=" * 20)
    print(title)
    print("=" * 20)
    for i, hit in enumerate(hits, start=1):
        entity = hit.get("entity", {})
        print(
            {
                "rank": i,
                "id": entity.get("id"),
                "distance": hit.get("distance"),
                "text": entity.get("text"),
                "metadata": entity.get("metadata"),
            }
        )

def dense_vector_search_example(client,query:str,limit: int =5):
    model = get_bge_m3_model();
    dense_vecs,_ = encode_query(model,query)
    results = client.search(
        collection_name=COLLECTION_NAME,
        data=[dense_vecs],
        anns_field="dense_vecs",
        limit=limit,
        search_params={"metric_type": "L2"},
        output_fields=["id", "text", "metadata"])
    print("稠密向量检索(vector)",results[0])
    return results

def spare_vector_search_example(client,query:str,limit: int =5):
    model = get_bge_m3_model();
    _,spare_vecs = encode_query(model,query)
    results = client.search(
        collection_name=COLLECTION_NAME,
        data=[spare_vecs],
        anns_field="spare_vecs",
        limit=limit,
        search_params={"metric_type": "IP"},
        output_fields=["id", "text", "metadata"])
    print_hits("稀疏向量检索（sparse_vector）", results[0])
    return results

def hybrid_vector_search_example(client,query:str,limit: int =5):
    model = get_bge_m3_model();
    dense_vecs,sparse_vec= encode_query(model,query)
    dense_req = AnnSearchRequest(
        data=[dense_vecs],
        anns_field="dense_vector",
        param={"metric_type": "L2"},
        limit=limit,
    )
    sparse_req = AnnSearchRequest(
        data=[sparse_vec],
        anns_field="sparse_vector",
        param={"metric_type": "IP"},
        limit=limit,
    )
    results = client.hybrid_search(
        collection_name=COLLECTION_NAME,
        reqs=[dense_req, sparse_req],
        ranker=RRFRanker(k=60),
        limit=limit,
        output_fields=["id", "text", "metadata"],
    )
    print_hits("混合向量检索（RRF 融合稠密+稀疏）", results[0])
    return results


#标量检索
def scalar_query_example(client,like_key_word:str="大模型"):
    try:
        like_res = client.query(
            collection_name=COLLECTION_NAME,
            filters=f'text like %"{like_key_word}"%',
            output_fields=["id", "text"],
            limit=5,
        )
        print("\n" + "=" * 20)
        print(f'标量检索（query: text like "%{like_key_word}%"）')
        print("=" * 20)
        for row in like_res:
            print({"id":row.get("id"),"text":row.get("text")})

    except Exception as e:
        print("VARCHAR like 过滤失败：", e)
    try:
        json_res = client.query(
            collection_name=COLLECTION_NAME,
            filter='metadata["source"] like "%sample%"',
            output_fields=["id", "metadata"],
            limit=5,
        )
        print("\n" + "=" * 20)
        print('标量检索（query: metadata["source"] like "%sample%"）')
        print("=" * 20)
        for row in json_res:
            print({"id": row.get("id"), "metadata": row.get("metadata")})
    except Exception as e:
        print("JSON 过滤失败（metadata 结构不匹配或不支持该表达式）：", e)

def rag_demo(client:MilvusClient,query:str):
    llm = init_chat_model(
        model="MiniMax-M3.1-Flash",
        model_provider="openai",  # 提供者
        base_url="https://api.minimax.cn/v1",
        api_key="sk-cp-fyd-8xZZTYZgmpv6s71zVL-nGnzWNfi4tUkHx_Z7ZtUhAEaHyojhvCbD0wTA5psj_-IqrwhpVKYRj9dnCojBpOf2bcXoxFJacAQb7MtgaxYvjCGGMDwhjJs"
    )
    retrieval_res = hybrid_vector_search_example(client=client, query=query)
    context = "\n".join([hit["entity"]["text"] for hit in retrieval_res[0]])
    message_list = [
        {"role": "system", "content": "你是一个专业的法律问答机器人，请根据上下文回答问题，当上下文无法回答问题时，请回答'根据上下文无法回答该问题'"},
         {"role": "user", "content": f"根据以下上下文回答问题：{context}\n问题：{query}"}
    ]
    res = llm.invoke(message_list)
    print(res)


if __name__ == '__main__':
    client = get_milvus_client()
    rag_demo(client,'父母对未成年子女是否具有抚养权？')

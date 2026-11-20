from pymilvus import MilvusClient
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
import numpy as np


def get_client():
	return MilvusClient(uri="http://localhost:19530",token="")


def to_sparse(lexical_weights):
    # Milvus 稀疏向量要 {词元id: 权重}，不能用 indices/values 这种结构
    return {int(i): float(v) for i, v in lexical_weights.items()}


def insert_data(client:MilvusClient,collection_name:str):
    doc_list = UnstructuredWordDocumentLoader("../../assets/sample.docx",
                                              mode="single").load()
    # 2、切分文件
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=50,
                                                   separators=["\n\n","\n","。"])
    splitted_doc_list =text_splitter.split_documents(doc_list)
    splitted_doc_list = splitted_doc_list[0:20]

    # 查看当前文本列表当中最大的文本长度
    max_len = max([len(bytes(doc.page_content.encode("utf-8"))) for doc in splitted_doc_list])
    print('当前最大长度是：',max_len)

    # 3、构建向量：稠密向量，稀疏向量
    from FlagEmbedding import BGEM3FlagModel
    model = BGEM3FlagModel("../../assets/models/bge-m3", use_fp16=False, devices="cpu", batch_size=2) # 避免 MPS 显存不足
    all_vectors = model.encode([doc.page_content for doc in splitted_doc_list], return_dense=True,return_sparse=True)
    dense_vectors = all_vectors["dense_vecs"]
    sparse_vectors = all_vectors['lexical_weights']

    # 4、准备数据：组装成 List[Dict]
    insert_data_list = []
    for doc, dense_vector, sparse_vector in zip(splitted_doc_list, dense_vectors, sparse_vectors):
        insert_data_list.append({
            "dense_vector": np.asarray(dense_vector, dtype=np.float32),
            "sparse_vector": to_sparse(sparse_vector),
            "metadata": doc.metadata,
            "text": doc.page_content
        })

    # 5、调用 client.insert()方法，插入数据
    res = client.insert(
        collection_name=collection_name,
        data=insert_data_list
    )

    # 有多少条数据插入成功
    print(res)

if __name__ == '__main__':
    client = MilvusClient(uri="http://localhost:19530",token="")
    collection_name = "test_collection"
    insert_data(client,collection_name)

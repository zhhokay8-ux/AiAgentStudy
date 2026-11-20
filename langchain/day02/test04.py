from huggingface_hub import create_collection
from langsmith.schemas import DataType
from pymilvus import MilvusClient, DataType
from pprint import pprint

def get_milvus_client():
    client = MilvusClient(
    	uri="http://localhost:19530",
    	token="",
    )
    res = client.list_collections()
    print(res)
    return client

def build_schema(client:MilvusClient):
    schema = client.create_schema(auto_id=True)
    schema.add_field(field_name="id", datatype=DataType.INT64,is_primary=True)
    schema.add_field(field_name="sparse_vector",datatype=DataType.SPARSE_FLOAT_VECTOR) #稀疏向量

    schema.add_field(field_name="dense_vector",datatype=DataType.FLOAT_VECTOR,dim=1024) #稠密向量
    schema.add_field(field_name="text",datatype=DataType.VARCHAR,max_length=1500)
    schema.add_field(field_name="metadata",datatype=DataType.JSON)
    return schema

def build_index(client:MilvusClient):
    #稠密向量
    index_params = client.prepare_index_params()
    index_params.add_index(
        field_name="dense_vector", # 建立索引的字段
        index_type="HNSW",
        metric_type="L2",# 向量相似度度量方式 Cosine(余弦相似度 夹角越小越相似) L2
    )
    #稀疏向量
    index_params.add_index(
        field_name="sparse_vector",
        index_type="SPARSE_INVERTED_INDEX", #倒排索引
        metric_type="IP",
    )
    return index_params

def build_collection(client:MilvusClient):
    client.drop_collection(collection_name="test_collection")
    if not client.has_collection(collection_name="test_collection"):
        client.create_collection(collection_name="test_collection",
                                 schema=build_schema(client),
                                 index_params=build_index(client))
        print(client.list_collections()) #查看collection
        client.describe_collection(collection_name="test_collection")

build_collection(get_milvus_client())


from pymilvus import MilvusClient

def get_client():
	return MilvusClient(uri="http://localhost:19530",token="")

def delete_demo(client):
    res = client.delete(
    collection_name="test_collection",
    	# 过滤条件，仅删除 id 在指定范围内的实体,也可以传递其他字段的过滤条件
    	filter="id in [470595996614359685, 470595996614359686]",
    )
    print(res)


if __name__ == "__main__":
    client = get_client()
    delete_demo(client)
from config import vector_collection
from modules.embedding import embed



# Define a vector search tool
def netflix_search_tool(user_input: str) -> str:
    query_embedding = embed(user_input).tolist()
    pipeline = [
        {
            "$vectorSearch": {
                "index": "netflix_index",
                "queryVector": query_embedding,
                "path": "embedding",
                "exact": True,
                "limit": 5
            }
        }, {
            "$project": {
                "_id": 0,
                "text": 1
            }
        }
    ]
    results = vector_collection.aggregate(pipeline)

    array_of_results = []
    for doc in results:
        array_of_results.append(doc)
    return array_of_results

def hbo_max_search_tool(user_input: str) -> str:
    query_embedding = embed(user_input).tolist()
    pipeline = [
        {
            "$vectorSearch": {
                "index": "hbo_max_index",
                "queryVector": query_embedding,
                "path": "embedding",
                "exact": True,
                "limit": 5
            }
        }, {
            "$project": {
                "_id": 0,
                "text": 1
            }
        }
    ]
    results = vector_collection.aggregate(pipeline)

    array_of_results = []
    for doc in results:
        array_of_results.append(doc)
    return array_of_results

def prime_search_tool(user_input: str) -> str:
    query_embedding = embed(user_input).tolist()
    pipeline = [
        {
            "$vectorSearch": {
                "index": "prime_index",
                "queryVector": query_embedding,
                "path": "embedding",
                "exact": True,
                "limit": 5
            }
        }, {
            "$project": {
                "_id": 0,
                "text": 1
            }
        }
    ]
    results = vector_collection.aggregate(pipeline)

    array_of_results = []
    for doc in results:
        array_of_results.append(doc)
    return array_of_results

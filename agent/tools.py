from config import vector_collection
from embedding import embed

# Define a vector search tool
def vector_search_tool(user_input: str) -> str:
    query_embedding = embed(user_input)
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
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

# Define a simple calculator tool
def calculator_tool(user_input: str) -> str:
    try:
        result = eval(user_input)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}" 
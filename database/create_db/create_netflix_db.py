print("importing rqst_db...")

from rqst_db import *

print("creating client...")

client = chromadb.Client(Settings(persist_directory = 'database/netflix_db'))

print("Creating collection...")
netflix_db = client.create_collection("netflix_db")

data_netflix = pd.read_csv("data/processed_data/netflix_help.csv", index_col=None)

print("Loading embedding...")
start_time = time.time()
embed = hub.load("https://www.kaggle.com/models/google/universal-sentence-encoder/TensorFlow2/universal-sentence-encoder/2")



print(f"Embedding loaded in {time.time() - start_time:.2f} seconds.")
print("Filling collection...")
for i, row in data_netflix.iterrows():
    try:

        chunks = chuncker(row['data'])
        embeddings = [embed([chunk]) for chunk in chunks]
        key_words = [row['Title']]
        print(chunks)

        for j in range(len(chunks)):
            current_id = f'{"NET"}_{i}_{j}'
            print(current_id)       
            netflix_db.add(
                documents=[chunks[j]],
                embeddings=[embeddings[j]],
                ids=[current_id],
                metadatas=[key_words]
            )
            # Depuración
            print(f"ID: {current_id}, Embedding Length: {len(embeddings[j])}, Metadata: {key_words}, texto: {chunks[j]}")
            
    except Exception as e:
        print(f"Error when loading the data: {current_id}")


data = {
    "documents": netflix_db.get_all_documents(),
    "embeddings": netflix_db.get_all_embeddings(),
    "ids": netflix_db.get_all_ids(),
    "metadatas": netflix_db.get_all_metadatas()
}

# Guardar como archivo JSON
with open('database/netflix_db.json', 'w') as file:
    json.dump(data, file)

print("Base de datos guardada en 'database/netflix_db.json'.")
        

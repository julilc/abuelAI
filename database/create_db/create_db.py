
def prepare(path):
    
    print("Loading data...")
    data = pd.read_csv(path, index_col=None)
    print(len(data))

    print("Loading embedding...")
    start_time = time.time()
    embed = hub.load("https://www.kaggle.com/models/google/universal-sentence-encoder/TensorFlow2/universal-sentence-encoder/2")
    print(f"Embedding loaded in {time.time() - start_time:.2f} seconds.")

    return data, embed

def prepare_info(data, embed, main_id):
    documents_all = []
    embeddings_all = []
    ids_all = []
    metadatas_all = []

    for i, row in data.iterrows():
        print(f"Processing row {i}")
        try:
            print(f"Processing row {i} with title: {row[row.index[1]]}")

            chunks = chuncker(row['Info'])
            print(len(chunks))
            if not chunks:
                print(f"No chunks for row {i}")
                continue

            # Crear key_words con todas las columnas
            key_words = {col: row[col] for col in row.index[1:]}

            j = 0
            for p in chunks:

                current_id = f'{main_id}_{i}_{j}'
                embedding = np.array(embed([p])).flatten()
                print(current_id)
                print(len(embedding))

                documents_all.append(p)
                embeddings_all.append(embedding)
                ids_all.append(current_id)
                metadatas_all.append(key_words)

                j += 1

        except Exception as e:
            print(f"Error when processing row {i}: {e}")
        time.sleep(0.1)
    print("Process done")
    
    return documents_all, embeddings_all, ids_all, metadatas_all

def save_db(documents_all, embeddings_all, ids_all, metadatas_all, db_name):
    procesed_data = {
        'documents': documents_all,
        'embeddings' :  [embedding.tolist() for embedding in embeddings_all],
        'ids': ids_all,
        'metadata': metadatas_all
    }
    try:
        json_path = f"database/{db_name}.json"
        with open(json_path, 'w') as file:
                json.dump(procesed_data, file)

        print(f"{db_name} database saved at {json_path}.")
        
    except Exception as e:
        print(f"Error when saving {db_name} database: {e}")
    
import argparse

def parse_args():
    # Configuración para recibir los argumentos
    parser = argparse.ArgumentParser(description="Process data and save it as a JSON file.")
    
    # Argumento para la ruta del archivo CSV
    parser.add_argument(
        'csv_path', 
        type=str, 
        help='The path to the CSV file containing the data'
    )
    
    # Argumento para la ruta del archivo JSON
    parser.add_argument(
        'db_name', 
        type=str, 
        help='The name of the JSON file where data will be saved'
    )

    parser.add_argument(
        'main_id', 
        type=str, 
        help='the main id for the db'
    )

    return parser.parse_args()

if __name__ == '__main__':
    print("Importing rqst_db...")

    from rqst_db import *
    
    # Paso 1: Parsear el argumento de la línea de comandos
    args = parse_args()
    csv_path = args.csv_path  # Obtén la ruta del archivo CSV
    json_path = args.db_name  # Obtén la ruta del archivo JSON
    main_id = args.main_id
    # Paso 2: Preparar el entorno y los datos
    data, embed = prepare(csv_path)

    # Paso 3: Preparar los documentos y sus embeddings
    documents_all, embeddings_all, ids_all, metadatas_all = prepare_info(data, embed, main_id)

    # Paso 4: Guardar la base de datos en un archivo JSON
    save_db(documents_all, embeddings_all, ids_all, metadatas_all, json_path)

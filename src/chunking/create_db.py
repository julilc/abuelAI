
def prepare(path):
    
    print("Loading data...")
    data = pd.read_csv(path, index_col=None)
    print(len(data))

    print("Loading embedding...")
    start_time = time.time()
    embed = SentenceTransformer('all-MiniLM-L6-v2')
    print(f"Embedding loaded in {time.time() - start_time:.2f} seconds.")

    return data, embed

def prepare_info(data, embed, main_id):
    database = []

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
            key_columns = row.index
            key_columns = key_columns.drop('Info')
            key_words = {col: row[col] for col in key_columns}

            j = 0
            for p in chunks:

                current_id = f'{main_id}_{i}_{j}'
                embedding = np.array(embed.encode([p])).flatten()
                print(current_id)
                print(len(embedding))

                object_db = {'id':current_id,'document': p,'embedding':embedding.tolist(), **key_words}
                database.append(object_db)

                j += 1

        except Exception as e:
            print(f"Error when processing row {i}: {e}")
        time.sleep(0.1)
    print("Process done")
    
    return database

def save_db(db_name,database):
    try:
        json_path = f"json_database/{db_name}.json"
        with open(json_path, 'w') as file:
                json.dump(database, file)

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
    database = prepare_info(data, embed, main_id)

    # Paso 4: Guardar la base de datos en un archivo JSON
    save_db(json_path,database)

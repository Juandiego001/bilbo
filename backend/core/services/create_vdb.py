from sqlalchemy.sql import text
from langchain_chroma import Chroma
from langchain.schema import Document
from sqlalchemy.exc import SQLAlchemyError
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_products(Session):
    try:
        with Session() as session:
            statement = text("""
                SELECT * FROM productos WHERE disponibilidad = TRUE;
            """)
            result = session.execute(statement).fetchall()

            # Formatear los resultados como una lista de diccionarios
            products = [
                {
                    "id_producto": row[0],
                    "nombre": row[1],
                    "descripcion": row[2],
                    "precio": row[3],
                    "disponibilidad": row[4],
                }
                for row in result
            ]
            return products
    except SQLAlchemyError as e:
        print(f"Error al obtener productos: {e}")
        return {"message": "Error al obtener productos", "error": str(e), "status": "error"}


def update_vectoredb(DB_PATH, MODEL_NAME, Session):  # for future create a endpoint for update de vectorestore
    '''Update the vector database with the new menu content for the RAG'''

    data = get_products(Session)
    PRODUCT_FILE = f'{DB_PATH}/products.txt'
    with open(PRODUCT_FILE, 'w+', encoding='utf-8') as file:
        for info in data:
            nombre = info['nombre']
            descripcion = info['descripcion'].replace('.', ',')
            precio = info['precio']
            full_text = f'El producto {nombre} tiene {descripcion} cuesta {str(precio)} pesos.'
            file.write(full_text + '\n')

    with open(PRODUCT_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
        docs = [Document(page_content=line) for line in lines]

    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    db = Chroma.from_documents(docs, embeddings, persist_directory=DB_PATH)

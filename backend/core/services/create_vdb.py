from langchain_chroma import Chroma
from langchain.schema import Document
from core.services.products import get_all_products
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter


def update_vectoredb(MODEL_NAME, DB_PATH):  # for future create a endpoint for update de vectorestore
    '''Update the vector database with the new menu content for the RAG'''

    data = get_all_products()['products']
    with open('products.txt', 'w', encoding='utf-8') as file:
        for info in data:
            nombre = info['nombre']
            descripcion = info['descripcion'].replace('.', ',')
            precio = info['precio']
            disponibilidad = info['disponibilidad']
            full_text = f'El producto {nombre} tiene {descripcion} cuesta {str(precio)} pesos.'
            file.write(full_text + '\n')

    def txt_loader(path):
        '''Return a list of documents'''

        with open(path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return [Document(page_content=line) for line in lines]

    docs = txt_loader('products.txt')
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    db = Chroma.from_documents(docs, embeddings, persist_directory=DB_PATH)

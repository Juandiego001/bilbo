from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from core.app import app

def rag (user_query:str ):
    MODEL_NAME = app.config["MODEL_NAME"]
    DB_PATH = app.config["DB_PATH"]

    # Crear los embeddings
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    # Cargar la base de datos vectorial desde el almacenamiento y asignar la función de embeddings
    db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    retriever = db.as_retriever(search_type="mmr",
                                #search_kwargs={'k': 2}
                                )

    retrieved_docs = retriever.invoke(user_query)

    context = " ".join([doc.page_content for doc in retrieved_docs])
    
    return(context)
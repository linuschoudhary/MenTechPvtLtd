import models
from langchain_community.vectorstores import Chroma

vector_store = Chroma(
    embedding_function=models.embedded_model,
    persist_directory="YoutubeVideoDB",
    collection_name='sample_video'
)

vector_store.delete_collection()

vector_store = Chroma(
    embedding_function=models.embedded_model,
    persist_directory="YoutubeVideoDB",
    collection_name='sample_video'
)

def add_chunks(chunks):
    vector_store.add_texts(chunks)

def get_retriever():
    retriever = vector_store.as_retriever(search_type = "similarity",search_kwargs={'k':2})
    return retriever
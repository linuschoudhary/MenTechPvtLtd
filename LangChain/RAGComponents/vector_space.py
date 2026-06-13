from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

embed = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

doc1 = Document(
    page_content= "Virat Kohli: Virat Kohli is one of the most successful and consistent batsmen in IPL history.",
    metadata= {'team': 'Royal Challengers Bangalore'}
)

doc2 = Document(
    page_content = "Rohit Sharma is a legendary opening batsman and captain.",
    metadata= {'team': 'Mumbai Indians'}
)

doc3 = Document(
    page_content= "MS Dhoni is one of the greatest finishers and captains in cricket history.",
    metadata= {'team': 'Chennai Super Kings'}
)

doc4 = Document(
    page_content = "Jasprit Bumrah is a world-class fast bowler known for his lethal yorkers.",
    metadata= {'team': 'Mumbai Indians'}
)

doc5 = Document(
    page_content = "Ravindra Jadeja is a brilliant all-rounder who excels in batting, bowling, and fielding.",
    metadata= {'team': 'Chennai Super Kings'}
)

docs = [doc1,doc2,doc3,doc4,doc5]

vector_store = Chroma(
    embedding_function=embed,
    persist_directory="chroma_db",
    collection_name='sample'
)

#Adding Documents

vector_store.add_documents(docs)

#View documents
vector_store.get(include=['embeddings','documents','metadatas'])

#Searching in vector stor via similarity search

rslt1 = vector_store.similarity_search(
    query='finisher player of the team.',
    k = 1
)

rslt2= vector_store.similarity_search_with_score(
    query = 'who is virat?',
    k = 1,
    # filter={'team': 'rcb'}
)

print(rslt1,"\n",rslt2)
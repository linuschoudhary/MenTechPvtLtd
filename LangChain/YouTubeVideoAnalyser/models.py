from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

embedded_model = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

model = ChatOllama(
    model = "deepseek-r1:1.5b",
    temperature=1
)
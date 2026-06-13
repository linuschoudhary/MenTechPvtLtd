from langchain_community.retrievers import WikipediaRetriever


retriever = WikipediaRetriever(top_k_results=2, lang='en')

query= "doraemon's 45th movie"

docs = retriever.invoke(query)

print(len(docs))

print(docs)

for i, doc in enumerate(docs):
    print(f"---Page-{i}---")
    print(doc.page_content)
    print(f"******MetaData for page {i}********")
    print(doc.metadata)
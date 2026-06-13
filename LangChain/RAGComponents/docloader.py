from langchain_community.document_loaders import WebBaseLoader
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

model = ChatOllama(
    model = "deepseek-r1:1.5b",
    num_ctx=32000,
)

loader = WebBaseLoader(web_path="https://www.amazon.in/Samsung-inches-Vision-Ultra-QA55QEF1AULXL/dp/B0F43CHDSN/ref=asc_df_B0F43CHDSN?mcid=340f6e6e5d203f79846b87e3da4cd972&tag=googleshopdes-21&linkCode=df0&hvadid=709962856271&hvpos=&hvnetw=g&hvrand=5396934445207801821&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9303291&hvtargid=pla-2421091886053&psc=1&hvocijid=5396934445207801821-B0F43CHDSN-&hvexpln=0&gad_source=1")

data = loader.load()


template = PromptTemplate(
    template= "You have given the data: {data} of flipkart item and a question: {question}, answer the question based on the data.",
    input_variables=['data','question']
)

chain = template | model

result = chain.invoke({'data': data,'question' : 'whats the short summary of this product.'})
print(result)
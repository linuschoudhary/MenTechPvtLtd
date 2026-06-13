from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser

model = ChatOllama(
    model = "deepseek-r1:1.5b"
)

template = PromptTemplate(
    template= "Write a joke on given topic: {topic}",
    input_variables=['topic']
)

parser = StrOutputParser()

chain = RunnableSequence(template,model,parser)
print(chain.invoke({'topic':'marvel'}))
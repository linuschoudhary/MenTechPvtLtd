from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate


model = OllamaLLM(
    model = "deepseek-r1:1.5b",
    temperature= .1
    )


template1 = PromptTemplate(
    template= "Write a detailed report on: {topic}",
    input_variables=['topic']
)

template2 = PromptTemplate(
    template= "write a 2 line summary on given text.\n{text}",
    input_variables=['text']
)

chain = template1 | model | template2 | model

result = chain.invoke({'topic':'black hole'})

print(result)
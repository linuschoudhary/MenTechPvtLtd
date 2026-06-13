from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

model = ChatOllama(
    model= "deepseek-r1:1.5b"
)

parser = JsonOutputParser()

template1 = PromptTemplate(
    template= "Give me the 5 facts of given topic:{topic} \n{format_instruction}",
    input_variables= ['topic'],
    partial_variables= {"format_instruction": parser.get_format_instructions()}   
)

chain = template1 | model | parser

result = chain.invoke({'topic':'black hole'})

print(result)
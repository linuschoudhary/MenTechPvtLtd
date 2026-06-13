from langchain_ollama import ChatOllama
from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.prompts import PromptTemplate

schema = [
    ResponseSchema(name = 'fact-1', description= 'fact 1 about the topic'),
    ResponseSchema(name = 'fact-2',description= 'fact 2 about the topic'),
    ResponseSchema(name = 'fact-3',description= "fact 3 about the topic")
]

parser = StructuredOutputParser.from_response_schemas(schema)

template = PromptTemplate(
    template='Give me 3 facts about given topic: {topic}\n {format_instructions}',
    input_variables= ['topic'],
    partial_variables= {'format_instructions':parser.get_format_instructions()}
)

model = ChatOllama(
    model= 'deepseek-r1:1.5b'
)

chain = template | model | parser
result = chain.invoke({'topic':'black hole'})
print(result)
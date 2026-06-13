from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel,Field


model = ChatOllama(
    model = "deepseek-r1:1.5b"
)


class Schema(BaseModel):
    name:str = Field(description="name of the character")
    age:int = Field(description= "age of the character", gt=0)
    movie:str = Field(description="Movie name in which the character appeared.")


parser = PydanticOutputParser(pydantic_object=Schema)

template = PromptTemplate(
    template = 'Get name, age and movie name of a marvel character\n{format_instructions}',
    input_variables=[],
    partial_variables= {'format_instructions':parser.get_format_instructions()}
)

chain = template | model | parser
result = chain.invoke({})
print(result)
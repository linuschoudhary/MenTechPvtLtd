from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_classic.text_splitter import CharacterTextSplitter,Language
text = """
In August 2022, Reuters reported that the European Space Agency (ESA) began initial discussions with SpaceX that could lead to the company's launchers being used temporarily, given that Russia blocked access to Soyuz rockets amid the Russian invasion of Ukraine.[90] Since that invasion and in the greater war between Russia and Ukraine, Starlink was extensively used.[91]

In 2022, SpaceX's Falcon 9 also became the world record holder for the most launches of a single vehicle type in a single year.[92][93][non-primary source needed] SpaceX launched a rocket approximately every six days in 2022, with 61 launches in total. All but one (a Falcon Heavy in November) was on a Falcon 9 rocket.[92]

In September 2023, SpaceX announced that it would cancel one of its current and upcoming live stream missions on YouTube focusing on live streaming them on X.[94]

In November 2023, SpaceX announced it would acquire its parachute supplier Pioneer Aerospace out of bankruptcy for $2.2 million.
"""

code_text = """
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
"""
splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size = 150,
    chunk_overlap = 0
)

chunks = splitter.split_text(code_text)

print(len(chunks))
count = 1
for i in chunks:
    print(f"\n-----Chunk : {count}")
    print(i)
    count+=1
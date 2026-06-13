from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnableSequence


model = ChatOllama(
    model= "deepseek-r1:1.5b"
)


# Templates
template1 = PromptTemplate(
    template= "Write a tweet on {topic}",
    input_variables=['topic']
)

template2 = PromptTemplate(
    template= "Write a linkedin post on {topic}",
    input_variables= ['text']
)

# Parser
parser = StrOutputParser()

runnableparallel = RunnableParallel({
    'twitter': RunnableSequence(template1,model,parser),
    'linkedin': RunnableSequence(template2,model,parser)
})
print(runnableparallel.invoke({'topic':'AI Summit India 2026'}))
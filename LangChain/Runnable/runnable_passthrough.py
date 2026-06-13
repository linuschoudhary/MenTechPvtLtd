from langchain_core.runnables import RunnablePassthrough,RunnableSequence,RunnableParallel
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOllama(
    model = "deepseek-r1:1.5b"
)

template = PromptTemplate(
    template = "Write a Joke on {topic}",
    input_variables= ['topic']
)

passthrough = RunnablePassthrough()
parser = StrOutputParser()

chain = RunnableParallel({
    'joke_topic': RunnablePassthrough(),
    'joke': RunnableSequence(template, model, parser)
})

print(chain.invoke({'topic': 'marvel'}))
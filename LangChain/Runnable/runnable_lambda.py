from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableParallel,RunnablePassthrough,RunnableLambda


model=  ChatOllama(
    model= "deepseek-r1:1.5b",
    temperature=1.9
)

parser = StrOutputParser()

passthrough = RunnablePassthrough()

template1 = PromptTemplate(
    template= "You are an expert child story writer, write a story on topic: {topic}",
    input_variables=['topic']
)

template2 = PromptTemplate(
    template='You are an expert summery creator Agent, create a summary:\n {text}',
    input_variables=['text']
)

def word_count(text):
    count = len(text.split())
    return count


story_chain = RunnableSequence(template1,model,parser)

parallel_chain = RunnableParallel({
    'story_topic': RunnablePassthrough(),
    'story_summary': RunnableSequence({'text':'RunnablePassthrough()'},template2,model,parser),
    'summary_word_count': RunnableLambda(word_count)
})


final_chain = story_chain | parallel_chain

print(final_chain.invoke({'topic':'doraemon'}))
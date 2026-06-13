from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel,RunnableLambda,RunnablePassthrough
from langchain_community.document_loaders import YoutubeLoader
from langchain_classic.vectorstores import Chroma
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser,StrOutputParser
from pydantic import BaseModel
VIDEO_ID = "PGUdWfB8nLg"
loader = YoutubeLoader(video_id=VIDEO_ID,language="en")

data = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 800,
    chunk_overlap = 200
)

chunks= splitter.split_text(data[0].page_content)

embedded_model = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")


vector_store = Chroma(
    embedding_function=embedded_model,
    persist_directory="YoutubeVideoDB",
    collection_name='sample_video'
)

vector_store.delete_collection()

vector_store = Chroma(
    embedding_function=embedded_model,
    persist_directory="YoutubeVideoDB",
    collection_name='sample_video'
)


vector_store.add_texts(chunks)

retriever = vector_store.as_retriever(search_type = "similarity",search_kwargs={'k':2})

def context_generate(context_list):
    final_context = ""
    for page in context_list:
        final_context += page.page_content
    return final_context

# For Generating questions based on asked question.


"""
class Question(BaseModel):
    question: list

question_parser = PydanticOutputParser(pydantic_object=Question)
"""
question_parser = StrOutputParser()

prompt = PromptTemplate(
    template = """You are an Question generator from given context.
    You do not need to say anything extra other than the questions.
    Questions should be very short in length.
    Every Questions should be in newline.
    No extra line shold be blank in between the questions.
    Start with only one line gap in first question's start.
    You Need to provide only 3 questions based on the given context.
    Questions should be from the listeners point of view.
    Question length should not be more than 10 words.
    
    Context: {context}""",
    input_variables=['context'],
    # partial_variables={'format_instruction':question_parser.get_format_instructions()}
)


model = ChatOllama(
    model = "deepseek-r1:1.5b",
    temperature=1
)

retriever_chain = retriever | RunnableLambda(context_generate)

model_chain = prompt | model | question_parser

question_chain = retriever_chain | model_chain

# For generating the Answer for current Question.
prompt = PromptTemplate(
    template = """You are an youtube video analyser using transcript of the video. 
    you will get a context of the video from transcript and a question from user. 
    You need to answer the question by using the provided context. 
    DO NOT USE WORDS LIKE: Based on the transcript provided, here is a summary of the video content.\n
    Context: {context}, Question: {question}""",
    input_variables=['context','question']
)

result_parser = StrOutputParser()

parallel_chain = RunnableParallel({
    "context": retriever | RunnableLambda(context_generate),
    "question": RunnablePassthrough()
})

model_chain = prompt | model | result_parser

result_chain = parallel_chain | model_chain


print('Ask like- Summarize this video.')
while True:
    user_input = input("Query: ")
    if user_input == "/quet":
        break
    
    result = result_chain.invoke(user_input)
    print(result)
    questions = question_chain.invoke(user_input)
    print(f"\nRelated questions to ask:{questions}")
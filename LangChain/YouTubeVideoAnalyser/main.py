from langchain_core.runnables import RunnableParallel,RunnableLambda,RunnablePassthrough
from helper_function import context_generate
from vector_store import add_chunks, get_retriever
import prompts
import models
import parsers
from splitter import get_chunks
from youtube_video_loader import get_transcript_data

transcript_data = get_transcript_data()

chunks = get_chunks(transcript_data)

add_chunks(chunks)

retriever = get_retriever()

# For Questions generation
question_retriever_chain = retriever | RunnableLambda(context_generate)
question_model_chain = prompts.question_prompt | models.model | parsers.parser
question_final_chain = question_retriever_chain | question_model_chain


# For Result Generation
result_parallel_chain = RunnableParallel({
    "context": retriever | RunnableLambda(context_generate),
    "question": RunnablePassthrough()
})

result_model_chain = prompts.answer_prompt | models.model | parsers.parser
result_final_chain = result_parallel_chain | result_model_chain

print('Ask like- Summarize this video.')
while True:
    user_input = input("Query: ")
    if user_input == "/quet":
        break
    
    result = result_final_chain.invoke(user_input)
    print(result)
    questions = question_final_chain.invoke(user_input)
    print(f"\nRelated questions to ask:{questions}")
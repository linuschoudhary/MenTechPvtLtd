from langchain_core.prompts import PromptTemplate

# For Generating questions based on asked question.
question_prompt = PromptTemplate(
    template = """You are an Question generator from given context.
    You do not need to say anything extra other than the questions.
    Questions should be very short in length.
    Every Questions should be in newline.
    No extra line shold be blank in between the questions.
    Start with only one line gap in first question's start.
    You Need to provide only 3 questions based on the given context.
    Questions should be from the listeners point of view and there should be no questions whose answer is out of the context or not available in this context.
    Question length should not be more than 10 words.
    
    Context: {context}""",
    input_variables=['context']
)


# For generating the Answer for current Question.
answer_prompt = PromptTemplate(
    template = """You are an youtube video analyser using transcript of the video. 
    you will get a context of the video from transcript and a question from user. 
    You need to answer the question by using the provided context. 
    DO NOT USE WORDS LIKE: Based on the transcript provided, here is a summary of the video content.\n
    Context: {context}, Question: {question}""",
    input_variables=['context','question']
)

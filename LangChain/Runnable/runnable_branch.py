from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser,StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableBranch,RunnablePassthrough
from pydantic import BaseModel,Field


useremail = """
Subject: Feature Request & Feedback: Loving the new update, but missing dark mode!

Dear TaskFlow Support Team,

I hope this email finds you well.

My name is Alex Mercer, and I have been using TaskFlow Pro for the past six months to help manage my daily freelance projects. First off, I want to say congratulations on the recent v2.4 update—the new dashboard layout is incredibly clean, and the app feels significantly faster than before. The improved loading times have made a noticeable difference in my daily workflow.

However, I wanted to reach out with a piece of feedback regarding accessibility. I often use the application late at night, and the current bright white interface strains my eyes. I was hoping the new update might introduce a native Dark Mode toggle.

Are there any plans to implement a dark or night theme in the upcoming product roadmap? I know many other users in the community would greatly benefit from this feature as well.

Thank you for your hard work and for continuously improving such a fantastic application. I look forward to seeing how TaskFlow grows!

Best regards,

Alex Mercer

alex.mercer99@email.com

MacBook Pro / macOS Sequoia
"""

model = ChatOllama(
    model= "qwen2.5:1.5b"
)

class EmailCategory(BaseModel):
    category: str = Field(description="The category of the email, e.g., 'Feedback', 'Complaint', 'Inquiry'")

parser = PydanticOutputParser(pydantic_object=EmailCategory)

strparser = StrOutputParser()


template1 = PromptTemplate(
    template = "You are an email category creator who create a single category based on given email.\n EMAIL:{email}\n{format_instruction}",
    input_variables=['email'],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

template2 = PromptTemplate(
    template= "Write a professional email reply for the given mail. Address their points directly:\n\n{mail}",
    input_variables= ['mail']
)

category_chain = RunnableSequence(template1, model, parser)

reply_chain = RunnableBranch(
    (lambda x: x.category == "Feedback",RunnableSequence(template2, model, strparser)),
    RunnablePassthrough()

)

final_chain = category_chain | reply_chain

result = final_chain.invoke({'email': useremail})

print(result)

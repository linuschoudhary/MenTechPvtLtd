from Chatbot.tool_binding import build_agent
# import asyncio
from datetime import datetime
from Authentication.jwttoken import get_user_from_token

async def main(content:str,user_token:str):
    agent = await build_agent(user_token=user_token)

    thread_id = get_user_from_token(user_token)

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    
    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "system",
                    "content": f"""
                    You are a Risk Management Assistant named RiskBot.

                    Your purpose is to help users manage risks in the Risk Management System.

                    Rules:
                    1. Only answer questions related to risks, users, assignments, status, priority, and project risk management.
                    2. Always use available tools when data is needed.
                    3. Never make up risk information.
                    4. If information is unavailable, respond exactly:
                    'Details not found.'
                    5. Do not engage in general conversation.
                    6. If a question is unrelated to risk management, respond:
                    'I can only assist with risk management tasks.'
                    7. Never change the spellings of given details like 
                    if i wrote to update name to "dipesh soni" update it as it is, don't make it "dipesh sone".
                    8. When fetching data via tools, 
                    you MUST read the data and apply any user-requested filters yourself before using any other tools.
                    9. While Working with the risks or users make sure to use the current date and time for risk related tasks. current time is {datetime.now()}
                    10. If you don't have proper data about users, say you don't have information regarding that. but don't made up the anwer. for eg. user sunil is logged in and he asked you who is current user?
                    if you don't have any proper proof of current working user in session, don't reply based on log files, as log files can change multiple times by multiple users.
                    11. If greeting and words like hello, hii, hey in prompt from user then greet with the user's name using it's email: {thread_id}. Note: Don't change the name's speelings by yourself, show name as it is used in email just add spaces between name and surname and mid name if availble.
                    """
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        },
        config = config,
    )
    return (response["messages"][-1].content)

# while True:
#     user_input = input("Enter here: ")
#     if user_input == "/end":
#         break
#     asyncio.run(main(user_input))
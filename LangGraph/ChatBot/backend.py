from langgraph.graph import START,END, StateGraph
from langchain_ollama import ChatOllama
from typing import TypedDict,Annotated
from langchain_core.messages import HumanMessage,BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages


model = ChatOllama(
    model="qwen2.5:1.5b",
    temperature=1
)


class State(TypedDict):
    message: Annotated[list[BaseMessage],add_messages]

def chat_model(state: State):
    message = state['message']
    response = model.invoke(message)
    return {"message": [response]}

graph = StateGraph(State)

graph.add_node("chat_model",chat_model)

graph.add_edge(START, 'chat_model')
graph.add_edge('chat_model',END)

checkpointer = InMemorySaver()
workflow = graph.compile(checkpointer=checkpointer)


config = {'configurable':{'thread_id':'1'}}


# while True:
#     user_input = input("Enter Query: ")

#     if user_input == '/end':
#         break

#     message = [HumanMessage(content=user_input)]


#     initial_state = {
#         "message": message
#     }

#     for message_chunk, metadata in workflow.stream(initial_state,config=config,stream_mode='messages'):
#         if message_chunk:
#             print(message_chunk.content,end = "")
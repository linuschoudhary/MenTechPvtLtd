import backend
import streamlit as st


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


with st.sidebar:
    st.header("History")
    
    for message in st.session_state['message_history']:
        with st.chat_message(message['role']):
            st.text(message['content'])

user_input = st.chat_input("Type Here")

if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    message = [backend.HumanMessage(content=user_input)]


    initial_state = {
        "message": user_input
    }
    model_response = backend.workflow.invoke(initial_state,config=backend.config)

    st.session_state['message_history'].append({'role':'AI','content':model_response['message'][-1].content})

    with st.chat_message('AI'):
        st.text(model_response['message'][-1].content)
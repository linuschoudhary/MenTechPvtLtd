import streamlit as st
import requests

CHATBOT_API_URL = "http://127.0.0.1:8000/chatbot/"
LOGIN_FASTAPI_URL = "http://127.0.0.1:8000/login"


st.title("RiskBot")


with st.sidebar:
    st.title("Login")

    username = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        response = requests.post(
            LOGIN_FASTAPI_URL,
            data={
                "username": username,
                "password": password
            }
        )

        if response.status_code == 200:

            token_data = response.json()

            st.session_state["token"] = token_data["access_token"]
            st.session_state["logged_in"] = True

            st.success("Login Successful")

        else:
            st.error("Invalid Credentials")


if "token" not in st.session_state:
    st.warning("Please login first")
    st.stop()

token = st.session_state.get("token")


headers = {
    "Authorization": f"Bearer {token}"
}

if st.session_state.get("logged_in", False):
    user_input = st.chat_input("Enter Your Message here...")
else:
    st.info("Please login to continue.")


if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    response =requests.post(CHATBOT_API_URL,params={"message": user_input},headers=headers)


    with st.chat_message("AI"):
        st.write(response.json())
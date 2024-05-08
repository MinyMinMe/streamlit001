from openai import OpenAI
import streamlit as st

## Load Config, 환경 설정 API를 가지고 온다.
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

## 제목 표시
st.title("ChatGPT Clone 001")

# LLM선언 OpenAI사의 API를 사용한다.
client = OpenAI()

## GPT3 or 4에 대한 모델 선정
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

## 메세지 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

## 사람과 AI간의 대화를 표시한다. 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

## 사용자의 입력을 받는다.
if prompt := st.chat_input("What is up?"):
    # 사람의 입력을 messages 이력에 집어 넣고 
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 사람의 입력을 화면에 표시
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant의 입력을 LLM에게 질의해서 받아 와서 표시한다.
    with st.chat_message("assistant"):
        # Stream을 열었음
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    ## AI의 입력을 messages 이력에 집어 넣음
    st.session_state.messages.append({"role": "assistant", "content": response})

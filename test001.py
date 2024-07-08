import streamlit as st
from langchain.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

## Load Config
#from dotenv import load_dotenv, find_dotenv
#load_dotenv(find_dotenv(), override=True)

st.set_page_config(page_title="🦜🔗 내 맘대로 생성기 ")
st.title('🦜🔗 Adlib - 홍보 문자 생성기')

def generate_response(pkgName, PkgDescription, From, To):
    system_message = """
당신은 광고 카피라이터입니다.
소상공인 사업자를 대상으로 특정 상품을 홍보하는 문구를 쉽지만 위트있게 작성합니다.

작성한 문구는 문자 메세지를 통해서 마케팅에 활용됩니다.

문구는 3문장 내외로 존댓말로 간결하게 작성하고, 수신자가 희망시 SNS 홍보가 가능함을 넣어줍니다.

- 홍보 상품명: {pkgName}
- 상품특징: {PkgDescription}
- 문구 발송 대상: {From}
- 문구 수신 대상: {To}
"""
    prompt = PromptTemplate.from_template(system_message)
    llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()
    
    return chain.invoke({
        "pkgName": pkgName,
        "PkgDescription": PkgDescription,
        "From": From,
        "To": To
    })

# Session state to keep track of input values
if 'reset' not in st.session_state:
    st.session_state.reset = False

def reset_fields():
    st.session_state.reset = True

with st.form('myform'):
  
    pkgName = st.text_input('상품명:', value='' if st.session_state.reset else '으라차차 패키지')
    PkgDescription = st.text_input('상품특징:', value='' if st.session_state.reset else '소상공인을 위한 맞춤형 결합 통신상품, 홍보+AI로봇+경영관리+고객관리 서비스를 제공')
    From = st.text_input('발송 대상:', value='' if st.session_state.reset else 'KT직원')
    To = st.text_input('수신 대상:', value='' if st.session_state.reset else '새로 오픈한 식당 사장님')

    # Reset 버튼
    if st.button('Reset'):
        reset_fields()
        st.experimental_rerun()
    else:
        st.session_state.reset = False
    
    # 전송 버튼이 눌러졌다면 답변 생성
    if st.form_submit_button('생성하기')
    st.markdown(generate_response(pkgName,"","",""))

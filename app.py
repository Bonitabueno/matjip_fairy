import streamlit as st
from llama_cpp import Llama
from datetime import datetime
import pytz

# LLM 모델 로드
# Llama 모델 로드
llm = Llama.from_pretrained(
    repo_id="LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct-GGUF",
    filename="EXAONE-3.5-2.4B-Instruct-BF16.gguf",
    verbose=False
)

# 현재 시간 가져오는 함수
def get_current_time():
    timezone = pytz.timezone('Asia/Seoul')
    return datetime.now(timezone).strftime('%Y.%m.%d.%A - %H:%M:%S')

# 시스템 프롬프트 설정
system_message = (
    "당신은 친절하고 전문적인 인공지능 어시스턴트입니다. 당신의 이름은 상상입니다.\n"
    "모든 응답은 간결하게 대답합니다.\n"
    "모든 질문을 15초 이내에 대답해주세요.\n"
    "사용자가 인사를 할 경우 안녕하세요라고 빠르게 대답합니다."
    f"현재 시간은 {get_current_time()}입니다. \n"
)

# Streamlit UI 구성
st.set_page_config(page_title="상상 AI 챗봇")
st.title("상상 AI 챗봇")
st.caption('AI 어시스턴트와 자유롭게 대화해 보세요!')

# 응답 대기 메시지를 위한 placeholder 설정
placeholder = st.empty()

# 초기 대화 문맥 설정
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = [{"role": "system", "content": system_message}]

if "messages" not in st.session_state:
    st.session_state.messages = []

def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

display_messages()

# 사용자 입력 처리
if prompt := st.chat_input("안녕하세요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # 모델 응답 생성
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        st.text("잠시만 기다려 주세요...")
        response = llm.create_chat_completion(messages=st.session_state.conversation_history)
        bot_response = response.get("choices")[0].get("message").get("content", "")
        response_placeholder.markdown(bot_response)

    # 응답을 메시지 히스토리에 추가
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.session_state.conversation_history.append({"role": "user", "content": prompt})
    st.session_state.conversation_history.append({"role": "assistant", "content": bot_response})

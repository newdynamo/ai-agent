import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
backend_port = os.getenv("PORT_BACKEND", "8600")
BACKEND_URL = f"http://127.0.0.1:{backend_port}"

st.set_page_config(page_title="HYUNDAI LNG SHIPPING", page_icon="ai_assistant/frontend/assets/logo.png", layout="wide")

# Initialize Session States
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# UI Translations Dictionary
TRANSLATIONS = {
    "ko": {
        "title": "HYUNDAI LNG SHIPPING",
        "caption": "PDF 지식 베이스에서 즉각적인 인사이트를 얻으세요.",
        "settings": "⚙️ 설정",
        "theme_label": "테마 설정",
        "light_mode": "🌞 라이트 모드",
        "dark_mode": "🌙 다크 모드",
        "tab_chat": "💬 채팅",
        "tab_docs": "📂 문서 관리",
        "tab_about": "ℹ️ 프로그램 정보",
        "sidebar_header": "⚙️ 설정 및 제어",
        "clear_chat": "🗑️ 대화 기록 삭제",
        "doc_count": "라이브러리 문서 수",
        "welcome": "👋 환영합니다! **문서 관리** 탭에서 PDF를 업로드한 후 여기서 질문을 시작하세요.",
        "suggested_title": "💡 **상황별 추천 질문:**",
        "suggested_q1": "내 문서의 주요 요약은 무엇인가요?",
        "suggested_q2": "'안전 규정'에 대한 모든 언급을 찾아주세요.",
        "suggested_q3": "이 파일들에서 실행 가능한 항목 리스트를 만들어주세요.",
        "chat_input": "문서에 대해 궁금한 점을 물어보세요...",
        "analyzing": "지식 베이스 분석 중...",
        "view_sources": "🔍 출처 보기",
        "upload_header": "📂 문서 관리 지식 베이스",
        "upload_label": "새 PDF 문서 업로드",
        "upload_btn": "➕ 지식 베이스에 추가",
        "upload_success": "성공적으로 색인되었습니다: ",
        "upload_fail": "색인에 실패했습니다. 파일을 확인해주세요.",
        "upload_tip": "💡 **팁**: 대용량 PDF는 페이지별 임베딩 생성 시 시간이 약간 걸릴 수 있습니다.",
        "search_label": "🔍 라이브러리 내 문서 검색",
        "search_placeholder": "파일명 입력...",
        "no_docs": "조건에 맞는 문서가 없습니다.",
        "delete_btn": "🗑️ 삭제",
        "delete_confirm": "정말 '{filename}' 문서를 삭제하시겠습니까?",
        "delete_yes": "예, 삭제합니다",
        "delete_no": "취소",
        "delete_toast": "문서가 삭제되었습니다.",
        "about_header": "ℹ️ AI 문서 분석 비서 소개",
        "how_it_works": """
        이 프로그램은 최신 AI 기술을 사용하여 PDF 문서와 대화할 수 있게 도와줍니다.
        
        ### 작동 원리:
        1. **업로드**: PDF를 업로드하면 텍스트가 여러 조각으로 나뉩니다.
        2. **임베딩**: 텍스트를 수치 데이터(임베딩)로 변환하여 저장합니다.
        3. **검색**: 질문을 하면 시스템이 가장 관련 있는 조각을 찾습니다.
        4. **답변**: AI가 해당 문맥을 바탕으로 정확하고 검증된 답변을 생성합니다.
        
        ### 주요 기능:
        - **RAG (검색 증강 생성)**: 답변은 전적으로 업로드한 파일에 기반합니다.
        - **출처 표기**: 정보가 어느 문서, 어느 페이지에서 나왔는지 항상 명시합니다.
        - **빠른 검색**: 최적화된 벡터 데이터베이스로 대량의 문서도 즉시 검색 가능합니다.
        """,
        "workflow_caption": "RAG 워크플로우 다이어그램",
        "error_backend": "🔴 백엔드 연결 오류",
        "ai_error": "AI 응답 중 오류가 발생했습니다.",
        "conn_error": "AI 엔진 연결 실패: ",
        "lang_selector": "🌐 언어 선택"
    },
    "en": {
        "title": "HYUNDAI LNG SHIPPING",
        "caption": "Unlock insights from your PDF knowledge base instantly.",
        "settings": "⚙️ Settings",
        "theme_label": "Theme Setting",
        "light_mode": "🌞 Light Mode",
        "dark_mode": "🌙 Dark Mode",
        "tab_chat": "💬 Chat",
        "tab_docs": "📂 Documents",
        "tab_about": "ℹ️ About",
        "sidebar_header": "⚙️ Controls",
        "clear_chat": "🗑️ Clear Chat History",
        "doc_count": "Documents In Library",
        "welcome": "👋 Welcome! Upload your documents in the **Documents** tab and start asking questions here.",
        "suggested_title": "💡 **Suggested Questions:**",
        "suggested_q1": "What is the main summary of my documents?",
        "suggested_q2": "Find all mentions of 'safety regulations'.",
        "suggested_q3": "Generate a list of action items from these files.",
        "chat_input": "Ask me anything about your documents...",
        "analyzing": "Analyzing knowledge base...",
        "view_sources": "🔍 View Sources",
        "upload_header": "📂 Document Management Library",
        "upload_label": "Upload New PDF Document",
        "upload_btn": "➕ Add to Knowledge Base",
        "upload_success": "Successfully indexed: ",
        "upload_fail": "Indexing failed. Please check the file.",
        "upload_tip": "💡 **Pro Tip**: Larger PDFs might take a few moments to process for page embedding.",
        "search_label": "🔍 Search documents in library",
        "search_placeholder": "Type filename...",
        "no_docs": "No matching documents found.",
        "delete_btn": "🗑️ Delete",
        "delete_confirm": "Are you sure you want to delete '{filename}'?",
        "delete_yes": "Yes, Delete",
        "delete_no": "Cancel",
        "delete_toast": "Document deleted.",
        "about_header": "ℹ️ About AI Document Assistant",
        "how_it_works": """
        This application allows you to interact with your PDF documents using state-of-the-art AI.
        
        ### How it works:
        1. **Upload**: PDFs are uploaded and split into chunks.
        2. **Embeddings**: Text is converted into numerical vectors (embeddings).
        3. **Search**: When you ask a question, the system finds the most relevant chunks.
        4. **Answer**: The AI uses the context to provide a grounded, accurate response.
        
        ### Features:
        - **RAG (Retrieval-Augmented Generation)**: Answers are based on your files.
        - **Citations**: Always know which document and page the information came from.
        - **Fast Retrieval**: Optimized vector database for instant searching.
        """,
        "workflow_caption": "RAG Workflow Diagram",
        "error_backend": "🔴 Backend Disconnected",
        "ai_error": "AI responded with an error.",
        "conn_error": "Failed to connect to AI engine: ",
        "lang_selector": "🌐 Select Language"
    }
}

T = TRANSLATIONS[st.session_state.lang]

# Dynamic CSS for Theme Switching
if st.session_state.theme == "light":
    bg_color = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
    main_bg = "#f5f7fa"
    card_bg = "white"
    text_color = "#121212"
    sidebar_bg = "#ffffff"
    border_color = "rgba(0,0,0,0.15)"
    input_bg = "rgba(255, 255, 255, 0.9)"
    button_bg = "#ffffff"
    button_text = "#1f2937"
    placeholder_color = "rgba(0,0,0,0.4)"
    hover_bg = "#f9fafb"
else:
    bg_color = "linear-gradient(135deg, #0e1117 0%, #262730 100%)"
    main_bg = "#0e1117"
    card_bg = "#262730"
    text_color = "#ffffff"
    sidebar_bg = "#111727"
    border_color = "rgba(255,255,255,0.2)"
    input_bg = "rgba(38, 39, 48, 0.9)"
    button_bg = "#3d3d5c"
    button_text = "#ffffff"
    placeholder_color = "rgba(255,255,255,0.6)"
    hover_bg = "#4a4a6a"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Base font and global text color */
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    html, body, [data-testid="stAppViewContainer"] {{
        color: {text_color} !important;
    }}

    /* Main background */
    [data-testid="stAppViewContainer"] {{
        background: {bg_color} !important;
    }}
    
    /* Hide Streamlit Header (Deploy button, MainMenu, etc.) */
    [data-testid="stHeader"] {{
        visibility: hidden;
        height: 0;
    }}
    .stAppDeployButton {{
        display: none !important;
    }}
    #MainMenu {{
        visibility: hidden !important;
    }}

    .stChatFloatingInputContainer {{
        bottom: 30px;
        background: {input_bg};
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 5px;
        border: 1px solid {border_color};
    }}

    /* Force input text color and placeholder */
    [data-testid="stChatInput"] textarea {{
        color: {text_color} !important;
    }}
    [data-testid="stChatInput"] textarea::placeholder {{
        color: {placeholder_color} !important;
    }}

    /* Force high contrast on all Streamlit buttons and popover triggers */
    [data-testid^="stBaseButton"],
    button[data-testid="stPopoverButton"] {{
        background-color: {button_bg} !important;
        color: {button_text} !important;
        border: 1px solid {border_color} !important;
        border-radius: 8px;
        transition: all 0.2s ease;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 2.5rem;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}

    [data-testid^="stBaseButton"]:hover,
    button[data-testid="stPopoverButton"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-color: #ff4b4b !important;
        background-color: {hover_bg} !important;
    }}

    /* Source Tags */
    .source-tag {{
        background: {"#e0f2fe" if st.session_state.theme == "light" else "#004a77"};
        color: {"#0369a1" if st.session_state.theme == "light" else "#ffffff"};
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        margin-right: 5px;
        border: 1px solid rgba(0,0,0,0.1);
    }}

    /* Sidebar colors and text */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
    }}
    
    [data-testid="stSidebar"] section {{
        color: {text_color} !important;
    }}

    /* Container/Card style */
    div[data-testid="stVerticalBlock"] > div > div > .stContainer {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
    }}
    
    /* Suggested questions grouping */
    div[data-testid="stHorizontalBlock"] > div > div > .stButton {{
        width: 100%;
    }}

    /* Fix for tabs text color and active state */
    button[data-baseweb="tab"] div {{
        color: {text_color} !important;
        font-weight: 600;
    }}
    
    /* Metrics contrast */
    [data-testid="stMetricValue"] {{
        color: {text_color} !important;
    }}

    /* Fix for popover background and text */
    div[data-testid="stPopover"] {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
    }}

    /* Center Sidebar Logo */
    [data-testid="stSidebar"] [data-testid="stFullScreenFrame"] > div {{
        display: flex;
        justify-content: center;
    }}
    [data-testid="stSidebar"] [data-testid="stImage"] {{
        text-align: center;
        display: flex;
        justify-content: center;
    }}
</style>
""", unsafe_allow_html=True)

# Application Header
col_title, col_actions = st.columns([0.8, 0.2])
with col_title:
    st.title(T["title"])
    st.caption(T["caption"])

with col_actions:
    # Global Settings (Top)
    with st.popover(T["settings"], use_container_width=True):
        st.subheader(T["theme_label"])
        theme_toggle = st.toggle(
            T["dark_mode"] if st.session_state.theme == "light" else T["light_mode"], 
            value=st.session_state.theme == "dark"
        )
        if theme_toggle != (st.session_state.theme == "dark"):
            st.session_state.theme = "dark" if theme_toggle else "light"
            st.rerun()

    # Language Selector (Below Settings)
    selected_lang = st.selectbox(
        T["lang_selector"], 
        options=["ko", "en"], 
        format_func=lambda x: "🇰🇷 한국어" if x == "ko" else "🇺🇸 English",
        index=0 if st.session_state.lang == "ko" else 1,
        key="lang_selector",
        label_visibility="collapsed"
    )
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

# Sidebar - Session Info & General Actions
with st.sidebar:
    st.image("ai_assistant/frontend/assets/logo.png", width=140)
    st.header(T["sidebar_header"])
    
    if st.button(T["clear_chat"], use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    try:
        docs_response = requests.get(f"{BACKEND_URL}/documents")
        if docs_response.status_code == 200:
            docs = docs_response.json()
            st.metric(T["doc_count"], len(docs), delta=f"{len(docs)} / 1000")
    except:
        st.error(T["error_backend"])

# Main Interface with Tabs
tab1, tab2, tab3 = st.tabs([T["tab_chat"], T["tab_docs"], T["tab_about"]])

# --- TAB 1: CHAT ---
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Create Columns 1:3
    col_left, col_right = st.columns([1, 3], gap="large")

    with col_left:
        st.image("ai_assistant/frontend/assets/logo.png", use_container_width=True)
        st.markdown("---")
        st.write(T["suggested_title"])
        
        suggestions = [T["suggested_q1"], T["suggested_q2"], T["suggested_q3"]]
        for i, sug in enumerate(suggestions):
            if st.button(sug, key=f"sug_left_{i}", use_container_width=True):
                st.session_state.pending_query = sug
                st.rerun()

    with col_right:
        # Welcome Message if no chat
        if not st.session_state.messages:
            st.info(T["welcome"])

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "citations" in message and message["citations"]:
                    with st.expander(T["view_sources"]):
                        for cite in message["citations"]:
                            st.markdown(f"<span class='source-tag'>📄 {cite['filename']}</span> (p. {cite['page']})", unsafe_allow_html=True)

        # Chat Input Handling (Note: st.chat_input is always fixed to bottom by default in Streamlit)
        query_to_process = None
        if "pending_query" in st.session_state:
            query_to_process = st.session_state.pop("pending_query")
        
        if prompt := st.chat_input(T["chat_input"]) or query_to_process:
            actual_query = prompt if prompt else query_to_process
            
            st.session_state.messages.append({"role": "user", "content": actual_query})
            with st.chat_message("user"):
                st.markdown(actual_query)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner(T["analyzing"]):
                    try:
                        response = requests.post(f"{BACKEND_URL}/chat", json={"query": actual_query})
                        if response.status_code == 200:
                            data = response.json()
                            answer = data["answer"]
                            citations = data["citations"]
                            
                            unique_citations = []
                            seen = set()
                            for c in citations:
                                cit_key = f"{c['filename']}_{c['page']}"
                                if cit_key not in seen:
                                    unique_citations.append(c)
                                    seen.add(cit_key)
                            
                            message_placeholder.markdown(answer)
                            if unique_citations:
                                with st.expander(T["view_sources"]):
                                    for cite in unique_citations:
                                        st.markdown(f"<span class='source-tag'>📄 {cite['filename']}</span> (p. {cite['page']})", unsafe_allow_html=True)
                            
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": answer, 
                                "citations": unique_citations
                            })
                        else:
                            st.error(T["ai_error"])
                    except Exception as e:
                        st.error(f"{T['conn_error']}{e}")

# --- TAB 2: DOCUMENTS ---
with tab2:
    st.header(T["upload_header"])
    
    upload_col, info_col = st.columns([0.6, 0.4])
    
    with upload_col:
        uploaded_file = st.file_uploader(T["upload_label"], type=["pdf"], label_visibility="collapsed")
        if uploaded_file:
            if st.button(T["upload_btn"], use_container_width=True, type="primary"):
                with st.spinner(f"'{uploaded_file.name}'..."):
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/upload", 
                            files={"file": (uploaded_file.name, uploaded_file.getvalue())}
                        )
                        if response.status_code == 200:
                            st.success(f"{T['upload_success']} {uploaded_file.name}")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(T["upload_fail"])
                    except:
                        st.error(T["error_backend"])

    with info_col:
        st.info(T["upload_tip"])

    st.markdown("---")
    
    # Document Search & List
    search_query = st.text_input(T["search_label"], placeholder=T["search_placeholder"])
    
    try:
        docs_response = requests.get(f"{BACKEND_URL}/documents")
        if docs_response.status_code == 200:
            all_docs = docs_response.json()
            filtered_docs = [d for d in all_docs if search_query.lower() in d["filename"].lower()] if search_query else all_docs
            
            if not filtered_docs:
                st.write(T["no_docs"])
            
            for doc in filtered_docs:
                with st.container():
                    c1, c2, c3 = st.columns([0.1, 0.7, 0.2])
                    c1.markdown("📄")
                    c2.markdown(f"**{doc['filename']}**")
                    if c3.button(T["delete_btn"], key=f"del_{doc['id']}", use_container_width=True):
                        st.session_state[f"confirm_del_{doc['id']}"] = True
                    
                    if st.session_state.get(f"confirm_del_{doc['id']}", False):
                        st.warning(T["delete_confirm"].format(filename=doc['filename']))
                        conf_1, conf_2 = st.columns(2)
                        if conf_1.button(T["delete_yes"], key=f"yes_{doc['id']}", type="primary"):
                            del_resp = requests.delete(f"{BACKEND_URL}/documents/{doc['id']}")
                            if del_resp.status_code == 200:
                                st.toast(T["delete_toast"])
                                st.session_state.pop(f"confirm_del_{doc['id']}")
                                st.rerun()
                        if conf_2.button(T["delete_no"], key=f"no_{doc['id']}"):
                            st.session_state.pop(f"confirm_del_{doc['id']}")
                            st.rerun()
                st.divider()
    except:
        st.error(T["error_backend"])

# --- TAB 3: ABOUT ---
with tab3:
    st.header(T["about_header"])
    st.markdown(T["how_it_works"])
    st.image("https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/static/img/langchain_flow.png", caption=T["workflow_caption"])

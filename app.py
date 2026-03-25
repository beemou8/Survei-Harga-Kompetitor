import streamlit as st

st.set_page_config(page_title="Survei Harga", layout="centered")

st.markdown("""
    <style>
        [data-testid="stSidebar"], 
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarCollapseButton"] {
            display: none !important;
            width: 0px !important;
        }
        .main .block-container {
            margin-left: auto;
            margin-right: auto;
            max-width: 600px;
        }
        header {
            visibility: hidden;
            height: 0px;
        }
    </style>
""", unsafe_allow_html=True)

if 'user_data' not in st.session_state:
    from pages.login import show_login
    show_login()
else:
    from pages.dashboard import show_dashboard
    show_dashboard()
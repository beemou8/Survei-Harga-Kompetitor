import streamlit as st
from services.auth import login_proses

def show_login():
    st.markdown("""
        <style>
            [data-testid="stSidebar"], 
            [data-testid="stSidebarNav"],
            [data-testid="stSidebarCollapseButton"] {
                display: none !important;
                width: 0px !important;
            }
            .main .block-container {
                max-width: 500px;
                padding-top: 5rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("📊 Survei Harga")
    st.caption("Please login to continue")

    st.divider()

    # Kita buat container kosong di luar form untuk pesan error
    placeholder = st.empty()

    with st.form("form_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", use_container_width=True)

        if submit:
            if not username or not password:
                st.warning("Username and password are required")
            else:
                with st.spinner("Authenticating..."):
                    user = login_proses(username, password)

                    if user:
                        st.session_state['user_data'] = user
                        st.success(f"Welcome, {user.get('nama_lengkap', username)}")
                        st.rerun()
                    else:
                        # Pesan ini akan muncul jika login_proses return None
                        st.error("Invalid username or password")

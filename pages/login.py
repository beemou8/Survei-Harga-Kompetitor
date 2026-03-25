# pages/login_page.py
import streamlit as st
from services.auth import login_proses  # import dari folder services

if "user_data" not in st.session_state:
    st.session_state["user_data"] = None

def show_login():
    st.title("📊 Survei Babi")
    st.caption("Silakan login untuk mengakses dashboard")
    st.divider()

    with st.form("form_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Masuk")

        if submit:
            if not username or not password:
                st.warning("⚠️ Username dan password wajib diisi!")
            else:
                with st.spinner("Menghubungkan ke Supabase..."):
                    user = login_proses(username, password)
                    if user:
                        st.session_state["user_data"] = user
                        st.success(f"✅ Selamat datang, {user.get('nama_lengkap', 'User')}!")
                        st.experimental_rerun()
                    else:
                        st.error("❌ Login gagal")

if st.session_state["user_data"] is None:
    show_login()
else:
    st.write(f"🏠 Dashboard - Selamat datang {st.session_state['user_data']['nama_lengkap']}")
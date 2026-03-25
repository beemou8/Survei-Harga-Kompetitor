import streamlit as st
from services.auth import login_proses

def show_login():
    # Styling CSS agar tampilan bersih tanpa sidebar
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarNav"] {display: none !important;}
            .main .block-container {max-width: 500px; padding-top: 5rem;}
        </style>
    """, unsafe_allow_html=True)

    st.title("📊 Survei Harga")
    st.caption("Masukan kredensial untuk akses Dashboard EDP 2T")
    st.divider()

    # Gunakan Form agar input tertata
    with st.form("form_login"):
        username = st.text_input("Username", placeholder="Username...")
        password = st.text_input("Password", type="password", placeholder="Password...")
        submit = st.form_submit_button("Masuk", use_container_width=True)

        if submit:
            if not username or not password:
                st.warning("⚠️ Isi username dan password!")
            else:
                with st.spinner("Otentikasi..."):
                    user = login_proses(username, password)

                    if user:
                        st.session_state['user_data'] = user
                        st.success(f"✅ Halo {user.get('nama_lengkap')}!")
                        st.rerun()
                    else:
                        st.error("❌ Login gagal. Cek log di atas atau periksa username/password.")

    st.divider()
    st.caption("Katapang (2T) - 2026")
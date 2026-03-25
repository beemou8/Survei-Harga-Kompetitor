import streamlit as st
from services.auth import login_proses

def show_login():

    st.title("📊 Survei Harga")
    st.caption("Silakan login untuk masuk ke sistem")

    st.divider()

    # form login
    with st.form("form_login"):

        # input username & password
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        tombol_login = st.form_submit_button("Masuk", use_container_width=True)

        # ketika tombol diklik
        if tombol_login:

            # validasi input
            if not username or not password:
                st.warning("Username dan password wajib diisi")
                return

            # proses login
            with st.spinner("Sedang login..."):
                user = login_proses(username, password)

                # kalau berhasil
                if user:
                    st.session_state['user_data'] = user
                    st.success(f"Selamat datang, {user['nama_lengkap']}")
                    st.rerun()

                # kalau gagal
                else:
                    st.error("Username atau password salah")
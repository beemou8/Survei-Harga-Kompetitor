import streamlit as st
from login import show_login  # Pastikan path import benar

# Inisialisasi Session State
if 'user_data' not in st.session_state:
    show_login()
else:
    # TAMPILAN SETELAH LOGIN BERHASIL
    user = st.session_state['user_data']
    st.title(f"Dashboard {user['role']}")
    st.write(f"Selamat datang kembali, **{user['nama_lengkap']}** (Cabang: {user['cabang']})")
    
    if st.button("Logout"):
        del st.session_state['user_data']
        st.rerun()
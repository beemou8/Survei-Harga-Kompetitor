import streamlit as st
import requests
import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

def show_add_user():

    st.subheader("Tambah User Baru")

    with st.form("form_add_user"):

        nama = st.text_input("Nama Lengkap")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        cabang = st.text_input("Cabang")
        role = st.selectbox("Role", ["user", "admin"])

        submit = st.form_submit_button("Simpan")

        if submit:

            if not nama or not username or not password:
                st.warning("Semua field wajib diisi")
                return

            # hash password
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

            data = {
                "nama_lengkap": nama,
                "username": username,
                "password_hash": hashed,
                "cabang": cabang,
                "role": role
            }

            headers = {
                "apikey": KEY,
                "Authorization": f"Bearer {KEY}",
                "Content-Type": "application/json"
            }

            res = requests.post(f"{URL}/rest/v1/users", json=data, headers=headers)

            if res.status_code in [200, 201]:
                st.success("User berhasil ditambahkan")
            else:
                st.error(res.text)
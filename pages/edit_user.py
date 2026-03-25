import streamlit as st
import requests
import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

def get_users():
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    }
    r = requests.get(f"{URL}/rest/v1/users?select=id,username,nama_lengkap,cabang,role", headers=headers)
    return r.json()

def show_edit_user():

    st.subheader("✏️ Edit User")

    users = get_users()

    if not users:
        st.warning("Tidak ada user")
        return

    user_map = {f"{u['username']} ({u['nama_lengkap']})": u for u in users}

    selected = st.selectbox("Pilih User", list(user_map.keys()))
    user_data = user_map[selected]

    with st.form("form_edit_user"):

        nama = st.text_input("Nama Lengkap", value=user_data['nama_lengkap'])
        cabang = st.text_input("Cabang", value=user_data['cabang'])
        role = st.selectbox("Role", ["user", "admin"], index=0 if user_data['role']=="user" else 1)

        st.markdown("### 🔐 Ganti Password (opsional)")
        password = st.text_input("Password Baru", type="password")

        submit = st.form_submit_button("Update User")

        if submit:

            data = {
                "nama_lengkap": nama,
                "cabang": cabang,
                "role": role
            }

            # 🔥 kalau isi password → hash
            if password:
                hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                data["password_hash"] = hashed

            headers = {
                "apikey": KEY,
                "Authorization": f"Bearer {KEY}",
                "Content-Type": "application/json"
            }

            try:
                res = requests.patch(
                    f"{URL}/rest/v1/users?id=eq.{user_data['id']}",
                    json=data,
                    headers=headers
                )

                if res.status_code in [200, 204]:
                    st.success("User berhasil diupdate!")
                else:
                    st.error(res.text)

            except Exception as e:
                st.error(f"Error: {e}")
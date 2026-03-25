# services/auth.py
import requests
import bcrypt
import streamlit as st

def login_proses(username, password):
    SUPABASE_URL = st.secrets.get("SUPABASE_URL")
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")  # service_role key

    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("❌ Supabase config tidak ditemukan!")
        return None

    endpoint = f"{SUPABASE_URL}/rest/v1/users?username=eq.{username}&select=nama_lengkap,password_hash,role,cabang"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    try:
        r = requests.get(endpoint, headers=headers)
        if r.status_code != 200:
            st.error(f"⚠️ Supabase Error ({r.status_code}): {r.text}")
            return None

        res = r.json()
        if not res:
            st.warning(f"🔍 User '{username}' tidak ditemukan")
            return None

        user = res[0]
        stored_password = user["password_hash"].strip()
        password = password.strip()

        if stored_password.startswith("$2b$"):
            if bcrypt.checkpw(password.encode(), stored_password.encode()):
                return user
            else:
                st.error("❌ Password salah")
                return None
        else:
            if password == stored_password:
                return user
            else:
                st.error("❌ Password salah")
                return None

    except Exception as e:
        st.error(f"🚫 Kesalahan Sistem: {str(e)}")
        return None
    
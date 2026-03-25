import requests
import os
import bcrypt
import streamlit as st
from dotenv import load_dotenv

# Load local .env
load_dotenv()

# Ambil Config dari Secrets (Cloud) atau .env (Local)
URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

def login_proses(username, password):
    # 1. Cek apakah variabel koneksi ada
    if not URL or not KEY:
        st.error("❌ Konfigurasi database tidak ditemukan di Secrets!")
        return None

    # 2. Siapkan Endpoint & Headers
    endpoint = f"{URL}/rest/v1/users?username=eq.{username}&select=nama_lengkap,cabang,password_hash,role"
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    }

    try:
        # 3. Request ke Supabase
        r = requests.get(endpoint, headers=headers)
        
        # DEBUG: Jika koneksi API gagal (misal 401 Unauthorized)
        if r.status_code != 200:
            st.error(f"⚠️ Error Database ({r.status_code}): {r.text}")
            return None

        res = r.json()

        # 4. Jika User ditemukan
        if res:
            user = res[0]
            stored_password = user['password_hash']
            
            # Bersihkan spasi
            password = password.strip()
            stored_password = stored_password.strip()

            # --- CEK PASSWORD ---
            # Jika pakai Bcrypt
            if stored_password.startswith("$2b$"):
                if bcrypt.checkpw(password.encode(), stored_password.encode()):
                    return user
            # Jika pakai Plaintext (Lama)
            else:
                if password == stored_password:
                    return user
        else:
            # DEBUG: Jika username tidak ada di tabel
            st.warning(f"🔍 User '{username}' tidak terdaftar di database.")

        return None

    except Exception as e:
        st.error(f"🚫 Kesalahan Sistem: {str(e)}")
        return None
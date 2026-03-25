import requests
import os
import bcrypt
import streamlit as st
from dotenv import load_dotenv

# Load config dari .env (untuk lokal)
load_dotenv()

# Ambil Config dari Secrets Streamlit (Cloud) atau .env (Lokal)
URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

def login_proses(username, password):
    # Cek apakah variabel config terbaca
    if not URL or not KEY:
        st.error("❌ Konfigurasi SUPABASE_URL atau SUPABASE_KEY tidak ditemukan!")
        return None

    # Endpoint untuk cek user berdasarkan username
    endpoint = f"{URL}/rest/v1/users?username=eq.{username}&select=nama_lengkap,cabang,password_hash,role"
    
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    }

    try:
        r = requests.get(endpoint, headers=headers)
        
        # DEBUG: Jika API Supabase error (misal Key salah/401)
        if r.status_code != 200:
            st.error(f"⚠️ Error Database ({r.status_code}): {r.text}")
            return None

        res = r.json()

        if res:
            user = res[0]
            stored_password = user['password_hash']
            
            # Bersihkan spasi jika ada
            password = password.strip()
            stored_password = stored_password.strip()

            # --- CEK PASSWORD ---
            # 1. Jika password di database adalah hash Bcrypt
            if stored_password.startswith("$2b$"):
                if bcrypt.checkpw(password.encode(), stored_password.encode()):
                    return user
            # 2. Jika password di database masih Plaintext (Lama)
            else:
                if password == stored_password:
                    return user
        else:
            # DEBUG: Jika username tidak ditemukan di tabel
            st.warning(f"🔍 Username '{username}' tidak ditemukan di database.")

        return None

    except Exception as e:
        st.error(f"🚫 Kesalahan Sistem: {str(e)}")
        return None
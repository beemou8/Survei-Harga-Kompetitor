import requests
import os
import bcrypt
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

def login_proses(username, password):
    if not URL or not KEY:
        return None

    endpoint = f"{URL}/rest/v1/users?username=eq.{username}&select=nama_lengkap,cabang,password_hash,role"import requests
import os
import bcrypt
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

def login_proses(username, password):
    # CEK APAKAH VARIABLE KONSISTEN
    if not URL or not KEY:
        st.error("Gagal konek: URL atau KEY tidak ditemukan di Secrets!")
        return None

    endpoint = f"{URL}/rest/v1/users?username=eq.{username}&select=nama_lengkap,cabang,password_hash,role"
    
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    }

    try:
        r = requests.get(endpoint, headers=headers)
        
        # JIKA API SUPABASE ERROR (401 atau 404)
        if r.status_code != 200:
            st.error(f"Error Database: {r.status_code} - {r.text}")
            return None

        res = r.json()

        if res:
            user = res[0]
            stored_password = user['password_hash']
            
            password = password.strip()
            stored_password = stored_password.strip()

            if stored_password.startswith("$2b$"):
                if bcrypt.checkpw(password.encode(), stored_password.encode()):
                    return user
            else:
                if password == stored_password:
                    return user
        else:
            st.warning(f"User '{username}' tidak ditemukan di tabel users.")

        return None
    except Exception as e:
        st.error(f"Terjadi kesalahan teknis: {str(e)}")
        return None
    
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    }

    try:
        r = requests.get(endpoint, headers=headers)
        res = r.json()

        if res:
            user = res[0]
            stored_password = user['password_hash']

            password = password.strip()
            stored_password = stored_password.strip()

            # Bcrypt check
            if stored_password.startswith("$2b$"):
                if bcrypt.checkpw(password.encode(), stored_password.encode()):
                    return user
            # Plaintext check
            else:
                if password == stored_password:
                    return user

        return None
    except Exception as e:
        return None

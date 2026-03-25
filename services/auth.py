# login_supabase_app.py
import streamlit as st
import requests
import bcrypt
import os

# =========================================
# 1️⃣ Ambil Config dari Secrets / .env
# =========================================
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")  # service_role key!

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("❌ Supabase config tidak ditemukan! Tambahkan di Secrets atau .env")
    st.stop()

# =========================================
# 2️⃣ Inisialisasi session_state untuk user
# =========================================
if "user" not in st.session_state:
    st.session_state.user = None

# =========================================
# 3️⃣ Fungsi login
# =========================================
def login_user(username: str, password: str):
    """
    Login user dengan username & password ke Supabase REST API
    """
    endpoint = f"{SUPABASE_URL}/rest/v1/users?username=eq.{username}&select=nama_lengkap,password_hash,role,cabang"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
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

        # Cek bcrypt hash
        if stored_password.startswith("$2b$"):
            if bcrypt.checkpw(password.encode(), stored_password.encode()):
                return user
            else:
                st.error("❌ Password salah")
                return None
        else:
            # Plaintext legacy
            if password == stored_password:
                return user
            else:
                st.error("❌ Password salah")
                return None

    except Exception as e:
        st.error(f"🚫 Kesalahan Sistem: {str(e)}")
        return None

# =========================================
# 4️⃣ Tampilkan login form jika user belum login
# =========================================
if st.session_state.user is None:
    st.title("🔑 Login Supabase")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        user = login_user(username, password)
        if user:
            st.session_state.user = user
            st.success(f"✅ Login berhasil! Halo, {user['nama_lengkap']} ({user['role']})")
            st.experimental_rerun()  # Rerun supaya tampil halaman utama
else:
    # =========================================
    # 5️⃣ Halaman setelah login
    # =========================================
    st.title("🏠 Dashboard")
    st.write(f"Selamat datang, **{st.session_state.user['nama_lengkap']}** dari cabang **{st.session_state.user['cabang']}**")
    
    # Logout
    if st.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()
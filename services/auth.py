import requests
import os
import bcrypt
from dotenv import load_dotenv

# ambil config dari .env
load_dotenv()
url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

def login_proses(username, password):
    """
    fungsi untuk login user
    cek ke database → cocokkan password
    """

    endpoint = f"{URL}/rest/v1/users?username=eq.{username}&select=nama_lengkap,cabang,password_hash,role"

    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    }

    try:
        # ambil data user dari database
        r = requests.get(endpoint, headers=headers)
        res = r.json()

        if res:
            user = res[0]

            stored_password = user['password_hash']

            # bersihin spasi (kadang bikin gagal login)
            password = password.strip()
            stored_password = stored_password.strip()

            # =========================
            # CEK JENIS PASSWORD
            # =========================

            # kalau sudah hash bcrypt
            if stored_password.startswith("$2b$"):
                if bcrypt.checkpw(password.encode(), stored_password.encode()):
                    return user

            # kalau masih plaintext (lama)
            else:
                if password == stored_password:
                    return user

        return None

    except Exception as e:
        print("Error login:", e)
        return None

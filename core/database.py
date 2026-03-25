import requests
import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

def login_user(username, password):
    # Kita cek data ke tabel users lewat jalur API (HTTP)
    # Jalur ini 99% tembus firewall kantor
    endpoint = f"{URL}/rest/v1/users?username=eq.{username}&password_hash=eq.{password}&select=nama_lengkap"
    
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(endpoint, headers=headers)
        data = response.json()
        if data and len(data) > 0:
            return data[0]['nama_lengkap']
        return None
    except Exception as e:
        return f"Error: {e}"
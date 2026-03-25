def login_proses(username, password):
    SUPABASE_URL = st.secrets.get("SUPABASE_URL")
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
    
    st.write("DEBUG: URL", SUPABASE_URL)
    st.write("DEBUG: KEY OK?", "Yes" if SUPABASE_KEY else "No")
    st.write("DEBUG: username input", username)
    
    endpoint = f"{SUPABASE_URL}/rest/v1/users?username=eq.{username}&select=nama_lengkap,password_hash,role,cabang"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    
    try:
        r = requests.get(endpoint, headers=headers)
        st.write("DEBUG: Status code", r.status_code)
        st.write("DEBUG: Response text", r.text)
        
        res = r.json()
        st.write("DEBUG: JSON result", res)
        
        # lanjutkan proses password...
        
    except Exception as e:
        st.write("DEBUG: Exception terjadi:", str(e))
        return None
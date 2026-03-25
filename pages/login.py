import streamlit as st
from services.auth import login_proses

def show_login():
    # --- 1. Styling UI ---
    st.markdown("""
        <style>
            [data-testid="stSidebar"], 
            [data-testid="stSidebarNav"],
            [data-testid="stSidebarCollapseButton"] {
                display: none !important;
                width: 0px !important;
            }
            .main .block-container {
                max-width: 500px;
                padding-top: 5rem;
            }
            .stForm {
                border: 1px solid #333;
                padding: 20px;
                border-radius: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- 2. Header ---
    st.title("📊 Survei Harga")
    st.caption("Silakan login untuk mengakses dashboard EDP SPI 2T")
    st.divider()

    # --- 3. Form Login ---
    # Kita bungkus dalam container agar rapi
    with st.container():
        with st.form("form_login_utama"):
            username = st.text_input("Username", placeholder="Masukkan username...")
            password = st.text_input("Password", type="password", placeholder="Masukkan password...")
            
            # Tombol login
            submit = st.form_submit_button("Masuk Sekarang", use_container_width=True)

            if submit:
                if not username or not password:
                    st.warning("⚠️ Username dan password wajib diisi!")
                else:
                    with st.spinner("Menghubungkan ke Supabase..."):
                        # Panggil fungsi login dari auth.py
                        user = login_proses(username, password)

                        if user:
                            # Jika login berhasil, simpan ke session
                            st.session_state['user_data'] = user
                            st.success(f"✅ Selamat datang, {user.get('nama_lengkap', 'User')}!")
                            st.rerun()
                        else:
                            # Jika user None, pesan error detail dari auth.py 
                            # otomatis akan muncul di layar karena kita pakai st.error di sana.
                            st.error("❌ Login gagal. Periksa kembali username/password atau koneksi database.")

    # --- 4. Debugger Area (Hanya muncul jika ada error di background) ---
    st.divider()
    st.caption("Status Sistem: Terhubung ke Streamlit Cloud")

# Pastikan fungsi ini dipanggil di app.py
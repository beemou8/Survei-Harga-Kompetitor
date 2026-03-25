import streamlit as st
from pages.login import show_login
from pages.dashboard import show_dashboard

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Survei Harga 2T",
    page_icon="📊",
    layout="centered"
)

# =========================
# STYLE SEDERHANA (BIAR RAPIH)
# =========================
st.markdown("""
<style>

/* background gelap biar adem */
html, body, [class*="css"] {
    background-color: #0f172a;
}

/* biar konten di tengah & responsive */
.block-container {
    max-width: 420px;
    margin: auto;
    padding-top: 2rem;
}

/* kalau di tablet */
@media (min-width: 768px) {
    .block-container {
        max-width: 700px;
    }
}

/* kalau di laptop */
@media (min-width: 1024px) {
    .block-container {
        max-width: 1000px;
    }
}

/* teks jadi putih */
h1, h2, h3 {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# CEK LOGIN
# =========================

# kalau belum login → tampilkan login
if 'user_data' not in st.session_state:
    show_login()

# kalau sudah login → masuk dashboard
else:
    show_dashboard()
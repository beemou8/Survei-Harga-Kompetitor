import streamlit as st
import requests
import os
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

# Load .env dari root folder
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

# =========================
# AMBIL DATA SURVEI
# =========================
@st.cache_data(ttl=60)
def get_survei(cabang_filter=None, user_filter=None, date_from=None, date_to=None, limit=500):
    """Ambil data survei dengan filter"""
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    }
    
    query = f"{URL}/rest/v1/survei?select=*&order=created_at.desc&limit={limit}"
    
    if cabang_filter:
        query += f"&cabang=eq.{cabang_filter}"
    if user_filter:
        query += f"&nama_user=eq.{user_filter}"
    
    res = requests.get(query, headers=headers)
    
    if res.status_code != 200:
        return []
    
    data = res.json()
    
    # Filter tanggal manual
    if date_from or date_to:
        filtered = []
        for item in data:
            created_str = item.get('created_at', '')
            if not created_str:
                continue
            
            try:
                created_str = created_str.replace('Z', '+00:00')
                if 'T' in created_str:
                    created_dt = datetime.fromisoformat(created_str)
                else:
                    created_dt = datetime.strptime(created_str, "%Y-%m-%d %H:%M:%S")
                
                created_date = created_dt.date()
                
                if date_from and created_date < date_from:
                    continue
                if date_to and created_date > date_to:
                    continue
                
                filtered.append(item)
            except:
                filtered.append(item)
        
        return filtered
    
    return data

# =========================
# AMBIL FILTER OPTIONS
# =========================
@st.cache_data(ttl=600)
def get_filter_options():
    """Ambil unique cabang dan user"""
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    }
    
    try:
        res_cabang = requests.get(f"{URL}/rest/v1/survei?select=cabang", headers=headers)
        res_user = requests.get(f"{URL}/rest/v1/survei?select=nama_user", headers=headers)
        
        cabang_list = list(set([item['cabang'] for item in res_cabang.json() if item.get('cabang')]))
        user_list = list(set([item['nama_user'] for item in res_user.json() if item.get('nama_user')]))
        
        return sorted(cabang_list), sorted(user_list)
    except:
        return [], []

# =========================
# HALAMAN HISTORY
# =========================
def show_history():
    user = st.session_state.get('user_data', {})
    is_admin = user.get('role') == 'admin'
    
    st.markdown("## 📋 History Survei")
    
    # =========================
    # FILTER
    # =========================
    with st.expander("🔍 Filter Data", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cabang_list, user_list = get_filter_options()
            
            if is_admin:
                cabang_filter = st.selectbox("Cabang", ["Semua"] + cabang_list, index=0)
            else:
                cabang_filter = user.get('cabang', 'Semua')
                st.text_input("Cabang", value=cabang_filter, disabled=True)
        
        with col2:
            if is_admin:
                user_filter = st.selectbox("Surveyor", ["Semua"] + user_list, index=0)
            else:
                user_filter = user.get('nama_lengkap', 'Semua')
                st.text_input("Surveyor", value=user_filter, disabled=True)
        
        with col3:
            limit_data = st.selectbox("Jumlah Data", [50, 100, 200, 500, 1000], index=3)
        
        col4, col5 = st.columns(2)
        with col4:
            date_from = st.date_input("Dari Tanggal", value=datetime.now() - timedelta(days=30))
        with col5:
            date_to = st.date_input("Sampai Tanggal", value=datetime.now())
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    # Convert filter
    cabang_filter = None if cabang_filter == "Semua" else cabang_filter
    user_filter = None if user_filter == "Semua" else user_filter
    
    # =========================
    # AMBIL DATA
    # =========================
    with st.spinner("Memuat data..."):
        data = get_survei(cabang_filter, user_filter, date_from, date_to, limit_data)
    
    if not data:
        st.info("📭 Tidak ada data survei")
        return
    
    # Total data saja
    st.caption(f"Total: {len(data)} data survei")
    
    st.divider()
    
    # =========================
    # TAMPILAN
    # =========================
    view_mode = st.radio("Mode", ["Tabel", "Card Detail"], horizontal=True)
    
    if view_mode == "Tabel":
        df = pd.DataFrame(data)
        display_cols = ['created_at', 'nama_barang', 'nama_kompetitor', 'harga', 'cabang', 'nama_user']
        
        if all(col in df.columns for col in display_cols):
            df_display = df[display_cols].copy()
            df_display['harga'] = df_display['harga'].apply(lambda x: f"Rp {x:,.0f}")
            df_display['created_at'] = pd.to_datetime(df_display['created_at']).dt.strftime('%d/%m/%Y %H:%M')
            df_display.columns = ['Tanggal', 'Produk', 'Kompetitor', 'Harga', 'Cabang', 'Surveyor']
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", csv, f"survei_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
    else:  # Card Detail
        for idx, item in enumerate(data):
            with st.container(border=True):
                col_info, col_foto = st.columns([3, 1])
                
                with col_info:
                    st.markdown(f"### {item.get('nama_barang', '-')}")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"**🏪 Kompetitor:** {item.get('nama_kompetitor', '-')}")
                        st.markdown(f"**💰 Harga:** Rp {item.get('harga', 0):,.0f}")
                    with col_b:
                        st.markdown(f"**📍 Cabang:** {item.get('cabang', '-')}")
                        st.markdown(f"**👤 Surveyor:** {item.get('nama_user', '-')}")
                    
                    created = item.get('created_at', '')
                    if created:
                        try:
                            dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                            st.caption(f"🕐 {dt.strftime('%d %B %Y, %H:%M WIB')}")
                        except:
                            st.caption(f"🕐 {created}")
                
                with col_foto:
                    foto_url = item.get('foto_struk')
                    if foto_url and str(foto_url).startswith('http'):
                        st.image(foto_url, use_container_width=True)
                    else:
                        st.info("📷 Tidak ada foto")
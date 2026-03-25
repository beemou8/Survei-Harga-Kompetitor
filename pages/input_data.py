import streamlit as st
import requests
import os
from dotenv import load_dotenv
from streamlit_searchbox import st_searchbox
from PIL import Image
import io
from datetime import datetime

load_dotenv()
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "foto_struk"  # <-- GANTI JADI UNDERSCORE

# =========================
# COMPRESS FOTO
# =========================
def compress_image(file, max_size=(1200, 1200), quality=60):
    """Compress foto 3MB jadi ~200-300KB"""
    try:
        image = Image.open(file)
        
        # Rotate kalau ada EXIF orientation
        try:
            orientation = image._getexif().get(274)
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
        except:
            pass
        
        # Resize kalau terlalu besar
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert ke RGB (handle PNG dengan transparency)
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        # Compress
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        
        # Info debug
        original_size = len(file.getvalue()) / 1024 / 1024
        compressed_size = len(buffer.getvalue()) / 1024 / 1024
        st.info(f"Foto dikompres: {original_size:.1f}MB → {compressed_size:.1f}MB")
        
        return buffer
        
    except Exception as e:
        st.error(f"Error compress: {e}")
        return file

# =========================
# UPLOAD KE SUPABASE STORAGE
# =========================
def upload_to_storage(file, user_cabang):
    """Upload ke Supabase Storage, return public URL"""
    try:
        # Compress dulu
        compressed = compress_image(file)
        
        # Buat nama file unik
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_cabang = user_cabang.replace(" ", "_").lower()
        extension = "jpg"  # Hasil compress selalu JPG
        
        file_path = f"{safe_cabang}/{timestamp}_{file.name.rsplit('.', 1)[0]}.jpg"
        
        # Upload
        upload_url = f"{URL}/storage/v1/object/{BUCKET_NAME}/{file_path}"
        
        headers = {
            "apikey": KEY,
            "Authorization": f"Bearer {KEY}",
        }
        
        files = {"file": (file_path, compressed, "image/jpeg")}
        
        res = requests.post(upload_url, headers=headers, files=files)
        
        if res.status_code in [200, 201]:
            # Public URL
            public_url = f"{URL}/storage/v1/object/public/{BUCKET_NAME}/{file_path}"
            return public_url
        else:
            st.error(f"Upload gagal: {res.text}")
            return None
            
    except Exception as e:
        st.error(f"Error upload: {e}")
        return None

# =========================
# AMBIL DATA BARANG
# =========================
@st.cache_data
def get_barang():
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    }

    res = requests.get(f"{URL}/rest/v1/barang?select=nama_barang", headers=headers)
    data = res.json()

    result = [
        item['nama_barang'].strip()
        for item in data
        if item.get('nama_barang')
    ]

    return sorted(result)

def search_barang(searchterm: str):
    list_barang = get_barang()
    if not searchterm:
        return list_barang[:50]
    return [item for item in list_barang if searchterm.lower() in item.lower()][:50]

# =========================
# HALAMAN INPUT
# =========================
def show_input():

    user = st.session_state['user_data']

    st.subheader("➕ Input Data Survei")

    st.write(f"Total produk tersedia: {len(get_barang())}")

    # Searchable dropdown
    produk = st_searchbox(
        search_function=search_barang,
        placeholder="Ketik nama produk...",
        label="Pilih Produk",
        default=None,
        clear_on_submit=False,
    )

    # Input lain
    kompetitor = st.text_input("Nama Kompetitor")
    harga = st.number_input("Harga", min_value=0, step=1000)

    foto = st.file_uploader("Upload Foto Struk", type=["jpg", "png", "jpeg"])

    st.caption(f"Disurvei oleh: {user['nama_lengkap']} ({user['cabang']})")

    # Simpan data
    if st.button("Simpan Data", use_container_width=True):

        if not produk:
            st.warning("Produk harus dipilih")
            return

        if not kompetitor:
            st.warning("Nama kompetitor harus diisi")
            return

        if harga <= 0:
            st.warning("Harga harus diisi")
            return

        # Upload foto ke Storage (kalau ada)
        foto_url = None
        if foto:
            with st.spinner("Mengupload foto..."):
                foto_url = upload_to_storage(foto, user['cabang'])
                if not foto_url:
                    st.error("Gagal upload foto, coba lagi")
                    return
                st.success(f"Foto terupload!")

        data = {
            "nama_barang": produk,
            "nama_kompetitor": kompetitor,
            "harga": harga,
            "foto_struk": foto_url,  # URL lengkap dari Supabase Storage
            "nama_user": user['nama_lengkap'],
            "cabang": user['cabang']
        }

        headers = {
            "apikey": KEY,
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json"
        }

        res = requests.post(f"{URL}/rest/v1/survei", json=data, headers=headers)

        if res.status_code in [200, 201]:
            st.success("Data berhasil disimpan!")
            st.rerun()
        else:
            st.error(res.text)
# 📊 Survei Harga Kompetitor

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg.svg)](https://share.streamlit.io/)  
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)  
![License](https://img.shields.io/badge/license-MIT-green)  

Aplikasi manajemen survei harga kompetitor untuk operasional lapangan. Memungkinkan user menginput data produk, harga, dan foto struk secara instan dengan optimasi kompresi otomatis (~3MB → 200KB) untuk efisiensi kuota dan penyimpanan.

---

## ✨ Fitur Utama

- 🔐 **Secure Login** – Autentikasi dengan enkripsi `bcrypt`.  
- 📸 **Smart Image Compression** – Kompresi foto otomatis untuk efisiensi penyimpanan Supabase.  
- 🔍 **Searchable Product** – Pencarian cepat untuk ribuan SKU.  
- 📋 **Data History & Filter** – Monitoring survei berdasarkan Cabang, Surveyor, dan Tanggal.  
- ⚙️ **Admin Control** – Tambah/Edit user langsung dari aplikasi.  
- 📱 **Mobile Friendly** – UI minimalis, optimal untuk smartphone di lapangan.

---

## 🛠 Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)  
- **Backend:** [Supabase](https://supabase.com/) (PostgreSQL & Storage)  
- **Libraries:**  
  - `pandas` – Manipulasi data  
  - `bcrypt` – Security  
  - `Pillow` – Image processing  
  - `requests` – API handling  
  - `streamlit-searchbox` – UI component  
  - `python-dotenv` – Environment management

---

## 📂 Struktur Proyek


survei-harga/
├── app.py # Main entry & routing
├── requirements.txt # Dependencies aplikasi
├── .env # Environment variables lokal
├── .gitignore # File yang diabaikan Git
├── services/
│ └── auth.py # Logika autentikasi & verifikasi bcrypt
├── pages/
│ ├── login.py # UI login
│ ├── dashboard.py # Sidebar & navigasi utama
│ ├── input_data.py # Form input & kompresi foto struk
│ ├── history_data.py # Visualisasi tabel & filter data
│ ├── add_user.py # Admin: tambah pengguna baru
│ └── edit_user.py # Admin: edit pengguna
└── assets/
└── css/ # Kustomisasi tema dark mode & layout


---

## 📥 Panduan Instalasi (Lokal)

1. **Clone repository**
```bash
git clone https://github.com/beemou8/survei-harga.git
cd survei-harga
Install dependencies
pip install -r requirements.txt
Setup environment
Buat file .env di root folder:
SUPABASE_URL=https://project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
Jalankan aplikasi
streamlit run app.py
☁️ Deployment (Streamlit Cloud)
Hubungkan repository ke Streamlit Cloud
.
Masukkan Secrets di menu Advanced Settings:
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
Klik Deploy dan tunggu selesai.
🗄 Skema Database (Supabase)

Tabel users

username (text, Unique)
password_hash (text)
nama_lengkap (text)
cabang (text)
role (text: admin/user)

Tabel survei

nama_barang (text)
nama_kompetitor (text)
harga (numeric)
foto_struk (text/URL)
nama_user (text)
cabang (text)
📧 Kontak & Developer
Developer: beemou8 (EDP 2T Katapang)
Email: dimasbimo19@gmail.com
GitHub: @beemou8

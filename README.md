# 📊 E-Commerce Public Dataset Analysis & Dashboard

Proyek analisis data komprehensif dan dashboard interaktif menggunakan data transaksi nyata dari marketplace **Olist di Brasil (2017-2018)**. Proyek ini dikembangkan untuk memenuhi kriteria submission akhir kelas **Belajar Analisis Data dengan Python** pada program Dicoding.

---

## 🎯 Pertanyaan Bisnis (SMART)

1. **Segmentasi Pelanggan Berbasis RFM**:
   > *Bagaimana segmentasi pelanggan Olist berdasarkan analisis RFM (Recency, Frequency, Monetary) pada periode transaksi 2017-2018 untuk menentukan strategi retensi dan promosi yang tepat?*
2. **Pengaruh Keterlambatan Logistik terhadap Kepuasan**:
   > *Bagaimana performa ketepatan waktu pengiriman pesanan dan pengaruh keterlambatan pengiriman terhadap skor kepuasan pelanggan (review score) di 5 negara bagian teratas Brasil sepanjang tahun 2017-2018?*

---

## 💡 Temuan Utama (Key Insights)

* **Dampak Keterlambatan Logistik**: Pesanan yang tiba tepat waktu (*On Time*) mendapatkan rata-rata skor kepuasan **4,29 / 5,0**, sedangkan pesanan yang terlambat (*Late*) anjlok drastis menjadi **2,57 / 5,0**.
* **Disparitas Regional**: Dari 5 negara bagian dengan transaksi terbanyak, **Rio de Janeiro (RJ)** mengalami tingkat keterlambatan paling tinggi (**13,52%**), jauh melampaui **São Paulo (SP)** yang hanya mencatatkan **5,88%**.
* **Segmentasi RFM**: Mayoritas pelanggan merupakan pembeli satu kali (*single-purchase*) dengan rata-rata pengeluaran 160 BRL. Analisis kuantil RFM memetakan pelanggan ke dalam 4 segmen strategis: *Champions*, *Active / Promising*, *At Risk*, dan *Hibernating*.

---

## 📁 Struktur Direktori

`	ext
submission/
├── dashboard/
│   ├── main_data.csv          # Data bersih teragregasi untuk Streamlit (~20 MB)
│   └── dashboard.py           # Aplikasi dashboard interaktif Streamlit
├── data/                      # Kumpulan berkas mentah CSV E-Commerce
├── notebook.ipynb             # Dokumentasi analisis data lengkap & visualisasi
├── requirements.txt           # Daftar dependensi pustaka Python
├── README.md                  # Dokumentasi proyek
└── url.txt                    # Tautan live dashboard Streamlit Cloud
`

---

## 🚀 Menjalankan Dashboard di Komputer Lokal

### 1. Prasyarat
Pastikan kamu telah menginstal **Python 3.9+** pada sistem.

### 2. Pasang Dependensi
Buka terminal / PowerShell di dalam folder proyek, lalu jalankan:
`ash
pip install -r requirements.txt
`

### 3. Jalankan Aplikasi Streamlit
Jalankan dashboard menggunakan perintah:
`ash
streamlit run dashboard/dashboard.py
`
Aplikasi akan secara otomatis terbuka di peramban web pada alamat http://localhost:8501.

---

## 🌐 Live Dashboard
Aplikasi dashboard ini dapat diakses secara daring melalui Streamlit Community Cloud pada tautan yang tercantum di file url.txt.

---

## 👤 Penulis
* **Nama**: Satria Musthofa 'Azmi
* **Email**: satriamusthofaazmi@gmail.com
* **ID Dicoding**: satriamusthofaazmi

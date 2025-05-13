import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("Data_Insight_5_Streamlit_Ready.csv")

st.title("📊 Dashboard Analisis Daya Tampung Jalur Mandiri PTN - Kelompok 8E")
# Judul dan Deskripsi Insight
st.markdown("""
### 📌 Insight 5: Jalur Mandiri PTN – Daya Tampung dan UKT Tertinggi per Jurusan

Banyak calon mahasiswa mengikuti jalur mandiri di Perguruan Tinggi Negeri (PTN) karena fleksibilitasnya.  
Dashboard ini menampilkan daya tampung dan kisaran UKT pada jalur mandiri di berbagai jurusan PTN tahun 2025/2026.

---

**Disusun oleh Tim:**  
Kelompok 8E – Universitas Sultan Ageng Tirtayasa  
- Shalfa Salsabilla (462)  
- Siti Nurfadiyah (463)  
- Syaeful Rachman (464)  
- Vio Reza Fahlevi (465)
""")

# Statistik Umum
st.markdown("### 📊 Statistik Umum")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Jumlah Program Studi", df['Program Studi'].nunique())
col2.metric("Jumlah PTN", df['Nama Universitas'].nunique())
col3.metric("Total Daya Tampung 2025", int(df['Daya Tampung'].sum()))
col4.metric("UKT Maksimum (Tertinggi)","Rp{int(df['UKT (Gol 1 - Max)'].max()):,}".replace(",", "."))

# Filter Provinsi & Universitas
st.markdown("### 🎛️ Filter Data")
provinsi = st.selectbox("Pilih Provinsi", sorted(df['Provinsi'].unique()))
filtered_df = df[df['Provinsi'] == provinsi]

universitas = st.selectbox("Pilih Universitas", sorted(filtered_df['Nama Universitas'].unique()))
final_df = filtered_df[filtered_df['Nama Universitas'] == universitas]

# Tabel
st.markdown("### 📋 Tabel Program Studi")
st.dataframe(final_df[['Program Studi', 'Daya Tampung', 'UKT (Gol 1 - Max)']])

# Visualisasi
st.markdown("### 📈 Daya Tampung per Program Studi")
chart_data = final_df.groupby('Program Studi')['Daya Tampung'].sum().sort_values(ascending=True)
st.bar_chart(chart_data)

st.markdown("---")
st.caption("Sumber data: Kelompok 8E | Data Jalur Mandiri PTN 2025/2026")

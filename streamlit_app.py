import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("Data_Insight_5_Streamlit_Ready.csv")

# Bersihkan dan ubah kolom UKT ke numerik
df['UKT (Gol 1 - Max)'] = (
    df['UKT (Gol 1 - Max)']
    .astype(str)
    .str.replace(r"[^\d]", "", regex=True)  # Hapus semua karakter non-digit
    .astype(float)
)

# Pastikan kolom UKT bertipe numerik
df['UKT (Gol 1 - Max)'] = pd.to_numeric(df['UKT (Gol 1 - Max)'], errors='coerce')

st.title("📊 Dashboard Analisis Daya Tampung Jalur Mandiri PTN - Kelompok 8E")
st.markdown("""
<div style="
    background-color:rgba(108, 99, 255, 0.1); 
    padding:20px; 
    border-radius:10px; 
    border-left:6px solid #6c63ff;
">
    <h4>📌 Insight 5: Jalur Mandiri PTN – Daya Tampung dan UKT Tertinggi per Jurusan</h4>
    <p>
    Banyak calon mahasiswa mengikuti jalur mandiri di Perguruan Tinggi Negeri (PTN) karena fleksibilitasnya. 
    Dashboard ini menampilkan daya tampung dan kisaran UKT pada jalur mandiri di berbagai jurusan PTN tahun 2025/2026.
    </p>
    <hr style="border-top: 1px dashed #bbb;">
    <b>Disusun oleh Tim:</b><br>
    Kelompok 8E – Universitas Sultan Ageng Tirtayasa<br>
    - Shalfa Salsabilla (462)<br>
    - Siti Nurfadiyah (463)<br>
    - Syaeful Rachman (464)<br>
    - Vio Reza Fahlevi (465)
</div>
""", unsafe_allow_html=True)

# Statistik Umum
st.markdown("### 📊 Statistik Umum")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Jumlah Program Studi", df['Program Studi'].nunique())
col2.metric("Jumlah PTN", df['Nama Universitas'].nunique())
col3.metric("Total Daya Tampung 2025", int(df['Daya Tampung'].sum()))
col4.metric(
    "UKT Maksimum (Tertinggi)",
    f"Rp{int(df['UKT (Gol 1 - Max)'].max()):,}".replace(",", ".")
)

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

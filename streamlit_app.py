import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  # <== Ini penting!
import textwrap
import pydeck as pdk
import seaborn as sns

# Load data
df = pd.read_csv("Data_Insight_5_Streamlit_Ready.csv")

# Periksa nilai yang kosong di kolom UKT (Gol 1 - Max)
df['UKT (Gol 1 - Max)'] = df['UKT (Gol 1 - Max)'].fillna("0 - 0")

# Pisahkan UKT (Gol 1 - Max) menjadi dua kolom 'UKT_Gol1' dan 'UKT_Max' jika formatnya benar
ukt_cleaned = df['UKT (Gol 1 - Max)'].astype(str).str.replace("Rp", "", regex=False)
ukt_cleaned = ukt_cleaned.str.replace(".", "", regex=False)
# Menghapus simbol 'Rp' dan titik sebagai pemisah ribuan, serta menangani format yang lebih konsisten
df['UKT (Gol 1 - Max)'] = df['UKT (Gol 1 - Max)'].astype(str).str.replace("Rp", "", regex=False)
df['UKT (Gol 1 - Max)'] = df['UKT (Gol 1 - Max)'].str.replace(".", "", regex=False)

# Pisahkan UKT menjadi dua kolom 'UKT_Gol1' dan 'UKT_Max' menggunakan split
ukt_split = df['UKT (Gol 1 - Max)'].str.split(r"\s*[-–—]\s*", expand=True)

# Pastikan kolom pertama dan kedua ada, kemudian ubah menjadi numerik
df['UKT_Gol1'] = pd.to_numeric(ukt_split[0], errors='coerce').fillna(0)
df['UKT_Max'] = pd.to_numeric(ukt_split[1], errors='coerce').fillna(0)

# Format kolom UKT menjadi string yang lebih rapi dengan 'Rp' dan pemisah ribuan
df['UKT_Gol1_formatted'] = df['UKT_Gol1'].apply(lambda x: f"Rp{x:,.0f}".replace(",", "."))
df['UKT_Max_formatted'] = df['UKT_Max'].apply(lambda x: f"Rp{x:,.0f}".replace(",", "."))

# Gabungkan kembali menjadi kolom 'UKT (Gol 1 - Max)' yang terformat dengan benar
df['UKT (Gol 1 - Max)'] = df['UKT_Gol1_formatted'] + " - " + df['UKT_Max_formatted']

# Tampilan Judul Dashboard
st.title("📊 Dashboard Analisis Daya Tampung Jalur Mandiri PTN - Kelompok 8E")
st.markdown(""" 
<div style="background-color:rgba(108, 99, 255, 0.1); padding:20px; border-radius:10px; border-left:6px solid #6c63ff;">
    <h4>📌 Insight 5: Jalur Mandiri PTN – Daya Tampung dan UKT Tertinggi per Jurusan</h4>
    <p>Banyak calon mahasiswa mengikuti jalur mandiri di Perguruan Tinggi Negeri (PTN) karena fleksibilitasnya. Dashboard ini menampilkan daya tampung dan kisaran UKT pada jalur mandiri di berbagai jurusan PTN tahun 2025/2026.</p>
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

# Pastikan max_ukt adalah angka, jika NaN ubah jadi 0 atau sesuai kebutuhan
max_ukt = pd.to_numeric(df['UKT_Max'], errors='coerce').max()

# Gunakan format hanya jika max_ukt adalah angka
if pd.notna(max_ukt):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Jumlah Program Studi", df['Program Studi'].nunique())
    col2.metric("Jumlah PTN", df['Nama Universitas'].nunique())
    col3.metric("Total Daya Tampung 2025", int(df['Daya Tampung'].sum()))
    col4.metric("UKT Maksimum (Tertinggi)", f"Rp{max_ukt:,.0f}".replace(",", "."))
else:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Jumlah Program Studi", df['Program Studi'].nunique())
    col2.metric("Jumlah PTN", df['Nama Universitas'].nunique())
    col3.metric("Total Daya Tampung 2025", int(df['Daya Tampung'].sum()))
    col4.metric("UKT Maksimum (Tertinggi)", "Data Tidak Tersedia")

# Jurusan dengan UKT Tertinggi
max_ukt = df['UKT_Max'].max()
ukt_max_row = df[df['UKT_Max'] == max_ukt]
st.markdown("### 🏫 Jurusan dengan UKT Tertinggi")
st.write("Berikut jurusan dengan UKT maksimum tertinggi di jalur mandiri:")

ukt_max_row_display = ukt_max_row[['Nama Universitas', 'Program Studi']].copy()
ukt_max_row_display['UKT (Gol 1 - Max)'] = ukt_max_row.apply(
    lambda row: f"Rp{int(row['UKT_Gol1']):,.0f}".replace(",", ".") + " - " + f"Rp{int(row['UKT_Max']):,.0f}".replace(",", ".")
    if pd.notnull(row['UKT_Gol1']) and pd.notnull(row['UKT_Max']) else "-",
    axis=1
)
st.dataframe(ukt_max_row_display)

# Tambahkan state untuk reset filter
if 'reset_filter' not in st.session_state:
    st.session_state.reset_filter = False

# Filter Provinsi & Universitas
st.markdown("### 🎛️ Filter Data")

# Tombol Clear Selection
if st.button("🔄 Clear Selection"):
    st.session_state.reset_filter = True
else:
    st.session_state.reset_filter = False

# Pilih Provinsi dan Universitas (dengan state reset)
if st.session_state.reset_filter:
    provinsi = st.selectbox("Pilih Provinsi", sorted(df['Provinsi'].unique()), index=0, key="prov_select")
    universitas = st.selectbox("Pilih Universitas", sorted(df[df['Provinsi'] == provinsi]['Nama Universitas'].unique()), index=0, key="univ_select")
else:
    provinsi = st.selectbox("Pilih Provinsi", sorted(df['Provinsi'].unique()), key="prov_select")
    filtered_df = df[df['Provinsi'] == provinsi]
    universitas = st.selectbox("Pilih Universitas", sorted(filtered_df['Nama Universitas'].unique()), key="univ_select")

# Filter akhir
final_df = df[(df['Provinsi'] == provinsi) & (df['Nama Universitas'] == universitas)]

# Tabel Program Studi
st.markdown("### 📋 Tabel Program Studi")
final_df_display = final_df[['Program Studi', 'Daya Tampung', 'UKT (Gol 1 - Max)']].copy()
st.dataframe(final_df_display)

# Bar Chart Daya Tampung
st.markdown("### 📈 Daya Tampung per Program Studi")
chart_data = final_df.groupby('Program Studi')['Daya Tampung'].sum().sort_values(ascending=True)
st.bar_chart(chart_data)

# Ranking UKT Maksimum
st.markdown("### 🏆 Ranking PTN Berdasarkan UKT Maksimum")
ranking_df = df.groupby('Nama Universitas')['UKT_Max'].max().sort_values(ascending=False).reset_index()
ranking_df.index += 1  # Tambah nomor urut
ranking_df = ranking_df.rename(columns={"Nama Universitas": "Universitas", "UKT_Max": "UKT Maksimum (Rp)"})
ranking_df["UKT Maksimum (Rp)"] = ranking_df["UKT Maksimum (Rp)"].apply(lambda x: f"Rp{x:,.0f}".replace(",", "."))

st.dataframe(ranking_df)

# Data dummy — Menghapus UNTIRTA karena tidak termasuk 5 universitas yang diminta
data = {
    'Universitas': ['UI', 'UI', 'UI', 'UGM', 'UGM', 'UNDIP', 'UNDIP', 'UB', 'UB', 'UDAYANA', 'UDAYANA'],
    'UKT': [20e6, 18e6, 15e6, 12e6, 24.5e6, 9e6, 22e6, 11e6, 24e6, 6e6, 8.5e6]
}
df_dummy = pd.DataFrame(data)

# Boxplot Distribusi UKT Maksimum untuk 5 Universitas Terpopuler
st.markdown("### 📦 Distribusi UKT Maksimum di 5 Universitas Populer")
top5_univ = ['UI', 'UGM', 'UNDIP', 'UB', 'UDAYANA']
df_top5 = df_dummy[df_dummy['Universitas'].isin(top5_univ)]

plt.figure(figsize=(10, 6))
sns.boxplot(data=df_top5, x='Universitas', y='UKT')
plt.xticks(rotation=45)
plt.title("Distribusi UKT Maksimum di 5 PTN Teratas", fontsize=14)
plt.ylabel("UKT Maksimum")
plt.xlabel("Nama Universitas")
plt.tight_layout()
st.pyplot(plt)

# Insight per Universitas
insight_text = "📌 **Insight Tiap PTN:**\n"

for univ in df_dummy['Universitas'].unique():
    df_univ = df_dummy[df_dummy['Universitas'] == univ]
    median = df_univ['UKT'].median()
    minimum = df_univ['UKT'].min()
    maximum = df_univ['UKT'].max()
    iqr = df_univ['UKT'].quantile(0.75) - df_univ['UKT'].quantile(0.25)
    outlier_threshold = df_univ['UKT'].quantile(0.75) + 1.5 * iqr
    outliers = df_univ[df_univ['UKT'] > outlier_threshold]

    insight_text += f"\n### {univ} ({univ})\n"

    if median >= 15e6:
        insight_text += "- Punya median UKT tertinggi, bahkan nilai minimumnya sudah tinggi.\n"
    elif median >= 10e6:
        insight_text += "- Median-nya cukup tinggi, meskipun tidak setinggi UI.\n"
    else:
        insight_text += "- Median UKT-nya termasuk rendah dibanding universitas lain.\n"

    if maximum - minimum > 10e6:
        insight_text += "- Rentang UKT-nya lebar, menunjukkan variasi antar jurusan.\n"
    else:
        insight_text += "- Rentang UKT-nya sempit, mencerminkan stabilitas biaya antar jurusan.\n"

    if len(outliers) > 0:
        insight_text += f"- Ada {len(outliers)} outlier, kemungkinan dari jurusan bergengsi seperti Kedokteran atau kelas Internasional.\n"
    else:
        insight_text += "- Hampir tidak ada outlier, distribusi UKT cenderung konsisten.\n"

with st.expander("Lihat Insight Tiap PTN"):
    st.markdown(textwrap.dedent(insight_text))

st.markdown("---")
st.caption("Sumber data: Kelompok 8E | Data Jalur Mandiri PTN 2025/2026")

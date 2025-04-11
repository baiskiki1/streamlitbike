import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load dan siapkan data
try:
    df = pd.read_csv("day.csv")
except FileNotFoundError:
    st.error("❌ File day.csv tidak ditemukan. Pastikan file sudah diunggah ke repositori.")
    st.stop()

df['dteday'] = pd.to_datetime(df['dteday'])

# Mapping kategori
season_dict = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weekday_dict = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
                4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
weathersit_dict = {1: 'Clear', 2: 'Mist + Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}

df['season'] = df['season'].map(season_dict)
df['weekday'] = df['weekday'].map(weekday_dict)
df['weathersit'] = df['weathersit'].map(weathersit_dict)
df['day_type'] = df['workingday'].apply(lambda x: 'Weekday' if x == 1 else 'Weekend')
df['year'] = df['yr'].map({0: '2011', 1: '2012'})

# Judul Aplikasi
st.title('🚲 Bike Sharing Analysis Dashboard')
st.caption("Proyek Analisis Data | Dicoding")

# Sidebar Filter
st.sidebar.header('🔍 Filter Data')
season_filter = st.sidebar.multiselect("Pilih Musim", df['season'].unique(), default=df['season'].unique())
year_filter = st.sidebar.multiselect("Pilih Tahun", df['year'].unique(), default=df['year'].unique())

# Filter DataFrame
df_filtered = df[(df['season'].isin(season_filter)) & (df['year'].isin(year_filter))]

# Layout Visualisasi
col1, col2 = st.columns(2)

with col1:
    st.subheader('📈 Tren Penyewaan Harian')
    fig1, ax1 = plt.subplots()
    sns.lineplot(data=df_filtered, x='dteday', y='cnt', ax=ax1)
    ax1.set_xlabel('Tanggal')
    ax1.set_ylabel('Jumlah Penyewaan')
    ax1.set_title('Total Penyewaan Sepeda')
    st.pyplot(fig1)

with col2:
    st.subheader('👥 Rata-rata Casual vs Registered')
    casual_mean = df_filtered.groupby('day_type')['casual'].mean()
    registered_mean = df_filtered.groupby('day_type')['registered'].mean()

    bar_data = pd.DataFrame({
        'Casual': casual_mean,
        'Registered': registered_mean
    })

    fig2, ax2 = plt.subplots()
    bar_data.plot(kind='bar', stacked=True, color=['skyblue', 'salmon'], ax=ax2)
    ax2.set_ylabel('Rata-rata Jumlah Penyewa')
    ax2.set_title('Rata-rata per Tipe Hari')
    st.pyplot(fig2)

# Statistik Ringkasan
st.subheader("📊 Statistik Ringkasan Penyewaan")
st.dataframe(df_filtered[['casual', 'registered', 'cnt']].describe())

# Footer
st.markdown("---")
st.markdown("🧑‍💻 Dibuat oleh [Nama Kamu] untuk Proyek Analisis Data Dicoding.")

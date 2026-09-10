import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="E-Commerce Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# Pengaturan tema visualisasi
sns.set_theme(style="whitegrid")

# Memuat data
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'main_data.csv')
    df = pd.read_csv(file_path)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

df = load_data()

# Sidebar filter
st.sidebar.title("Filter Analisis")
st.sidebar.markdown("Sesuaikan rentang tanggal transaksi:")

min_date = df['order_purchase_timestamp'].min().date()
max_date = df['order_purchase_timestamp'].max().date()

date_range = st.sidebar.date_input(
    label="Rentang Tanggal",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# Filter dataframe berdasarkan rentang tanggal
filtered_df = df[
    (df['order_purchase_timestamp'].dt.date >= start_date) &
    (df['order_purchase_timestamp'].dt.date <= end_date)
].copy()

# Header Dashboard
st.title("📊 E-Commerce Public Dataset Dashboard")
st.caption("Analisis Performa Pengiriman, Kepuasan Pelanggan, dan Segmentasi RFM (Olist Brasil)")

# Metrik Utama
st.markdown("### Ringkasan Metrik")
col1, col2, col3, col4 = st.columns(4)

total_orders = len(filtered_df)
total_revenue = filtered_df['payment_value'].sum()
avg_review = filtered_df['review_score'].mean()
late_orders = (filtered_df['delivery_status'] == 'Late').sum()
late_pct = (late_orders / total_orders * 100) if total_orders > 0 else 0

with col1:
    st.metric("Total Pesanan", f"{total_orders:,}")
with col2:
    st.metric("Total Pendapatan", f"BRL {total_revenue:,.2f}")
with col3:
    st.metric("Rata-rata Ulasan", f"{avg_review:.2f} / 5.0")
with col4:
    st.metric("Tingkat Keterlambatan", f"{late_pct:.1f}%")

st.markdown("---")

# Tab Analisis
tab1, tab2, tab3 = st.tabs([
    "🚚 Logistik & Kepuasan Pelanggan",
    "👥 Analisis RFM & Segmentasi",
    "🗺️ Analisis Geospasial"
])

# Tab 1: Logistik & Kepuasan
with tab1:
    st.subheader("Pengaruh Keterlambatan Pengiriman terhadap Kepuasan Pelanggan")
    
    col_plot1, col_plot2 = st.columns(2)
    
    with col_plot1:
        fig, ax = plt.subplots(figsize=(7, 5))
        palette_colors = {'On Time': '#2ecc71', 'Late': '#e74c3c'}
        bar_score = sns.barplot(
            x='delivery_status',
            y='review_score',
            data=filtered_df,
            palette=palette_colors,
            errorbar=None,
            ax=ax
        )
        ax.set_title("Rata-rata Skor Ulasan: On Time vs Late", fontsize=12)
        ax.set_xlabel("Status Pengiriman")
        ax.set_ylabel("Rata-rata Skor Ulasan")
        ax.set_ylim(0, 5)
        for p in bar_score.patches:
            height = p.get_height()
            if not np.isnan(height) and height > 0:
                ax.annotate(f"{height:.2f}",
                            (p.get_x() + p.get_width() / 2., height / 2),
                            ha='center', va='center', fontsize=11, color='white', weight='bold')
        st.pyplot(fig)
        plt.close(fig)
        
    with col_plot2:
        top_states = filtered_df['customer_state'].value_counts().head(5).index
        state_perf = filtered_df[filtered_df['customer_state'].isin(top_states)].groupby('customer_state').agg(
            total=('order_id', 'count'),
            late=('delivery_status', lambda x: (x == 'Late').sum())
        ).reset_index()
        state_perf['late_pct'] = (state_perf['late'] / state_perf['total']) * 100
        state_perf = state_perf.sort_values(by='late_pct', ascending=False)
        
        fig, ax = plt.subplots(figsize=(7, 5))
        bar_state = sns.barplot(
            x='customer_state',
            y='late_pct',
            data=state_perf,
            palette='Reds_r',
            ax=ax
        )
        ax.set_title("Keterlambatan di 5 Negara Bagian Teratas", fontsize=12)
        ax.set_xlabel("Negara Bagian (State)")
        ax.set_ylabel("Keterlambatan (%)")
        for p in bar_state.patches:
            height = p.get_height()
            if not np.isnan(height):
                ax.annotate(f"{height:.1f}%",
                            (p.get_x() + p.get_width() / 2., height + 0.3),
                            ha='center', va='bottom', fontsize=10, weight='bold')
        st.pyplot(fig)
        plt.close(fig)

    st.info("💡 **Insight**: Pesanan yang tiba tepat waktu mendapatkan skor kepuasan rata-rata 4,29, sedangkan pesanan terlambat anjlok ke 2,57. Rio de Janeiro (RJ) memiliki tingkat keterlambatan paling tinggi di antara negara bagian utama.")

# Tab 2: RFM & Segmentasi
with tab2:
    st.subheader("Segmentasi Pelanggan Berdasarkan RFM")
    
    snapshot_date = filtered_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
    rfm = filtered_df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
        'order_id': 'nunique',
        'payment_value': 'sum'
    }).reset_index()
    rfm.columns = ['customer_unique_id', 'recency', 'frequency', 'monetary']
    
    col_rfm1, col_rfm2, col_rfm3 = st.columns(3)
    
    with col_rfm1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(rfm['recency'], bins=20, color='#3498db', ax=ax)
        ax.set_title("Distribusi Recency (Hari)", fontsize=11)
        ax.set_xlabel("Hari")
        ax.set_ylabel("Pelanggan")
        st.pyplot(fig)
        plt.close(fig)
        
    with col_rfm2:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(rfm['frequency'], bins=10, color='#2ecc71', ax=ax)
        ax.set_title("Distribusi Frequency", fontsize=11)
        ax.set_xlabel("Jumlah Transaksi")
        ax.set_ylabel("Pelanggan (Log)")
        ax.set_yscale('log')
        st.pyplot(fig)
        plt.close(fig)
        
    with col_rfm3:
        top_monetary = rfm.sort_values(by='monetary', ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x='monetary', y='customer_unique_id', data=top_monetary, palette='Blues_r', ax=ax)
        ax.set_title("Top 5 Monetary (BRL)", fontsize=11)
        ax.set_xlabel("Total Belanja")
        ax.set_ylabel("ID Pelanggan")
        st.pyplot(fig)
        plt.close(fig)
        
    # Segmentasi
    r_labels = [4, 3, 2, 1]
    m_labels = [1, 2, 3, 4]
    rfm['r_score'] = pd.qcut(rfm['recency'].rank(method='first'), q=4, labels=r_labels).astype(int)
    rfm['m_score'] = pd.qcut(rfm['monetary'].rank(method='first'), q=4, labels=m_labels).astype(int)
    
    def assign_segment(row):
        if row['r_score'] >= 3 and row['m_score'] >= 3:
            return 'Champions'
        elif row['r_score'] >= 3 and row['m_score'] < 3:
            return 'Active / Promising'
        elif row['r_score'] < 3 and row['m_score'] >= 3:
            return 'At Risk'
        else:
            return 'Hibernating'
            
    rfm['customer_segment'] = rfm.apply(assign_segment, axis=1)
    seg_counts = rfm['customer_segment'].value_counts().reset_index()
    seg_counts.columns = ['customer_segment', 'count']
    
    st.markdown("#### Distribusi Segmen Pelanggan")
    fig, ax = plt.subplots(figsize=(9, 3.5))
    bar_seg = sns.barplot(x='count', y='customer_segment', data=seg_counts, palette='viridis', ax=ax)
    ax.set_title("Jumlah Pelanggan per Segmen RFM", fontsize=12)
    ax.set_xlabel("Jumlah Pelanggan")
    ax.set_ylabel("Segmen")
    for p in bar_seg.patches:
        width = p.get_width()
        if not np.isnan(width):
            ax.annotate(f"{int(width):,}",
                        (width - (width * 0.12), p.get_y() + p.get_height() / 2),
                        ha='center', va='center', fontsize=10, color='white', weight='bold')
    st.pyplot(fig)
    plt.close(fig)

# Tab 3: Geospatial
with tab3:
    st.subheader("Peta Sebaran Pelanggan di Brasil")
    
    geo_data = filtered_df.dropna(subset=['geolocation_lat', 'geolocation_lng'])
    geo_brazil = geo_data[
        (geo_data['geolocation_lat'] >= -35) & (geo_data['geolocation_lat'] <= 5) &
        (geo_data['geolocation_lng'] >= -75) & (geo_data['geolocation_lng'] <= -30)
    ]
    
    map_df = geo_brazil[['geolocation_lat', 'geolocation_lng']].rename(
        columns={'geolocation_lat': 'lat', 'geolocation_lng': 'lon'}
    ).sample(n=min(5000, len(geo_brazil)), random_state=42)
    
    st.map(map_df, zoom=3)
    
    st.markdown("#### Top 5 Kota dengan Pesanan Terbanyak")
    top_cities = filtered_df['customer_city'].value_counts().head(5).reset_index()
    top_cities.columns = ['Kota', 'Total Pesanan']
    st.dataframe(top_cities, use_container_width=True)

st.caption("Submission Proyek Akhir: Belajar Analisis Data dengan Python - Dicoding | Satria Musthofa 'Azmi")

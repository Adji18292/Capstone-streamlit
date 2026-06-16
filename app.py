import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="OmniSight BI - Streamlit",
    page_icon="📊",
    layout="wide"
)

# API URL Backend FastAPI
API_URL = "http://127.0.0.1:8000"

# ================= SIDEBAR NAVIGATION =================
st.sidebar.title("📊 OmniSight BI")
st.sidebar.markdown("*(Versi Streamlit Sederhana)*")
st.sidebar.divider()

menu = st.sidebar.radio(
    "Pilih Menu:",
    ["📈 Dashboard Overview", "🔮 AI Sales Forecast", "⚠️ Customer Churn", "🤖 AI Assistant Chat"]
)

# ================= MENU 1: DASHBOARD =================
if menu == "📈 Dashboard Overview":
    st.title("📈 Dashboard Overview")
    st.markdown("Ringkasan performa bisnis Anda.")
    
    # Indikator Utama (Metrics)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Omzet", "Rp 4.925.000", "-5% dari bulan lalu")
    col2.metric("Total Pesanan", "124", "12%")
    col3.metric("Pelanggan Aktif", "89", "3%")
    col4.metric("Risiko Churn", "7", "-2")
    
    st.divider()
    
    # Grafik dummy menggunakan Plotly
    st.subheader("Grafik Tren Penjualan 7 Hari Terakhir")
    dates = pd.date_range(start="2023-10-01", periods=7)
    sales = np.random.randint(100, 500, size=7)
    df_sales = pd.DataFrame({"Tanggal": dates, "Penjualan": sales})
    
    fig = px.line(df_sales, x="Tanggal", y="Penjualan", markers=True, line_shape="spline")
    fig.update_traces(line_color="#1f77b4", marker=dict(size=8))
    st.plotly_chart(fig, use_container_width=True)

# ================= MENU 2: AI SALES FORECAST =================
elif menu == "🔮 AI Sales Forecast":
    st.title("🔮 AI Sales Forecast")
    st.markdown("Prediksi penjualan menggunakan model AI (SARIMAX / Exponential Smoothing) dari backend.")
    
    if st.button("Jalankan Prediksi AI Sekarang", type="primary"):
        with st.spinner("Memproses data melalui mesin AI..."):
            # Dummy data historis untuk dikirim ke API
            hist_data = [{"date": f"2023-10-0{i}", "sales": float(np.random.randint(100, 500))} for i in range(1, 8)]
            payload = {
                "Target_Month": "November 2023",
                "Current_Quantity": 0,
                "Historical_Data": hist_data
            }
            try:
                res = requests.post(f"{API_URL}/forecast-sales", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.success(f"✅ Prediksi berhasil! Confidence Score AI: {data.get('confidence_score')}%")
                    
                    preds = data.get("predictions_array", [])
                    df_pred = pd.DataFrame({
                        "Hari ke-": [f"Hari {i}" for i in range(1, len(preds)+1)],
                        "Prediksi Penjualan": preds
                    })
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.bar_chart(df_pred.set_index("Hari ke-"), color="#00C853")
                    with col2:
                        st.dataframe(df_pred, use_container_width=True)
                else:
                    st.error("Gagal mendapatkan prediksi dari server.")
            except Exception as e:
                st.error("⚠️ Tidak dapat terhubung ke server backend. Pastikan uvicorn berjalan.")

# ================= MENU 3: CUSTOMER CHURN =================
elif menu == "⚠️ Customer Churn":
    st.title("⚠️ Customer Churn Prediction")
    st.markdown("Deteksi pelanggan yang berisiko meninggalkan bisnis Anda menggunakan algoritma Machine Learning.")
    
    if st.button("Mulai Analisis Risiko Pelanggan", type="primary"):
        with st.spinner("Menganalisis profil pelanggan..."):
            # Data sampel pelanggan
            customers = [
                {"customer_id": 1, "recency": 5, "frequency": 10, "monetary": 500},
                {"customer_id": 2, "recency": 45, "frequency": 2, "monetary": 50},
                {"customer_id": 3, "recency": 12, "frequency": 8, "monetary": 300},
                {"customer_id": 4, "recency": 65, "frequency": 1, "monetary": 20},
            ]
            try:
                res = requests.post(f"{API_URL}/predict-churn-batch", json={"customers": customers})
                if res.status_code == 200:
                    data = res.json()
                    st.success(f"✅ Analisis Selesai (Mesin yang digunakan: **{data.get('engine')}**)")
                    
                    df_res = pd.DataFrame(data.get("predictions", []))
                    if "Prediction_Label" in df_res.columns:
                        # Membuat kolom visual Status
                        df_res["Status Risiko"] = df_res["Prediction_Label"].apply(
                            lambda x: "🚨 Berisiko Tinggi" if x == 1 else "✅ Aman"
                        )
                        # Mengatur urutan kolom
                        cols = ["customer_id", "recency", "frequency", "monetary", "Churn_Probability", "Status Risiko"]
                        df_res = df_res[[c for c in cols if c in df_res.columns]]
                        
                    st.dataframe(df_res, use_container_width=True)
                else:
                    st.error("Gagal menganalisis data churn.")
            except Exception as e:
                st.error("⚠️ Tidak dapat terhubung ke server backend.")

# ================= MENU 4: AI ASSISTANT =================
elif menu == "🤖 AI Assistant Chat":
    st.title("🤖 OmniSight AI Assistant")
    st.markdown("Tanyakan insight bisnis Anda melalui asisten chat ini.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Halo! Saya OmniSight AI. Ada yang bisa saya bantu hari ini? (Coba tanyakan seputar omzet, prakiraan, atau churn pelanggan)"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Tanyakan sesuatu ke OmniSight AI..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("⏳ Berpikir...")
            try:
                response = requests.post(f"{API_URL}/chat", json={"message": prompt})
                if response.status_code == 200:
                    data = response.json()
                    reply = data.get("reply", "Maaf, tidak ada respons valid.")
                else:
                    reply = f"Error dari API Backend: {response.status_code}"
            except Exception as e:
                reply = "⚠️ Gagal terhubung ke server. Pastikan server uvicorn sedang berjalan."
                
            message_placeholder.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

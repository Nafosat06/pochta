import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Kurs ishi | Dashboard", layout="wide")
st.title("🚀 Ma'lumotlar Tahlili va Bashorat Dashboardi")

@st.cache_data
def load_data():
    df = pd.read_csv('combined_data.csv')
    # SIZDAGI USTUN NOMI 'text' EKANLIGINI HISOBGA OLAMIZ
    if 'text' in df.columns:
        df['length'] = df['text'].astype(str).apply(len)
    elif 'message' in df.columns:
        df['length'] = df['message'].astype(str).apply(len)
    
    df = df.dropna(subset=['length'])
    return df

try:
    data = load_data()

    # 1-QISM: MATN TAHLILI
    st.header("📂 Dataset Tahlili (Spam/Ham)")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Xabarlar uzunligi taqsimoti")
        fig1 = px.histogram(data, x="length", color="label", 
                            nbins=30, barmode="overlay",
                            color_discrete_map={'ham':'#00CC96', 'spam':'#FF4B4B'},
                            labels={'length':'Xabar uzunligi', 'label':'Turi'})
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("🍩 Xabarlar turlari ulushi")
        label_counts = data['label'].value_counts().reset_index()
        label_counts.columns = ['Tur', 'Soni']
        fig2 = px.pie(label_counts, names='Tur', values='Soni', hole=0.4,
                      color='Tur', color_discrete_map={'ham':'#00CC96', 'spam':'#FF4B4B'})
        st.plotly_chart(fig2, use_container_width=True)

    st.write("---")

    # 2-QISM: HARORAT DINAMIKASI (Rasmda so'ralgan grafik)
    st.header("📈 Tashqi omillar tahlili")
    temp_df = pd.DataFrame({
        'Soat': ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00'],
        'Harorat': [24, 28, 32, 35, 33, 29, 27]
    })
    fig3 = px.line(temp_df, x='Soat', y='Harorat', markers=True, color_discrete_sequence=['red'])
    st.plotly_chart(fig3, use_container_width=True)

    st.success("Tahlil: Eng yuqori harorat 14:00 da (35°C) kuzatildi.")

except Exception as e:
    st.error(f"Xatolik yuz berdi: {e}")

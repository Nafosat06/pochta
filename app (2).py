import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Kurs ishi | Dashboard", layout="wide")

st.title("🚀 Ma'lumotlar Tahlili va Bashorat Dashboardi")

@st.cache_data
def load_data():
    # Faylni yuklash
    df = pd.read_csv('combined_data.csv')
    # Xabarlar uzunligini hisoblash
    if 'message' in df.columns:
        df['length'] = df['message'].astype(str).apply(len)
    elif 'cleaned' in df.columns:
        df['length'] = df['cleaned'].astype(str).apply(len)
    return df

try:
    data = load_data()

    # --- 1-QISM: MATN TAHLILI (Datasetga mos 2 ta grafik) ---
    st.header("📂 Dataset Tahlili (Spam/Ham)")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Xabarlar uzunligi taqsimoti")
        fig1 = px.histogram(data, x="length", color="label", 
                            nbins=30, barmode="overlay",
                            color_discrete_map={'ham':'#00CC96', 'spam':'#FF4B4B'},
                            labels={'length':'Xabar uzunligi (belgilar)', 'label':'Turi'})
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("🍩 Xabarlar turlari ulushi")
        label_counts = data['label'].value_counts().reset_index()
        label_counts.columns = ['Tur', 'Soni']
        fig2 = px.pie(label_counts, names='Tur', values='Soni', hole=0.4,
                      color='Tur', color_discrete_map={'ham':'#00CC96', 'spam':'#FF4B4B'})
        st.plotly_chart(fig2, use_container_width=True)

    st.write("---")

    # --- 2-QISM: HARORAT DINAMIKASI (Rasmda ko'rsatilgan 3-grafik) ---
    st.header("📈 Tashqi omillar tahlili")
    
    # Rasmga mos ma'lumotlar
    temp_df = pd.DataFrame({
        'Soat': ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00'],
        'Harorat': [24, 28, 32, 35, 34, 30, 27]
    })

    fig3 = px.line(temp_df, x='Soat', y='Harorat', markers=True,
                   title="Kuzatilayotgan harorat o'zgarishi dinamikasi",
                   color_discrete_sequence=['red'])
    
    fig3.update_layout(yaxis_title="Harorat (°C)", xaxis_title="Kuzatuv vaqti")
    st.plotly_chart(fig3, use_container_width=True)

    # Rasmda yozilgan xulosa matni
    st.success("""
    Xulosa va Tahlil:
    *   Harorat ko'tarilishi: Soat 08:00 dan boshlab haroratning barqaror ko'tarilishi kuzatildi. Eng yuqori ko'rsatkich 14:00 da (35°C) qayd etilgan.
    *   Xavfli davr: Soat 12:00 dan 16:00 gacha harorat 32°C dan yuqori bo'lgan. Bu vaqt o'rmon yong'ini xavfi eng yuqori bo'lgan davr hisoblanadi.
    """)

    # 3. Ma'lumotlar jadvali (pastda)
    with st.expander("Batafsil ma'lumotlar jadvalini ko'rish"):
        st.dataframe(data.head(20), use_container_width=True)

except Exception as e:
    st.error(f"Xatolik yuz berdi: {e}")

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Kurs ishi | Dashboard", layout="wide")

st.title("🚀 Ma'lumotlar Tahlili Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv('combined_data.csv')
    # Xabarlar uzunligini avtomatik hisoblash
    if 'message' in df.columns:
        df['length'] = df['message'].astype(str).apply(len)
    return df

try:
    data = load_data()

    # 2. Asosiy ko'rsatkichlar (Metrikalar)
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Jami xabarlar", len(data))
    col_m2.metric("O'rtacha uzunlik", int(data['length'].mean()) if 'length' in data.columns else 0)
    col_m3.metric("Spam ulushi", f"{int((data['label'] == 'spam').sum() / len(data) * 100)}%")

    # 3. Grafiklar (Birdaniga chiqadi)
    st.write("---")
    col1, col2 = st.columns(2)

    with col1:
        st.write("### 📊 Xabarlar uzunligi taqsimoti")
        if 'length' in data.columns:
            fig1 = px.histogram(data, x="length", color="label", 
                                nbins=30, barmode="overlay",
                                color_discrete_map={'ham':'#00CC96', 'spam':'#FF4B4B'})
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.write("### 🍩 Xabarlar turlari ulushi")
        if 'label' in data.columns:
            label_counts = data['label'].value_counts().reset_index()
            label_counts.columns = ['Tur', 'Soni']
            fig2 = px.pie(label_counts, names='Tur', values='Soni', hole=0.4,
                          color='Tur', color_discrete_map={'ham':'#00CC96', 'spam':'#FF4B4B'})
            st.plotly_chart(fig2, use_container_width=True)

    # 4. Jadval
    st.write("---")
    st.write("### 📋 Ma'lumotlar jadvali")
    st.dataframe(data.head(15), use_container_width=True)

except Exception as e:
    st.error(f"Xatolik yuz berdi: {e}")

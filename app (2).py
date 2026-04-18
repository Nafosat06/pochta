import streamlit as st
import pandas as pd
import plotly.express as px

# Sahifa sozlamalari
st.set_page_config(page_title="Kurs ishi | Dashboard", layout="wide")

st.title("🚀 Ma'lumotlar Tahlili Veb-ilovasi")

@st.cache_data
def load_data():
    # Faylni yuklaymiz
    df = pd.read_csv('combined_data.csv')
    # Agar 'length' ustuni bo'lmasa, uni yaratib olamiz (tahlil uchun kerak)
    if 'length' not in df.columns and 'message' in df.columns:
        df['length'] = df['message'].astype(str).apply(len)
    return df

try:
    data = load_data()

    # 1. Ma'lumotlar jadvali
    st.write("### 📋 Ma'lumotlar jadvali")
    st.dataframe(data.head(10))

    col1, col2 = st.columns(2)

    with col1:
        # 2. Gistogramma (Shamol tezligi prognozi kabi ko'rinadi)
        st.write("### 📊 Xabarlar uzunligi taqsimoti")
        if 'length' in data.columns:
            fig1 = px.histogram(data, x="length", color="label", 
                                 nbins=30, color_discrete_sequence=['#FF4B4B', '#00CC96'],
                                 title="Xabarlar uzunligi gistogrammasi")
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # 3. Doiraviy diagramma (Pie chart)
        st.write("### 🍩 Xabarlar turlari ulushi")
        if 'label' in data.columns:
            label_counts = data['label'].value_counts().reset_index()
            label_counts.columns = ['Tur', 'Soni']
            fig2 = px.pie(label_counts, names='Tur', values='Soni', hole=0.4,
                          color_discrete_sequence=px.colors.sequential.RdBu,
                          title="Spam va Oddiy xabarlar nisbati")
            st.plotly_chart(fig2, use_container_width=True)

    # Sidebar uchun qo'shimcha filtrlar
    st.sidebar.header("Qidiruv")
    search = st.sidebar.text_input("Xabarlarni qidirish:")
    if search:
        filtered_data = data[data['message'].str.contains(search, case=False, na=False)]
        st.write(f"Topilgan natijalar: {len(filtered_data)}")
        st.dataframe(filtered_data)

except Exception as e:
    st.error(f"Xatolik yuz berdi: {e}")

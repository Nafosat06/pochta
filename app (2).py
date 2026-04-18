import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Intellektual Tasniflash | Dashboard", layout="wide")

st.title("🛡️ Elektron pochta xabarlarini intellektual tasniflash")
st.markdown("### Ma'lumotlarni tahlil qilish va intellektual monitoring")

@st.cache_data
def load_data():
    # Faylni o'qish
    df = pd.read_csv('combined_data.csv')
    
    # Kaggle datasetiga mos ustunlarni tekshirish va uzunlikni hisoblash
    text_col = 'text' if 'text' in df.columns else 'message'
    if text_col in df.columns:
        df['length'] = df[text_col].astype(str).apply(len)
        # So'zlar sonini ham hisoblaymiz (ilmiyroq ko'rinadi)
        df['words_count'] = df[text_col].astype(str).apply(lambda x: len(x.split()))
    
    return df

try:
    data = load_data()

    # 2. Asosiy ko'rsatkichlar (Metrikalar)
    m1, m2, m3, m4 = st.columns(4)
    total = len(data)
    spam_count = (data['label'] == 'spam').sum()
    ham_count = (data['label'] == 'ham').sum()
    
    m1.metric("Jami xabarlar", total)
    m2.metric("Spam xabarlar", f"{spam_count} ta")
    m3.metric("Oddiy (Ham)", f"{ham_count} ta")
    m4.metric("Spam ulushi", f"{int(spam_count/total*100)}%")

    st.write("---")

    # 3. Vizual tahlil bo'limi
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Xabarlar uzunligi taqsimoti")
        # Spam va Ham xabarlar uzunligi orasidagi farqni ko'rsatuvchi gistogramma
        fig1 = px.histogram(data, x="length", color="label", 
                            marginal="rug", # Pastda zichlik chiziqlari
                            color_discrete_map={'ham':'#00CC96', 'spam':'#FF4B4B'},
                            labels={'length':'Belgilar soni', 'label':'Xabar turi'})
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("🍩 Xabarlarning foiz nisbati")
        # Doiraviy diagramma
        fig2 = px.pie(data, names='label', hole=0.4,
                      color='label', color_discrete_map={'ham':'#00CC96', 'spam':'#FF4B4B'})
        st.plotly_chart(fig2, use_container_width=True)

    # 4. Qo'shimcha tahlil: So'zlar soni bo'yicha bog'liqlik
    st.write("---")
    st.subheader("📈 Xabardagi so'zlar soni bo'yicha tahlil")
    fig3 = px.box(data, x="label", y="words_count", color="label",
                  color_discrete_map={'ham':'#00CC96', 'spam':'#FF4B4B'},
                  title="Spam va Ham xabarlardagi so'zlar soni (Box Plot)")
    st.plotly_chart(fig3, use_container_width=True)

    # 5. Ma'lumotlar jadvali
    with st.expander("Batafsil ma'lumotlar jadvali"):
        st.dataframe(data.head(50), use_container_width=True)

except Exception as e:
    st.error(f"Xatolik yuz berdi: {e}")

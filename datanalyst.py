import streamlit as st
import pandas as pd
import google.generativeai as genai
import matplotlib.pyplot as plt
import seaborn as sns

# --- AYARLAR ---
st.set_page_config(page_title="AI Veri Analisti", page_icon="📊", layout="wide")

# --- GÜVENLİK ---
# API Key'i Streamlit Secrets'tan alıyoruz (Böylece çalınmaz)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key bulunamadı! Lütfen Streamlit Secrets ayarlarını yapın.")
    st.stop()

def analyze_data(df, question):
    """Veriyi Gemini'ye yorumlatır."""
    data_summary = f"""
    Sütunlar: {list(df.columns)}
    Veri Tipleri: {list(df.dtypes)}
    İlk 5 Satır:
    {df.head().to_string()}
    """
    
    prompt = f"""
    Sen uzman bir Veri Analistisin. Veri özeti:
    {data_summary}
    
    Kullanıcı Sorusu: "{question}"
    
    Lütfen bu soruyu Türkçe olarak, profesyonel bir dille yanıtla.
    """
    response = model.generate_content(prompt)
    return response.text

# --- ARAYÜZ ---
st.title("📊 AI Veri Analisti")
st.markdown("Excel/CSV dosyanı yükle, yapay zeka analiz etsin.")

uploaded_file = st.file_uploader("Dosya Yükle", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("✅ Veri Yüklendi!")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.dataframe(df.head())
            
        with col2:
            question = st.text_input("Veri hakkında ne bilmek istersin?")
            if st.button("Analiz Et") and question:
                with st.spinner("Analiz ediliyor..."):
                    result = analyze_data(df, question)
                    st.write(result)
                    
                    # Otomatik Grafik (Sayısal veri varsa)
                    numeric_cols = df.select_dtypes(include=['float', 'int']).columns
                    if len(numeric_cols) > 0:
                        st.subheader("Otomatik Grafik")
                        col_to_plot = st.selectbox("Grafik Sütunu", numeric_cols)
                        fig, ax = plt.subplots()
                        sns.histplot(df[col_to_plot], kde=True, ax=ax)
                        st.pyplot(fig)
                        
    except Exception as e:
        st.error(f"Hata: {e}")

import streamlit as st
import pandas as pd
import google.generativeai as genai
import matplotlib.pyplot as plt
import seaborn as sns

# --- AYARLAR ---
st.set_page_config(page_title="AI Veri Analisti", page_icon="📊", layout="wide")

# --- YAN MENÜ (SIDEBAR) - API KEY GİRİŞİ ---
with st.sidebar:
    st.header("🔑 Ayarlar")
    st.markdown("Bu uygulama Google Gemini modelini kullanır.")
    
    # Kullanıcıdan anahtar istiyoruz
    api_key = st.text_input("Google API Anahtarınızı Girin:", type="password", placeholder="AIzaSy...")
    
    # Anahtar alma linki
    st.markdown("""
    ---
    👉 **API Anahtarınız yok mu?**
    [Buraya tıklayarak Google AI Studio'dan ücretsiz alabilirsiniz.](https://aistudio.google.com/app/apikey)
    """)
    
    st.info("Anahtarınız kaydedilmez, sadece bu oturumda kullanılır.")

# --- ANA EKRAN ---
st.title("📊 AI Veri Analisti")
st.markdown("Excel/CSV dosyanı yükle, verilerinle sohbet et.")

# --- KONTROL: ANAHTAR GİRİLDİ Mİ? ---
if not api_key:
    st.warning("⚠️ Lütfen sol taraftaki menüden Google API Anahtarınızı girin ve Enter'a basın.")
    st.stop()  # Anahtar yoksa aşağıyı çalıştırma, burada dur.

# --- GEMINI KURULUMU (Kullanıcının anahtarı ile) ---
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Hatalı API Anahtarı! Lütfen kontrol edin. Hata: 

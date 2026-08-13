import streamlit as st
import json

st.set_page_config(page_title="Fiyat & İskonto", page_icon="🏷️", layout="centered")

st.title("🏷️ Ürün Fiyat & İskonto Hesaplayıcı")

@st.cache_data
def load_data():
    with open("urunler.json", "r", encoding="utf-8") as f:
        return json.load(f)

try:
    urunler = load_data()
except Exception as e:
    st.error("Ürün verisi yüklenemedi!")
    urunler = []

arama = st.text_input("🔍 Ürün Adı, Stok Kodu veya Barkod", "").strip().lower()

if arama:
    sonuclar = [u for u in urunler if arama in u["ad"].lower() or arama in u["kod"] or arama in u["barkod"]]
    
    if not sonuclar:
        st.warning("❌ Ürün bulunamadı.")
    else:
        st.success(f"🎯 {len(sonuclar)} Ürün Bulundu")
        
        secenekler = [f"{u['ad']} | Kod: {u['kod']} | {u['fiyat']}" for u in sonuclar]
        secilen_idx = st.selectbox("Hesaplama Yapılacak Ürünü Seçin:", range(len(secenekler)), format_func=lambda x: secenekler[x])
        
        secilen_urun = sonuclar[secilen_idx]
        
        st.markdown("---")
        st.subheader(f"📦 {secilen_urun['ad']}")
        st.write(f"**Stok Kodu:** {secilen_urun['kod']} | **Barkod:** {secilen_urun['barkod']}")
        
        raw_fiyat = float(secilen_urun['fiyat'].replace('.', '').replace(',', '.').replace('₺', '').strip())
        
        st.metric("Liste Fiyatı", f"{raw_fiyat:,.2f} ₺")
        
        iskonto = st.number_input("İskonto Oranı (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0)
        
        net_fiyat = raw_fiyat * (1 - iskonto / 100)
        
        st.success(f"✅ **İskontolu Net Fiyat:** {net_fiyat:,.2f} ₺")

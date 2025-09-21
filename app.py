
%%writefile app.py
import streamlit as st
import pandas as pd
import base64
import os

# Google Drive ကို Colab နဲ့ ချိတ်ဆက်ခြင်း
try:
    from google.colab import drive
    drive.mount('/content/drive', force_remount=True)
except ImportError:
    st.error("Google Drive ကို ချိတ်ဆက်ရာတွင် အမှားဖြစ်ပွားခဲ့ပါသည်။")
    st.stop()

# Page ကို Configure လုပ်ပါ
st.set_page_config(
    page_title="Merchant Data Search App",
    page_icon="🔍"
)

# Web App ရဲ့ ခေါင်းစဉ်ကို ပြသပါ
st.title("AYA Merchant Data Search")
st.markdown("အချက်အလက်ရှာဖွေရန် Merchant Code ကို ထည့်ပါ")

# ဖိုင်လမ်းကြောင်းကို သတ်မှတ်ပါ
file_path = '/content/drive/MyDrive/merchant_data.csv'

# Data ကို Load လုပ်ပါ
try:
    df = pd.read_csv(file_path, encoding='latin1', on_bad_lines='skip', engine='python')
    df.columns = df.columns.str.strip()
except Exception as e:
    st.error(f"အမှားတစ်ခုခုဖြစ်ပွားခဲ့ပါသည်: {e}")
    st.stop()

# User ထံမှ Merchant Code ကို လက်ခံရန် Input Box တစ်ခု ဖန်တီးပါ
user_code = st.text_input("Merchant Code", help="ဥပမာ- 300479128")

# Button ကို နှိပ်ပြီး အချက်အလက်များကို ရှာဖွေပါ
if st.button("Search"):
    if user_code:
        result = df[df['Merchant Short Code'].astype(str).str.strip() == user_code.strip()]
        
        if not result.empty:
            st.success("အချက်အလက်တွေ့ရှိပါသည်!")
            
            # ရှာဖွေတွေ့ရှိသော အချက်အလက်များကို ပြသပါ
            st.write(f"**စီးပွားရေးလုပ်ငန်းအမည်:** {result.iloc[0]['Name of Business '].strip()}")
            st.write(f"**ပိုင်ရှင်အမည်:** {result.iloc[0]['Owner Name'].strip()}")
            st.write(f"**ဖုန်းနံပါတ်:** {result.iloc[0]['Merchant Phone Number'].strip()}")
            st.write(f"**လိပ်စာ:** {result.iloc[0]['Full Business Address ( House Number, Street, Ward )'].strip()}")
        else:
            st.warning("ထည့်သွင်းလိုက်သော Code နှင့် ကိုက်ညီသည့် အချက်အလက်မတွေ့ပါ။")
    else:
        st.info("ရှာဖွေရန် Merchant Code ထည့်ပါ။")

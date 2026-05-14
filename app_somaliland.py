import streamlit as st
import sqlite3
import re

# 1. Database-ka
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS tartamayaasha (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, telefoonka TEXT UNIQUE, gobolka TEXT, xafada TEXT)')
    conn.commit()
    conn.close()

bilow_database()

# 2. CSS-ta Qarinta Badhamada iyo Bilicda (Madow & Cagaar)
st.set_page_config(page_title="18 May Event", layout="centered")

st.markdown("""
    <style>
    /* Qari Menu-ga iyo Header-ka */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}

    /* Background-ka madow */
    .stApp {
        background-color: #0d1117 !important;
        color: #ffffff !important;
    }
    
    /* Input-yada */
    .stTextInput>div>div>input {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #10B981 !important;
    }

    /* Badhanka Submit */
    .stButton>button {
        background-color: #10B981 !important;
        color: black !important;
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- QAYBTA ADMIN-KA (Sirta ah) ---
if st.query_params.get("key") == "9a2b8c4e7f":
    st.title("🔐 Admin Dashboard")
    # Halkan koodhkii maamulka ee hore geli...
else:
    # --- BOGGA ISTICMAALAHA ---
    st.title("Somaliland 18 May")
    st.write("Fadlan buuxi xogtaada si aad uga qayb gasho.")
    
    with st.form("user_form"):
        magaca = st.text_input("Magacaaga oo Buuxa")
        telefoonka = st.text_input("Telefoonka (Tiro kaliya)")
        gobolka = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
        xafada = st.text_input("Xafadda")
        
        submit = st.form_submit_button("Submit")
        
        if submit:
            if magaca and telefoonka and xafada:
                # Hubi telefoonka
                if not telefoonka.isdigit():
                    st.error("Telefoonku waa inuu tiro noqdaa!")
                else:
                    try:
                        conn = sqlite3.connect('somaliland_18may.db')
                        cursor = conn.cursor()
                        cursor.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada) VALUES (?,?,?,?)', (magaca, telefoonka, gobolka, xafada))
                        conn.commit()
                        conn.close()
                        st.success("Waad ku mahadsantahay is-diiwaangelinta!")
                    except:
                        st.error("Lambarkan hore ayaa loo isticmaalay.")
            else:
                st.warning("Fadlan wada buuxi meelaha bannaan.")

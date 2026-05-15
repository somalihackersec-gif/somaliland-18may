import streamlit as st
import sqlite3
import pandas as pd

# 1. DATABASE SETUP
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tartamayaasha 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, telefoonka TEXT UNIQUE, gobolka TEXT, xafada TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS rayiga 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, faallada TEXT)''')
    conn.commit()
    conn.close()

bilow_database()

# 2. CALANKA URL
calanka_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10&ec=121691707"

# 3. SETTINGS & CSS (Qarinta Toolbar-ka iyo Bilicda)
st.set_page_config(page_title="18 May Online", page_icon=calanka_url, layout="centered")

st.markdown("""
    <style>
    [data-testid="stStatusWidget"], .stAppDeployButton, #MainMenu, header, footer {
        visibility: hidden;
        display: none !important;
    }
    .stApp { background-color: #0d1117 !important; color: white !important; }
    
    /* Input Style */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #10B981 !important;
        border-radius: 8px;
    }
    
    /* Button Style */
    .stButton>button {
        background-color: #10B981 !important;
        color: black !important;
        width: 100%;
        font-weight: bold;
        border-radius: 10px;
    }
    
    /* Share Button Styling */
    .share-btn {
        display: inline-block;
        padding: 10px 20px;
        background-color: #25D366;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. MAAMULKA BOGAGGA
if 'guul' not in st.session_state:
    st.session_state.guul = False

# --- BOGGA 2AAD: GUUSHA + VIRAL SHARE + DASHBOARD ---
if st.session_state.guul:
    st.balloons()
    st.image(calanka_url, width=100)
    st.title("🎊 Waad ku Jirtaa Tartanka!")
    st.success("Xogtaada si guul leh ayaa loo qabtay. Waxaad fursad u leedahay inaad ku guulaysato abaal-marino qaali ah!")

    # A. VIRAL SHARE BUTTON (WhatsApp)
    share_text = "Saaxiib, anigu waxaan is-diiwaangeliyey tartanka weyn ee 18-ka May! Kaalay adna oo is-diiwaangeli halkan: https://18may-somaliland.streamlit.app"
    whatsapp_url = f"https://wa.me/?text={share_text.replace(' ', '%20')}"
    
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="share-btn">📢 La wadaag asxaabtaada WhatsApp (Viral)</a>', unsafe_allow_html=True)
    st.write("---")

    # B. DASHBOARD-KA GOBOLADA (Competition Mode)
    st.subheader("📊 Tartanka Gobollada (Yaa Hoggaaminaya?)")
    conn = sqlite3.connect('somaliland_18may.db')
    df = pd.read_sql_query("SELECT gobolka, COUNT(*) as tirada FROM tartamayaasha GROUP BY gobolka", conn)
    conn.close()

    if not df.empty:
        st.bar_chart(df.set_index('gobolka'))
        hoggaanka = df.loc[df['tirada'].idxmax()]['gobolka']
        st.info(f"🏆 Hadda waxaa hoggaaminaya Gobolka: **{hoggaanka}**")
    
    st.write("---")
    # Qaybta Rayiga
    st.subheader("💬 Hambalyadaada 18 May")
    with st.form("form_rayiga"):
        r_magaca = st.text_input("Magacaaga")
        r_faallo = st.text_area("Maxaad u rajaynaysaa dalkaaga?")
        submit_r = st.form_submit_button("Soo Gudbi")
        if submit_r and r_magaca and r_faallo:
            conn = sqlite3.connect('somaliland_18may.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO rayiga (magaca, faallada) VALUES (?,?)', (r_magaca, r_faallo))
            conn.commit()
            conn.close()
            st.rerun()

    if st.button("← Ku noqo Bogga Tartanka"):
        st.session_state.guul = False
        st.rerun()

# --- BOGGA 1AAD: TARTANKA ---
else:
    st.image(calanka_url, use_container_width=True)
    st.title("Somaliland 18 May 🇸🇴")
    st.markdown("#### Ka qayb-gal tartanka weyn ee 18-ka May ka dibna la wadaag asxaabtaada!")
    
    # Competition Incentive
    st.warning("🎁 5-ta qof ee ugu horraysa ee Gobol kasta laga soo xulo waxay heli doonaan abaal-marino!")

    with st.form("form_tartanka"):
        magaca = st.text_input("Magacaaga oo Buuxa")
        tel = st.text_input("Telefoonkaaga")
        gobol = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
        xafad = st.text_input("Xafadda")
        submit_t = st.form_submit_button("Submit & Eeg Natiijada")
        
        if submit_t:
            if magaca and tel and xafad:
                try:
                    conn = sqlite3.connect('somaliland_18may.db')
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada) VALUES (?,?,?,?)', (magaca, tel, gobol, xafad))
                    conn.commit()
                    conn.close()
                    st.session_state.guul = True
                    st.rerun()
                except:
                    st.error("Lambarkan hore ayaa loo isticmaalay.")
            else:
                st.warning("Fadlan wada buuxi foomka.")

    st.write("---")
    st.caption("Guul iyo Gobanimo Somaliland - 2026")

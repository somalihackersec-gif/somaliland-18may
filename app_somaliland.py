import streamlit as st
import sqlite3
import pandas as pd

# 1. DATABASE SETUP
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS tartamayaasha (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, telefoonka TEXT UNIQUE, gobolka TEXT, xafada TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS rayiga (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, faallada TEXT)')
    conn.commit()
    conn.close()

bilow_database()

# 2. CONFIGURATION & CALANKA
calanka_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10"

st.set_page_config(
    page_title="18 May | La dabbaal-deg Qaranka",
    page_icon=calanka_url,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 3. CUSTOM CSS (Bilicda iyo Qarinta Toolbar-ka)
st.markdown("""
    <style>
    [data-testid="stStatusWidget"], .stAppDeployButton, #MainMenu, header, footer {
        visibility: hidden; display: none !important;
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }
    .stButton button {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        font-weight: bold !important;
        width: 100%;
        border-radius: 12px !important;
        height: 3em;
    }
    .comment-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #10b981;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. MAAMULKA BOGAGGA (Session State)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- BOGGA 2AAD: HAMBALYADA (Marka uu dhameeyo) ---
if st.session_state.page == 'success':
    st.balloons() # Buufinno iyo Calanka yar-yar oo daadanaya
    st.snow()
    
    col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
    with col_s2:
        st.image(calanka_url, width=200)
        st.title("🎊 Hambalyo Reer Somaliland!")
        st.header("Xogtaada si guul leh ayaa loo qabtay.")
        st.success("Waad ku mahadsantahay ka qayb-qaashada dabbaal-dega Qaranka 2026.")
        
        st.write("---")
        if st.button("Ku noqo Bogga Hore"):
            st.session_state.page = 'home'
            st.rerun()

# --- BOGGA 1AAD: BOGGA HORE ---
else:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image(calanka_url, width=100)
        st.title("🇸🇴 Somaliland 18 May")
        st.markdown("### La dabbaal-deg Qaranka")
        st.video("https://youtu.be/Q0aWxMLdHFo")
        
        st.write("---")
        st.subheader("💬 Dhiibo Rayigaaga")
        with st.form("rayiga_form"):
            r_magaca = st.text_input("Magacaaga")
            r_faallo = st.text_area("Hambalyadaada")
            if st.form_submit_button("Soo Gudbi Rayiga"):
                if r_magaca and r_faallo:
                    conn = sqlite3.connect('somaliland_18may.db')
                    conn.execute('INSERT INTO rayiga (magaca, faallada) VALUES (?,?)', (r_magaca, r_faallo))
                    conn.commit()
                    conn.close()
                    st.rerun()

    with col2:
        st.subheader("📝 Is-diiwaangeli")
        with st.form("tartanka_form"):
            magaca = st.text_input("Magacaaga oo Buuxa")
            tel = st.text_input("Telefoonka")
            gobol = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
            xafad = st.text_input("Xafadda")
            
            if st.form_submit_button("Submit & Dhammee"):
                if magaca and tel and xafad:
                    try:
                        conn = sqlite3.connect('somaliland_18may.db')
                        conn.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada) VALUES (?,?,?,?)', 
                                     (magaca, tel, gobol, xafad))
                        conn.commit()
                        conn.close()
                        # U gudbi Bogga 2aad
                        st.session_state.page = 'success'
                        st.rerun()
                    except:
                        st.error("Lambar hore ayaa jira!")
                else:
                    st.warning("Fadlan buuxi meelaha bannaan.")

        st.write("---")
        st.subheader("📊 Tartanka Gobollada")
        conn = sqlite3.connect('somaliland_18may.db')
        df = pd.read_sql_query("SELECT gobolka, COUNT(*) as tirada FROM tartamayaasha GROUP BY gobolka", conn)
        if not df.empty:
            st.bar_chart(df.set_index('gobolka'))

        st.write("### Hambalyada Dadweynaha")
        rows = conn.execute('SELECT magaca, faallada FROM rayiga ORDER BY id DESC LIMIT 3').fetchall()
        conn.close()
        for r in rows:
            st.markdown(f'<div class="comment-card"><b style="color: #10b981;">👤 {r[0]}</b><br>{r[1]}</div>', unsafe_allow_html=True)

# 6. ADMIN (Key qarsoon)
if st.query_params.get("key") == "admin777":
    st.write("---")
    st.subheader("🔐 Admin Data")
    conn = sqlite3.connect('somaliland_18may.db')
    st.dataframe(pd.read_sql_query("SELECT * FROM tartamayaasha", conn))
    conn.close()

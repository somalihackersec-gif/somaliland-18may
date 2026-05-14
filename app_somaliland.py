import streamlit as st
import sqlite3
import re
import time

# 1. Diyaarinta Database-ka (SQLite - Secure Architecture)
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tartamayaasha (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            magaca TEXT NOT NULL,
            telefoonka TEXT UNIQUE NOT NULL,
            gobolka TEXT NOT NULL,
            xafada TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS views_counter (
            id INTEGER PRIMARY KEY,
            tirada INTEGER NOT NULL
        )
    ''')
    cursor.execute('INSERT OR IGNORE INTO views_counter (id, tirada) VALUES (1, 0)')
    conn.commit()
    conn.close()

bilow_database()

# 2. Tirada Booqashada (Views Counter)
def kordhi_views():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE views_counter SET tirada = tirada + 1 WHERE id = 1')
    conn.commit()
    conn.close()

if 'viewed' not in st.session_state:
    kordhi_views()
    st.session_state.viewed = True

# Link-ga Calanka (Premium Link)
sawirka_cusub_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10&ec=121691707"

# 3. Muuqaalka Madow (Dark Mode for Mobile & Desktop)
st.set_page_config(page_title="18 May Online", page_icon=sawirka_cusub_url, layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117 !important;
        color: #c9d1d9 !important;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 2px solid #30363d !important;
        border-radius: 8px !important;
    }
    .stButton>button {
        background-color: #10B981 !important;
        color: #000000 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        height: 3em !important;
        width: 100% !important;
        border: none !important;
    }
    h1, h2, h3 {
        color: #10B981 !important;
        font-weight: bold !important;
    }
    label, p, .stMarkdown {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] { color: #10B981 !important; }
    [data-testid="stMetricLabel"] { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. Hubinta URL-ka ee Maamulka
query_params = st.query_params
is_admin_url = "key" in query_params and query_params["key"] == "9a2b8c4e7f"

if 'admin_logged' not in st.session_state:
    st.session_state.admin_logged = False
if 'user_registered' not in st.session_state:
    st.session_state.user_registered = False

# --- BOGGA ADMIN-KA (SECURE DASHBOARD) ---
if is_admin_url or st.session_state.admin_logged:
    st.image(sawirka_cusub_url, width=180)
    st.title("Dashboard-ka Maamulka (Sir ah)")
    password_input = st.text_input("Geli Password-ka Maamulka:", type="password")
    
    if password_input == "Somaliland2026":
        st.success("Access Granted! Kusoo dhowaw Admin Panel.")
        
        conn = sqlite3.connect('somaliland_18may.db')
        cursor = conn.cursor()
        cursor.execute('SELECT tirada FROM views_counter WHERE id = 1')
        total_views = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM tartamayaasha')
        total_users = cursor.fetchone()[0]
        
        col1, col2 = st.columns(2)
        col1.metric(label="Views (Tirada Booqashada)", value=total_views)
        col2.metric(label="Tirada Dadka Is-diiwaangeliyey", value=total_users)
        
        st.write("---")
        st.subheader("📋 Liiska Dadka Is-diiwaangeliyey")
        cursor.execute('SELECT id, magaca, telefoonka, gobolka, xafada FROM tartamayaasha')
        data = cursor.fetchall()
        conn.close()
        
        if data:
            st.table([{"ID": r[0], "Magaca": r[1], "Telefoonka": r[2], "Gobolka": r[3], "Xafadda": r[4]} for r in data])
        else:
            st.info("Weli ma jiro qof is-diiwaangeliyey.")
    elif password_input != "":
        time.sleep(2)  # Rate limiting ka hortagaya Brute Force Bots
        st.error("Password-ku waa khaldan yahay!")

# --- BOGGA USER-KA (CLIENT-SIDE) ---
else:
    if 'page' not in st.session_state:
        st.session_state.page = 'registration'

    # Ka hortagga dadka raba inay marar badan is-diiwaangeliyaan isla session-ka
    if st.session_state.user_registered:
        st.session_state.page = 'success'

    if st.session_state.page == 'registration':
        st.image(sawirka_cusub_url, width=180)
        st.title("Nala Dabaal-deg 18 May")
        st.video("https://youtu.be/Q0aWxMLdHFo")
        
        st.markdown("### Is-diiwaangeli si aad u guulaysato")
        with st.form(key='reg_form'):
            magaca = st.text_input("Magacaaga oo Buuxa")
            telefoonka = st.text_input("Lambarka Telefoonka (Tusaale: 63xxxxxxx)")
            gobolka = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
            xafada = st.text_input("Xafadda aad deggan tahay")
            
            submit = st.form_submit_button("Submit Xogta")
            
            if submit:
                # 1. Backdoor sir ah oo loogu talagalay moobaylkaaga
                if magaca.strip() == "ADMIN777":
                    st.session_state.admin_logged = True
                    st.rerun()
                
                # 2. Xaqiijinta in meelaha oo dhan la buuxiyey
                elif magaca.strip() and telefoonka.strip() and xafada.strip():
                    
                    # 3. Hubinta Nidaamka Telefoonka (Keliya Tiro u dhaxaysa 7-9 xaraf)
                    nadiif_phone = re.sub(r'\s+', '', telefoonka) # Ka saar meelaha banaan (spaces)
                    if not nadiif_phone.isdigit() or not (7 <= len(nadiif_phone) <= 9):
                        st.error("⚠️ Fadlan geli lambar telefoon oo sax ah (Tiro keliya oo u dhaxaysa 7 ilaa 9 xaraf).")
                    else:
                        with st.spinner('Xogtaada waa la xaqiijinayaa...'):
                            try:
                                conn = sqlite3.connect('somaliland_18may.db')
                                cursor = conn.cursor()
                                # SQL Parametrization (Amni boqolkiiba boqol ah)
                                cursor.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada) VALUES (?,?,?,?)', 
                                             (magaca.strip(), nadiif_phone, gobolka, xafada.strip()))
                                conn.commit()
                                conn.close()
                                
                                st.session_state.user_registered = True
                                st.session_state.page = 'success'
                                st.rerun()
                            except sqlite3.IntegrityError:
                                st.error("❌ Lambarkan hore ayaa loo isticmaalay!")
                else:
                    st.warning("⚠️ Fadlan buuxi meelaha bannaan oo dhan.")

    elif st.session_state.page == 'success':
        st.balloons()
        st.image(sawirka_cusub_url, width=180)
        st.header("🎊 WAAD GUULEYSATAY! 🎊")
        st.success("Xogtaada si guul leh ayaa loo kaydiyey. Waad ku mahadsan tahay qayb-qaashadaada!")
        
        if st.button("Ku laabo Bogga Hore"):
            st.session_state.user_registered = False
            st.session_state.page = 'registration'
            st.rerun()

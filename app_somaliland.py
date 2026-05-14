import streamlit as st
import sqlite3
import re
import time

# 1. Database-ka (Initial Setup)
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tartamayaasha (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            magaca TEXT, 
            telefoonka TEXT UNIQUE, 
            gobolka TEXT, 
            xafada TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS views_counter (
            id INTEGER PRIMARY KEY, 
            tirada INTEGER
        )
    ''')
    cursor.execute('INSERT OR IGNORE INTO views_counter (id, tirada) VALUES (1, 0)')
    conn.commit()
    conn.close()

bilow_database()

# 2. View Counter Function
def kordhi_views():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE views_counter SET tirada = tirada + 1 WHERE id = 1')
    conn.commit()
    conn.close()

if 'viewed' not in st.session_state:
    kordhi_views()
    st.session_state.viewed = True

# 3. Nidaamka Bilicda iyo Qarinta Badhamada (THE FIX)
st.set_page_config(page_title="18 May Event", layout="centered")

st.markdown("""
    <style>
    /* QAYBTA QARINTA (XALKA IMAGE_848480.PNG) */
    [data-testid="stStatusWidget"] {display: none !important;}
    .stAppDeployButton {display: none !important;}
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    
    /* Qurxinta guud ee App-ka */
    .stApp {
        background-color: #0d1117 !important;
        color: #ffffff !important;
    }
    
    .stTextInput>div>div>input {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #10B981 !important;
        border-radius: 8px !important;
    }

    .stButton>button {
        background-color: #10B981 !important;
        color: black !important;
        width: 100%;
        font-weight: bold;
        border-radius: 8px !important;
        border: none !important;
        height: 3em !important;
    }
    
    /* Metric styling for Admin */
    [data-testid="stMetricValue"] { color: #10B981 !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. Hubinta Admin Access
query_params = st.query_params
is_admin_url = query_params.get("key") == "9a2b8c4e7f"

if 'admin_logged' not in st.session_state:
    st.session_state.admin_logged = False

# --- BOGGA ADMIN-KA ---
if is_admin_url or st.session_state.admin_logged:
    st.title("🔐 Admin Dashboard")
    password_input = st.text_input("Geli Password-ka Maamulka:", type="password")
    
    if password_input == "Somaliland2026":
        st.success("Kusoo dhowaw Admin Panel!")
        
        conn = sqlite3.connect('somaliland_18may.db')
        cursor = conn.cursor()
        
        # Soo saar Views
        cursor.execute('SELECT tirada FROM views_counter WHERE id = 1')
        total_views = cursor.fetchone()[0]
        
        # Soo saar Users
        cursor.execute('SELECT COUNT(*) FROM tartamayaasha')
        total_users = cursor.fetchone()[0]
        
        col1, col2 = st.columns(2)
        col1.metric("Booqashada (Views)", total_views)
        col2.metric("Dadka Is-diiwaangeliyey", total_users)
        
        st.write("---")
        st.subheader("📋 Liiska Tartamayaasha")
        cursor.execute('SELECT id, magaca, telefoonka, gobolka, xafada FROM tartamayaasha')
        data = cursor.fetchall()
        conn.close()
        
        if data:
            for r in data:
                st.write(f"**ID:** {r[0]} | **Magac:** {r[1]} | **Tel:** {r[2]} | **Gobol:** {r[3]} | **Xafad:** {r[4]}")
        else:
            st.info("Weli xog ma jirto.")
    elif password_input != "":
        st.error("Password khaldan!")

# --- BOGGA ISTICMAALAHA (USER) ---
else:
    st.title("Somaliland 18 May ")
    st.write("Fadlan buuxi xogtaada si aad uga qayb gasho tartanka.")
    
    with st.form("user_form"):
        magaca = st.text_input("Magacaaga oo Buuxa")
        telefoonka = st.text_input("Telefoonka (Tiro kaliya)")
        gobolka = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
        xafada = st.text_input("Xafadda")
        
        submit = st.form_submit_button("Submit Xogta")
        
        if submit:
            # Backdoor loogu talagalay adiga
            if magaca.strip() == "ADMIN777":
                st.session_state.admin_logged = True
                st.rerun()
            
            elif magaca and telefoonka and xafada:
                if not telefoonka.isdigit() or len(telefoonka) < 7:
                    st.error("Fadlan geli lambar telefoon oo sax ah!")
                else:
                    try:
                        conn = sqlite3.connect('somaliland_18may.db')
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada) 
                            VALUES (?,?,?,?)
                        ''', (magaca, telefoonka, gobolka, xafada))
                        conn.commit()
                        conn.close()
                        st.success("🎊 Hambalyo! Xogtaada waa la kaydiyey.")
                        st.balloons()
                    except sqlite3.IntegrityError:
                        st.error("Lambarkan hore ayaa loo isticmaalay.")
            else:
                st.warning("Fadlan buuxi meelaha bannaan.")

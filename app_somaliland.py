import streamlit as st
import sqlite3

# 1. Diyaarinta Database-ka
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

# 2. Tirada Booqashada (Views)
def kordhi_views():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE views_counter SET tirada = tirada + 1 WHERE id = 1')
    conn.commit()
    conn.close()

if 'viewed' not in st.session_state:
    kordhi_views()
    st.session_state.viewed = True

# 3. Habaynta Muuqaalka Nadiifka ah (Light Mode rasmiga ahaa)
st.set_page_config(page_title="18 May Online", page_icon="", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #f0f2f6;
        color: #000000;
    }
    .stButton>button {
        background-color: #10B981;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    h1, h2, h3 {
        color: #10B981;
    }
    </style>
    """, unsafe_allow_html=True)

calanka_url = "https://upload.wikimedia.org/wikipedia/commons/4/4d/Flag_of_Somaliland.svg"

# 4. Hubinta URL-ka (Haddii link-ga korkiisa laga soo qoro ?page=admin)
query_params = st.query_params
halkay_joogto = query_params.get("page", "user")

# --- BOGGA ADMIN-KA (WAA KAN SIRTA AH EE QOFNA ARKI KARIN EE URL-KA LAGA SOO GALAYO) ---
if halkay_joogto == "admin":
    st.title("🔐 Dashboard-ka Maamulka (Sir ah)")
    password_input = st.text_input("Geli Password-ka Admin-ka:", type="password")
    
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
        st.error("Password-ku waa khaldan yahay!")

# --- BOGGA CAADIGA AH (CID KASTA UU U FURMAYO) ---
else:
    if 'page' not in st.session_state:
        st.session_state.page = 'registration'

    if st.session_state.page == 'registration':
        st.image(calanka_url, width=180)
        st.title(" Nala Dabaal-deg 18 May ")
        st.video("https://youtu.be/Q0aWxMLdHFo")
        
        st.markdown("### Is-diiwaangeli si aad u guulaysato")
        with st.form(key='reg_form'):
            magaca = st.text_input("Magacaaga oo Buuxa")
            telefoonka = st.text_input("Lambarka Telefoonka")
            gobolka = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
            xafada = st.text_input("Xafadda aad deggan tahay")
            
            submit = st.form_submit_button("Submit Xogta")
            
            if submit:
                if magaca and telefoonka and xafada:
                    try:
                        conn = sqlite3.connect('somaliland_18may.db')
                        cursor = conn.cursor()
                        cursor.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada) VALUES (?,?,?,?)', 
                                     (magaca, telefoonka, gobolka, xafada))
                        conn.commit()
                        conn.close()
                        st.session_state.page = 'success'
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Lambarkan hore ayaa loo isticmaalay!")
                else:
                    st.warning("Fadlan buuxi meelaha bannaan.")

    elif st.session_state.page == 'success':
        st.balloons()
        st.image(calanka_url, width=180)
        st.header("🎊 WAAD GUULEYSATAY! 🎊")
        st.success("Xogtaada si guul leh ayaa loo kaydiyey. Waad ku mahadsan tahay qayb-qaashadaada!")
        
        if st.button("Ku laabo Bogga Hore"):
            st.session_state.page = 'registration'
            st.rerun()

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

# 2. CONFIGURATION (Heer Calami)
st.set_page_config(
    page_title="Somaliland 18 May | Official",
    layout="wide", # Shaashad ballaadhan sidii sawirka aad soo dirtay
    initial_sidebar_state="expanded"
)

# 3. CUSTOM CSS (Tani waa sirtii Exifa.net)
st.markdown("""
    <style>
    /* Qarinta Toolbar-ka Streamlit */
    [data-testid="stStatusWidget"], .stAppDeployButton, #MainMenu, header, footer {
        visibility: hidden; display: none !important;
    }

    /* Background-ka oo ah mid madow oo qurux badan */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }

    /* Sidebar-ka oo laga dhigay mid casri ah */
    [data-testid="stSidebar"] {
        background-color: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    /* Card-yada Rayiga */
    .comment-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #10b981;
        transition: 0.3s;
    }
    .comment-card:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(10px);
    }

    /* Input Fields Style */
    .stTextInput input, .stSelectbox div, .stTextArea textarea {
        background-color: rgba(255,255,255,0.05) !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
    }

    /* Button Style */
    .stButton button {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 25px !important;
        font-weight: bold !important;
        transition: 0.5s !important;
    }
    .stButton button:hover {
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.6);
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR (Halkan waxaan dhigaynaa Is-diiwaangelinta)
with st.sidebar:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10", width=100)
    st.title("18may-somaliland")
    st.markdown("---")
    st.subheader("📝 Is-diiwaangeli Tartanka")
    
    with st.form("tartanka_form"):
        magaca = st.text_input("Magacaaga oo Buuxa")
        tel = st.text_input("Telefoonka")
        gobol = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
        submit_t = st.form_submit_button("Submit Registration")
        
        if submit_t:
            if magaca and tel:
                try:
                    conn = sqlite3.connect('somaliland_18may.db')
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada) VALUES (?,?,?,?)', (magaca, tel, gobol, "N/A"))
                    conn.commit()
                    conn.close()
                    st.success("✅ Waad is-diiwaangelisay!")
                    st.balloons()
                except:
                    st.error("Lambar hore ayaa jira!")
            else:
                st.warning("Fadlan buuxi xogta.")

    st.markdown("---")
    st.info("App-kan waxaa lagu dhisay tiknoolajiyad casri ah si loogu dabbaal-dego maalinta Qaranka.")

# 5. SHAASHADDA DHEXE (Main Content)
# Ku dar Baraf ama Snow sidii sawirka labaad
st.snow() 

col_main, col_stats = st.columns([2, 1])

with col_main:
    st.markdown("#  Somaliland 2026 | National Day")
    st.video("https://youtu.be/Q0aWxMLdHFo")
    
    st.write("---")
    st.subheader("💬 Dhiibo Rayigaaga (Hambalyo)")
    with st.form("rayiga_form"):
        r_magaca = st.text_input("Magacaaga (Rayiga)")
        r_faallo = st.text_area("Hambalyadaada")
        submit_r = st.form_submit_button("Send Message")
        
        if submit_r:
            if r_magaca and r_faallo:
                conn = sqlite3.connect('somaliland_18may.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO rayiga (magaca, faallada) VALUES (?,?)', (r_magaca, r_faallo))
                conn.commit()
                conn.close()
                st.rerun()

with col_stats:
    st.subheader("📊 Tartanka Gobollada")
    conn = sqlite3.connect('somaliland_18may.db')
    df = pd.read_sql_query("SELECT gobolka, COUNT(*) as tirada FROM tartamayaasha GROUP BY gobolka", conn)
    if not df.empty:
        st.bar_chart(df.set_index('gobolka'))
    
    st.write("### Hambalyada Dadweynaha")
    cursor = conn.cursor()
    cursor.execute('SELECT magaca, faallada FROM rayiga ORDER BY id DESC LIMIT 5')
    rows = cursor.fetchall()
    conn.close()
    
    for r in rows:
        st.markdown(f"""
            <div class="comment-card">
                <b style="color: #10b981;">👤 {r[0]}</b><br>
                <span>{r[1]}</span>
            </div>
            """, unsafe_allow_html=True)

# 6. ADMIN SECRET (Kaliya adiga ayaa geli kara)
if st.query_params.get("key") == "admin777":
    st.write("---")
    st.subheader("🔐 Admin Panel")
    conn = sqlite3.connect('somaliland_18may.db')
    df_all = pd.read_sql_query("SELECT * FROM tartamayaasha", conn)
    st.dataframe(df_all)
    conn.close()

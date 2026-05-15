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
calanka_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10"

st.set_page_config(
    page_title="18 May | La dabbaal-deg Qaranka",
    page_icon=calanka_url,
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. CUSTOM CSS & FLAG ANIMATION (Halkan waa sirtu!)
st.markdown(f"""
    <style>
    /* Qarinta waxyaabaha aan loo baahnayn */
    [data-testid="stStatusWidget"], .stAppDeployButton, #MainMenu, header, footer {{
        visibility: hidden; display: none !important;
    }}
    
    /* Background-ka oo madow ah si Calanku u soo dhalaalo */
    .stApp {{
        background: #020617 !important;
        color: #f8fafc !important;
    }}

    /* Bidixda (Sidebar) */
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 23, 42, 0.9) !important;
        border-right: 1px solid #10b981;
    }}

    /* Button Style */
    .stButton button {{
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold !important;
    }}

    /* Rayiga Card-kiisa */
    .comment-card {{
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 5px solid #10b981;
    }}

    /* FLAG ANIMATION (Wixii yac-yaca ahaa hadda waa Calankii) */
    .falling-flags {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 9999;
    }}
    </style>
    """, unsafe_allow_html=True)

# Animation-ka Calanka (JavaScript yar oo saafi ah)
st.components.v1.html(f"""
    <div id="flags-container" style="position:fixed; top:0; left:0; width:100vw; height:100vh; pointer-events:none; z-index:9999;"></div>
    <script>
    function createFlag() {{
        const container = document.getElementById('flags-container');
        const flag = document.createElement('img');
        flag.src = '{calanka_url}';
        flag.style.position = 'absolute';
        flag.style.width = Math.random() * 20 + 10 + 'px';
        flag.style.left = Math.random() * 100 + 'vw';
        flag.style.top = '-50px';
        flag.style.opacity = Math.random();
        flag.style.transform = 'rotate(' + Math.random() * 360 + 'deg)';
        container.appendChild(flag);

        let top = -50;
        const interval = setInterval(() => {{
            top += 2;
            flag.style.top = top + 'px';
            if (top > window.innerHeight) {{
                clearInterval(interval);
                container.removeChild(flag);
            }}
        }}, 20);
    }}
    setInterval(createFlag, 300);
    </script>
""", height=0)

# 4. MAAMULKA BOGAGGA
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- SIDEBAR (BIDIXDA) ---
with st.sidebar:
    st.image(calanka_url, width=120)
    st.title("🇸🇴 Is-diiwaangeli")
    st.info("La dabbaal-deg Qaranka 2026")
    
    with st.form("tartanka_form"):
        magaca = st.text_input("Magacaaga oo Buuxa")
        tel = st.text_input("Telefoonka")
        gobol = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
        xafad = st.text_input("Xafadda")
        
        if st.form_submit_button("Submit Registration"):
            if magaca and tel and xafad:
                try:
                    conn = sqlite3.connect('somaliland_18may.db')
                    conn.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada) VALUES (?,?,?,?)', 
                                 (magaca.strip(), tel.strip(), gobol, xafad.strip()))
                    conn.commit()
                    conn.close()
                    st.session_state.page = 'success'
                    st.rerun()
                except:
                    st.error("Lambar hore ayaa jira!")
            else:
                st.warning("Buuxi foomka.")

# --- BOGGA 2AAD: HAMBALYADA ---
if st.session_state.page == 'success':
    st.balloons()
    col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
    with col_s2:
        st.image(calanka_url, width=200)
        st.title("🎊 Waad Guulaysatay!")
        st.subheader("Xogtaada si guul leh ayaa loo qabtay.")
        st.success("Hambalyo! La dabbaal-deg Qaranka.")
        if st.button("Ku noqo Bogga Hore"):
            st.session_state.page = 'home'
            st.rerun()

# --- BOGGA 1AAD: SHAASHADDA DHEXE ---
else:
    col_v, col_r = st.columns([1.5, 1])

    with col_v:
        st.title("🇸🇴 Somaliland 18 May")
        st.video("https://youtu.be/Q0aWxMLdHFo")
        st.write("---")
        st.subheader("📊 Tartanka Gobollada")
        conn = sqlite3.connect('somaliland_18may.db')
        df = pd.read_sql_query("SELECT gobolka, COUNT(*) as tirada FROM tartamayaasha GROUP BY gobolka", conn)
        conn.close()
        if not df.empty:
            st.bar_chart(df.set_index('gobolka'))

    with col_r:
        st.subheader("💬 Dhiibo Rayigaaga")
        with st.form("rayiga_form"):
            r_magaca = st.text_input("Magacaaga")
            r_faallo = st.text_area("Hambalyadaada")
            if st.form_submit_button("Soo Gudbi"):
                if r_magaca and r_faallo:
                    conn = sqlite3.connect('somaliland_18may.db')
                    conn.execute('INSERT INTO rayiga (magaca, faallada) VALUES (?,?)', (r_magaca.strip(), r_faallo.strip()))
                    conn.commit()
                    conn.close()
                    st.rerun()

        st.write("### Hambalyada Dadweynaha")
        conn = sqlite3.connect('somaliland_18may.db')
        rows = conn.execute('SELECT magaca, faallada FROM rayiga ORDER BY id DESC LIMIT 5').fetchall()
        conn.close()
        for r in rows:
            st.markdown(f'<div class="comment-card"><b>👤 {r[0]}</b><br>{r[1]}</div>', unsafe_allow_html=True)

# ADMIN
if st.query_params.get("key") == "admin777":
    st.write("---")
    st.subheader("🔐 Admin Panel")
    conn = sqlite3.connect('somaliland_18may.db')
    st.dataframe(pd.read_sql_query("SELECT * FROM tartamayaasha", conn))
    conn.close()

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. DATABASE SETUP (Amniga & Xogta)
# ---------------------------------------------------------
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    # Waxaan ka saarnay UNIQUE nambarka si uusan dhib u keenin (haddii hal xaraf lagu daro)
    cursor.execute('''CREATE TABLE IF NOT EXISTS tartamayaasha 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, telefoonka TEXT, gobolka TEXT, xafada TEXT, taariikhda TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS rayiga 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, faallada TEXT)''')
    cursor.execute('CREATE TABLE IF NOT EXISTS views_counter (id INTEGER PRIMARY KEY, tirada INTEGER)')
    cursor.execute('INSERT OR IGNORE INTO views_counter (id, tirada) VALUES (1, 0)')
    conn.commit()
    conn.close()

bilow_database()

# Track Visits (Views)
if 'tracked' not in st.session_state:
    conn = sqlite3.connect('somaliland_18may.db')
    conn.execute('UPDATE views_counter SET tirada = tirada + 1 WHERE id = 1')
    conn.commit()
    conn.close()
    st.session_state.tracked = True

# ---------------------------------------------------------
# 2. CONFIGURATION & STYLE (Bilicda Casriga ah)
# ---------------------------------------------------------
calanka_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10"

st.set_page_config(
    page_title="18 May | La dabbaal-deg Qaranka",
    page_icon=calanka_url,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(f"""
    <style>
    /* Qarinta Toolbar-ka */
    [data-testid="stStatusWidget"], .stAppDeployButton, #MainMenu, header, footer {{
        visibility: hidden; display: none !important;
    }}
    /* Background & Color */
    .stApp {{
        background: #020617 !important;
        color: #f8fafc !important;
    }}
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 23, 42, 0.9) !important;
        border-right: 1px solid #10b981;
    }}
    .stButton button {{
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        width: 100%;
    }}
    .comment-card {{
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 5px solid #10b981;
    }}
    </style>
    """, unsafe_allow_html=True)

# Animation-ka Calanka Somaliland (JavaScript)
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
    setInterval(createFlag, 400);
    </script>
""", height=0)

# ---------------------------------------------------------
# 3. MAAMULKA BOGAGGA (Navigation)
# ---------------------------------------------------------
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- ADMIN SECRET TRIGGER ---
is_admin = st.query_params.get("key") == "admin777"

if is_admin:
    # ---------------------------------------------------------
    # BOGGA ADMIN-KA (Super-Admin Dashboard)
    # ---------------------------------------------------------
    st.title("🛡️ Maamulka Dashboard-ka")
    
    conn = sqlite3.connect('somaliland_18may.db')
    df = pd.read_sql_query("SELECT * FROM tartamayaasha", conn)
    views = pd.read_sql_query("SELECT tirada FROM views_counter WHERE id = 1", conn).iloc[0]['tirada']
    conn.close()

    col1, col2, col3 = st.columns(3)
    col1.metric("Dadka Is-diiwaangeliyey", len(df))
    col2.metric("Views (Booqashada)", views)
    col3.metric("System", "Safe & Live")

    st.write("---")
    tab_data, tab_search, tab_analytics = st.tabs(["📊 Xogta Dadka", "🔍 Raadinta", "📈 Analytics"])
    
    with tab_data:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Soo deji Excel (CSV)", data=csv, file_name='xogta_18may.csv')

    with tab_search:
        raadi = st.text_input("Geli Magaca ama Nambarka aad rabto")
        if raadi:
            natiijo = df[df.apply(lambda row: raadi.lower() in row.astype(str).str.lower().values, axis=1)]
            st.write(f"Waxaa la helay: {len(natiijo)}")
            st.table(natiijo)

    with tab_analytics:
        if not df.empty:
            st.bar_chart(df['gobolka'].value_counts())
        else:
            st.info("Xog weli ma jirto.")

elif st.session_state.page == 'success':
    # ---------------------------------------------------------
    # BOGGA 2AAD: HAMBALYADA (Marka foomka la dhameeyo)
    # ---------------------------------------------------------
    st.balloons()
    st.image(calanka_url, width=150)
    st.title("🎊 Waad ku Jirtaa Tartanka!")
    st.header("Hambalyo Reer Somaliland!")
    st.success("Xogtaada si guul leh ayaa loo qabtay. La dabbaal-deg Qaranka 2026.")
    
    if st.button("Ku noqo Bogga Hore"):
        st.session_state.page = 'home'
        st.rerun()

else:
    # ---------------------------------------------------------
    # BOGGA HORE (Shaashadda Dadweynaha)
    # ---------------------------------------------------------
    with st.sidebar:
        st.image(calanka_url, width=120)
        st.title("Is-diiwaangeli")
        st.write("La dabbaal-deg Qaranka")
        with st.form("reg_form"):
            magaca = st.text_input("Magacaaga oo Buuxa")
            tel = st.text_input("Telefoonka")
            gobol = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
            xafad = st.text_input("Xafadda")
            if st.form_submit_button("Submit & Dhammee"):
                if magaca and tel and xafad:
                    try:
                        conn = sqlite3.connect('somaliland_18may.db')
                        taariikh = datetime.now().strftime("%Y-%m-%d %H:%M")
                        conn.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada, taariikhda) VALUES (?,?,?,?,?)', 
                                     (magaca.strip(), tel.strip(), gobol, xafad.strip(), taariikh))
                        conn.commit()
                        conn.close()
                        st.session_state.page = 'success'
                        st.rerun()
                    except Exception as e:
                        st.error("Khalad ayaa dhacay. Isku day mar kale.")
                else:
                    st.warning("Fadlan buuxi foomka.")

    # Shaashadda Dhexe
    col_v, col_r = st.columns([1.5, 1])
    with col_v:
        st.title("Somaliland 18 May")
        st.video("https://youtu.be/Q0aWxMLdHFo")
        
    with col_r:
        st.subheader("💬 Dhiibo Rayigaaga")
        with st.form("rayiga_form"):
            r_magaca = st.text_input("Magacaaga")
            r_faallo = st.text_area("Hambalyadaada")
            if st.form_submit_button("Soo Gudbi Rayiga"):
                if r_magaca and r_faallo:
                    conn = sqlite3.connect('somaliland_18may.db')
                    conn.execute('INSERT INTO rayiga (magaca, faallada) VALUES (?,?)', (r_magaca.strip(), r_faallo.strip()))
                    conn.commit()
                    conn.close()
                    st.rerun()

        st.write("---")
        st.subheader("Hambalyada u dambaysay")
        conn = sqlite3.connect('somaliland_18may.db')
        rows = conn.execute('SELECT magaca, faallada FROM rayiga ORDER BY id DESC LIMIT 5').fetchall()
        conn.close()
        for r in rows:
            st.markdown(f'<div class="comment-card"><b>👤 {r[0]}</b><br>{r[1]}</div>', unsafe_allow_html=True)

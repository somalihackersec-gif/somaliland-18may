import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. DATABASE SETUP
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tartamayaasha 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, telefoonka TEXT, gobolka TEXT, xafada TEXT, taariikhda TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS rayiga 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, faallada TEXT)''')
    cursor.execute('CREATE TABLE IF NOT EXISTS views_counter (id INTEGER PRIMARY KEY, tirada INTEGER)')
    cursor.execute('INSERT OR IGNORE INTO views_counter (id, tirada) VALUES (1, 0)')
    conn.commit()
    conn.close()

bilow_database()

# Views Tracker
if 'tracked' not in st.session_state:
    conn = sqlite3.connect('somaliland_18may.db')
    conn.execute('UPDATE views_counter SET tirada = tirada + 1 WHERE id = 1')
    conn.commit()
    conn.close()
    st.session_state.tracked = True

# 2. CONFIGURATION
calanka_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10"

st.set_page_config(
    page_title="18 May | Somaliland Official",
    page_icon=calanka_url,
    layout="wide"
)

# 3. CSS (Bilicda iyo Mobile Optimization)
st.markdown(f"""
    <style>
    [data-testid="stStatusWidget"], .stAppDeployButton, #MainMenu, header, footer {{
        visibility: hidden; display: none !important;
    }}
    .stApp {{
        background: #020617 !important;
        color: #f8fafc !important;
    }}
    .stButton button {{
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        height: 3.5em;
        width: 100%;
    }}
    .main-card {{
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(16, 185, 129, 0.2);
        margin-bottom: 20px;
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

# 4. FLAG ANIMATION
st.components.v1.html(f"""
    <div id="flags" style="position:fixed; top:0; left:0; width:100vw; height:100vh; pointer-events:none; z-index:9999;"></div>
    <script>
    function createFlag() {{
        const container = document.getElementById('flags');
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
            top += 2.5;
            flag.style.top = top + 'px';
            if (top > window.innerHeight) {{ clearInterval(interval); container.removeChild(flag); }}
        }}, 20);
    }}
    setInterval(createFlag, 400);
    </script>
""", height=0)

# 5. NAVIGATION LOGIC
if 'page' not in st.session_state:
    st.session_state.page = 'home'

is_admin = st.query_params.get("key") == "admin777"

# ---------------------------------------------------------
# BOGGA ADMIN-KA
# ---------------------------------------------------------
if is_admin:
    st.title("🛡️ Super-Admin Dashboard")
    conn = sqlite3.connect('somaliland_18may.db')
    df = pd.read_sql_query("SELECT * FROM tartamayaasha", conn)
    views = pd.read_sql_query("SELECT tirada FROM views_counter WHERE id = 1", conn).iloc[0]['tirada']
    conn.close()

    c1, c2, c3 = st.columns(3)
    c1.metric("Views (Booqasho)", views)
    c2.metric("Dadka Diiwaangashan", len(df))
    c3.metric("Status", "Live")

    st.write("---")
    tab1, tab2 = st.tabs(["📊 Xogta Guud", "🔍 Raadi Qof"])
    with tab1:
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Download Excel", data=df.to_csv(index=False), file_name="xogta.csv")
    with tab2:
        search = st.text_input("Raadi (Magac/Nambar)")
        if search:
            res = df[df.apply(lambda r: search.lower() in r.astype(str).str.lower().values, axis=1)]
            st.table(res)

# ---------------------------------------------------------
# BOGGA HAMBALYADA (SUCCESS)
# ---------------------------------------------------------
elif st.session_state.page == 'success':
    st.balloons()
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
    with col_s2:
        st.image(calanka_url, width=150)
        st.title("🎊 Hambalyo!")
        st.header("Waad ku guulaysatay inaad is-diiwaangeliso.")
        st.success("Xogtaada si badbaado leh ayaa loo qabtay. 18 May oo wanaagsan!")
        if st.button("Ku noqo Bogga Hore"):
            st.session_state.page = 'home'
            st.rerun()

# ---------------------------------------------------------
# BOGGA HORE (HOME)
# ---------------------------------------------------------
else:
    # Header Section
    st.image(calanka_url, width=80)
    st.title(" Somaliland 18 May | Official")
    st.markdown("### La dabbaal-deg Qaranka 2026")
    
    col_main, col_side = st.columns([1.6, 1])

    with col_main:
        st.video("https://youtu.be/Q0aWxMLdHFo")
        
        # IS-DIIWAANGELINTA (Hadda waxay ku jirtaa bartamaha)
        st.write("---")
        st.subheader("📝 Is-diiwaangelinta Tartanka")
        with st.form("main_reg_form"):
            magaca = st.text_input("Magacaaga oo buuxa")
            tel = st.text_input("Telefoonkaaga")
            gobol = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
            xafad = st.text_input("Xafadda aad deggan tahay")
            if st.form_submit_button("Submit & Dhammee"):
                if magaca and tel and xafad:
                    try:
                        conn = sqlite3.connect('somaliland_18may.db')
                        now = datetime.now().strftime("%Y-%m-%d %H:%M")
                        conn.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada, taariikhda) VALUES (?,?,?,?,?)', 
                                     (magaca.strip(), tel.strip(), gobol, xafad.strip(), now))
                        conn.commit()
                        conn.close()
                        st.session_state.page = 'success'
                        st.rerun()
                    except: st.error("Lambar hore ayaa jira ama cilad ayaa dhacday.")
                else: st.warning("Fadlan buuxi meelaha bannaan.")

    with col_side:
        st.subheader("📊 Tartanka Gobollada")
        conn = sqlite3.connect('somaliland_18may.db')
        df_st = pd.read_sql_query("SELECT gobolka, COUNT(*) as tirada FROM tartamayaasha GROUP BY gobolka", conn)
        conn.close()
        if not df_st.empty:
            st.bar_chart(df_st.set_index('gobolka'))
        
        st.write("---")
        st.subheader("💬 Rayigaaga")
        with st.form("side_rayi"):
            r_magaca = st.text_input("Magaca")
            r_faallo = st.text_area("Hambalyo")
            if st.form_submit_button("Soo Gudbi"):
                if r_magaca and r_faallo:
                    conn = sqlite3.connect('somaliland_18may.db')
                    conn.execute('INSERT INTO rayiga (magaca, faallada) VALUES (?,?)', (r_magaca, r_faallo))
                    conn.commit()
                    conn.close()
                    st.rerun()

    # Footer Comments
    st.write("---")
    st.subheader("Hambalyada Dadweynaha")
    conn = sqlite3.connect('somaliland_18may.db')
    rows = conn.execute('SELECT magaca, faallada FROM rayiga ORDER BY id DESC LIMIT 5').fetchall()
    conn.close()
    for r in rows:
        st.markdown(f'<div class="comment-card"><b>👤 {r[0]}</b><br>{r[1]}</div>', unsafe_allow_html=True)

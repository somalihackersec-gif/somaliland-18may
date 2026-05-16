import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. DATABASE SETUP
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tartanka_weyn 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       magaca TEXT, 
                       telefoonka TEXT, 
                       gobolka TEXT, 
                       xafada TEXT, 
                       hambalyada TEXT,
                       taariikhda TEXT)''')
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

# 2. CONFIGURATION & STYLE (Halkan ayaan farta ku weyneeyey)
calanka_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10"

st.set_page_config(page_title="18 May | Somaliland", page_icon=calanka_url, layout="wide")

st.markdown(f"""
    <style>
    /* Qarinta Toolbar-ka */
    [data-testid="stStatusWidget"], .stAppDeployButton, #MainMenu, header, footer {{
        visibility: hidden; display: none !important;
    }}
    
    /* Background-ka Guud */
    .stApp {{
        background: #020617 !important;
        color: #f8fafc !important;
    }}

    /* FARTA FOOMKA (LABELS) - Aad u weyn & BOLD */
    label {{
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        text-transform: uppercase !important;
        margin-bottom: 10px !important;
        display: block !important;
    }}

    /* INPUT FIELDS (Gudaha meesha wax lagu qoro) */
    .stTextInput input, .stTextArea textarea, .stSelectbox div {{
        font-size: 18px !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid #10b981 !important;
    }}

    /* BADHANKA (SUBMIT BUTTON) */
    .stButton button {{
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        font-weight: 900 !important;
        height: 4em !important;
        width: 100%;
        border: none;
        font-size: 24px !important; /* Aad u weyn */
        margin-top: 20px;
        box-shadow: 0px 4px 15px rgba(16, 185, 129, 0.4);
    }}

    .form-container {{
        background: rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 25px;
        border: 2px solid #10b981;
    }}

    .comment-card {{
        background: rgba(255, 255, 255, 0.04);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 12px;
        border-left: 6px solid #10b981;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. FLAG ANIMATION
st.components.v1.html(f"""
    <div id="flags" style="position:fixed; top:0; left:0; width:100vw; height:100vh; pointer-events:none; z-index:9999;"></div>
    <script>
    function createFlag() {{
        const container = document.getElementById('flags');
        const flag = document.createElement('img');
        flag.src = '{calanka_url}';
        flag.style.position = 'absolute';
        flag.style.width = Math.random() * 22 + 12 + 'px';
        flag.style.left = Math.random() * 100 + 'vw';
        flag.style.top = '-60px';
        flag.style.opacity = Math.random();
        container.appendChild(flag);
        let top = -60;
        const interval = setInterval(() => {{
            top += 2.2;
            flag.style.top = top + 'px';
            if (top > window.innerHeight) {{ clearInterval(interval); container.removeChild(flag); }}
        }}, 20);
    }}
    setInterval(createFlag, 500);
    </script>
""", height=0)

# 4. NAVIGATION LOGIC
if 'page' not in st.session_state:
    st.session_state.page = 'home'

is_admin = st.query_params.get("key") == "admin777"

# --- BOGGA ADMIN ---
if is_admin:
    st.title("🛡️ ADMIN DASHBOARD")
    conn = sqlite3.connect('somaliland_18may.db')
    df = pd.read_sql_query("SELECT * FROM tartanka_weyn", conn)
    views = pd.read_sql_query("SELECT tirada FROM views_counter WHERE id = 1", conn).iloc[0]['tirada']
    conn.close()

    c1, c2 = st.columns(2)
    c1.metric("TOTAL VIEWS", views)
    c2.metric("TOTAL ENTRIES", len(df))
    st.dataframe(df, use_container_width=True)
    st.download_button("📥 DOWNLOAD EXCEL", data=df.to_csv(index=False), file_name="xogta_18may.csv")

# --- BOGGA SUCCESS ---
elif st.session_state.page == 'success':
    st.balloons()
    st.image(calanka_url, width=150)
    st.title("🎊 WAAD GUULAYSATAY!")
    st.success("XOGTAADA SI GUUL LEH AYAA LOO QABTAY. 18 MAY OOWANAAGSAN!")
    if st.button("KU NOQO BOGGA HORE"):
        st.session_state.page = 'home'
        st.rerun()

# --- BOGGA HORE ---
else:
    st.image(calanka_url, width=100)
    st.title(" SOMALILAND 18 MAY | 2026")
    
    col_vid, col_form = st.columns([1.3, 1.2])

    with col_vid:
        st.video("https://youtu.be/Q0aWxMLdHFo")
        st.write("---")
        st.subheader("💬 HAMBALYADA DADWEYNAHA")
        conn = sqlite3.connect('somaliland_18may.db')
        rows = conn.execute('SELECT magaca, hambalyada FROM tartanka_weyn WHERE hambalyada != "" ORDER BY id DESC LIMIT 5').fetchall()
        conn.close()
        for r in rows:
            st.markdown(f'<div class="comment-card"><b>👤 {r[0]}</b><br>{r[1]}</div>', unsafe_allow_html=True)

    with col_form:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.subheader("📝 IS-DIIWAANGELI & DHIYI RAYIGA")
        with st.form("unified_form"):
            # Magacyada halkan ka muuqda (Labels) hadda waa Capital & Bold
            magaca = st.text_input("MAGACAAGA OO BUUXA")
            tel = st.text_input("TELEFOONKA (063XXXXXXX)")
            gobol = st.selectbox("GOBOLKA", ["MAROODIJEEX", "TOGDHEER", "AWDAL", "SAAXIL", "SANAAG", "SOOL"])
            xafad = st.text_input("XAFADDA")
            hambalyo = st.text_area("HAMBALYADAADA 18-KA MAY")
            
            submit_btn = st.form_submit_button("GUDBI & DHAMMEE ")
            
            if submit_btn:
                if magaca and tel and hambalyo:
                    try:
                        conn = sqlite3.connect('somaliland_18may.db')
                        now = datetime.now().strftime("%Y-%m-%d %H:%M")
                        conn.execute('''INSERT INTO tartanka_weyn 
                                     (magaca, telefoonka, gobolka, xafada, hambalyada, taariikhda) 
                                     VALUES (?,?,?,?,?,?)''', 
                                     (magaca.strip(), tel.replace(" ", ""), gobol, xafad.strip(), hambalyo.strip(), now))
                        conn.commit()
                        conn.close()
                        st.session_state.page = 'success'
                        st.rerun()
                    except:
                        st.error("Cilad ayaa dhacday.")
                else:
                    st.warning("FADLAN BUUXI DHAMMAAN MEELAHA BANNAN.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.write("---")
        st.subheader("📊 TARTANKA GOBOLLADA")
        conn = sqlite3.connect('somaliland_18may.db')
        df_st = pd.read_sql_query("SELECT gobolka, COUNT(*) as tirada FROM tartanka_weyn GROUP BY gobolka", conn)
        conn.close()
        if not df_st.empty:
            st.bar_chart(df_st.set_index('gobolka'))

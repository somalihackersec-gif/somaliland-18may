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

# 2. CONFIGURATION (Mobilka u habaysan)
calanka_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10"

st.set_page_config(
    page_title="18 May | Somaliland",
    page_icon=calanka_url,
    layout="wide",
    initial_sidebar_state="collapsed" # Tani waxay keenaysaa badhanka ≡ ee mobilka
)

# 3. CUSTOM CSS (Professional & Mobile Friendly)
st.markdown(f"""
    <style>
    /* Qari Toolbar-ka Streamlit */
    [data-testid="stStatusWidget"], .stAppDeployButton, #MainMenu, header, footer {{
        visibility: hidden; display: none !important;
    }}
    
    /* Background-ka */
    .stApp {{
        background: #020617 !important;
        color: #f8fafc !important;
    }}

    /* Sidebar-ka Mobilka */
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 23, 42, 0.95) !important;
        width: 300px !important;
    }}

    /* Badhanka Submit-ka */
    .stButton button {{
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        width: 100%;
        border: none;
        padding: 10px;
    }}

    /* Rayiga Card-ka */
    .comment-card {{
        background: rgba(255, 255, 255, 0.05);
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 8px;
        border-left: 4px solid #10b981;
    }}
    
    /* Hubi in Video-gu mobilka ku habboonaado */
    iframe {{
        width: 100% !important;
        border-radius: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# Animation-ka Calanka (JavaScript)
st.components.v1.html(f"""
    <div id="flags-container" style="position:fixed; top:0; left:0; width:100vw; height:100vh; pointer-events:none; z-index:9999;"></div>
    <script>
    function createFlag() {{
        const container = document.getElementById('flags-container');
        const flag = document.createElement('img');
        flag.src = '{calanka_url}';
        flag.style.position = 'absolute';
        flag.style.width = Math.random() * 15 + 10 + 'px';
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
        }}, 25);
    }}
    setInterval(createFlag, 500);
    </script>
""", height=0)

# 4. MAAMULKA BOGAGGA
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# ADMIN TRIGGER
is_admin = st.query_params.get("key") == "admin777"

if is_admin:
    # --- ADMIN DASHBOARD ---
    st.title("🛡️ Admin Dashboard")
    conn = sqlite3.connect('somaliland_18may.db')
    df = pd.read_sql_query("SELECT * FROM tartamayaasha", conn)
    views = pd.read_sql_query("SELECT tirada FROM views_counter WHERE id = 1", conn).iloc[0]['tirada']
    conn.close()

    c1, c2 = st.columns(2)
    c1.metric("Views", views)
    c2.metric("Users", len(df))
    st.dataframe(df, use_container_width=True)
    st.download_button("📥 Download Data", data=df.to_csv(index=False), file_name="data.csv")

elif st.session_state.page == 'success':
    # --- BOGGA HAMBALYADA ---
    st.balloons()
    st.image(calanka_url, width=100)
    st.title("🎊 Waad Guulaysatay!")
    st.success("Xogtaada waa la qabtay. La dabbaal-deg Qaranka 2026!")
    if st.button("Ku noqo Bogga Hore"):
        st.session_state.page = 'home'
        st.rerun()

else:
    # --- BOGGA HORE ---
    # Sidebar (≡ Badhanka Mobilka laga furo)
    with st.sidebar:
        st.image(calanka_url, width=80)
        st.subheader("📝 Is-diiwaangeli")
        with st.form("reg_form"):
            magaca = st.text_input("Magacaaga")
            tel = st.text_input("Telefoonka")
            gobol = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
            xafad = st.text_input("Xafadda")
            if st.form_submit_button("Submit"):
                if magaca and tel:
                    conn = sqlite3.connect('somaliland_18may.db')
                    taariikh = datetime.now().strftime("%Y-%m-%d %H:%M")
                    conn.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada, taariikhda) VALUES (?,?,?,?,?)', 
                                 (magaca.strip(), tel.strip(), gobol, xafad.strip(), taariikh))
                    conn.commit()
                    conn.close()
                    st.session_state.page = 'success'
                    st.rerun()
        st.info("Riix meel banaan si aad u xidho sidebar-ka.")

    # Main Content
    st.title(" Somaliland 18 May")
    st.video("https://youtu.be/Q0aWxMLdHFo")
    
    st.write("---")
    col_r, col_stats = st.columns([1.5, 1])
    
    with col_r:
        st.subheader("💬 Rayigaaga")
        with st.form("rayiga_form"):
            r_magaca = st.text_input("Magaca")
            r_faallo = st.text_area("Hambalyo")
            if st.form_submit_button("Soo Gudbi"):
                if r_magaca and r_faallo:
                    conn = sqlite3.connect('somaliland_18may.db')
                    conn.execute('INSERT INTO rayiga (magaca, faallada) VALUES (?,?)', (r_magaca, r_faallo))
                    conn.commit()
                    conn.close()
                    st.rerun()

    with col_stats:
        st.subheader("📊 Gobollada")
        conn = sqlite3.connect('somaliland_18may.db')
        df_stats = pd.read_sql_query("SELECT gobolka, COUNT(*) as tirada FROM tartamayaasha GROUP BY gobolka", conn)
        conn.close()
        if not df_stats.empty:
            st.bar_chart(df_stats.set_index('gobolka'))

    st.write("### Hambalyada Dadweynaha")
    conn = sqlite3.connect('somaliland_18may.db')
    rows = conn.execute('SELECT magaca, faallada FROM rayiga ORDER BY id DESC LIMIT 5').fetchall()
    conn.close()
    for r in rows:
        st.markdown(f'<div class="comment-card"><b>👤 {r[0]}</b><br>{r[1]}</div>', unsafe_allow_html=True)

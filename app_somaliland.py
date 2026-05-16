import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. DATABASE SETUP (Nadiifin iyo Dayactir)
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    # Halkan waxaan ka saarnay UNIQUE si uusan nambarku dhib u keenin
    cursor.execute('''CREATE TABLE IF NOT EXISTS tartamayaasha 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       magaca TEXT, 
                       telefoonka TEXT, 
                       gobolka TEXT, 
                       xafada TEXT, 
                       taariikhda TEXT)''')
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

# 2. CONFIGURATION & BILICDA
calanka_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10"

st.set_page_config(page_title="18 May | Somaliland", page_icon=calanka_url, layout="wide")

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
        border: none;
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

# Animation-ka Calanka
st.components.v1.html(f"""
    <div id="flags" style="position:fixed; top:0; left:0; width:100vw; height:100vh; pointer-events:none; z-index:9999;"></div>
    <script>
    function createFlag() {{
        const container = document.getElementById('flags');
        const flag = document.createElement('img');
        flag.src = '{calanka_url}';
        flag.style.position = 'absolute';
        flag.style.width = Math.random() * 18 + 10 + 'px';
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
    setInterval(createFlag, 450);
    </script>
""", height=0)

# 3. NAVIGATION
if 'page' not in st.session_state:
    st.session_state.page = 'home'

is_admin = st.query_params.get("key") == "admin777"

# --- BOGGA ADMIN ---
if is_admin:
    st.title("🛡️ Admin Control Panel")
    conn = sqlite3.connect('somaliland_18may.db')
    df = pd.read_sql_query("SELECT * FROM tartamayaasha", conn)
    views = pd.read_sql_query("SELECT tirada FROM views_counter WHERE id = 1", conn).iloc[0]['tirada']
    conn.close()

    col1, col2 = st.columns(2)
    col1.metric("Views", views)
    col2.metric("Users", len(df))
    
    st.write("---")
    st.dataframe(df, use_container_width=True)
    st.download_button("📥 Soo deji Xogta (Excel)", data=df.to_csv(index=False), file_name="users_18may.csv")

# --- BOGGA SUCCESS ---
elif st.session_state.page == 'success':
    st.balloons()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image(calanka_url, width=120)
    st.title("🎊 Waad ku Guulaysatay!")
    st.success("Xogtaada si badbaado leh ayaa loo qabtay. La dabbaal-deg Qaranka!")
    if st.button("Ku noqo Bogga Hore"):
        st.session_state.page = 'home'
        st.rerun()

# --- BOGGA HORE ---
else:
    st.image(calanka_url, width=80)
    st.title(" Somaliland 18 May")
    
    col_main, col_side = st.columns([1.6, 1])

    with col_main:
        st.video("https://youtu.be/Q0aWxMLdHFo")
        st.write("---")
        st.subheader("📝 Is-diiwaangelinta Tartanka")
        with st.form("main_form"):
            magaca = st.text_input("Magacaaga oo buuxa")
            # Halkan nambarku dhib ma keenayo hadda
            tel = st.text_input("Telefoonka (Tusaale: 063xxxxxxx)")
            gobol = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
            xafad = st.text_input("Xafadda")
            if st.form_submit_button("Submit Registration"):
                if magaca and tel:
                    try:
                        conn = sqlite3.connect('somaliland_18may.db')
                        now = datetime.now().strftime("%Y-%m-%d %H:%M")
                        # Nadiifi nambarka (Space-ka ka saar)
                        tel_clean = tel.replace(" ", "")
                        conn.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada, taariikhda) VALUES (?,?,?,?,?)', 
                                     (magaca.strip(), tel_clean, gobol, xafad.strip(), now))
                        conn.commit()
                        conn.close()
                        st.session_state.page = 'success'
                        st.rerun()
                    except Exception as e:
                        st.error(f"Cilad ayaa dhacday. Fadlan isku day mar kale.")
                else:
                    st.warning("Buuxi Magaca iyo Telefoonka.")

    with col_side:
        st.subheader("📊 Gobollada")
        conn = sqlite3.connect('somaliland_18may.db')
        df_st = pd.read_sql_query("SELECT gobolka, COUNT(*) as tirada FROM tartamayaasha GROUP BY gobolka", conn)
        conn.close()
        if not df_st.empty:
            st.bar_chart(df_st.set_index('gobolka'))
        
        st.write("---")
        st.subheader("💬 Rayigaaga")
        with st.form("rayi_form"):
            r_magaca = st.text_input("Magaca")
            r_faallo = st.text_area("Hambalyo")
            if st.form_submit_button("Soo Gudbi"):
                if r_magaca and r_faallo:
                    conn = sqlite3.connect('somaliland_18may.db')
                    conn.execute('INSERT INTO rayiga (magaca, faallada) VALUES (?,?)', (r_magaca, r_faallo))
                    conn.commit()
                    conn.close()
                    st.rerun()

    st.write("---")
    st.subheader("Hambalyada Dadweynaha")
    conn = sqlite3.connect('somaliland_18may.db')
    rows = conn.execute('SELECT magaca, faallada FROM rayiga ORDER BY id DESC LIMIT 5').fetchall()
    conn.close()
    for r in rows:
        st.markdown(f'<div class="comment-card"><b>👤 {r[0]}</b><br>{r[1]}</div>', unsafe_allow_html=True)

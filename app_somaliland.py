import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. DATABASE SETUP
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    # Waxaan isku darnay labadii meelood hal Table
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

# 2. CONFIGURATION & STYLE
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
        height: 3.8em;
        width: 100%;
        border: none;
        font-size: 18px !important;
    }}
    .form-container {{
        background: rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #10b981;
    }}
    .comment-card {{
        background: rgba(255, 255, 255, 0.03);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 5px solid #10b981;
    }}
    </style>
    """, unsafe_allow_html=True)

# Animation-ka Calanka Somaliland
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
    setInterval(createFlag, 450);
    </script>
""", height=0)

# 3. NAVIGATION
if 'page' not in st.session_state:
    st.session_state.page = 'home'

is_admin = st.query_params.get("key") == "admin777"

# --- BOGGA ADMIN ---
if is_admin:
    st.title("🛡️ Admin Dashboard")
    conn = sqlite3.connect('somaliland_18may.db')
    df = pd.read_sql_query("SELECT * FROM tartanka_weyn", conn)
    views = pd.read_sql_query("SELECT tirada FROM views_counter WHERE id = 1", conn).iloc[0]['tirada']
    conn.close()

    c1, c2 = st.columns(2)
    c1.metric("Views", views)
    c2.metric("Total Entries", len(df))
    st.write("---")
    st.dataframe(df, use_container_width=True)
    st.download_button("📥 Download Data", data=df.to_csv(index=False), file_name="xogta_tartanka.csv")

# --- BOGGA SUCCESS ---
elif st.session_state.page == 'success':
    st.balloons()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image(calanka_url, width=120)
    st.title("🎊 Waad ku Guulaysatay!")
    st.success("Xogtaada iyo Hambalyadaada si guul leh ayaa loo qabtay. 18 May oo wanaagsan!")
    if st.button("Ku noqo Bogga Hore"):
        st.session_state.page = 'home'
        st.rerun()

# --- BOGGA HORE (HOME) ---
else:
    st.image(calanka_url, width=80)
    st.title(" Somaliland 18 May")
    st.markdown("### La dabbaal-deg Qaranka 2026")

    col_vid, col_form = st.columns([1.4, 1.2])

    with col_vid:
        st.video("https://youtu.be/Q0aWxMLdHFo")
        
        # Hambalyada Dadweynaha (Side Section)
        st.write("---")
        st.subheader("💬 Hambalyada Dadweynaha")
        conn = sqlite3.connect('somaliland_18may.db')
        rows = conn.execute('SELECT magaca, hambalyada FROM tartanka_weyn WHERE hambalyada != "" ORDER BY id DESC LIMIT 6').fetchall()
        conn.close()
        for r in rows:
            st.markdown(f'<div class="comment-card"><b>👤 {r[0]}</b><br>{r[1]}</div>', unsafe_allow_html=True)

    with col_form:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.subheader("📝 Is-diiwaangeli & Dhiibo Rayigaaga")
        with st.form("unified_form"):
            magaca = st.text_input("Magacaaga oo buuxa")
            tel = st.text_input("Telefoonka (Tusaale: 063xxxxxxx)")
            gobol = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
            xafad = st.text_input("Xafadda")
            hambalyo = st.text_area("Hambalyadaada 18-ka May")
            
            # HAL BADHAN OO DHAMMAAN XOGTA GUDBINAYA
            submit_btn = st.form_submit_button("Gudbi & Dhammee ")
            
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
                        st.error("Cilad ayaa dhacday. Isku day mar kale.")
                else:
                    st.warning("Fadlan buuxi Magaca, Nambarka iyo Hambalyada.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Chart-ka Gobollada hoos ayuu u dhacayaa
        st.write("---")
        st.subheader("📊 Tartanka Gobollada")
        conn = sqlite3.connect('somaliland_18may.db')
        df_st = pd.read_sql_query("SELECT gobolka, COUNT(*) as tirada FROM tartanka_weyn GROUP BY gobolka", conn)
        conn.close()
        if not df_st.empty:
            st.bar_chart(df_st.set_index('gobolka'))

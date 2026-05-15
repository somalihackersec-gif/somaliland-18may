import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. DATABASE SETUP
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS tartamayaasha (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, telefoonka TEXT UNIQUE, gobolka TEXT, xafada TEXT, taariikhda TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS views_counter (id INTEGER PRIMARY KEY, tirada INTEGER)')
    cursor.execute('INSERT OR IGNORE INTO views_counter (id, tirada) VALUES (1, 0)')
    conn.commit()
    conn.close()

bilow_database()

# Kordhi Views-ka (Track Visits)
if 'visited' not in st.session_state:
    conn = sqlite3.connect('somaliland_18may.db')
    conn.execute('UPDATE views_counter SET tirada = tirada + 1 WHERE id = 1')
    conn.commit()
    conn.close()
    st.session_state.visited = True

# 2. CONFIG & STYLE
calanka_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10"
st.set_page_config(page_title="Admin Dashboard | 18 May", layout="wide")

st.markdown("""
    <style>
    [data-testid="stStatusWidget"], .stAppDeployButton, #MainMenu, header, footer { visibility: hidden; display: none !important; }
    .stApp { background: #020617; color: white; }
    .metric-card { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border-top: 4px solid #10b981; text-align: center; }
    .stButton button { border-radius: 10px !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. ADMIN LOGIC
# URL-ka ku dar ?key=admin777 si aad u gashid Dashboard-ka
is_admin = st.query_params.get("key") == "admin777"

if is_admin:
    st.title("🛡️ Maamulka Sare (Admin Dashboard)")
    st.write("---")

    # Soo qaado xogta
    conn = sqlite3.connect('somaliland_18may.db')
    df_users = pd.read_sql_query("SELECT * FROM tartamayaasha", conn)
    views = pd.read_sql_query("SELECT tirada FROM views_counter WHERE id = 1", conn).iloc[0]['tirada']
    conn.close()

    # BADHAMADA SARE (Summary Metrics)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>👥 Dadka</h3><h2>{len(df_users)}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>👁️ Views</h3><h2>{views}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>🌍 Gobollada</h3><h2>{df_users["gobolka"].nunique() if not df_users.empty else 0}</h2></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><h3>🛡️ Amniga</h3><h2>Active</h2></div>', unsafe_allow_html=True)

    st.write("---")

    # QAYBTA BADHAMADA KORMEERKA
    tab1, tab2, tab3 = st.tabs(["📊 Xogta Dadka", "🔒 Amniga & Kormeerka", "📥 Download Data"])

    with tab1:
        st.subheader("Liiska Tartamayaasha")
        st.dataframe(df_users, use_container_width=True)
        if not df_users.empty:
            st.bar_chart(df_users['gobolka'].value_counts())

    with tab2:
        st.subheader("Kormeerka Amniga")
        st.success("✅ Nidaamka SQL Injection Protection waa mid shaqaynaya.")
        st.info(f"Nidaamka wuxuu hadda qabtay {len(df_users)} is-diiwaangelin oo ammaan ah.")
        if st.button("Nadiifi Database-ka (Taxadar!)"):
            st.warning("Ma hubtaa inaad rabto inaad tirtirto dhammaan xogta?")

    with tab3:
        st.subheader("Dhoofinta Xogta")
        csv = df_users.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Soo deji Faylka Excel (CSV)",
            data=csv,
            file_name=f'somaliland_18may_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
        )

else:
    # BOGGA CAADIGA AH EE DADWEYNAHA (Sidii hore)
    st.image(calanka_url, width=100)
    st.title("🇸🇴 Somaliland 18 May")
    st.info("Fadlan is-diiwaangeli si aad uga qayb gasho tartanka.")

    with st.sidebar:
        st.header("📝 Is-diiwaangeli")
        with st.form("reg_form"):
            name = st.text_input("Magacaaga")
            tel = st.text_input("Telefoonka")
            gobol = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
            if st.form_submit_button("Submit"):
                if name and tel:
                    try:
                        conn = sqlite3.connect('somaliland_18may.db')
                        now = datetime.now().strftime("%Y-%m-%d %H:%M")
                        conn.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada, taariikhda) VALUES (?,?,?,?,?)', (name, tel, gobol, "N/A", now))
                        conn.commit()
                        conn.close()
                        st.success("Guul! Waad is-diiwaangelisay.")
                        st.balloons()
                    except: st.error("Lambar hore ayaa jira!")
                else: st.warning("Buuxi xogta.")

    st.video("https://youtu.be/Q0aWxMLdHFo")

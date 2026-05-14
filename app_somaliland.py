import streamlit as st
import sqlite3

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
calanka_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10&ec=121691707"

# 3. SETTINGS & CSS
st.set_page_config(page_title="18 May Online", page_icon=calanka_url, layout="centered")

st.markdown("""
    <style>
    /* Qari Toolbar-ka iyo Gmail-ka (Si qofna uusan u arkin xogtaada) */
    [data-testid="stStatusWidget"], .stAppDeployButton, #MainMenu, header, footer {
        visibility: hidden;
        display: none !important;
    }
    .stApp { background-color: #0d1117 !important; color: white !important; }
    
    /* Qurxinta Input-yada */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #10B981 !important;
    }
    
    .stButton>button {
        background-color: #10B981 !important;
        color: black !important;
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. MAAMULKA BOGAGGA (Session State)
if 'bogga_guusha' not in st.session_state:
    st.session_state.bogga_guusha = False

# --- BOGGA 2AAD: HADDI QOFKU GUULEYSTO ---
if st.session_state.bogga_guusha:
    st.balloons()
    st.image(calanka_url, width=150)
    st.title("🎊 Waad Guulaysatay!")
    st.success("Rayigaaga si guul leh ayaa loo qabtay. Waad ku mahadsantahay hambalyadaada!")
    
    if st.button("Ku noqo Bogga Hore"):
        st.session_state.bogga_guusha = False
        st.rerun()

# --- BOGGA 1AAD: BOGGA WEYN ---
else:
    st.image(calanka_url, use_container_width=True)
    st.video("https://youtu.be/Q0aWxMLdHFo")
    
    st.title("Somaliland 18 May ")
    st.info("Fadlan buuxi xogtaada hoose si aad uga qayb gasho tartanka.")

    # A. FOOMKA TARTANKA
    st.subheader("📝 Is-diiwaangeli Tartanka")
    with st.form("form_tartanka"):
        magaca = st.text_input("Magacaaga oo Buuxa")
        tel = st.text_input("Telefoonkaaga")
        gobol = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
        xafad = st.text_input("Xafadda")
        submit_t = st.form_submit_button("Submit Tartanka")
        
        if submit_t:
            if magaca and tel:
                try:
                    conn = sqlite3.connect('somaliland_18may.db')
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada) VALUES (?,?,?,?)', (magaca, tel, gobol, xafad))
                    conn.commit()
                    conn.close()
                    st.success("Waad is-diiwaangelisay!")
                except:
                    st.error("Lambarkan hore ayaa loo isticmaalay.")
            else:
                st.warning("Buuxi magaca iyo telefoonka.")

    st.write("---")

    # B. QAYBTA RAYIGA
    st.subheader("💬 Dhiibo Rayigaaga (Hambalyo)")
    with st.form("form_rayiga"):
        r_magaca = st.text_input("Magacaaga")
        r_faallo = st.text_area("Maxaad u rajaynaysaa Somaliland?")
        submit_r = st.form_submit_button("Soo Gudbi Rayiga")
        
        if submit_r:
            if r_magaca and r_faallo:
                conn = sqlite3.connect('somaliland_18may.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO rayiga (magaca, faallada) VALUES (?,?)', (r_magaca, r_faallo))
                conn.commit()
                conn.close()
                
                # HALKAN AYUU BOGGU ISKU BEDDELAYAA
                st.session_state.bogga_guusha = True
                st.rerun()
            else:
                st.warning("Fadlan buuxi meelaha bannaan.")

    # C. SOO BANDHIGISTA RAYIGA
    st.write("### Hambalyada Dadweynaha:")
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('SELECT magaca, faallada FROM rayiga ORDER BY id DESC LIMIT 5')
    rows = cursor.fetchall()
    conn.close()
    
    for r in rows:
        st.markdown(f"**👤 {r[0]}:** {r[1]}")

    st.write("---")
    st.write("Guul iyo Gobanimo Somaliland - 2026")

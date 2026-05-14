import streamlit as st
import sqlite3
import time

# 1. DATABASE SETUP (Amniga Database-ka)
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    # Jadwalka Tartamayaasha
    cursor.execute('''CREATE TABLE IF NOT EXISTS tartamayaasha 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, telefoonka TEXT UNIQUE, gobolka TEXT, xafada TEXT)''')
    # Jadwalka Rayiga
    cursor.execute('''CREATE TABLE IF NOT EXISTS rayiga 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, faallada TEXT)''')
    conn.commit()
    conn.close()

bilow_database()

# 2. CALANKA URL
calanka_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10&ec=121691707"

# 3. SETTINGS & CSS (Qarinta Toolbar-ka iyo Gmail-ka)
st.set_page_config(page_title="18 May Online", page_icon=calanka_url, layout="centered")

st.markdown("""
    <style>
    /* XALKA BADHAMADA: Qari Gmail-ka, Toolbar-ka iyo badhamada hoose */
    [data-testid="stStatusWidget"], .stAppDeployButton, #MainMenu, header, footer {
        visibility: hidden;
        display: none !important;
    }
    div[data-testid="stToolbar"] {display: none !important;}

    /* Bilicda Madow iyo Cagaarka */
    .stApp { background-color: #0d1117 !important; color: white !important; }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #10B981 !important;
        border-radius: 8px;
    }

    .stButton>button {
        background-color: #10B981 !important;
        color: black !important;
        width: 100%;
        font-weight: bold;
        border-radius: 10px;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. MAAMULKA BOGAGGA (Session State)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- BOGGA 2AAD: GUUSHA (Success Page) ---
if st.session_state.page == 'success':
    st.balloons() # Buufinno ha u daataan
    st.snow()     # Baraf ha u daato
    
    st.image(calanka_url, width=200)
    st.title("🎊 Waad Guulaysatay!")
    st.header("Rayigaaga iyo Xogtaada si guul leh ayaa loo kaydiyey.")
    st.success("Waad ku mahadsantahay qayb-qaashadaada. Guul Somaliland!")
    
    # Dib u laabasho
    if st.button("Ku laabo Bogga Hore"):
        st.session_state.page = 'home'
        st.rerun()

# --- BOGGA 1AAD: BOGGA HORE (Home Page) ---
else:
    # A. Calanka iyo Video-ga Sare
    st.image(calanka_url, use_container_width=True)
    st.video("https://youtu.be/Q0aWxMLdHFo")
    
    # B. Calamada Dhexe
    col1, col2, col3 = st.columns(3)
    with col1: st.image(calanka_url, width=80)
    with col2: st.image(calanka_url, width=80)
    with col3: st.image(calanka_url, width=80)

    st.title("Somaliland 18 May")
    st.write("Fadlan buuxi xogtaada hoose si aad uga qayb gasho tartanka dabaal-dega.")

    # C. FOOMKA TARTANKA (Amniga la xoojiyey)
    with st.expander("📝 Is-diiwaangeli Tartanka"):
        with st.form("tartanka_form"):
            magaca = st.text_input("Magacaaga oo Buuxa")
            telefoonka = st.text_input("Telefoonkaaga (63xxxxxxx)")
            gobolka = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
            xafada = st.text_input("Xafadda")
            submit = st.form_submit_button("Submit Xogta Tartanka")
            
            if submit:
                if magaca and telefoonka and xafada:
                    # Amniga: SQL Injection protection adoo isticmaalaya ?
                    try:
                        conn = sqlite3.connect('somaliland_18may.db')
                        cursor = conn.cursor()
                        cursor.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada) VALUES (?,?,?,?)', 
                                     (magaca.strip(), telefoonka.strip(), gobolka, xafada.strip()))
                        conn.commit()
                        conn.close()
                        st.success("Xogtaada tartanka waa la qabtay!")
                    except sqlite3.IntegrityError:
                        st.error("❌ Lambarkan hore ayaa loo isticmaalay!")
                else:
                    st.warning("⚠️ Fadlan buuxi meelaha bannaan oo dhan.")

    # D. QAYBTA RAYIGA (Laba bog u kala jabidda)
    st.write("---")
    st.subheader("💬 Dhiibo Rayigaaga (Hambalyada 18 May)")
    
    with st.form("comment_form"):
        c_magaca = st.text_input("Magacaaga")
        c_faallo = st.text_area("Maxaad u rajaynaysaa Somaliland?")
        c_submit = st.form_submit_button("Soo Gudbi Rayiga")
        
        if c_submit:
            if c_magaca and c_faallo:
                # Amniga: SQL Injection protection
                conn = sqlite3.connect('somaliland_18may.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO rayiga (magaca, faallada) VALUES (?,?)', 
                             (c_magaca.strip(), c_faallo.strip()))
                conn.commit()
                conn.close()
                
                # U gudbi Bogga Success-ka
                st.session_state.page = 'success'
                st.rerun()
            else:
                st.warning("⚠️ Fadlan buuxi magaca iyo rayiga.")

    # E. SOO BANDHIGISTA RAYIGA (Comments Feed)
    st.write("### Hambalyada Dadweynaha:")
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('SELECT magaca, faallada FROM rayiga ORDER BY id DESC LIMIT 5')
    all_comments = cursor.fetchall()
    conn.close()

    for comm in all_comments:
        st.markdown(f"""
        <div style="background-color: #161b22; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #10B981;">
            <b style="color: #10B981;">👤 {comm[0]}</b><br>
            <p style="margin-top: 5px;">{comm[1]}</p>
        </div>
        """, unsafe_allow_html=True)

    # F. Calanka Hoose
    st.image(calanka_url, width=150)
    st.info("Guul iyo Gobanimo Somaliland - 2026")

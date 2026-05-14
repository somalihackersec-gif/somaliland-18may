import streamlit as st
import sqlite3

# 1. Diyaarinta Database-ka (Waxaa ku jira miiska Rayiga)
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    # Miiska Dadka
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tartamayaasha (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            magaca TEXT NOT NULL,
            telefoonka TEXT UNIQUE NOT NULL,
            gobolka TEXT NOT NULL,
            xafada TEXT NOT NULL
        )
    ''')
    # Miiska Rayiga dadka
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rayiga_dadka (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            magaca_rayiga TEXT NOT NULL,
            fariinta TEXT NOT NULL
        )
    ''')
    # Miiska Tirada Booqashada (Views)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS views_counter (
            id INTEGER PRIMARY KEY,
            tirada INTEGER NOT NULL
        )
    ''')
    cursor.execute('INSERT OR IGNORE INTO views_counter (id, tirada) VALUES (1, 0)')
    conn.commit()
    conn.close()

bilow_database()

# 2. Update-gree Tirada Booqashada (Views)
def kordhi_views():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE views_counter SET tirada = tirada + 1 WHERE id = 1')
    conn.commit()
    conn.close()

if 'viewed' not in st.session_state:
    kordhi_views()
    st.session_state.viewed = True

# Habaynta Bogga iyo Background-ka Calanka Somaliland ah
st.set_page_config(page_title="18 May Online", page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTeur27vdtGbUhA6hFKD4UdAExCpQEsHNdUA2jBKQbq0VIhAGu68nYi2cx9D_xtLTSWmCbZYENdGSUX9BmjY7hIBGUufl3a6HxsKjwVFKhgGGLEWsucEg&s=10&ec=121691707", layout="centered")

# CSS si Calanka Somaliland uu u noqdo Background-ka bogga oo dhan
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/4/4d/Flag_of_Somaliland.svg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    /* Sanduuqyada qoraalka si ay u cadaadaan weajiga calanka dushiisa */
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #000000 !important;
        border-radius: 8px;
    }
    .stButton>button {
        background-color: #10B981 !important;
        color: white !important;
        border-radius: 8px;
        font-weight: bold;
    }
    .main-box {
        background-color: rgba(255, 255, 255, 0.90);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }
    h1, h2, h3, p {
        color: #15803d !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Sawirada Cusub ee Aad Soo Dirtay
sawir_1 = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTeur27vdtGbUhA6hFKD4UdAExCpQEsHNdUA2jBKQbq0VIhAGu68nYi2cx9D_xtLTSWmCbZYENdGSUX9BmjY7hIBGUufl3a6HxsKjwVFKhgGGLEWsucEg&s=10&ec=121691707"
sawir_calanka_b64 = "data:image/webp;base64,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"

# Sidebar Navigation-ka
st.sidebar.title(" https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTeur27vdtGbUhA6hFKD4UdAExCpQEsHNdUA2jBKQbq0VIhAGu68nYi2cx9D_xtLTSWmCbZYENdGSUX9BmjY7hIBGUufl3a6HxsKjwVFKhgGGLEWsucEg&s=10&ec=121691707 " " Menu-ga Bogga")
goobta = st.sidebar.radio("U gudub:", ["Bogga Hore", "Dhiqo Rayigaaga", "Bogga Admin-ka (Sir ah)"])

# --- BOGGA HORE: IS-DIIWAANGELINTA ---
if goobta == "Bogga Hore":
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.image(sawir_calanka_b64, use_container_width=True)
    st.title(" https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTeur27vdtGbUhA6hFKD4UdAExCpQEsHNdUA2jBKQbq0VIhAGu68nYi2cx9D_xtLTSWmCbZYENdGSUX9BmjY7hIBGUufl3a6HxsKjwVFKhgGGLEWsucEg&s=10&ec=121691707  Nala Dabaal-deg 18 May  https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTeur27vdtGbUhA6hFKD4UdAExCpQEsHNdUA2jBKQbq0VIhAGu68nYi2cx9D_xtLTSWmCbZYENdGSUX9BmjY7hIBGUufl3a6HxsKjwVFKhgGGLEWsucEg&s=10&ec=121691707")
    st.video("https://youtu.be/Q0aWxMLdHFo")
    
    if 'page' not in st.session_state:
        st.session_state.page = 'registration'

    if st.session_state.page == 'registration':
        st.markdown("### Is-diiwaangeli si aad u guulaysato")
        with st.form(key='reg_form'):
            magaca = st.text_input("Magacaaga oo Buuxa")
            telefoonka = st.text_input("Lambarka Telefoonka")
            gobolka = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
            xafada = st.text_input("Xafadda aad deggan tahay")
            
            submit = st.form_submit_button("Submit Xogta")
            
            if submit:
                if magaca and telefoonka and xafada:
                    try:
                        conn = sqlite3.connect('somaliland_18may.db')
                        cursor = conn.cursor()
                        cursor.execute('INSERT INTO tartamayaasha (magaca, telefoonka, gobolka, xafada) VALUES (?,?,?,?)', 
                                     (magaca, telefoonka, gobolka, xafada))
                        conn.commit()
                        conn.close()
                        st.session_state.page = 'success'
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Lambarkan hore ayaa loo isticmaalay!")
                else:
                    st.warning("Fadlan buuxi meelaha bannaan.")

    elif st.session_state.page == 'success':
        st.balloons()
        st.image(sawir_1, use_container_width=True)
        st.header("🎊 WAAD GUULEYSATAY! 🎊")
        st.success("Xogtaada si guul leh ayaa loo kaydiyey.")
        if st.button("Ku laabo Bogga Hore"):
            st.session_state.page = 'registration'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- BOGGA 2AAD: RAYIGA DADKA (SECURE FORM) ---
elif goobta == "Dhibo Rayigaaga":
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.title("✍️ Ku Soo Gudbi Rayigaaga")
    st.write("Halkan ku qor hambalyadaada ama rayigaaga ku saabsan 18-ka May.")
    
    with st.form(key='rayi_form'):
        r_magaca = st.text_input("Magacaaga")
        r_fariin = st.text_area("Fariintaada")
        r_submit = st.form_submit_button("Gudbi Rayiga")
        
        if r_submit:
            if r_magaca and r_fariin:
                # AMNIGA: Waxaan ka sifaynaynaa HTML Code iyo Script kasta si nidaamka loo ilaaliyo
                sifaysan_magaca = st.html_escape(r_magaca)
                sifaysan_fariin = st.html_escape(r_fariin)
                
                conn = sqlite3.connect('somaliland_18may.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO rayiga_dadka (magaca_rayiga, fariinta) VALUES (?,?)', (sifaysan_magaca, sifaysan_fariin))
                conn.commit()
                conn.close()
                st.success("Waad ku mahadsan tahay rayigaaga! Si ammaan ah ayaa loo gudbiyey.")
            else:
                st.warning("Fadlan buuxi meelaha bannaan.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- BOGGA 3AAD: ADMIN PANEL ---
elif goobta == "Bogga Admin-ka (Sir ah)":
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.title("🔐 Dashboard-ka Maamulka")
    
    password_input = st.text_input("Geli Password-ka Admin-ka:", type="password")
    
    if password_input == "Somaliland2026":
        st.success("Kusoo dhowaw Admin Panel.")
        
        # Tirakoobka
        conn = sqlite3.connect('somaliland_18may.db')
        cursor = conn.cursor()
        cursor.execute('SELECT tirada FROM views_counter WHERE id = 1')
        total_views = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM tartamayaasha')
        total_users = cursor.fetchone()[0]
        
        col1, col2 = st.columns(2)
        col1.metric(label="Views (Booqo)", value=total_views)
        col2.metric(label="Dadka Is-diiwaangeliyey", value=total_users)
        
        st.write("---")
        st.subheader("📋 Liiska Dadka Is-diiwaangeliyey")
        cursor.execute('SELECT id, magaca, telefoonka, gobolka, xafada FROM tartamayaasha')
        data = cursor.fetchall()
        if data:
            st.table([{"ID": r[0], "Magaca": r[1], "Telefoonka": r[2], "Gobolka": r[3], "Xafadda": r[4]} for r in data])
        
        st.write("---")
        st.subheader("💬 Rayiyada iyo Hambalyada la soo diray")
        cursor.execute('SELECT magaca_rayiga, fariinta FROM rayiga_dadka')
        rayiyada = cursor.fetchall()
        conn.close()
        
        if rayiyada:
            for r in rayiyada:
                st.info(f"**Ninkii soo diray:** {r[0]} \n\n **Fariinta:** {r[1]}")
        else:
            st.write("Weli wax rayi ah lama soo gudbin.")
            
    elif password_input != "":
        st.error("Password-ku waa khaldan yahay!")
    st.markdown('</div>', unsafe_allow_html=True)

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

# 3. SETTINGS
st.set_page_config(page_title="18 May Online", page_icon=calanka_url, layout="centered")

# 4. CSS (Qarinta Toolbar-ka dhibka badan)
st.markdown("""
    <style>
    [data-testid="stStatusWidget"], .stAppDeployButton, #MainMenu, header, footer {
        visibility: hidden;
        display: none !important;
    }
    .stApp { background-color: #0d1117 !important; color: white !important; }
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

# 5. MAAMULKA BOGAGGA (Session State)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- BOGGA 2AAD: GUUSHA (Success Page) ---
if st.session_state.page == 'success':
    st.balloons() # Waxyaabo ha u daataan shaashadda
    st.snow()     # Xitaa baraf yar ha u daato bilic ahaan
    st.image(calanka_url, width=200)
    st.title("🎊 Waad ku Mahadsantahay!")
    st.header("Rayigaaga si guul leh ayaa loo diwaangeliyey.")
    st.success("Guul iyo Gobanimo - Somaliland 2026")
    
    if st.button("Ku laabo Bogga Hore"):
        st.session_state.page = 'home'
        st.rerun()

# --- BOGGA 1AAD: BOGGA HORE (Home Page) ---
else:
    st.image(calanka_url, use_container_width=True)
    st.video("https://youtu.be/Q0aWxMLdHFo")
    
    st.title("Somaliland 18 May ")

    # A. FOOMKA TARTANKA
    with st.expander("📝 Is-diiwaangeli Tartanka"):
        with st.form("tartanka_form"):
            magaca = st.text_input("Magacaaga oo Buuxa")
            telefoonka = st.text_input("Telefoonkaaga")
            gobolka = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
            xafada = st.text_input("Xafadda")
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
                        st.success("Xogtaada tartanka waa la qabtay!")
                    except:
                        st.error("Lambarkan hore ayaa loo isticmaalay.")
                else:
                    st.warning("Fadlan buuxi meelaha bannaan.")

    # B. QAYBTA RAYIGA (Laba bog u kala jabidda halkan ayay ka bilaabataa)
    st.write("---")
    st.subheader("💬 Dhiibo Rayigaaga (Hambalyada 18 May)")
    
    with st.form("comment_form"):
        c_magaca = st.text_input("Magacaaga")
        c_faallo = st.text_area("Maxaad u rajaynaysaa Somaliland?")
        c_submit = st.form_submit_button("Soo Gudbi Rayiga")
        
        if c_submit:
            if c_magaca and c_faallo:
                conn = sqlite3.connect('somaliland_18may.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO rayiga (magaca, faallada) VALUES (?,?)', (c_magaca, c_faallo))
                conn.commit()
                conn.close()
                
                # Halkan ayaan kaga gudbaynaa Bogga kale
                st.session_state.page = 'success'
                st.rerun()
            else:
                st.warning("Fadlan buuxi magaca iyo rayiga.")

    # C. SOO BANDHIGISTA RAYIGA (Comments Feed)
    st.write("### Hambalyada Dadweynaha:")
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('SELECT magaca, faallada FROM rayiga ORDER BY id DESC LIMIT 5')
    all_comments = cursor.fetchall()
    conn.close()

    for comm in all_comments:
        st.markdown(f"**👤 {comm[0]}:** {comm[1]}")

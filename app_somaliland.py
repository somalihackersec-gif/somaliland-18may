import streamlit as st
import sqlite3
import re

# 1. DATABASE SETUP (Tartanka & Rayiga)
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    # Jadwalka Tartanka
    cursor.execute('''CREATE TABLE IF NOT EXISTS tartamayaasha 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, telefoonka TEXT UNIQUE, gobolka TEXT, xafada TEXT)''')
    # Jadwalka Rayiga (Comments)
    cursor.execute('''CREATE TABLE IF NOT EXISTS rayiga 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, faallada TEXT)''')
    conn.commit()
    conn.close()

bilow_database()

# 2. CALANKA SOMALILAND (URL)
calanka_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10&ec=121691707"

# 3. SETTINGS & CSS (Qarinta Badhamada & Bilicda)
st.set_page_config(page_title="happy 18 May ", page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk24G0SMgJLAP6BzsykgsuLEwMd1IHSXcf6wp2Z3AJhb6xG-bRJ1pWq2-UCP_ER7si8W8RcC_DoB3KNr7x8mR1b69B3zaEOCdnhGsP-Ki0uSwi97Bp&s=10&ec=121691707", layout="centered")

st.markdown("""
    <style>
    /* Qarinta Toolbar-ka (Xalka image_848480.png) */
    [data-testid="stStatusWidget"], .stAppDeployButton, #MainMenu, header, footer {
        visibility: hidden;
        display: none !important;
    }

    /* Background-ka Madow */
    .stApp { background-color: #0d1117 !important; color: white !important; }
    
    /* Qurxinta Form-ka */
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
        border-radius: 10px;
    }
    
    /* Calanka Tool-ka */
    .flag-banner { text-align: center; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- BOGGA ADMIN-KA (Sirta ah) ---
if st.query_params.get("key") == "9a2b8c4e7f":
    st.title("🔐 Dashboard-ka Maamulka")
    # Halkan waxaad dhex gelin kartaa koodhkii Admin-ka ee hore hadaad u baahato.
else:
    # --- BOGGA USER-KA ---
    
    # A. Calanka Sare
    st.image(calanka_url, use_column_width=True)
    
    # B. Video-ga Sare
    st.video("https://youtu.be/Q0aWxMLdHFo")
    
    # C. Calamada Dhexe (Ku celcelis)
    col1, col2, col3 = st.columns(3)
    with col1: st.image(calanka_url, width=100)
    with col2: st.image(calanka_url, width=100)
    with col3: st.image(calanka_url, width=100)

    st.title("Somaliland 18 May ")
    st.subheader("Is-diiwaangeli si aad uga qayb gasho dabaal-dega")

    # D. FOOMKA TARTANKA
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
                    st.success("Waad ku mahadsantahay is-diiwaangelinta!")
                    st.balloons()
                except:
                    st.error("Lambarkan hore ayaa loo isticmaalay.")
            else:
                st.warning("Fadlan buuxi meelaha bannaan.")

    # E. Calan kale oo dhexe
    st.image(calanka_url, use_column_width=True)

    # F. QAYBTA RAYIGA (Comments - Amaan ah)
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
                # Isticmaalka ? waa midka amniga suga (SQL Injection protection)
                cursor.execute('INSERT INTO rayiga (magaca, faallada) VALUES (?,?)', (c_magaca, c_faallo))
                conn.commit()
                conn.close()
                st.info("Rayigaaga si guul leh ayaa loo qabtay!")
            else:
                st.warning("Fadlan buuxi magaca iyo rayiga.")

    # G. SOO BANDHIGISTA RAYIGA (Comments Feed)
    st.write("### Hambalyada Dadweynaha:")
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('SELECT magaca, faallada FROM rayiga ORDER BY id DESC LIMIT 5')
    all_comments = cursor.fetchall()
    conn.close()
    
    for comm in all_comments:
        st.markdown(f"**👤 {comm[0]}:** {comm[1]}")

    # H. Calanka Hoose
    st.image(calanka_url, width=150)
    st.write("Guul iyo Gobanimo - 2026")

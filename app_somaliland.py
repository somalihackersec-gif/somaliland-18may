import streamlit as st
import sqlite3

# 1. Diyaarinta Database-ka
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tartamayaasha (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            magaca TEXT NOT NULL,
            telefoonka TEXT UNIQUE NOT NULL,
            gobolka TEXT NOT NULL,
            xafada TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

bilow_database()

st.set_page_config(page_title="18 May Dabaal-deg", page_icon="https://upload.wikimedia.org/wikipedia/commons/4/4d/Flag_of_Somaliland.svg", layout="centered")

# Sawirka Calanka Somaliland (Link toos ah si uusan khalad u bixin)
calanka_url = "https://upload.wikimedia.org/wikipedia/commons/4/4d/Flag_of_Somaliland.svg"

st.image(calanka_url, width=200)
st.markdown("<h1 style='text-align: center; color: #10B981;'>🎊 Nala Dabaal-deg 18 May 🎊</h1>", unsafe_allow_html=True)
st.video("https://youtu.be/Q0aWxMLdHFo") 

if 'page' not in st.session_state:
    st.session_state.page = 'registration'

if st.session_state.page == 'registration':
    st.write("---")
    with st.form(key='registration_form'):
        magaca = st.text_input("Magacaaga oo Buuxa")
        telefoonka = st.text_input("Lambarka Telefoonka")
        gobolka = st.selectbox("Gobolka", ["Maroodijeex", "Togdheer", "Awdal", "Saaxil", "Sanaag", "Sool"])
        xafada = st.text_input("Xafadda")
        submit_button = st.form_submit_button(label="Is Diiwaangeli Hadda")

    if submit_button:
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
            st.warning("Fadlan buuxi dhammaan xogta.")

elif st.session_state.page == 'success':
    st.balloons()
    st.image(calanka_url, use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: #059669;'>🎉 WAAD GUULEYSATAY! 🎉</h2>", unsafe_allow_html=True)
    st.success("Xogtaada si guul leh ayaa loo kaydiyey.")
    if st.button("Ku laabo Bogga Hore"):
        st.session_state.page = 'registration'
        st.rerun()

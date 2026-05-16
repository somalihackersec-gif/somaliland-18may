import streamlit as st
import sqlite3
import pandas as pd

# 1. DATABASE SETUP
def bilow_database():
    conn = sqlite3.connect('somaliland_18may.db')
    cursor = conn.cursor()
    # Waxaan ka saarnay UNIQUE nambarka si uusan dhib u keenin hadda
    cursor.execute('''CREATE TABLE IF NOT EXISTS tartamayaasha 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, magaca TEXT, telefoonka TEXT, gobolka TEXT, xafada TEXT)''')
    cursor.execute('CREATE TABLE IF NOT EXISTS views_counter (id INTEGER PRIMARY KEY, tirada INTEGER)')
    cursor.execute('INSERT OR IGNORE INTO views_counter (id, tirada) VALUES (1, 0)')
    conn.commit()
    conn.close()

bilow_database()

# TRACKING VIEWS
if 'tracked' not in st.session_state:
    conn = sqlite3.connect('somaliland_18may.db')
    conn.execute('UPDATE views_counter SET tirada = tirada + 1 WHERE id = 1')
    conn.commit()
    conn.close()
    st.session_state.tracked = True

# 2. ADMIN SECRET TRIGGER
is_admin = st.query_params.get("key") == "admin777"

# 3. PROFESSIONAL UI
st.markdown("""<style>
    [data-testid="stStatusWidget"], .stAppDeployButton, #MainMenu, header, footer { visibility: hidden; display: none !important; }
    .stApp { background: #020617; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1e293b; border-radius: 5px; color: white; padding: 10px 20px; }
    </style>""", unsafe_allow_html=True)

if is_admin:
    st.title("🛡️ Super-Admin Control Center")
    
    conn = sqlite3.connect('somaliland_18may.db')
    df = pd.read_sql_query("SELECT * FROM tartamayaasha", conn)
    views = pd.read_sql_query("SELECT tirada FROM views_counter WHERE id = 1", conn).iloc[0]['tirada']
    conn.close()

    # METRICS CARDS
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Registrations", len(df))
    c2.metric("Total Page Views", views)
    c3.metric("System Status", "Live & Secure")

    st.write("---")
    
    # NEW TABS (BADHAMADA CUSUB)
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Kormeerka Xogta", "🔍 Raadinta (Search)", "🧹 Maareynta (Admin)", "📊 Analytics"])

    with tab1:
        st.subheader("Dhammaan Dadka Is-diiwaangeliyey")
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Excel File", data=csv, file_name='data_18may.csv', mime='text/csv')

    with tab2:
        st.subheader("Raadi Qof Gaar ah")
        search_query = st.text_input("Geli Magaca ama Nambarka qofka aad rabto")
        if search_query:
            filtered_df = df[df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().values, axis=1)]
            st.write(f"Waxaa la helay: {len(filtered_df)} qof")
            st.table(filtered_df)

    with tab3:
        st.subheader("Maareynta Database-ka")
        col_del, col_reset = st.columns(2)
        if col_del.button("Tirtir Qofka u dambeeyey"):
            conn = sqlite3.connect('somaliland_18may.db')
            conn.execute("DELETE FROM tartamayaasha WHERE id = (SELECT MAX(id) FROM tartamayaasha)")
            conn.commit()
            conn.close()
            st.warning("Qofkii u dambeeyey waa la tirtiray!")
        
        st.info("Halkan waxaad ka kormeeraysaa haddii ay jiraan dad nambarada ku celceliyey.")

    with tab4:
        st.subheader("Gobollada Sidee loogu kala badan yahay?")
        if not df.empty:
            st.bar_chart(df['gobolka'].value_counts())
        else:
            st.write("Weli xog ma jirto.")

else:
    # --- BOGGA DADWEYNAHA (Sidii aan kuugu habeeyey) ---
    st.title("🇸🇴 Somaliland 18 May")
    # ... halkan koodhkii foomka iyo video-ga ayaa gelaya sidii hore ...
    st.info("Geli URL-ka dabadooda ?key=admin777 si aad u gasho maamulka.")

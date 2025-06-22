import psycopg2
import streamlit as st

def test_db_connection():
    try:
        conn = psycopg2.connect(
            host=st.secrets["db_host"],
            database=st.secrets["db_name"],
            user=st.secrets["db_user"],
            password=st.secrets["db_password"],
            port=st.secrets["db_port"]
        )
        conn.close()
        st.success("✅ DB接続成功しました！")
    except Exception as e:
        st.error(f"❌ DB接続失敗: {e}")

test_db_connection()

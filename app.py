import streamlit as st
import psycopg2
from datetime import datetime

st.set_page_config(page_title="アクセスカウンター", layout="centered")
st.title("📊 アクセスカウンター")

# DB接続関数
def connect_to_db_old():
    try:
        conn = psycopg2.connect(
            host=st.secrets["db_host"],
            dbname=st.secrets["db_name"],
            user=st.secrets["db_user"],
            password=st.secrets["db_password"],
            port=st.secrets["db_port"],
            sslmode="require"
        )
        return conn
    except Exception as e:
        st.error(f"❌ DB接続失敗: {e}")
        return None

def connect_to_db():
    # Render 上では st.secrets ではなく os.environ から読む
    host = os.environ.get("db_host")
    dbname = os.environ.get("db_name")
    user = os.environ.get("db_user")
    password = os.environ.get("db_password")
    port = os.environ.get("db_port", "5432")
    try:
        conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port,
            sslmode="require"
        )
        return conn
    except Exception as e:
        st.error(f"❌ DB接続失敗: {e}")
        return None

# テーブル作成（存在しなければ）
def create_table_if_not_exists(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS access_log (
                    id SERIAL PRIMARY KEY,
                    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
    except Exception as e:
        st.error(f"❌ テーブル作成エラー: {e}")

# アクセス記録
def log_access(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO access_log DEFAULT VALUES;")
            conn.commit()
    except Exception as e:
        st.error(f"❌ ログ記録エラー: {e}")

# 総アクセス数を取得
def get_access_count(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM access_log;")
            count = cur.fetchone()[0]
            return count
    except Exception as e:
        st.error(f"❌ カウント取得エラー: {e}")
        return 0

# 実行処理
conn = connect_to_db()

if conn:
    create_table_if_not_exists(conn)  # ← ここで自動作成！
    log_access(conn)
    count = get_access_count(conn)
    st.metric("📈 総アクセス数", f"{count} 回")
    conn.close()

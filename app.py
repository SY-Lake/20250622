import streamlit as st
import psycopg2
from datetime import datetime
import os

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
    host = "dpg-d1bm5j95pdvs73e19cgg-a.oregon-postgres.render.com"
    dbname = "page_access_db_eak4"
    user = "user123"
    password = "2KB1FZK3uwWrtmaeYgxiOvGqg79PODIX"
    port = "5432"
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

# テーブル作成（初回のみ）
def create_table_if_not_exists(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS access_log (
                id SERIAL PRIMARY KEY,
                accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

# アクセスログ記録
def log_access(conn):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO access_log DEFAULT VALUES;")
        conn.commit()

# 1時間単位でアクセスを集計
def get_hourly_counts(conn):
    query = """
        SELECT
            date_trunc('hour', accessed_at) AS hour,
            COUNT(*) AS access_count
        FROM access_log
        GROUP BY hour
        ORDER BY hour DESC
        LIMIT 24;  -- 最新24時間分だけ
    """
    df = pd.read_sql(query, conn)
    return df.sort_values("hour")  # 昇順で表示

# 実行ブロック
conn = connect_to_db()
if conn:
    create_table_if_not_exists(conn)
    log_access(conn)
    df = get_hourly_counts(conn)
    conn.close()

    # 表示
    st.subheader("🕒 時間帯別アクセス数（最新24時間）")
    st.dataframe(df, use_container_width=True)

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("hour:T", title="時間（hour）"),
        y=alt.Y("access_count:Q", title="アクセス数"),
        tooltip=["hour:T", "access_count"]
    ).properties(height=400)

    st.altair_chart(chart, use_container_width=True)

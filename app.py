import streamlit as st
import sqlite3

# DB接続とテーブル作成（初回のみ）
def init_db():
    conn = sqlite3.connect('counter.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS access_count (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            count INTEGER
        )
    ''')
    # 初回レコードがない場合は追加
    c.execute('SELECT COUNT(*) FROM access_count')
    if c.fetchone()[0] == 0:
        c.execute('INSERT INTO access_count (count) VALUES (0)')
    conn.commit()
    conn.close()

# カウントを1つ増やす
def increment_count():
    conn = sqlite3.connect('counter.db')
    c = conn.cursor()
    c.execute('UPDATE access_count SET count = count + 1 WHERE id = 1')
    conn.commit()
    conn.close()

# カウントを取得する
def get_count():
    conn = sqlite3.connect('counter.db')
    c = conn.cursor()
    c.execute('SELECT count FROM access_count WHERE id = 1')
    result = c.fetchone()[0]
    conn.close()
    return result

# メイン処理
init_db()
increment_count()
count = get_count()

st.title("アクセスカウンター")
st.write(f"このページは **{count} 回** アクセスされました！")

import streamlit as st

st.title("プルダウン選択サンプル")

fruits = ["りんご", "バナナ", "みかん"]
choice = st.selectbox("好きな果物は？", fruits)

st.write(f"あなたが選んだのは **{choice}** です！")

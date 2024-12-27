import streamlit as st
import pandas as pd
import numpy as np

# タイトル
st.title("Agriboard: 野菜価格予測アプリ")


# サイドバー
st.sidebar.header("設定")
vegetable = st.sidebar.selectbox(
    "予測したい野菜を選んでください",
    ("トマト", "キャベツ", "ニンジン", "キュウリ")
)
days = st.sidebar.slider("予測する日数 (未来の日数)", 1, 30, 7)


# メイン画面
st.header(f"{vegetable} の価格予測")
st.write(f"{days} 日後までの価格予測結果を以下に表示します。")

# ダミーデータ生成
np.random.seed(42)  # 再現性のため
dates = pd.date_range(start="2023-01-01", periods=days)
prices = np.round(np.random.uniform(100, 300, size=days), 2)
data = pd.DataFrame({"日付": dates, "価格 (円)": prices})

# データの表示
st.line_chart(data.set_index("日付"))
st.table(data)

# メッセージ
st.success(f"{vegetable} の価格予測が完了しました！")

# app.py

import streamlit as st
from PIL import Image

# --- ページ設定 (変更なし) ---
st.set_page_config(
    page_title="画像加工ツールボックス",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSSでメインコンテンツの幅を調整 ---
# max-widthを少し広げて4カラムでも見やすくします
st.markdown(
    """
    <style>
        .main .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- メインページコンテンツ ---
st.title("🖼️ 画像加工ツールボックス")
st.markdown("---")
st.markdown(
    """
    このアプリは、AIイラストの質感調整、画像の背景除去、ピクセルアート化など、
    さまざまな画像加工機能を提供するツールボックスです。

    **👈 サイドバーから使用したいツールを選択してください。**

    ---

    ### 🛠️ 各ツールの紹介 (サンプル画像での実行例)
    """
)

# --- 機能紹介を4カラムで表示 ---
col1, col2, col3, col4 = st.columns(4)

# --- 1. オリジナル画像のカード ---
with col1:
    with st.container(border=True):
        st.markdown(
            "<h4 style='text-align:center;'>🖼️ オリジナル画像</h4>",
            unsafe_allow_html=True,
        )
        try:
            image = Image.open("assets/sample.png")
            st.image(image, caption="この画像を元に加工しています。")
        except FileNotFoundError:
            st.warning("サンプル画像(assets/sample.png)が見つかりません。")

        # 説明は少しシンプルに
        st.markdown(
            """
            - 比較用元画像
            - 画質が悪い方が効果的
            - 可愛いが正義！
            """
        )

# --- 2. ピクセルアートのカード ---
with col2:
    with st.container(border=True):
        st.markdown(
            "<h4 style='text-align:center;'>🕹️ ピクセルアート</h4>",
            unsafe_allow_html=True,
        )
        try:
            image = Image.open("assets/pixelart_sample.png")
            st.image(image, caption="レトロなドット絵に変換。")
        except FileNotFoundError:
            st.warning("サンプル画像(assets/pixelart_sample.png)が見つかりません。")

        st.markdown(
            """
            - ピクセルサイズ調整
            - 多彩なカラースタイル
            - オリジナルとの比較
            """
        )

# --- 3. 背景リムーバーのカード ---
with col3:
    with st.container(border=True):
        st.markdown(
            "<h4 style='text-align:center;'>🪄 背景リムーバー</h4>",
            unsafe_allow_html=True,
        )
        try:
            image = Image.open("assets/removed_bg_sample.png")
            st.image(image, caption="背景をきれいに除去。")
        except FileNotFoundError:
            st.warning("サンプル画像(assets/removed_bg_sample.png)が見つかりません。")

        st.markdown(
            """
            - 高精度な自動切り抜き
            - PNG形式でダウンロード
            - `rembg`ライブラリ活用
            """
        )

# --- 4. AIイラスト補正のカード ---
with col4:
    with st.container(border=True):
        st.markdown(
            "<h4 style='text-align:center;'>🎨 AIイラスト補正</h4>",
            unsafe_allow_html=True,
        )
        try:
            image = Image.open("assets/fixed_sample.png")
            st.image(image, caption="自然な風合いに調整。")
        except FileNotFoundError:
            st.warning("サンプル画像(assets/fixed_sample.png)が見つかりません。")

        st.markdown(
            """
            - ノイズ・色収差効果
            - 明るさ・彩度調整
            - K-Meansによる減色
            """
        )

st.markdown("---")
st.info(
    "このアプリは複数の画像処理機能を一つに統合したものです。個人利用の範囲でお楽しみください。"
)

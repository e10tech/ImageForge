# pages/2_🪄_背景リムーバー.py
import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import os

# --- CSSでメインコンテンツの幅を調整 ---
st.markdown(
    """
    <style>
        .main .block-container {
            max-width: 1000px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🪄 背景リムーバー")
st.markdown("アップロードした画像の背景を自動で除去します。")
st.info("👈 サイドバーから画像をアップロードするか、サンプル画像でお試しください。")

# --- 定数 ---
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
SAMPLE_IMAGE_PATH = "assets/sample.png"


# --- 関数 ---
@st.cache_data
def convert_image_to_bytes(img):
    """PIL Imageをバイトに変換"""
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@st.cache_data
def process_image_rembg(image_bytes):
    """rembgで背景を除去"""
    try:
        original_image = Image.open(BytesIO(image_bytes)).convert("RGB")
        processed_image = remove(original_image)
        return original_image, processed_image
    except Exception as e:
        st.error(f"画像処理中にエラーが発生しました: {e}")
        return None, None


# --- サイドバー ---
with st.sidebar:
    st.header("⚙️ 操作パネル")
    st.markdown("---")
    uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])
    st.markdown("または")
    use_sample = st.button("サンプル画像を使用", use_container_width=True)
    st.markdown("---")

    with st.expander("ℹ️ 画像ガイドライン"):
        st.write(
            """
        - **最大ファイルサイズ:** 10MB
        - **対応フォーマット:** PNG, JPG, JPEG
        - 処理時間は画像のサイズに依存します。
        """
        )

# --- メイン処理 ---
image_to_process = None
image_bytes_to_process = None
filename = "source_image"

if uploaded_file:
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error(
            f"ファイルサイズが大きすぎます。{MAX_FILE_SIZE/1024/1024:.1f}MB以下の画像をアップロードしてください。"
        )
    else:
        image_bytes_to_process = uploaded_file.getvalue()
        filename, _ = os.path.splitext(uploaded_file.name)

elif use_sample:
    if os.path.exists(SAMPLE_IMAGE_PATH):
        with open(SAMPLE_IMAGE_PATH, "rb") as f:
            image_bytes_to_process = f.read()
        filename = "sample"
    else:
        st.warning("サンプル画像が見つかりません。画像をアップロードしてください。")

if image_bytes_to_process:
    with st.spinner("背景を除去しています..."):
        original_pil, processed_pil = process_image_rembg(image_bytes_to_process)

    if original_pil and processed_pil:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🖼️ オリジナル画像")
            st.image(original_pil, use_container_width=True)
        with col2:
            st.subheader("✨ 背景除去後の画像")
            st.image(processed_pil, use_container_width=True)

        # ダウンロードボタンをメインエリアの下部に配置
        st.markdown("---")
        st.download_button(
            label="💾 背景除去画像をダウンロード",
            data=convert_image_to_bytes(processed_pil),
            file_name=f"removed_bg_{filename}.png",
            mime="image/png",
            use_container_width=True,
        )
    else:
        st.error("画像の処理に失敗しました。別の画像でお試しください。")
else:
    st.info("画像をアップロードするか、サンプル画像を使用してください。")

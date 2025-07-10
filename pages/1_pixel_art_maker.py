# pages/3_🕹️_ピクセルアートメーカー.py
import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance
import io
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

st.title("🕹️ ピクセルアートメーカー")
st.markdown("お気に入りの画像をレトロなドット絵に変換します。")
st.info("👈 サイドバーから画像をアップロードし、スタイルを選択してください。")


# --- 画像処理関数 ---
@st.cache_data
def create_pixel_art(image, pixel_size=10):
    original_width, original_height = image.size
    new_width = max(1, original_width // pixel_size)
    new_height = max(1, original_height // pixel_size)
    small_image = image.resize((new_width, new_height), Image.NEAREST)
    return small_image.resize((original_width, original_height), Image.NEAREST)


@st.cache_data
def quantize_to_16bit(image: Image.Image) -> Image.Image:
    arr = np.array(image.convert("RGB"))
    arr[..., 0] = (arr[..., 0] >> 3) << 3  # R
    arr[..., 1] = (arr[..., 1] >> 2) << 2  # G
    arr[..., 2] = (arr[..., 2] >> 3) << 3  # B
    return Image.fromarray(arr, "RGB")


@st.cache_data
def to_grayscale(image: Image.Image) -> Image.Image:
    return image.convert("L").convert("RGB")


@st.cache_data
def to_colorful(image: Image.Image, factor=2.0) -> Image.Image:
    enhancer = ImageEnhance.Color(image.convert("RGB"))
    return enhancer.enhance(factor)


def apply_palette_style(image: Image.Image, style: str) -> Image.Image:
    if style == "16ビット風":
        return quantize_to_16bit(image)
    elif style == "モノクロ":
        return to_grayscale(image)
    elif style == "カラフル":
        return to_colorful(image)
    else:  # "オリジナル"
        return image.convert("RGB")


# --- サイドバー ---
with st.sidebar:
    st.header("⚙️ 操作パネル")
    st.markdown("---")
    uploaded_file = st.file_uploader(
        "画像をアップロード", type=["png", "jpg", "jpeg", "gif", "bmp"]
    )
    st.markdown("---")

    st.header("🎨 スタイル設定")
    style = st.selectbox(
        "カラースタイル",
        ["オリジナル", "16ビット風", "モノクロ", "カラフル"],
        help="ピクセルアートの雰囲気を変えられます。",
    )
    pixel_size = st.slider(
        "ピクセルサイズ",
        min_value=2,
        max_value=50,
        value=10,
        step=1,
        help="大きいほどドットが粗くなります。",
    )
    st.markdown("---")

# --- メインエリア ---
if uploaded_file is not None:
    try:
        original_image = Image.open(uploaded_file).convert("RGB")
    except Exception as e:
        st.error(f"画像の読み込みに失敗しました: {e}")
        st.stop()

    with st.spinner("ピクセルアートを作成中..."):
        pixelated_image = create_pixel_art(original_image, pixel_size)
        styled_art = apply_palette_style(pixelated_image, style)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "<h4 style='text-align:center;'>🖼️ オリジナル</h4>", unsafe_allow_html=True
        )
        st.image(original_image, use_container_width=True)
    with col2:
        st.markdown(
            f"<h4 style='text-align:center;'>✨ ピクセルアート</h4>",
            unsafe_allow_html=True,
        )
        st.image(styled_art, use_container_width=True)

    st.markdown("---")

    # ダウンロードボタン
    buf = io.BytesIO()
    styled_art.save(buf, format="PNG")
    filename, _ = os.path.splitext(uploaded_file.name)
    st.download_button(
        label=f"💾 ピクセルアートをダウンロード",
        data=buf.getvalue(),
        file_name=f"pixelart_{style}_{pixel_size}_{filename}.png",
        mime="image/png",
        use_container_width=True,
    )

    with st.expander("📝 画像情報"):
        st.write(
            f"**元のサイズ**: {original_image.size[0]} × {original_image.size[1]} pixels"
        )
        st.write(f"**ピクセルサイズ**: {pixel_size}")
        st.write(
            f"**ダウンサンプルサイズ**: {max(1, original_image.size[0] // pixel_size)} × {max(1, original_image.size[1] // pixel_size)} pixels"
        )
else:
    st.info(
        "サイドバーから画像をアップロードして、ピクセルアート作成を開始してください。"
    )

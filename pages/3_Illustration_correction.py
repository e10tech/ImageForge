# pages/1_🎨_AIイラスト補正ツール.py
import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image, ImageEnhance, ImageOps
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


# --- 画像処理関数 (変更なし) ---
def add_noise(img_pil, strength=0.05):
    img_np = np.array(img_pil).astype(np.float32) / 255.0
    noise = (np.random.rand(*img_np.shape) - 0.5) * (strength * 2)
    noisy_img = np.clip(img_np + noise, 0, 1)
    return Image.fromarray((noisy_img * 255).astype(np.uint8))


def add_chromatic_aberration(img_pil, strength=1):
    if strength <= 0:
        return img_pil
    img_np = np.array(img_pil)
    h, w, _ = img_np.shape
    offset = max(1, int(strength * min(h, w) * 0.002))
    r, g, b = img_pil.split()
    try:
        from PIL import ImageChops

        r_shifted = ImageChops.offset(r, -offset, 0)
        b_shifted = ImageChops.offset(b, offset, 0)
        g_shifted = g
    except ImportError:
        r_shifted = Image.new("L", (w, h))
        g_shifted = Image.new("L", (w, h))
        b_shifted = Image.new("L", (w, h))
        r_shifted.paste(r, (-offset, 0))
        g_shifted.paste(g, (0, 0))
        b_shifted.paste(b, (offset, 0))
        if offset > 0:
            r_edge = r.crop((w - offset, 0, w, h))
            b_edge = b.crop((0, 0, offset, h))
            r_shifted.paste(r_edge, (0, 0))
            b_shifted.paste(b_edge, (w - offset, 0))
    merged = Image.merge("RGB", (r_shifted, g_shifted, b_shifted))
    final_img = Image.blend(img_pil, merged, alpha=0.3)
    return final_img


@st.cache_data(show_spinner=False)
def apply_kmeans(img_bgr, k=24):
    img_filtered = cv2.bilateralFilter(img_bgr, d=3, sigmaColor=15, sigmaSpace=15)
    h, w, _ = img_filtered.shape
    pixels = cv2.cvtColor(img_filtered, cv2.COLOR_BGR2RGB).reshape(-1, 3)
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=5, max_iter=200).fit(pixels)
    centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    new_img = centers[labels].reshape(h, w, 3).astype("uint8")
    return cv2.cvtColor(new_img, cv2.COLOR_RGB2BGR)


def add_vignette(img_pil, strength=0.3):
    img_np = np.array(img_pil)
    h, w = img_np.shape[:2]
    Y, X = np.ogrid[:h, :w]
    center_y, center_x = h / 2, w / 2
    distance = np.sqrt((X - center_x) ** 2 + (Y - center_y) ** 2)
    max_dist = np.sqrt((w / 2) ** 2 + (h / 2) ** 2)
    vignette = 1.0 - strength * (distance / max_dist) ** 2
    vignette = np.clip(vignette, 0.0, 1.0)
    vignette_mask = np.dstack([vignette] * 3)
    img_vignette = (img_np * vignette_mask).astype(np.uint8)
    return Image.fromarray(img_vignette)


def process_image(img_pil, params):
    processed_img = img_pil.copy()
    if params["noise_strength"] > 0:
        processed_img = add_noise(processed_img, params["noise_strength"])
    if params["brightness"] != 1.0:
        processed_img = ImageEnhance.Brightness(processed_img).enhance(
            params["brightness"]
        )
    if params["contrast"] != 1.0:
        processed_img = ImageEnhance.Contrast(processed_img).enhance(params["contrast"])
    if params["saturation"] != 1.0:
        processed_img = ImageEnhance.Color(processed_img).enhance(params["saturation"])
    img_bgr = cv2.cvtColor(np.array(processed_img), cv2.COLOR_RGB2BGR)
    if params["use_kmeans"]:
        img_bgr = apply_kmeans(img_bgr, params["k_value"])
    sharpness_val = params["sharpness"]
    if sharpness_val > 0:
        original_bgr = img_bgr.copy()
        sigma_blur = max(0.5, 1.5 - sharpness_val * 0.1)
        blurred = cv2.GaussianBlur(img_bgr, (0, 0), sigma_blur)
        sharpness_factor = 1.0 + sharpness_val * 0.3
        img_bgr = cv2.addWeighted(
            original_bgr, sharpness_factor, blurred, 1 - sharpness_factor, 0
        )
        img_bgr = np.clip(img_bgr, 0, 255).astype(np.uint8)
    elif sharpness_val < 0:
        sigma_val = abs(sharpness_val) * 0.8 + 0.5
        if sigma_val > 0.3:
            img_bgr = cv2.GaussianBlur(img_bgr, (0, 0), sigmaX=sigma_val)
    processed_img = Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
    if params["chromatic_aberration"] > 0:
        processed_img = add_chromatic_aberration(
            processed_img, params["chromatic_aberration"]
        )
    if params["vignette_strength"] > 0:
        processed_img = add_vignette(processed_img, params["vignette_strength"])
    return processed_img


# --- Streamlit UI ---
st.title("🎨 AIイラスト補正ツール")
st.markdown("AIイラスト特有の質感を和らげ、より自然な見た目に調整します。")
st.info("👈 サイドバーから画像をアップロードし、パラメータを調整してください。")

# --- Session Stateの初期化 ---
if "corrector_image_processed" not in st.session_state:
    st.session_state.corrector_image_processed = False
if "corrector_download_buffer" not in st.session_state:
    st.session_state.corrector_download_buffer = None
if "corrector_last_processed_image_pil" not in st.session_state:
    st.session_state.corrector_last_processed_image_pil = None
if "corrector_processing_error" not in st.session_state:
    st.session_state.corrector_processing_error = None
if "corrector_original_image_pil" not in st.session_state:
    st.session_state.corrector_original_image_pil = None
if "corrector_uploaded_filename" not in st.session_state:
    st.session_state.corrector_uploaded_filename = None

# --- サイドバー ---
with st.sidebar:
    st.header("📂 画像の選択")
    uploaded = st.file_uploader(
        "画像をアップロード",
        type=["png", "jpg", "jpeg"],
        help="補正したいAIイラストの画像ファイルを選択してください。",
        key="corrector_file_uploader",
    )

    # 画像アップロード/クリア処理
    current_uploaded_filename = uploaded.name if uploaded else None
    previous_uploaded_filename = st.session_state.get(
        "corrector_uploaded_filename", None
    )
    if current_uploaded_filename != previous_uploaded_filename:
        if uploaded is not None:
            try:
                st.session_state.corrector_image_processed = False
                st.session_state.corrector_download_buffer = None
                st.session_state.corrector_last_processed_image_pil = None
                st.session_state.corrector_processing_error = None
                st.session_state.corrector_original_image_pil = Image.open(
                    uploaded
                ).convert("RGB")
                st.session_state.corrector_uploaded_filename = uploaded.name
            except Exception as e:
                st.error(f"画像読み込みエラー: {e}")
                st.session_state.corrector_original_image_pil = None
                st.session_state.corrector_uploaded_filename = None
        else:  # ファイルがクリアされた場合
            st.session_state.corrector_original_image_pil = None
            st.session_state.corrector_uploaded_filename = None
            st.session_state.corrector_image_processed = False
            st.session_state.corrector_download_buffer = None
            st.session_state.corrector_last_processed_image_pil = None
            st.session_state.corrector_processing_error = None

    st.header("🛠️ 調整パラメータ")
    params = {}
    params["noise_strength"] = st.slider(
        "ノイズ強度", 0.0, 0.2, 0.03, 0.01, help="アナログ感を加える"
    )
    params["brightness"] = st.slider("明るさ", 0.5, 1.5, 1.0, 0.05)
    params["contrast"] = st.slider("コントラスト", 0.5, 1.5, 0.98, 0.01)
    params["saturation"] = st.slider("彩度", 0.0, 2.0, 0.95, 0.05)
    params["sharpness"] = st.slider(
        "シャープネス", -5.0, 5.0, 0.4, 0.1, help="(-:ぼかし, +:強調)"
    )
    params["chromatic_aberration"] = st.slider(
        "色収差", 0.0, 5.0, 0.4, 0.1, help="レンズ風の色ずれ効果"
    )
    params["vignette_strength"] = st.slider(
        "ビネット効果", 0.0, 0.8, 0.15, 0.05, help="周辺減光効果"
    )
    st.markdown("---")
    params["use_kmeans"] = st.checkbox(
        "K-Means減色", value=False, help="色数を減らしフラット化"
    )
    params["k_value"] = st.slider(
        "K-Means色数 (k)", 8, 48, 24, 1, disabled=not params["use_kmeans"]
    )
    st.markdown("---")

    process_button_pressed = st.button(
        "🔄 補正実行",
        key="process_button",
        use_container_width=True,
        disabled=st.session_state.corrector_original_image_pil is None,
    )

# --- メインエリア ---
if st.session_state.corrector_original_image_pil is not None:
    # ボタン押下時の処理ロジック
    if process_button_pressed:
        st.session_state.corrector_processing_error = None
        with st.spinner("ナチュラル処理中…🪄"):
            try:
                fixed_pil = process_image(
                    st.session_state.corrector_original_image_pil.copy(), params
                )
                buffer = io.BytesIO()
                fixed_pil.save(buffer, format="PNG")
                buffer.seek(0)
                st.session_state.corrector_download_buffer = buffer.getvalue()
                st.session_state.corrector_last_processed_image_pil = fixed_pil
                st.session_state.corrector_image_processed = True
            except Exception as e:
                st.session_state.corrector_processing_error = (
                    f"画像処理中にエラーが発生しました: {e}"
                )
                st.session_state.corrector_image_processed = False
                st.session_state.corrector_download_buffer = None
                st.session_state.corrector_last_processed_image_pil = None
        # rerunを使わずに直接表示を更新する

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🖼️ オリジナル画像")
        st.image(
            st.session_state.corrector_original_image_pil, use_container_width=True
        )
    with col2:
        st.subheader("✨ 補正後の画像")
        if st.session_state.corrector_processing_error:
            st.error(st.session_state.corrector_processing_error)
        elif (
            st.session_state.corrector_image_processed
            and st.session_state.corrector_last_processed_image_pil
        ):
            st.image(
                st.session_state.corrector_last_processed_image_pil,
                caption="🌟 補正結果",
                use_container_width=True,
            )
        else:
            st.info("パラメータを調整し、「補正実行」ボタンを押してください。")
else:
    st.info("サイドバーから補正したい画像をアップロードしてください。")

# --- ダウンロードボタンをヒントの下に移動 ---
buffer_data = st.session_state.get("corrector_download_buffer")
download_data = buffer_data if buffer_data is not None else b""
can_download = (
    st.session_state.corrector_image_processed
    and st.session_state.corrector_download_buffer is not None
)
download_filename = "fixed_image.png"
uploaded_filename_state = st.session_state.get("corrector_uploaded_filename")
if uploaded_filename_state:
    base_name, _ = os.path.splitext(uploaded_filename_state)
    download_filename = f"fixed_{base_name}.png"
st.download_button(
    label="💾 画像をダウンロード",
    data=download_data,
    file_name=download_filename,
    mime="image/png",
    key="download_button",
    disabled=not can_download,
    use_container_width=True,
    help=(
        "補正後の画像をPNG形式でダウンロードします。"
        if can_download
        else "補正を実行するとダウンロード可能になります。"
    ),
)


with st.expander("💡 調整のヒントを見る"):
    st.markdown(
        """
    - **ノイズ強度:** アナログ感を加え、均一さを崩します。
    - **明るさ/コントラスト/彩度:** 全体の色味や雰囲気を調整します。AI絵は彩度高めが多いので少し下げると自然かも。
    - **シャープネス:** +でディテール強調、-でソフトに。滑らかすぎる場合に+が有効。
    - **色収差:** 微妙な色ずれでデジタル感を薄めます。
    - **ビネット:** 周辺減光で中央に視線を集めます。
    - **K-Means:** 色数を減らしフラット化。グラデーションは失われやすいです。
    """
    )

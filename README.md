# ImageForge 🖼️ - 多機能・画像加工ツールボックス

**ImageForge**へようこそ！このアプリは、AIイラストの質感調整、画像の背景除去、レトロなピクセルアート化など、さまざまな画像加工のニーズに応える多機能なWebアプリケーションです。複数の強力なツールを、Streamlitで構築された一つの使いやすいインターフェースに統合しました。

**[➡️ こちらをクリックしてアプリを試す！]([https://your-streamlit-app-url.streamlit.app/](https://imageforge-qr3hqqd2q9mobaw39n3bec.streamlit.app/))**
*(デプロイ完了後、このURLをあなたのStreamlit CloudアプリのURLに書き換えてください)*

---

## ✨ 主な機能

ImageForgeは、サイドバーから選択できる3つの主要なツールを提供します。

### 1. 🎨 AIイラスト補正ツール
AIによって生成されたイラスト特有の、デジタル感の強すぎる質感を和らげ、より自然でアナログな風合いを与えます。
- **効果の追加**: ノイズ、色収差、ビネット効果でアナログ感を演出。
- **色彩調整**: 明るさ、コントラスト、彩度を直感的に調整。
- **K-Means減色**: 色数を減らして、イラスト風のフラットな表現に。
- **シャープネス調整**: 画像をシャープにしたり、ソフトにぼかしたりできます。

### 2. 🪄 背景リムーバー
ワンクリックで画像の背景をきれいに除去します。高性能な`rembg`ライブラリを搭載。
- **かんたん操作**: 画像をアップロードするだけで、あとは全自動で処理。
- **高い精度**: 人物、商品、動物など、さまざまな被写体に対応。
- **PNG形式で保存**: 背景が透明な高画質の画像をダウンロードできます。

### 3. 🕹️ ピクセルアートメーカー
お気に入りの写真を、どこか懐かしいレトロな雰囲気のドット絵に変換します。
- **ピクセルサイズの調整**: ドットの粗さを細かく調整可能。
- **多彩なカラースタイル**: 「16ビット風」「モノクロ」「カラフル」など、好きなスタイルを選択。
- **ビフォーアフター比較**: 元の画像と変換後の画像を並べて比較できます。

---

## 🚀 使い方（ローカル環境）

### 必要なもの
このアプリをローカルで動かすには、Python 3.8以降がインストールされている必要があります。

### インストールと実行手順

1.  **リポジトリをクローン（ダウンロード）します:**
    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2.  **仮想環境を作成し、有効化します（推奨）:**
    ```bash
    # Windowsの場合
    python -m venv venv
    venv\Scripts\activate

    # macOS / Linux の場合
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **必要なライブラリをインストールします:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Streamlitアプリを起動します:**
    ```bash
    streamlit run app.py
    ```

    自動的にブラウザが開き、アプリケーションが表示されます。

---

## 🛠️ 使用技術

*   **フレームワーク**: [Streamlit](https://streamlit.io/)
*   **画像処理**: [Pillow (PIL)](https://python-pillow.org/), [OpenCV](https://opencv.org/)
*   **機械学習**: [scikit-learn](https://scikit-learn.org/) (K-Means減色)
*   **背景除去**: [rembg](https://github.com/danielgatis/rembg)
*   **数値計算**: [NumPy](https://numpy.org/)

---

## 🙏謝辞

このプロジェクトを実現可能にしてくれた、素晴らしいオープンソースライブラリの作者とコミュニティに心から感謝します。

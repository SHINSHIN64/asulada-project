# Asurada GPT + Zonos 統合システム

このプロジェクトは、Asurada GPT（Dify API）とZonosを統合し、音声認識と自然言語処理を組み合わせたインテリジェントなシステムを構築するためのものです。

## 機能

- 音声ファイルの処理と認識
- Asurada GPT（Dify API）を使用した自然言語処理
- Zonosフレームワークとの統合
- 対話型応答システム
- RESTful APIエンドポイント
- Dockerコンテナによる簡単なデプロイ

## 必要条件

- Python 3.8以上
- requirements.txtに記載されたパッケージ
- Dify APIアクセスキー
- Zonosフレームワーク（オプション - モックが含まれています）
- Docker と Docker Compose（Docker環境で実行する場合）

## インストール方法

### 通常のインストール

1. リポジトリをクローンします：
   ```
   git clone https://github.com/SHINSHIN64/asulada-project.git
   cd asulada-project
   ```

2. 必要なパッケージをインストールします：
   ```
   pip install -r requirements.txt
   ```

3. Zonosフレームワークをインストールします（別途入手が必要）：
   ```
   pip install -e /path/to/Zonos
   ```
   注: 実際のZonosフレームワークがない場合は、内蔵のモック（zonos_mock.py）が使用されます。

4. 環境変数を設定します：
   `.env`ファイルを作成し、以下の内容を記入します：
   ```
   DIFY_API_KEY=your_dify_api_key
   DIFY_API_ENDPOINT=your_dify_api_endpoint
   DEBUG=False
   PORT=8000
   ```

### Docker環境でのインストール

1. リポジトリをクローンします：
   ```
   git clone https://github.com/SHINSHIN64/asulada-project.git
   cd asulada-project
   ```

2. サンプル環境変数ファイルをコピーして編集します：
   ```
   cp .env.sample .env
   # .envファイルを編集して、実際のAPIキーを設定してください
   ```

3. Dockerイメージをビルドして実行します：
   ```
   # Linuxまたはmacの場合
   ./run_docker.sh
   
   # Windowsの場合
   run_docker.bat
   ```

## 使用方法

### コマンドラインインターフェース

1. メインスクリプトを実行します：
   ```
   python asulada_zonos_integration.py --text "こんにちは、Asurada GPT"
   ```

2. 音声ファイルを処理するには：
   ```
   python asulada_zonos_integration.py --audio path/to/audio/file.mp3
   ```

3. Dify APIをバイパスしてZonosのみを使用するには：
   ```
   python asulada_zonos_integration.py --text "こんにちは" --no-dify
   ```

### APIサーバー

1. APIサーバーを起動します：
   ```
   python api_server.py
   ```

2. APIエンドポイントを使用します：
   - `GET /` - APIの基本情報を取得
   - `POST /api/process-text` - テキスト入力を処理
   - `POST /api/process-audio` - 音声ファイルを処理
   - `POST /api/direct-response` - Zonosを使用して直接レスポンスを生成

3. APIテストスクリプトを使用してテストします：
   ```
   # APIの基本情報を取得
   python test_api.py --info
   
   # テキスト処理をテスト
   python test_api.py --text "こんにちは、Asurada GPT"
   
   # 直接レスポンス生成をテスト
   python test_api.py --direct "今日の天気は？"
   
   # 音声処理をテスト
   python test_api.py --audio assets/exampleaudio.mp3
   ```

### Docker環境での実行方法

1. Dockerコンテナ内でコマンドを実行するには：
   ```
   docker-compose exec asurada-app python asulada_zonos_integration.py --text "こんにちは、Asurada GPT"
   ```

2. 音声ファイルを処理するには：
   ```
   # ホストマシンの音声ファイルをassetsディレクトリに配置してから
   docker-compose exec asurada-app python asulada_zonos_integration.py --audio /app/assets/your_audio_file.mp3
   ```

3. APIサーバーにアクセスするには：
   ```
   # ブラウザで以下のURLにアクセス
   http://localhost:8000/
   
   # または、curlコマンドを使用
   curl http://localhost:8000/
   curl -X POST -H "Content-Type: application/json" -d '{"text":"こんにちは"}' http://localhost:8000/api/process-text
   ```

## プロジェクト構造

```
asulada-project/
├── asulada_zonos_integration.py  # メインスクリプト
├── zonos_mock.py                 # Zonosフレームワークのモック
├── api_server.py                 # APIサーバー
├── test_api.py                   # APIテストスクリプト
├── requirements.txt              # 必要なパッケージリスト
├── .env                          # 環境変数（gitignoreに含める）
├── .env.sample                   # 環境変数のサンプル
├── Dockerfile                    # Dockerイメージ定義
├── docker-compose.yml            # Docker Compose設定
├── run_docker.sh                 # Linux/Mac用Docker実行スクリプト
├── run_docker.bat                # Windows用Docker実行スクリプト
├── uploads/                      # アップロードされた音声ファイルの保存先
└── assets/                       # 音声ファイルなどのアセット
    └── exampleaudio.mp3          # サンプル音声ファイル
```

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。

## 貢献

プルリクエストは歓迎します。大きな変更を加える場合は、まずissueを開いて議論してください。

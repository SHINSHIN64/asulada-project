# Asurada GPT + Zonos 統合システム

このプロジェクトは、Asurada GPT（Dify API）とZonosを統合し、音声認識と自然言語処理を組み合わせたインテリジェントなシステムを構築するためのものです。

## 機能

- 音声ファイルの処理と認識
- Asurada GPT（Dify API）を使用した自然言語処理
- Zonosフレームワークとの統合
- 対話型応答システム

## 必要条件

- Python 3.8以上
- requirements.txtに記載されたパッケージ
- Dify APIアクセスキー
- Zonosフレームワーク
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

4. 環境変数を設定します：
   `.env`ファイルを作成し、以下の内容を記入します：
   ```
   DIFY_API_KEY=your_dify_api_key
   DIFY_API_ENDPOINT=your_dify_api_endpoint
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

### 通常の実行方法

1. メインスクリプトを実行します：
   ```
   python asulada_zonos_integration.py
   ```

2. 音声ファイルを処理するには：
   ```
   python asulada_zonos_integration.py --audio path/to/audio/file.mp3
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

## プロジェクト構造

```
asulada-project/
├── asulada_zonos_integration.py  # メインスクリプト
├── requirements.txt              # 必要なパッケージリスト
├── .env                          # 環境変数（gitignoreに含める）
├── .env.sample                   # 環境変数のサンプル
├── Dockerfile                    # Dockerイメージ定義
├── docker-compose.yml            # Docker Compose設定
├── run_docker.sh                 # Linux/Mac用Docker実行スクリプト
├── run_docker.bat                # Windows用Docker実行スクリプト
└── assets/                       # 音声ファイルなどのアセット
    └── exampleaudio.mp3          # サンプル音声ファイル
```

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。

## 貢献

プルリクエストは歓迎します。大きな変更を加える場合は、まずissueを開いて議論してください。

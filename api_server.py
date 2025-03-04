#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Asurada GPT + Zonos 統合システム APIサーバー
RESTful APIエンドポイントを提供し、外部からのアクセスを可能にします。
"""

import os
import json
import logging
import tempfile
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# 自作モジュールのインポート
from asulada_zonos_integration import AsuradaZonosIntegration

# Flaskアプリケーションの初期化
app = Flask(__name__)
CORS(app)  # Cross-Origin Resource Sharingを有効化

# ロギングの設定
logging.basicConfig(
    level=logging.INFO if os.getenv("DEBUG", "False").lower() != "true" else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("api_server.log")
    ]
)
logger = logging.getLogger("api_server")

# アップロードされた音声ファイルの保存先
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 許可する音声ファイルの拡張子
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac'}

# 統合システムのインスタンスを作成
integration = AsuradaZonosIntegration()

def allowed_file(filename):
    """アップロードされたファイルが許可された拡張子を持つか確認"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """ルートエンドポイント - APIの基本情報を返す"""
    return jsonify({
        "name": "Asurada GPT + Zonos 統合システム API",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "APIの基本情報を取得"},
            {"path": "/api/process-text", "method": "POST", "description": "テキスト入力を処理"},
            {"path": "/api/process-audio", "method": "POST", "description": "音声ファイルを処理"},
            {"path": "/api/direct-response", "method": "POST", "description": "Zonosを使用して直接レスポンスを生成"}
        ]
    })

@app.route('/api/process-text', methods=['POST'])
def process_text():
    """テキスト入力を処理するエンドポイント"""
    data = request.json
    
    if not data or 'text' not in data:
        logger.error("リクエストにテキストが含まれていません")
        return jsonify({"error": "テキストが必要です"}), 400
    
    text_input = data['text']
    logger.info(f"テキスト処理リクエストを受信: {text_input[:50]}...")
    
    # 統合システムを使用してテキストを処理
    result = integration.run(text_input=text_input, use_dify=True)
    
    return jsonify(result)

@app.route('/api/process-audio', methods=['POST'])
def process_audio():
    """音声ファイルを処理するエンドポイント"""
    # ファイルがリクエストに含まれているか確認
    if 'audio' not in request.files:
        logger.error("リクエストに音声ファイルが含まれていません")
        return jsonify({"error": "音声ファイルが必要です"}), 400
    
    file = request.files['audio']
    
    # ファイル名が空でないか確認
    if file.filename == '':
        logger.error("ファイル名が空です")
        return jsonify({"error": "ファイル名が空です"}), 400
    
    # ファイルが許可された形式か確認
    if not allowed_file(file.filename):
        logger.error(f"許可されていないファイル形式: {file.filename}")
        return jsonify({"error": "許可されていないファイル形式です"}), 400
    
    # 安全なファイル名を生成
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    # ファイルを保存
    file.save(filepath)
    logger.info(f"音声ファイルを保存しました: {filepath}")
    
    # 統合システムを使用して音声ファイルを処理
    result = integration.run(audio_file=filepath, use_dify=True)
    
    return jsonify(result)

@app.route('/api/direct-response', methods=['POST'])
def direct_response():
    """Zonosを使用して直接レスポンスを生成するエンドポイント"""
    data = request.json
    
    if not data or 'text' not in data:
        logger.error("リクエストにテキストが含まれていません")
        return jsonify({"error": "テキストが必要です"}), 400
    
    text_input = data['text']
    logger.info(f"直接レスポンス生成リクエストを受信: {text_input[:50]}...")
    
    # 統合システムを使用して直接レスポンスを生成
    result = integration.run(text_input=text_input, use_dify=False)
    
    return jsonify(result)

@app.errorhandler(404)
def not_found(error):
    """404エラーハンドラ"""
    return jsonify({"error": "リソースが見つかりません"}), 404

@app.errorhandler(500)
def server_error(error):
    """500エラーハンドラ"""
    logger.error(f"サーバーエラー: {error}")
    return jsonify({"error": "サーバー内部エラー"}), 500

if __name__ == '__main__':
    # 環境変数からポート番号を取得（デフォルトは8000）
    port = int(os.environ.get('PORT', 8000))
    
    # デバッグモードで実行するかどうか
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"APIサーバーを起動します（ポート: {port}, デバッグモード: {debug}）")
    
    # サーバーを起動
    app.run(host='0.0.0.0', port=port, debug=debug) 
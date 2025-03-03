#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Asurada GPT + Zonos 統合システム
このスクリプトは、Asurada GPT（Dify API）とZonosを統合し、
音声認識と自然言語処理を組み合わせたインテリジェントなシステムを構築します。
"""

import os
import sys
import argparse
import json
import requests
import time
import logging
from pathlib import Path
from dotenv import load_dotenv
import speech_recognition as sr
from pydub import AudioSegment

# 環境変数の読み込み
load_dotenv()

# ロギングの設定
logging.basicConfig(
    level=logging.INFO if os.getenv("DEBUG", "False").lower() != "true" else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("asurada_zonos.log")
    ]
)
logger = logging.getLogger("asurada_zonos")

# Dify API設定
DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_API_ENDPOINT = os.getenv("DIFY_API_ENDPOINT")

# Zonos関連のインポート
try:
    # 実際のZonosパッケージがある場合はそちらを優先
    try:
        from zonos import ZonosClient
        logger.info("実際のZonosパッケージをインポートしました")
        USING_REAL_ZONOS = True
    except ImportError:
        # モックを使用
        from zonos_mock import ZonosClient
        logger.info("Zonosモックをインポートしました")
        USING_REAL_ZONOS = False
except ImportError:
    logger.error("Zonosパッケージもモックも見つかりません。システムは正常に動作しません。")
    sys.exit(1)

class AsuradaZonosIntegration:
    """Asurada GPT（Dify API）とZonosを統合するクラス"""
    
    def __init__(self):
        """初期化メソッド"""
        self.validate_environment()
        self.zonos_client = ZonosClient()
        logger.info(f"AsuradaZonosIntegrationが初期化されました（実際のZonos: {USING_REAL_ZONOS}）")
        
    def validate_environment(self):
        """環境変数が正しく設定されているか確認"""
        if not DIFY_API_KEY or not DIFY_API_ENDPOINT:
            logger.error("環境変数が設定されていません。.envファイルを確認してください。")
            logger.error("必要な環境変数: DIFY_API_KEY, DIFY_API_ENDPOINT")
            sys.exit(1)
        logger.debug("環境変数の検証が完了しました")
    
    def process_audio(self, audio_file_path):
        """音声ファイルを処理して文字起こしを行う"""
        if not Path(audio_file_path).exists():
            logger.error(f"音声ファイル '{audio_file_path}' が見つかりません。")
            return None
        
        logger.info(f"音声ファイル '{audio_file_path}' を処理中...")
        
        # 音声ファイルの形式を確認し、必要に応じて変換
        audio_format = Path(audio_file_path).suffix.lower()
        if audio_format == '.mp3':
            # MP3をWAVに変換
            sound = AudioSegment.from_mp3(audio_file_path)
            wav_path = audio_file_path.replace('.mp3', '.wav')
            sound.export(wav_path, format="wav")
            audio_file_path = wav_path
            logger.info(f"MP3をWAVに変換しました: {wav_path}")
        
        # 音声認識
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google_cloud(audio_data, language="ja-JP")
                logger.info(f"音声認識結果: {text}")
                
                # Zonosで音声テキストを分析
                analysis = self.zonos_client.analyze_audio(text)
                logger.info(f"Zonos音声分析結果: {analysis.get('sentiment', 'unknown')}")
                
                return text
            except sr.UnknownValueError:
                logger.error("音声を認識できませんでした")
                return None
            except sr.RequestError as e:
                logger.error(f"音声認識サービスへのリクエストに失敗しました: {e}")
                return None
    
    def query_dify_api(self, text_input):
        """Dify APIにクエリを送信"""
        if not text_input:
            logger.warning("空のテキスト入力が渡されました")
            return None
        
        logger.info(f"Dify APIにクエリを送信: {text_input[:50]}...")
        
        headers = {
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": {},
            "query": text_input,
            "response_mode": "streaming",
            "conversation_id": "",
            "user": "user"
        }
        
        try:
            response = requests.post(
                f"{DIFY_API_ENDPOINT}/chat-messages",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                logger.info("Dify APIからの応答を受信しました")
                return response.json()
            else:
                logger.error(f"Dify APIエラー: {response.status_code}")
                logger.error(response.text)
                return None
        except Exception as e:
            logger.error(f"Dify APIリクエスト中にエラーが発生しました: {e}")
            return None
    
    def integrate_with_zonos(self, dify_response):
        """Dify APIのレスポンスをZonosと統合"""
        if not dify_response:
            logger.warning("空のDify応答が渡されました")
            return None
        
        logger.info("Zonosとの統合処理を実行中...")
        
        # Zonosクライアントを使用してレスポンスを処理
        zonos_result = self.zonos_client.process_response(dify_response)
        
        # 統合結果を返す
        result = {
            "status": zonos_result.get("status", "unknown"),
            "message": zonos_result.get("message", "不明なレスポンス"),
            "session_id": zonos_result.get("session_id", ""),
            "timestamp": zonos_result.get("timestamp", ""),
            "content": zonos_result.get("processed_content", ""),
            "dify_response": dify_response,
            "zonos_metadata": zonos_result.get("metadata", {})
        }
        
        logger.info(f"Zonosとの統合が完了しました: {result['status']}")
        return result
    
    def generate_direct_response(self, text_input):
        """Zonosを使用して直接レスポンスを生成（Dify APIをバイパス）"""
        if not text_input:
            logger.warning("空のテキスト入力が渡されました")
            return None
        
        logger.info(f"Zonosを使用して直接レスポンスを生成: {text_input[:50]}...")
        
        # Zonosクライアントを使用してレスポンスを生成
        zonos_response = self.zonos_client.generate_response(text_input)
        
        # 結果を返す
        result = {
            "status": zonos_response.get("status", "unknown"),
            "message": zonos_response.get("message", "不明なレスポンス"),
            "session_id": zonos_response.get("session_id", ""),
            "timestamp": zonos_response.get("timestamp", ""),
            "response_text": zonos_response.get("response", {}).get("text", ""),
            "input_text": text_input,
            "zonos_metadata": zonos_response.get("metadata", {})
        }
        
        logger.info(f"Zonosによる直接レスポンス生成が完了しました: {result['status']}")
        return result
    
    def run(self, audio_file=None, text_input=None, use_dify=True):
        """メインの実行メソッド"""
        # 音声ファイルが指定されている場合は処理
        if audio_file:
            logger.info(f"音声ファイル処理モード: {audio_file}")
            text_input = self.process_audio(audio_file)
            if not text_input:
                logger.error("音声処理に失敗しました")
                return {"status": "error", "message": "音声処理に失敗しました"}
        
        # テキスト入力がない場合はエラー
        if not text_input:
            logger.error("テキスト入力が必要です")
            return {"status": "error", "message": "テキスト入力が必要です"}
        
        # Dify APIを使用するかどうかで処理を分岐
        if use_dify:
            logger.info("Dify API + Zonos統合モードで実行")
            # Dify APIにクエリを送信
            dify_response = self.query_dify_api(text_input)
            if not dify_response:
                logger.error("Dify APIへのクエリに失敗しました")
                return {"status": "error", "message": "Dify APIへのクエリに失敗しました"}
            
            # Zonosとの統合
            result = self.integrate_with_zonos(dify_response)
        else:
            logger.info("Zonos直接レスポンスモードで実行")
            # Zonosを使用して直接レスポンスを生成
            result = self.generate_direct_response(text_input)
        
        return result

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="Asurada GPT + Zonos 統合システム")
    parser.add_argument("--audio", help="処理する音声ファイルのパス")
    parser.add_argument("--text", help="直接処理するテキスト入力")
    parser.add_argument("--no-dify", action="store_true", help="Dify APIをバイパスしてZonosのみを使用")
    args = parser.parse_args()
    
    # 統合システムのインスタンスを作成
    integration = AsuradaZonosIntegration()
    
    # 音声ファイルまたはテキスト入力を処理
    result = integration.run(
        audio_file=args.audio, 
        text_input=args.text,
        use_dify=not args.no_dify
    )
    
    # 結果を表示
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

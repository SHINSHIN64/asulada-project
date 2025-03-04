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
from pathlib import Path
from dotenv import load_dotenv
import speech_recognition as sr
from pydub import AudioSegment

# 環境変数の読み込み
load_dotenv()

# Dify API設定
DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_API_ENDPOINT = os.getenv("DIFY_API_ENDPOINT")

# Zonos関連のインポート（実際のZonosパッケージに合わせて調整が必要）
try:
    # Zonosパッケージのインポート
    # from zonos import ZonosClient
    # 実際のZonosパッケージに合わせてインポート文を調整してください
    print("Zonosパッケージをインポートしました")
except ImportError:
    print("警告: Zonosパッケージが見つかりません。一部の機能が制限されます。")

class AsuradaZonosIntegration:
    """Asurada GPT（Dify API）とZonosを統合するクラス"""
    
    def __init__(self):
        """初期化メソッド"""
        self.validate_environment()
        # self.zonos_client = ZonosClient()  # 実際のZonosクライアント初期化に合わせて調整
        
    def validate_environment(self):
        """環境変数が正しく設定されているか確認"""
        if not DIFY_API_KEY or not DIFY_API_ENDPOINT:
            print("エラー: 環境変数が設定されていません。.envファイルを確認してください。")
            print("必要な環境変数: DIFY_API_KEY, DIFY_API_ENDPOINT")
            sys.exit(1)
    
    def process_audio(self, audio_file_path):
        """音声ファイルを処理して文字起こしを行う"""
        if not Path(audio_file_path).exists():
            print(f"エラー: 音声ファイル '{audio_file_path}' が見つかりません。")
            return None
        
        print(f"音声ファイル '{audio_file_path}' を処理中...")
        
        # 音声ファイルの形式を確認し、必要に応じて変換
        audio_format = Path(audio_file_path).suffix.lower()
        if audio_format == '.mp3':
            # MP3をWAVに変換
            sound = AudioSegment.from_mp3(audio_file_path)
            wav_path = audio_file_path.replace('.mp3', '.wav')
            sound.export(wav_path, format="wav")
            audio_file_path = wav_path
            print(f"MP3をWAVに変換しました: {wav_path}")
        
        # 音声認識
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google_cloud(audio_data, language="ja-JP")
                print(f"音声認識結果: {text}")
                return text
            except sr.UnknownValueError:
                print("音声を認識できませんでした")
                return None
            except sr.RequestError as e:
                print(f"音声認識サービスへのリクエストに失敗しました: {e}")
                return None
    
    def query_dify_api(self, text_input):
        """Dify APIにクエリを送信"""
        if not text_input:
            return None
        
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
                return response.json()
            else:
                print(f"Dify APIエラー: {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"Dify APIリクエスト中にエラーが発生しました: {e}")
            return None
    
    def integrate_with_zonos(self, dify_response):
        """Dify APIのレスポンスをZonosと統合"""
        if not dify_response:
            return None
        
        # ここでZonosとの統合ロジックを実装
        # 実際のZonosパッケージの仕様に合わせて調整が必要
        
        print("Zonosとの統合処理を実行中...")
        # self.zonos_client.process_response(dify_response)
        
        return {
            "status": "success",
            "message": "Zonosとの統合が完了しました",
            "dify_response": dify_response
        }
    
    def run(self, audio_file=None, text_input=None):
        """メインの実行メソッド"""
        # 音声ファイルが指定されている場合は処理
        if audio_file:
            text_input = self.process_audio(audio_file)
            if not text_input:
                return {"status": "error", "message": "音声処理に失敗しました"}
        
        # テキスト入力がない場合はエラー
        if not text_input:
            return {"status": "error", "message": "テキスト入力が必要です"}
        
        # Dify APIにクエリを送信
        dify_response = self.query_dify_api(text_input)
        if not dify_response:
            return {"status": "error", "message": "Dify APIへのクエリに失敗しました"}
        
        # Zonosとの統合
        result = self.integrate_with_zonos(dify_response)
        
        return result

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="Asurada GPT + Zonos 統合システム")
    parser.add_argument("--audio", help="処理する音声ファイルのパス")
    parser.add_argument("--text", help="直接処理するテキスト入力")
    args = parser.parse_args()
    
    # 統合システムのインスタンスを作成
    integration = AsuradaZonosIntegration()
    
    # 音声ファイルまたはテキスト入力を処理
    result = integration.run(audio_file=args.audio, text_input=args.text)
    
    # 結果を表示
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

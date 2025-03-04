#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Asurada GPT + Zonos 統合システム APIテスト
APIサーバーのエンドポイントをテストするためのスクリプトです。
"""

import os
import sys
import json
import requests
import argparse
from pathlib import Path

# デフォルトのAPIエンドポイント
DEFAULT_API_URL = "http://localhost:8000"

def test_api_info(api_url):
    """APIの基本情報を取得するテスト"""
    print("APIの基本情報を取得中...")
    
    response = requests.get(f"{api_url}/")
    
    if response.status_code == 200:
        print("成功！APIの基本情報:")
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
        return True
    else:
        print(f"エラー: ステータスコード {response.status_code}")
        print(response.text)
        return False

def test_process_text(api_url, text):
    """テキスト処理エンドポイントのテスト"""
    print(f"テキスト処理をテスト中: '{text}'")
    
    payload = {"text": text}
    response = requests.post(f"{api_url}/api/process-text", json=payload)
    
    if response.status_code == 200:
        print("成功！処理結果:")
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
        return True
    else:
        print(f"エラー: ステータスコード {response.status_code}")
        print(response.text)
        return False

def test_direct_response(api_url, text):
    """直接レスポンス生成エンドポイントのテスト"""
    print(f"直接レスポンス生成をテスト中: '{text}'")
    
    payload = {"text": text}
    response = requests.post(f"{api_url}/api/direct-response", json=payload)
    
    if response.status_code == 200:
        print("成功！処理結果:")
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
        return True
    else:
        print(f"エラー: ステータスコード {response.status_code}")
        print(response.text)
        return False

def test_process_audio(api_url, audio_file_path):
    """音声処理エンドポイントのテスト"""
    if not Path(audio_file_path).exists():
        print(f"エラー: 音声ファイル '{audio_file_path}' が見つかりません。")
        return False
    
    print(f"音声処理をテスト中: '{audio_file_path}'")
    
    with open(audio_file_path, 'rb') as audio_file:
        files = {'audio': (Path(audio_file_path).name, audio_file, 'audio/mpeg')}
        response = requests.post(f"{api_url}/api/process-audio", files=files)
    
    if response.status_code == 200:
        print("成功！処理結果:")
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
        return True
    else:
        print(f"エラー: ステータスコード {response.status_code}")
        print(response.text)
        return False

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="Asurada GPT + Zonos 統合システム APIテスト")
    parser.add_argument("--url", default=DEFAULT_API_URL, help="APIサーバーのURL")
    parser.add_argument("--info", action="store_true", help="APIの基本情報を取得")
    parser.add_argument("--text", help="テキスト処理をテスト")
    parser.add_argument("--direct", help="直接レスポンス生成をテスト")
    parser.add_argument("--audio", help="音声処理をテスト（音声ファイルのパス）")
    args = parser.parse_args()
    
    # 引数がない場合はヘルプを表示
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    # APIの基本情報を取得
    if args.info:
        test_api_info(args.url)
    
    # テキスト処理をテスト
    if args.text:
        test_process_text(args.url, args.text)
    
    # 直接レスポンス生成をテスト
    if args.direct:
        test_direct_response(args.url, args.direct)
    
    # 音声処理をテスト
    if args.audio:
        test_process_audio(args.url, args.audio)

if __name__ == "__main__":
    main() 
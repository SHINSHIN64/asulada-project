#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Zonosフレームワークのモック
実際のZonosフレームワークが利用可能になるまでの間、このモックを使用します。
"""

import json
import logging
from datetime import datetime

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('zonos_mock')

class ZonosClient:
    """Zonosクライアントのモッククラス"""
    
    def __init__(self, config=None):
        """初期化メソッド"""
        self.config = config or {}
        self.session_id = datetime.now().strftime("%Y%m%d%H%M%S")
        logger.info(f"ZonosClientが初期化されました。セッションID: {self.session_id}")
    
    def process_response(self, response_data):
        """レスポンスを処理するメソッド"""
        if not response_data:
            logger.warning("空のレスポンスデータが渡されました")
            return {
                "status": "error",
                "message": "空のレスポンスデータ",
                "session_id": self.session_id
            }
        
        logger.info(f"レスポンスデータを処理しています: {json.dumps(response_data, ensure_ascii=False)[:100]}...")
        
        # 実際の処理をシミュレート
        processed_data = {
            "status": "success",
            "message": "Zonosによる処理が完了しました",
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "processed_content": self._extract_content(response_data),
            "metadata": {
                "source": "zonos_mock",
                "version": "0.1.0"
            }
        }
        
        logger.info("レスポンスデータの処理が完了しました")
        return processed_data
    
    def _extract_content(self, response_data):
        """レスポンスデータからコンテンツを抽出するヘルパーメソッド"""
        # Dify APIのレスポンス形式に合わせて調整
        if isinstance(response_data, dict):
            if "answer" in response_data:
                return response_data["answer"]
            elif "response" in response_data:
                return response_data["response"]
            elif "message" in response_data:
                return response_data["message"]
        
        # 形式が不明な場合は元のデータを返す
        return str(response_data)
    
    def analyze_audio(self, audio_text):
        """音声テキストを分析するメソッド"""
        if not audio_text:
            logger.warning("空の音声テキストが渡されました")
            return {
                "status": "error",
                "message": "空の音声テキスト",
                "session_id": self.session_id
            }
        
        logger.info(f"音声テキストを分析しています: {audio_text[:100]}...")
        
        # 感情分析のシミュレーション
        sentiment = "positive" if "ありがとう" in audio_text or "嬉しい" in audio_text else "neutral"
        
        analysis_result = {
            "status": "success",
            "message": "音声テキストの分析が完了しました",
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "analysis": {
                "text": audio_text,
                "sentiment": sentiment,
                "word_count": len(audio_text.split()),
                "char_count": len(audio_text)
            },
            "metadata": {
                "source": "zonos_mock",
                "version": "0.1.0"
            }
        }
        
        logger.info("音声テキストの分析が完了しました")
        return analysis_result
    
    def generate_response(self, input_text, context=None):
        """入力テキストに基づいてレスポンスを生成するメソッド"""
        if not input_text:
            logger.warning("空の入力テキストが渡されました")
            return {
                "status": "error",
                "message": "空の入力テキスト",
                "session_id": self.session_id
            }
        
        logger.info(f"レスポンスを生成しています: {input_text[:100]}...")
        context = context or {}
        
        # 簡単なルールベースのレスポンス生成
        if "こんにちは" in input_text or "hello" in input_text.lower():
            response_text = "こんにちは！Zonosアシスタントです。どのようにお手伝いできますか？"
        elif "ありがとう" in input_text or "thank" in input_text.lower():
            response_text = "どういたしまして！他にお手伝いできることがあればお知らせください。"
        elif "さようなら" in input_text or "bye" in input_text.lower():
            response_text = "さようなら！またのご利用をお待ちしております。"
        else:
            response_text = f"「{input_text[:20]}...」についてのお問い合わせを承りました。詳細を教えていただけますか？"
        
        response_data = {
            "status": "success",
            "message": "レスポンスの生成が完了しました",
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "response": {
                "text": response_text,
                "input": input_text,
                "context": context
            },
            "metadata": {
                "source": "zonos_mock",
                "version": "0.1.0"
            }
        }
        
        logger.info("レスポンスの生成が完了しました")
        return response_data

# モジュールとして実行された場合のテスト
if __name__ == "__main__":
    # ZonosClientのインスタンスを作成
    client = ZonosClient()
    
    # テスト用の入力
    test_input = "こんにちは、Zonosさん。今日の天気はどうですか？"
    
    # レスポンスを生成
    response = client.generate_response(test_input)
    
    # 結果を表示
    print(json.dumps(response, ensure_ascii=False, indent=2))
"""
クイズデータを管理するモジュール
"""

import json
import os
import random


class QuizData:
    """クイズデータを管理するクラス"""
    
    def __init__(self, data_file):
        """
        クイズデータを初期化
        
        Args:
            data_file (str): クイズデータファイルのパス
        """
        self.data_file = data_file
        self.quizzes = {"easy": [], "hard": []}
        self.load_quiz_data()
    
    def load_quiz_data(self):
        """
        JSONファイルからクイズデータを読み込む
        ファイルが存在しない場合はサンプルデータを作成
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.quizzes = json.load(f)
            else:
                # サンプルデータを作成
                self._create_sample_data()
        except Exception as e:
            print(f"Quiz data loading error: {e}")
            # エラー時もサンプルデータを作成
            self._create_sample_data()
    
    def _create_sample_data(self):
        """サンプルのクイズデータを作成"""
        self.quizzes = {
            "easy": [
                {
                    "question": "What is the capital of Japan?",
                    "options": ["Osaka", "Tokyo", "Nagoya", "Fukuoka"],
                    "correct_answer": 1
                },
                {
                    "question": "1 + 1 = ?",
                    "options": ["1", "2", "3", "4"],
                    "correct_answer": 1
                },
                {
                    "question": "What color do you get when mixing red and blue?",
                    "options": ["Green", "Purple", "Orange", "Black"],
                    "correct_answer": 1
                }
            ],
            "hard": [
                {
                    "question": "What is another name for Othello?",
                    "options": ["Chess", "Shogi", "Reversi", "Go"],
                    "correct_answer": 2
                },
                {
                    "question": "What is 2 to the power of 8?",
                    "options": ["128", "256", "512", "1024"],
                    "correct_answer": 1
                },
                {
                    "question": "What are the three primary colors of light?",
                    "options": ["Red, Blue, Yellow", "Red, Green, Blue", "Cyan, Magenta, Yellow", "Red, White, Black"],
                    "correct_answer": 1
                }
            ]
        }
        
        # サンプルデータを保存
        self.save_quiz_data()
    
    def save_quiz_data(self):
        """クイズデータをJSONファイルに保存"""
        try:
            # ディレクトリが存在しない場合は作成
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.quizzes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"クイズデータの保存エラー: {e}")
    
    def get_random_quiz(self, difficulty):
        """
        指定された難易度のクイズをランダムに取得
        
        Args:
            difficulty (str): 難易度 ("easy" または "hard")
            
        Returns:
            dict: クイズデータ、または難易度に合うクイズがない場合はNone
        """
        if difficulty in self.quizzes and self.quizzes[difficulty]:
            return random.choice(self.quizzes[difficulty])
        return None
    
    def add_quiz(self, difficulty, question, options, correct_answer):
        """
        新しいクイズを追加
        
        Args:
            difficulty (str): 難易度 ("easy" または "hard")
            question (str): 問題文
            options (list): 選択肢のリスト
            correct_answer (int): 正解の選択肢のインデックス
            
        Returns:
            bool: 追加に成功したかどうか
        """
        if difficulty not in self.quizzes:
            return False
        
        new_quiz = {
            "question": question,
            "options": options,
            "correct_answer": correct_answer
        }
        
        self.quizzes[difficulty].append(new_quiz)
        self.save_quiz_data()
        return True

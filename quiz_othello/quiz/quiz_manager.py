"""
クイズの出題と回答判定を管理するモジュール
"""

from .timer import Timer
from game.constants import DIFFICULTY_EASY, DIFFICULTY_HARD, QUIZ_TIMER_SECONDS


class QuizManager:
    """クイズの出題と回答判定を管理するクラス"""
    
    def __init__(self, quiz_data):
        """
        クイズマネージャーを初期化
        
        Args:
            quiz_data (QuizData): クイズデータオブジェクト
        """
        self.quiz_data = quiz_data
        self.current_quiz = None
        self.timer = None
        self.time_up_callback = None
    
    def start_quiz(self, difficulty, time_up_callback=None):
        """
        指定された難易度のクイズを出題
        
        Args:
            difficulty (str): 難易度 ("easy" または "hard")
            time_up_callback (function): 時間切れ時のコールバック関数
            
        Returns:
            dict: 出題するクイズデータ、または出題できない場合はNone
        """
        # 前回のタイマーが動いていれば停止
        if self.timer and self.timer.is_running:
            self.timer.stop()
        
        # クイズを取得
        self.current_quiz = self.quiz_data.get_random_quiz(difficulty)
        
        if not self.current_quiz:
            return None
        
        # コールバックを設定
        self.time_up_callback = time_up_callback
        
        # タイマーを初期化して開始
        self.timer = Timer(QUIZ_TIMER_SECONDS, self.time_up)
        self.timer.start()
        
        return self.current_quiz
    
    def check_answer(self, answer_index):
        """
        回答を判定
        
        Args:
            answer_index (int): 選択された回答のインデックス
            
        Returns:
            bool: 正解かどうか
        """
        if not self.current_quiz:
            return False
        
        # タイマーを停止
        if self.timer:
            self.timer.stop()
        
        # 回答を判定
        is_correct = (answer_index == self.current_quiz["correct_answer"])
        
        return is_correct
    
    def time_up(self):
        """
        時間切れ処理
        """
        if self.time_up_callback:
            self.time_up_callback()
    
    def get_remaining_time(self):
        """
        残り時間を返す
        
        Returns:
            float: 残り時間（秒）
        """
        if self.timer:
            return self.timer.get_remaining_time()
        return 0
    
    def get_difficulty_for_attack_chance(self, attack_chance_count):
        """
        アタックチャンスの回数に応じた難易度を返す
        
        Args:
            attack_chance_count (int): アタックチャンスの使用回数
            
        Returns:
            str: 難易度 ("easy" または "hard")
        """
        if attack_chance_count == 1:
            return DIFFICULTY_EASY
        else:
            return DIFFICULTY_HARD

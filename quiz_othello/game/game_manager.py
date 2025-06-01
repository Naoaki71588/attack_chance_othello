"""
ゲーム全体の進行を管理するモジュール
"""

from .board import Board
from .player import Player
from .constants import BLACK, WHITE, STATE_PLAYING, STATE_ATTACK_CHANCE, STATE_GAME_OVER


class GameManager:
    """ゲーム全体の進行を管理するクラス"""
    
    def __init__(self, quiz_manager):
        """
        ゲームマネージャーを初期化
        
        Args:
            quiz_manager (QuizManager): クイズマネージャーオブジェクト
        """
        self.board = None
        self.players = []
        self.current_player_idx = 0
        self.state = STATE_PLAYING
        self.quiz_manager = quiz_manager
        self.attack_target = None  # アタックチャンスの対象位置
        self.game_over_callback = None
        
    def start_game(self, player1_name="Player 1", player2_name="Player 2"):
        """
        ゲームを開始
        
        Args:
            player1_name (str): プレイヤー1の名前
            player2_name (str): プレイヤー2の名前
        """
        # 盤面の初期化
        self.board = Board()
        
        # プレイヤーの初期化
        self.players = [
            Player(BLACK, player1_name),
            Player(WHITE, player2_name)
        ]
        
        # 黒から開始
        self.current_player_idx = 0
        
        # ゲーム状態を設定
        self.state = STATE_PLAYING
        
        # アタックターゲットをリセット
        self.attack_target = None
    
    def get_current_player(self):
        """
        現在の手番プレイヤーを返す
        
        Returns:
            Player: 現在の手番プレイヤー
        """
        return self.players[self.current_player_idx]
    
    def switch_turn(self):
        """
        手番を交代
        
        Returns:
            bool: 次のプレイヤーが石を置ける場合はTrue、そうでない場合はFalse
        """
        self.current_player_idx = 1 - self.current_player_idx
        
        # 次のプレイヤーが石を置ける場所があるかチェック
        current_player = self.get_current_player()
        valid_moves = self.board.get_valid_moves(current_player.player_id)
        
        if not valid_moves:
            # 石を置ける場所がない場合、さらに手番を交代
            self.current_player_idx = 1 - self.current_player_idx
            
            # 両プレイヤーとも石を置ける場所がなければゲーム終了
            next_player = self.get_current_player()
            if not self.board.get_valid_moves(next_player.player_id):
                self.state = STATE_GAME_OVER
                if self.game_over_callback:
                    self.game_over_callback()
                return False
            
            return False  # パスを示す
        
        return True
    
    def place_stone(self, row, col):
        """
        現在のプレイヤーが石を置く
        
        Args:
            row (int): 行インデックス
            col (int): 列インデックス
            
        Returns:
            bool: 石を置けたかどうか
        """
        if self.state != STATE_PLAYING:
            return False
        
        current_player = self.get_current_player()
        result = self.board.place_stone(row, col, current_player.player_id)
        
        if result:
            # 石を置けたら手番を交代
            self.switch_turn()
        
        return result
    
    def start_attack_chance(self, row, col):
        """
        アタックチャンスを開始
        
        Args:
            row (int): 行インデックス
            col (int): 列インデックス
            
        Returns:
            bool: アタックチャンスを開始できたかどうか
        """
        if self.state != STATE_PLAYING:
            return False
        
        current_player = self.get_current_player()
        
        # アタックチャンスが残っているかチェック
        if not current_player.has_attack_chance():
            return False
        
        # 指定位置が相手の石かチェック
        opponent_id = 1 - current_player.player_id
        if not (0 <= row < 8 and 0 <= col < 8) or self.board.grid[row][col] != opponent_id:
            return False
        
        # アタックチャンスを使用
        attack_chance_count = current_player.use_attack_chance()
        
        if attack_chance_count > 0:
            # アタックターゲットを記録
            self.attack_target = (row, col)
            
            # ゲーム状態を変更
            self.state = STATE_ATTACK_CHANCE
            
            # 難易度を決定
            difficulty = self.quiz_manager.get_difficulty_for_attack_chance(attack_chance_count)
            
            # クイズを出題
            self.quiz_manager.start_quiz(difficulty, self.on_quiz_time_up)
            
            return True
        
        return False
    
    def process_attack_result(self, is_correct):
        """
        クイズの結果を処理
        
        Args:
            is_correct (bool): クイズに正解したかどうか
        """
        if self.state != STATE_ATTACK_CHANCE or self.attack_target is None:
            return
        
        current_player = self.get_current_player()
        
        if is_correct:
            # 正解の場合、指定した石を反転
            row, col = self.attack_target
            self.board.attack_stone(row, col, current_player.player_id)
        
        # アタックターゲットをリセット
        self.attack_target = None
        
        # ゲーム状態を戻す
        self.state = STATE_PLAYING
        
        # 手番を交代
        self.switch_turn()
    
    def on_quiz_time_up(self):
        """
        クイズの時間切れ時の処理
        """
        # 時間切れの場合は不正解として処理
        self.process_attack_result(False)
    
    def answer_quiz(self, answer_index):
        """
        クイズに回答
        
        Args:
            answer_index (int): 選択された回答のインデックス
            
        Returns:
            bool: 正解かどうか
        """
        if self.state != STATE_ATTACK_CHANCE:
            return False
        
        # 回答を判定
        is_correct = self.quiz_manager.check_answer(answer_index)
        
        # 結果を処理
        self.process_attack_result(is_correct)
        
        return is_correct
    
    def check_game_over(self):
        """
        ゲーム終了条件をチェック
        
        Returns:
            bool: ゲームが終了したかどうか
        """
        if self.state == STATE_GAME_OVER:
            return True
        
        is_over = self.board.is_game_over()
        
        if is_over:
            self.state = STATE_GAME_OVER
            if self.game_over_callback:
                self.game_over_callback()
        
        return is_over
    
    def get_winner(self):
        """
        勝者を判定して返す
        
        Returns:
            int: 勝者のプレイヤーID、引き分けの場合は-1
        """
        if self.state != STATE_GAME_OVER:
            return None
        
        black_count, white_count = self.board.count_stones()
        
        if black_count > white_count:
            return BLACK
        elif white_count > black_count:
            return WHITE
        else:
            return -1  # 引き分け
    
    def set_game_over_callback(self, callback):
        """
        ゲーム終了時のコールバック関数を設定
        
        Args:
            callback (function): コールバック関数
        """
        self.game_over_callback = callback
    
    def get_current_quiz(self):
        """
        現在出題中のクイズを返す
        
        Returns:
            dict: クイズデータ、または出題中でない場合はNone
        """
        if self.state == STATE_ATTACK_CHANCE:
            return self.quiz_manager.current_quiz
        return None
    
    def get_quiz_remaining_time(self):
        """
        クイズの残り時間を返す
        
        Returns:
            float: 残り時間（秒）
        """
        if self.state == STATE_ATTACK_CHANCE:
            return self.quiz_manager.get_remaining_time()
        return 0

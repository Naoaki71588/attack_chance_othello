"""
オセロ盤を管理するモジュール
"""

from .constants import BOARD_SIZE, BLACK, WHITE, EMPTY, DIRECTIONS


class Board:
    """オセロ盤を管理するクラス"""
    
    def __init__(self):
        """
        8x8の盤面を初期化し、初期配置（中央に黒白を配置）を設定
        """
        # 8x8の盤面を初期化（-1は空きマス）
        self.grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        # 初期配置（中央に黒白を配置）
        center = BOARD_SIZE // 2
        self.grid[center-1][center-1] = WHITE
        self.grid[center][center] = WHITE
        self.grid[center-1][center] = BLACK
        self.grid[center][center-1] = BLACK
    
    def place_stone(self, row, col, player_id):
        """
        指定位置に石を置き、反転処理を行う
        
        Args:
            row (int): 行インデックス
            col (int): 列インデックス
            player_id (int): プレイヤーID（0:黒, 1:白）
            
        Returns:
            bool: 石を置けたかどうか
        """
        # 有効な手かどうかをチェック
        if not self.is_valid_move(row, col, player_id):
            return False
        
        # 石を置く
        self.grid[row][col] = player_id
        
        # 反転処理
        self.flip_stones(row, col, player_id)
        
        return True
    
    def is_valid_move(self, row, col, player_id):
        """
        指定位置が有効な手かどうかをチェック
        
        Args:
            row (int): 行インデックス
            col (int): 列インデックス
            player_id (int): プレイヤーID（0:黒, 1:白）
            
        Returns:
            bool: 有効な手かどうか
        """
        # 盤面の範囲外
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return False
        
        # すでに石が置かれている
        if self.grid[row][col] != EMPTY:
            return False
        
        # 8方向のいずれかで相手の石を挟めるかチェック
        for dr, dc in DIRECTIONS:
            if self._check_direction(row, col, dr, dc, player_id):
                return True
        
        return False
    
    def _check_direction(self, row, col, dr, dc, player_id):
        """
        指定方向に相手の石を挟めるかチェック
        
        Args:
            row (int): 行インデックス
            col (int): 列インデックス
            dr (int): 行方向の増分
            dc (int): 列方向の増分
            player_id (int): プレイヤーID（0:黒, 1:白）
            
        Returns:
            bool: 相手の石を挟めるかどうか
        """
        opponent = 1 - player_id
        r, c = row + dr, col + dc
        
        # 隣が相手の石でなければ挟めない
        if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE) or self.grid[r][c] != opponent:
            return False
        
        # さらに隣を調べる
        r += dr
        c += dc
        
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            # 空きマスがあれば挟めない
            if self.grid[r][c] == EMPTY:
                return False
            
            # 自分の石があれば挟める
            if self.grid[r][c] == player_id:
                return True
            
            # 次のマスへ
            r += dr
            c += dc
        
        return False
    
    def flip_stones(self, row, col, player_id):
        """
        石を置いた時に挟まれる相手の石を反転させる
        
        Args:
            row (int): 行インデックス
            col (int): 列インデックス
            player_id (int): プレイヤーID（0:黒, 1:白）
            
        Returns:
            list: 反転した石の位置リスト [(row, col), ...]
        """
        flipped = []
        
        for dr, dc in DIRECTIONS:
            if self._check_direction(row, col, dr, dc, player_id):
                r, c = row + dr, col + dc
                while self.grid[r][c] != player_id:
                    self.grid[r][c] = player_id
                    flipped.append((r, c))
                    r += dr
                    c += dc
        
        return flipped
    
    def attack_stone(self, row, col, player_id):
        """
        アタックチャンス成功時に石を反転させる処理
        
        Args:
            row (int): 行インデックス
            col (int): 列インデックス
            player_id (int): プレイヤーID（0:黒, 1:白）
            
        Returns:
            list: 反転した石の位置リスト [(row, col), ...]
        """
        flipped = []
        
        # 指定位置の石を反転
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.grid[row][col] != EMPTY:
            self.grid[row][col] = player_id
            flipped.append((row, col))
            
            # 通常の反転ルールで挟まれる石も反転
            flipped.extend(self.flip_stones(row, col, player_id))
        
        return flipped
    
    def get_valid_moves(self, player_id):
        """
        プレイヤーが石を置ける位置のリストを返す
        
        Args:
            player_id (int): プレイヤーID（0:黒, 1:白）
            
        Returns:
            list: 有効な手の位置リスト [(row, col), ...]
        """
        valid_moves = []
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.is_valid_move(row, col, player_id):
                    valid_moves.append((row, col))
        
        return valid_moves
    
    def count_stones(self):
        """
        黒と白の石の数をカウントして返す
        
        Returns:
            tuple: (黒の石の数, 白の石の数)
        """
        black_count = 0
        white_count = 0
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.grid[row][col] == BLACK:
                    black_count += 1
                elif self.grid[row][col] == WHITE:
                    white_count += 1
        
        return black_count, white_count
    
    def is_game_over(self):
        """
        ゲーム終了条件を判定
        
        Returns:
            bool: ゲームが終了したかどうか
        """
        # 両プレイヤーとも石を置ける場所がなければゲーム終了
        return not self.get_valid_moves(BLACK) and not self.get_valid_moves(WHITE)
    
    def get_opponent_stones(self, player_id):
        """
        相手の石の位置リストを返す（アタックチャンス用）
        
        Args:
            player_id (int): プレイヤーID（0:黒, 1:白）
            
        Returns:
            list: 相手の石の位置リスト [(row, col), ...]
        """
        opponent = 1 - player_id
        stones = []
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.grid[row][col] == opponent:
                    stones.append((row, col))
        
        return stones

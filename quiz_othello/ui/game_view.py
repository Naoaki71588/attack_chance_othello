"""
ゲーム画面を表示するモジュール
"""

import pygame
from game.constants import BOARD_SIZE, BLACK, WHITE, EMPTY


class GameView:
    """ゲーム画面を表示するクラス"""
    
    def __init__(self, game_manager, screen_width=800, screen_height=600):
        """
        ゲーム画面を初期化
        
        Args:
            game_manager: ゲームマネージャーオブジェクト
            screen_width (int): 画面の幅
            screen_height (int): 画面の高さ
        """
        self.game_manager = game_manager
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 盤面の描画パラメータ
        self.board_size = min(screen_width * 0.8, screen_height * 0.8)
        self.cell_size = self.board_size / BOARD_SIZE
        self.board_x = (screen_width - self.board_size) / 2
        self.board_y = (screen_height - self.board_size) / 2
        
        # 色の定義
        self.board_color = (0, 128, 0)  # 緑色
        self.line_color = (0, 0, 0)     # 黒色
        self.valid_move_color = (100, 100, 100, 128)  # 半透明グレー
        
        # フォントの初期化
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        self.large_font = pygame.font.SysFont(None, 36)
        
        # アタックモードの初期化
        self.attack_mode = False
        
        # ボタンの初期化
        from .components import Button
        button_width = 150
        button_height = 40
        button_x = self.screen_width - button_width - 10
        button_y = 10
        self.attack_button = Button(
            button_x, button_y, button_width, button_height,
            "Attack Chance", (200, 0, 0), (255, 0, 0)
        )
    def draw(self, screen):
        """
        ゲーム画面を描画
        
        Args:
            screen (pygame.Surface): 描画先の画面
        """
        # 背景を描画
        screen.fill((240, 240, 240))
        
        # 盤面を描画
        self.draw_board(screen)
        
        # 石を描画
        self.draw_stones(screen)
        
        # アタックモードの場合は相手の石をハイライト
        if self.attack_mode:
            self.highlight_opponent_stones(screen)
        else:
            # 通常モードでは有効な手を表示
            self.draw_valid_moves(screen)
        
        # ゲーム情報を表示
        self.draw_game_info(screen)
        
        # アタックチャンスボタンを描画
        if self.attack_button:
            self.attack_button.draw(screen, self.font)
    def draw_board(self, screen):
        """
        オセロ盤を描画
        
        Args:
            screen (pygame.Surface): 描画先の画面
        """
        # 盤面の背景を描画
        board_rect = pygame.Rect(self.board_x, self.board_y, self.board_size, self.board_size)
        pygame.draw.rect(screen, self.board_color, board_rect)
        
        # 格子線を描画
        for i in range(BOARD_SIZE + 1):
            # 横線
            start_x = self.board_x
            start_y = self.board_y + i * self.cell_size
            end_x = self.board_x + self.board_size
            end_y = start_y
            pygame.draw.line(screen, self.line_color, (start_x, start_y), (end_x, end_y), 2)
            
            # 縦線
            start_x = self.board_x + i * self.cell_size
            start_y = self.board_y
            end_x = start_x
            end_y = self.board_y + self.board_size
            pygame.draw.line(screen, self.line_color, (start_x, start_y), (end_x, end_y), 2)
    def draw_stones(self, screen):
        """
        石を描画
        
        Args:
            screen (pygame.Surface): 描画先の画面
        """
        if not self.game_manager.board:
            return
            
        board = self.game_manager.board
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                cell_value = board.grid[row][col]
                if cell_value != EMPTY:
                    # 石の中心座標
                    center_x = self.board_x + (col + 0.5) * self.cell_size
                    center_y = self.board_y + (row + 0.5) * self.cell_size
                    radius = self.cell_size * 0.4
                    
                    # 石の色
                    color = (0, 0, 0) if cell_value == BLACK else (255, 255, 255)
                    
                    # 石を描画
                    pygame.draw.circle(screen, color, (center_x, center_y), radius)
                    
                    # 白い石には黒い輪郭を付ける
                    if cell_value == WHITE:
                        pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius, 1)
    def highlight_opponent_stones(self, screen):
        """
        相手の石をハイライト表示
        
        Args:
            screen (pygame.Surface): 描画先の画面
        """
        if not self.game_manager.board:
            return
            
        board = self.game_manager.board
        current_player = self.game_manager.get_current_player()
        opponent_id = 1 - current_player.player_id
        
        # ハイライトの色（半透明の黄色）
        highlight_color = (255, 255, 0, 128)
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board.grid[row][col] == opponent_id:
                    # 相手の石の中心座標
                    center_x = self.board_x + (col + 0.5) * self.cell_size
                    center_y = self.board_y + (row + 0.5) * self.cell_size
                    radius = self.cell_size * 0.45
                    
                    # 半透明の円を描画
                    s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(s, highlight_color, (radius, radius), radius)
                    screen.blit(s, (center_x - radius, center_y - radius))
    def draw_valid_moves(self, screen):
        """
        有効な手を表示
        
        Args:
            screen (pygame.Surface): 描画先の画面
        """
        if not self.game_manager.board or self.game_manager.state != 0:  # STATE_PLAYING
            return
            
        current_player = self.game_manager.get_current_player()
        valid_moves = self.game_manager.board.get_valid_moves(current_player.player_id)
        
        for row, col in valid_moves:
            # 有効な手の中心座標
            center_x = self.board_x + (col + 0.5) * self.cell_size
            center_y = self.board_y + (row + 0.5) * self.cell_size
            radius = self.cell_size * 0.2
            
            # 半透明の円を描画
            s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, self.valid_move_color, (radius, radius), radius)
            screen.blit(s, (center_x - radius, center_y - radius))
    def draw_game_info(self, screen):
        """
        ゲーム情報（手番、石の数など）を表示
        
        Args:
            screen (pygame.Surface): 描画先の画面
        """
        if not self.game_manager.board:
            return
            
        # 石の数をカウント
        black_count, white_count = self.game_manager.board.count_stones()
        
        # 現在のプレイヤー
        current_player = self.game_manager.get_current_player()
        player_color = "Black" if current_player.player_id == BLACK else "White"
        
        # 情報テキスト
        info_text = f"Turn: {player_color}  Black: {black_count}  White: {white_count}"
        
        # アタックチャンス情報
        attack_text = f"Attack Chances Left: {current_player.attack_chances}"
        
        # テキストを描画
        info_surface = self.font.render(info_text, True, (0, 0, 0))
        attack_surface = self.font.render(attack_text, True, (0, 0, 0))
        
        # 位置を設定
        info_rect = info_surface.get_rect(topleft=(10, 10))
        attack_rect = attack_surface.get_rect(topleft=(10, 40))
        
        # 描画
        screen.blit(info_surface, info_rect)
        screen.blit(attack_surface, attack_rect)
        
        # ゲーム終了時は勝者を表示
        if self.game_manager.state == 2:  # STATE_GAME_OVER
            winner = self.game_manager.get_winner()
            if winner == BLACK:
                result_text = "Black Wins!"
            elif winner == WHITE:
                result_text = "White Wins!"
            else:
                result_text = "Draw!"
                
            result_surface = self.large_font.render(result_text, True, (255, 0, 0))
            result_rect = result_surface.get_rect(center=(self.screen_width // 2, 50))
            screen.blit(result_surface, result_rect)
    def handle_click(self, pos):
        """
        クリックイベントを処理
        
        Args:
            pos (tuple): クリック位置 (x, y)
            
        Returns:
            bool: イベントが処理されたかどうか
        """
        # アタックボタンのクリック処理
        if self.attack_button and self.attack_button.is_clicked(pos, True):
            self.start_attack_mode()
            return True
        
        # 通常モードでの盤面クリック処理
        if self.game_manager.state == 0 and not self.attack_mode:  # STATE_PLAYING
            board_pos = self.get_board_position(pos)
            if board_pos:
                row, col = board_pos
                # 石を置く
                return self.game_manager.place_stone(row, col)
        
        # アタックモードでの盤面クリック処理
        elif self.attack_mode:
            board_pos = self.get_board_position(pos)
            if board_pos:
                row, col = board_pos
                # アタックチャンスを開始
                result = self.game_manager.start_attack_chance(row, col)
                if result:
                    self.attack_mode = False
                return result
        
        return False
    def start_attack_mode(self):
        """
        アタックモードを開始
        """
        current_player = self.game_manager.get_current_player()
        if current_player.has_attack_chance():
            self.attack_mode = True
            # アタックモードの説明テキストを表示
            print("相手の石を選択してください")
        else:
            # アタックチャンスがない場合は何もしない
            self.attack_mode = False
    def update(self):
        """
        ゲーム画面の状態を更新
        """
        # アタックボタンの状態を更新
        if self.attack_button:
            # マウス位置を取得
            mouse_pos = pygame.mouse.get_pos()
            self.attack_button.update(mouse_pos)
    
    def get_board_position(self, pos):
        """
        画面座標から盤面上の位置（行、列）に変換
        
        Args:
            pos (tuple): 画面座標 (x, y)
            
        Returns:
            tuple: 盤面上の位置 (row, col)、盤面外の場合は None
        """
        x, y = pos
        
        # 盤面の範囲外
        if (x < self.board_x or x >= self.board_x + self.board_size or
            y < self.board_y or y >= self.board_y + self.board_size):
            return None
        
        # 盤面上の位置に変換
        col = int((x - self.board_x) / self.cell_size)
        row = int((y - self.board_y) / self.cell_size)
        
        # 範囲チェック
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        
        return None

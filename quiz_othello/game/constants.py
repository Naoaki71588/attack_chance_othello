"""
ゲームの定数を定義するモジュール
"""

# ボードサイズ
BOARD_SIZE = 8

# プレイヤーID
BLACK = 0
WHITE = 1

# セルの状態
EMPTY = -1

# ゲームの状態
STATE_PLAYING = 0
STATE_ATTACK_CHANCE = 1
STATE_GAME_OVER = 2

# 方向ベクトル（8方向）
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

# クイズの難易度
DIFFICULTY_EASY = "easy"
DIFFICULTY_HARD = "hard"

# タイマー設定
QUIZ_TIMER_SECONDS = 30

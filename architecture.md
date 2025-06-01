# クイズオセロ - アーキテクチャ設計

## プロジェクト構造

```
quiz_othello/
├── main.py                 # ゲームのエントリーポイント
├── game/
│   ├── __init__.py
│   ├── board.py            # オセロ盤の管理クラス
│   ├── game_manager.py     # ゲーム全体の管理クラス
│   ├── player.py           # プレイヤークラス
│   └── constants.py        # ゲーム定数
├── quiz/
│   ├── __init__.py
│   ├── quiz_manager.py     # クイズ管理クラス
│   ├── quiz_data.py        # クイズデータ構造
│   └── timer.py            # タイマー機能
├── ui/
│   ├── __init__.py
│   ├── game_view.py        # ゲーム画面表示
│   ├── quiz_view.py        # クイズ画面表示
│   ├── components.py       # UI共通コンポーネント
│   └── assets/             # 画像・音声などのアセット
│       ├── images/
│       └── sounds/
├── utils/
│   ├── __init__.py
│   └── helpers.py          # ユーティリティ関数
└── data/
    └── quiz_data.json      # クイズデータ
```

## クラス設計

### Game モジュール

#### Board クラス
```python
class Board:
    """オセロ盤を管理するクラス"""
    
    def __init__(self):
        # 8x8の盤面を初期化
        # 初期配置（中央に黒白を配置）
    
    def place_stone(self, row, col, player_id):
        # 指定位置に石を置く
        # 反転処理を行う
        # 成功/失敗を返す
    
    def get_valid_moves(self, player_id):
        # プレイヤーが石を置ける位置のリストを返す
    
    def flip_stones(self, row, col, player_id):
        # 石を置いた時に挟まれる相手の石を反転させる
    
    def attack_stone(self, row, col, player_id):
        # アタックチャンス成功時に石を反転させる処理
    
    def count_stones(self):
        # 黒と白の石の数をカウントして返す
    
    def is_game_over(self):
        # ゲーム終了条件を判定
```

#### Player クラス
```python
class Player:
    """プレイヤー情報を管理するクラス"""
    
    def __init__(self, player_id, name):
        # プレイヤーID（0:黒, 1:白）
        # プレイヤー名
        # 残りアタックチャンス回数（初期値2）
    
    def use_attack_chance(self):
        # アタックチャンスを使用
        # 残り回数を減らす
        # 現在の使用回数（1回目か2回目か）を返す
    
    def has_attack_chance(self):
        # アタックチャンスが残っているかどうかを返す
```

#### GameManager クラス
```python
class GameManager:
    """ゲーム全体の進行を管理するクラス"""
    
    def __init__(self):
        # 盤面の初期化
        # プレイヤーの初期化
        # 現在の手番プレイヤー
        # ゲーム状態（通常/アタックチャンス中/ゲーム終了）
    
    def start_game(self):
        # ゲームを開始
    
    def switch_turn(self):
        # 手番を交代
    
    def place_stone(self, row, col):
        # 現在のプレイヤーが石を置く
    
    def start_attack_chance(self, row, col):
        # アタックチャンスを開始
        # クイズマネージャーにクイズ出題を依頼
    
    def process_attack_result(self, is_correct):
        # クイズの結果を処理
        # 正解なら石を反転
    
    def check_game_over(self):
        # ゲーム終了条件をチェック
    
    def get_winner(self):
        # 勝者を判定して返す
```

### Quiz モジュール

#### QuizData クラス
```python
class QuizData:
    """クイズデータを管理するクラス"""
    
    def __init__(self, data_file):
        # クイズデータファイルを読み込む
    
    def get_random_quiz(self, difficulty):
        # 指定された難易度のクイズをランダムに取得
    
    def load_quiz_data(self):
        # JSONファイルからクイズデータを読み込む
```

#### QuizManager クラス
```python
class QuizManager:
    """クイズの出題と回答判定を管理するクラス"""
    
    def __init__(self, quiz_data):
        # クイズデータを初期化
        # タイマーを初期化
    
    def start_quiz(self, difficulty):
        # 指定された難易度のクイズを出題
        # タイマーをスタート
    
    def check_answer(self, answer_index):
        # 回答を判定
        # 正解/不正解を返す
    
    def time_up(self):
        # 時間切れ処理
```

#### Timer クラス
```python
class Timer:
    """タイマー機能を提供するクラス"""
    
    def __init__(self, duration, callback):
        # タイマーの時間（秒）
        # タイムアップ時のコールバック関数
    
    def start(self):
        # タイマーをスタート
    
    def stop(self):
        # タイマーを停止
    
    def get_remaining_time(self):
        # 残り時間を返す
```

### UI モジュール

#### GameView クラス
```python
class GameView:
    """ゲーム画面を表示するクラス"""
    
    def __init__(self, game_manager):
        # ゲームマネージャーへの参照
        # 画面の初期化
    
    def draw(self):
        # ゲーム画面を描画
    
    def draw_board(self):
        # オセロ盤を描画
    
    def draw_stones(self):
        # 石を描画
    
    def draw_valid_moves(self):
        # 有効な手を表示
    
    def draw_game_info(self):
        # ゲーム情報（手番、石の数など）を表示
    
    def handle_click(self, x, y):
        # クリックイベントを処理
        # 盤面上の位置に変換
```

#### QuizView クラス
```python
class QuizView:
    """クイズ画面を表示するクラス"""
    
    def __init__(self, quiz_manager):
        # クイズマネージャーへの参照
    
    def draw(self, quiz):
        # クイズ画面を描画
    
    def draw_question(self, question):
        # 問題文を表示
    
    def draw_options(self, options):
        # 選択肢を表示
    
    def draw_timer(self, remaining_time):
        # タイマーを表示
    
    def handle_click(self, x, y):
        # クリックイベントを処理
        # 選択肢の選択を処理
```

## データ構造

### クイズデータ（JSON形式）
```json
{
  "easy": [
    {
      "question": "問題文1",
      "options": ["選択肢1", "選択肢2", "選択肢3", "選択肢4"],
      "correct_answer": 0
    },
    {
      "question": "問題文2",
      "options": ["選択肢1", "選択肢2", "選択肢3", "選択肢4"],
      "correct_answer": 1
    }
  ],
  "hard": [
    {
      "question": "問題文1",
      "options": ["選択肢1", "選択肢2", "選択肢3", "選択肢4"],
      "correct_answer": 2
    },
    {
      "question": "問題文2",
      "options": ["選択肢1", "選択肢2", "選択肢3", "選択肢4"],
      "correct_answer": 3
    }
  ]
}
```

## ゲームフロー

1. `main.py`がゲームを起動
2. `GameManager`がゲームを初期化
3. メインループ開始
   - `GameView`がゲーム画面を描画
   - プレイヤーの入力を処理
   - 通常の石配置またはアタックチャンス
4. アタックチャンス選択時：
   - `QuizManager`がクイズを出題
   - `QuizView`がクイズ画面を表示
   - `Timer`が30秒カウントダウン
   - プレイヤーが回答または時間切れ
   - `GameManager`が結果を処理
5. ゲーム終了条件を満たすまで3-4を繰り返す
6. ゲーム終了、勝者表示

## 状態遷移

1. ゲーム開始状態
2. プレイヤーターン状態
   - 石を置く
   - アタックチャンスを使用
3. クイズ状態
   - クイズ回答
   - タイムアップ
4. ゲーム終了状態

## 拡張性

- クイズのジャンル追加
- 難易度レベルの追加
- 盤面サイズの変更
- ネットワーク対戦機能
- スコア記録・ランキング機能

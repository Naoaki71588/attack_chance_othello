# クイズオセロ - 要件定義書

## ゲーム概要
- ベースはオセロ（リバーシ）
- 2人プレイヤー制
- 通常のオセロルールに加え、特殊ルール「アタックチャンス」を追加

## 基本ルール
- 通常のオセロと同様、黒と白の石を交互に置いていく
- 相手の石を挟むと自分の色に変わる
- 石を置ける場所がなくなった場合はパス
- 両者とも置ける場所がなくなった場合、ゲーム終了
- 石の数が多い方が勝利

## アタックチャンスのルール
- 各プレイヤーは対局中に2回まで使用可能
- 相手の石を指定してアタックチャンスを宣言
- クイズが出題される（選択問題形式）
- 正解：指定した石が自分の石になり、挟まれた石も反転
- 不正解：答えは公開されず、アタックチャンスのみ消費
- アタックチャンスの使用は任意（使わなくてもよい）

## アタックチャンスの詳細
- 1回目のアタックチャンス：易しい問題が出題される
- 2回目のアタックチャンス：難しい問題が出題される
- 回答制限時間：30秒
- 制限時間内に回答できなかった場合：アタックチャンスは消費されるが、石の状態は変化なし

## クイズシステム
- 選択問題形式（複数の選択肢から一つを選ぶ）
- 難易度は「易しい」と「難しい」の2段階
- ジャンル分けなし
- クイズデータは事前に登録

## ゲームフロー
1. オセロの初期配置からスタート
2. プレイヤーが交互に手番を行う
3. 手番では以下のいずれかを選択
   - 通常のオセロルールに従って石を置く
   - アタックチャンスを宣言する（残りがある場合）
4. アタックチャンス宣言時：
   - 相手の石を指定
   - 使用回数に応じた難易度のクイズが出題される
   - 30秒タイマーがスタート
   - プレイヤーが回答または時間切れ
   - 結果に応じて盤面が更新される
5. 両者とも石を置けなくなったらゲーム終了
6. 石の数が多い方が勝利

## 技術的な実装要件

### ゲームロジック
- オセロの盤面管理（8x8マス）
- 石の配置と反転ロジック
- 有効な手の判定
- ゲーム終了条件の判定
- 勝敗判定

### アタックチャンス機能
- プレイヤーごとのアタックチャンス回数カウント
- 相手の石を指定する機能
- 難易度に応じたクイズ出題システム
- 回答判定システム

### クイズシステム
- 難易度別のクイズデータベース（易しい/難しい）
- ランダムなクイズ出題機能
- 回答判定機能
- 30秒タイマー機能

### UI/UX
- オセロ盤の表示
- 石の配置・反転のアニメーション
- アタックチャンス使用時の特殊演出
- クイズ表示インターフェース
- タイマー表示
- ゲーム状態の表示（現在の手番、石の数など）

### データ管理
- クイズデータの構造設計
- クイズデータの読み込み機能

## 開発環境
- 言語：Python
- フレームワーク：PyGate

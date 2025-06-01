"""
Quiz Othello Game Main Module
"""

import sys
import pygame
from quiz.quiz_data import QuizData
from quiz.quiz_manager import QuizManager
from game.game_manager import GameManager
from ui.game_view import GameView
from ui.quiz_view import QuizView
from utils.helpers import get_quiz_data_path


def main():
    """Main function"""
    # Initialize Pygame
    pygame.init()
    
    # Set up fonts
    pygame.font.init()
    screen_width = 800
    screen_height = 600
    
    # 画面を作成
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Quiz Othello")
    
    # クロックを作成
    clock = pygame.time.Clock()
    
    # クイズデータを初期化
    quiz_data = QuizData(get_quiz_data_path())
    
    # クイズマネージャーを初期化
    quiz_manager = QuizManager(quiz_data)
    
    # ゲームマネージャーを初期化
    game_manager = GameManager(quiz_manager)
    
    # ゲームを開始
    game_manager.start_game("Player 1", "Player 2")
    
    # ゲーム画面を初期化
    game_view = GameView(game_manager, screen_width, screen_height)
    
    # クイズ画面を初期化
    quiz_view = QuizView(quiz_manager, screen_width, screen_height)
    
    # メインループ
    running = True
    while running:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 左クリック
                if game_manager.state == 1:  # STATE_ATTACK_CHANCE
                    # クイズ画面でのクリック
                    answer_index = quiz_view.handle_click(event.pos)
                    if answer_index >= 0:
                        game_manager.answer_quiz(answer_index)
                else:
                    # ゲーム画面でのクリック
                    game_view.handle_click(event.pos)
        
        # マウス位置を取得
        mouse_pos = pygame.mouse.get_pos()
        
        # 画面を更新
        game_view.update()
        
        if game_manager.state == 1:  # STATE_ATTACK_CHANCE
            # クイズ画面を更新
            quiz_view.update(mouse_pos)
            
            # クイズ画面を描画
            current_quiz = game_manager.get_current_quiz()
            remaining_time = game_manager.get_quiz_remaining_time()
            quiz_view.draw(screen, current_quiz, remaining_time)
        else:
            # ゲーム画面を描画
            game_view.draw(screen)
        
        # 画面を更新
        pygame.display.flip()
        
        # フレームレートを制限
        clock.tick(60)
    
    # Pygameを終了
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

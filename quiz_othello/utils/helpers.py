"""
ユーティリティ関数を提供するモジュール
"""

import os
import pygame


def load_image(filename, scale=None):
    """
    画像を読み込む
    
    Args:
        filename (str): 画像ファイル名
        scale (tuple): リサイズするサイズ (width, height)
        
    Returns:
        pygame.Surface: 読み込んだ画像
    """
    try:
        image = pygame.image.load(filename)
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Image loading error: {e}")
        # エラー時は代替の画像（色付きの矩形）を返す
        surface = pygame.Surface((50, 50))
        surface.fill((255, 0, 0))  # 赤色
        return surface


def create_data_directory():
    """
    データディレクトリを作成
    
    Returns:
        str: データディレクトリのパス
    """
    # スクリプトのディレクトリを取得
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # データディレクトリのパス
    data_dir = os.path.join(script_dir, "data")
    
    # ディレクトリが存在しない場合は作成
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    return data_dir


def get_quiz_data_path():
    """
    クイズデータファイルのパスを取得
    
    Returns:
        str: クイズデータファイルのパス
    """
    data_dir = create_data_directory()
    return os.path.join(data_dir, "quiz_data.json")

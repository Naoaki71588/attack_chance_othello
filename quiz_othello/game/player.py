"""
プレイヤー情報を管理するモジュール
"""

class Player:
    """プレイヤー情報を管理するクラス"""
    
    def __init__(self, player_id, name):
        """
        プレイヤー情報を初期化
        
        Args:
            player_id (int): プレイヤーID（0:黒, 1:白）
            name (str): プレイヤー名
        """
        self.player_id = player_id
        self.name = name
        self.attack_chances = 2  # 残りアタックチャンス回数（初期値2）
        self.used_attack_chances = 0  # 使用済みアタックチャンス回数
    
    def use_attack_chance(self):
        """
        アタックチャンスを使用
        
        Returns:
            int: 現在の使用回数（1回目か2回目か）、使用できない場合は0
        """
        if self.attack_chances <= 0:
            return 0
        
        self.attack_chances -= 1
        self.used_attack_chances += 1
        return self.used_attack_chances
    
    def has_attack_chance(self):
        """
        アタックチャンスが残っているかどうかを返す
        
        Returns:
            bool: アタックチャンスが残っているかどうか
        """
        return self.attack_chances > 0

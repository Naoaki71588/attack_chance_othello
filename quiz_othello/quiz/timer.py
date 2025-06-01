"""
タイマー機能を提供するモジュール
"""

import time
import threading


class Timer:
    """タイマー機能を提供するクラス"""
    
    def __init__(self, duration, callback):
        """
        タイマーを初期化
        
        Args:
            duration (int): タイマーの時間（秒）
            callback (function): タイムアップ時のコールバック関数
        """
        self.duration = duration
        self.callback = callback
        self.start_time = None
        self.is_running = False
        self.timer_thread = None
    
    def start(self):
        """
        タイマーをスタート
        """
        if self.is_running:
            return
        
        self.start_time = time.time()
        self.is_running = True
        
        # 別スレッドでタイマーを実行
        self.timer_thread = threading.Thread(target=self._run_timer)
        self.timer_thread.daemon = True
        self.timer_thread.start()
    
    def _run_timer(self):
        """
        タイマーを実行（内部メソッド）
        """
        while self.is_running:
            elapsed = time.time() - self.start_time
            
            if elapsed >= self.duration:
                self.is_running = False
                if self.callback:
                    self.callback()
                break
            
            # CPUの負荷を減らすために少し待機
            time.sleep(0.1)
    
    def stop(self):
        """
        タイマーを停止
        """
        self.is_running = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(0.5)
    
    def get_remaining_time(self):
        """
        残り時間を返す
        
        Returns:
            float: 残り時間（秒）、タイマーが動いていない場合は0
        """
        if not self.is_running or self.start_time is None:
            return 0
        
        elapsed = time.time() - self.start_time
        remaining = max(0, self.duration - elapsed)
        return remaining

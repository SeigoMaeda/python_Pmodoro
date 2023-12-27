class Timer:
    TIMER_COUNT = 1500
    
    def __init__(self, callback):
        self.timer_running = False 
        self.count_time = self.TIMER_COUNT
        self.callback = callback

    def update_timer(self):
        """
        タイマーの動作処理
        """
        if not self.timer_running:
            return
        
        if self.count_time > 0:
            self.count_time -= 1
            self.minutes, self.seconds = divmod(self.count_time, 60)
            self.callback(f"{self.minutes:02}:{self.seconds:02}")
        else:
            self.stop_timer()
            self.reset_timer()

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False
        
    def reset_timer(self):
        self.count_time = self.TIMER_COUNT

    def get_count_time(self):
        return self.count_time
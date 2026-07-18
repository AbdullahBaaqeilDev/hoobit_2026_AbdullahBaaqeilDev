import time


class Timer:
    def __init__(self, callback, delay_s = 1, periodic = False):
        self.delay_s = delay_s
        self.callback = callback
        self.periodic = periodic
        self.disabled = False
        self.ran = False
        self.start_time = time.time()

    def start(self):
        self.disabled = False
        self.start_time = time.time()

    def elapsed_time(self):
        return time.time() - self.start_time
    
    def remaining_time(self):
        return self.delay_s - (time.time() - self.start_time) 

    def update(self):
        if self.disabled:
            self.start_time = time.time()
            return
        
        if time.time() - self.start_time > self.delay_s and self.callback:
            self.callback()
            self.ran = True
            if not self.periodic:
                return
            self.start_time = time.time()
from fake_useragent import UserAgent
import random


class UAPool:
    count = 0
    ua_pool = []

    def add_ua_to_pool(self, times):
        rand = random.randrange(1, 4, 1)
        for i in range(times + 1):
            if rand == 1:
                self.ua_pool.append(self.ua.chrome)
            elif rand == 2:
                self.ua_pool.append(self.ua.firefox)
            elif rand == 3:
                self.ua_pool.append(self.ua.edge)
            else:
                self.ua_pool.append(self.ua.safari)

    def __init__(self):
        self.ua = UserAgent()
        times = random.randrange(5, 15, 1)
        self.add_ua_to_pool(times)
        self.count = times

    def pop_pool(self):
        if self.count >= 1:
            self.count -= 1
        else:
            self.add_ua_to_pool(10)
            self.count += 9
        return self.ua_pool.pop()

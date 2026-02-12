import random
import time

def random_sleep(min_delay=0.1, max_delay=1.0):
    """Рандомна затримка від min_delay до max_delay секунд"""
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)
    return delay

def random_duration():
    """Рандомна тривалість для анімацій від 0.1 до 1 секунди"""
    return random.uniform(0.1, 1.0)
import random
import time

def random_sleep():
    """Рандомна затримка від 0.1 до 1 секунди"""
    delay = random.uniform(0.1, 1.0)
    time.sleep(delay)
    return delay

def random_duration():
    """Рандомна тривалість для анімацій від 0.1 до 1 секунди"""
    return random.uniform(0.1, 1.0)
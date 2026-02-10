import random
import time

def random_sleep(min_seconds=0.1, max_seconds=1.0):
    """Рандомна затримка"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    return delay

def random_duration(min_seconds=0.1, max_seconds=0.5):
    """Рандомна тривалість для анімацій"""
    return random.uniform(min_seconds, max_seconds)
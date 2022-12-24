import random
import time


def random_sleep(max_sleep: float = 2.0, min_sleep: float = 0.2):
    time.sleep(random.uniform(min_sleep, max_sleep))

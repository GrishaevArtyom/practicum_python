# Исследуйте библиотеки и функции Python для генерации параметров Диффи-Хеллмана.
# Сравните различные методы генерации и выберите оптимальный для вашей реализации.\

# С помощью библиотеки

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh

parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())

# Вручную

import random
import math

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_dh_parameters():
    while True:
        p = random.randint(2**2047, 2**2048)  # Большое простое число
        if is_prime(p):
            break
    g = random.randint(2, p - 1)  # Первый подходящий первообразный корень
    return p, g

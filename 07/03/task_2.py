# Реализуйте обмен ключами между двумя сторонами с добавлением механизма проверки успешности обмена.
# Убедитесь, что обе стороны получили одинаковый общий секретный ключ.

from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

# Генерация параметров
parameters = dh.generate_parameters(generator=2, key_size=2048)

# Алиса
alice_private_key = parameters.generate_private_key()
alice_public_key = alice_private_key.public_key()

# Боб
bob_private_key = parameters.generate_private_key()
bob_public_key = bob_private_key.public_key()

# Обмен публичными ключами
alice_shared_secret = alice_private_key.exchange(bob_public_key)
bob_shared_secret = bob_private_key.exchange(alice_public_key)

# Проверка успешности обмена
assert alice_shared_secret == bob_shared_secret, "Общий секретный ключ не совпадает!"

# Вывод общего секретного ключа
print("Общий секретный ключ успешно сгенерирован!")

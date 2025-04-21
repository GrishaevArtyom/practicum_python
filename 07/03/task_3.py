# Изучите различные режимы работы AES (например, CBC, CFB, OFB, GCM) и реализуйте шифрование и дешифрование сообщений с использованием каждого из них.
# Сравните результаты и безопасность каждого режима.

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import urandom


# 1. CBC (Cipher Block Chaining)
# Преимущества:
# - Высокая безопасность при правильном использовании уникального IV.
#   Каждый блок шифруется с учетом предыдущего зашифрованного блока,
#   что делает атаки на основе повторяющихся блоков невозможными.
# - Подходит для шифрования больших объемов данных.
#
# Недостатки:
# - Не параллелизуемый: каждый блок зависит от предыдущего,
#   что снижает производительность при работе с большими данными.
# - Требует дополнения данных до размера блока (16 байт для AES).
# - Уязвим к атакам, если IV повторяется или предсказуем.

# Генерация ключа и IV
key = urandom(32)
iv = urandom(16)

# Шифрование
cipher = Cipher(algorithms.AES(key), modes.OFB(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update("Секретное сообщение".encode("utf-8")) + encryptor.finalize()

# Дешифрование
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()

print("OFB ciphertext:", ciphertext)
print("OFB plaintext:", plaintext)


# 2. CFB (Cipher Feedback)
# Преимущества:
# - Преобразует блочный шифр в потоковый, что позволяет шифровать данные
#   без необходимости дополнения до размера блока.
# - Подходит для шифрования потоковых данных (например, сетевой трафик).
# - Параллелизуемый (за исключением первого блока).
#
# Недостатки:
# - Уязвим к атакам при повторении IV.
# - Ошибки в передаче данных могут распространяться на последующие блоки.
# - Менее распространен по сравнению с CBC.
# Генерация ключа и IV

key = urandom(32)
iv = urandom(16)

# Шифрование
cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update("Секретное сообщение".encode("utf-8")) + encryptor.finalize()

# Дешифрование
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()

print("CFB ciphertext:", ciphertext)
print("CFB plaintext:", plaintext)


# 3. OFB (Output Feedback)
# Преимущества:
# - Преобразует блочный шифр в потоковый, что устраняет необходимость
#   дополнения данных до размера блока.
# - Ошибки в передаче данных не распространяются на другие блоки,
#   так как зашифрованный текст независим от открытого текста.
# - Подходит для шифрования потоковых данных.
#
# Недостатки:
# - Уязвим к атакам при повторении IV.
# - Менее распространен и менее эффективен по сравнению с CBC и CFB.
# - Отсутствие зависимости от открытого текста может быть недостатком
#   в некоторых сценариях использования.
# Генерация ключа и IV

key = urandom(32)
iv = urandom(16)

# Шифрование
cipher = Cipher(algorithms.AES(key), modes.OFB(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update("Секретное сообщение".encode("utf-8")) + encryptor.finalize()

# Дешифрование
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()

print("OFB ciphertext:", ciphertext)
print("OFB plaintext:", plaintext)


# 4. GCM (Galois/Counter Mode)
# Преимущества:
# - Очень высокая безопасность благодаря встроенной аутентификации.
#   Защищает от атак с подменой данных (обеспечивает целостность).
# - Высокая производительность благодаря параллелизму.
# - Не требует дополнения данных до размера блока.
# - Широко используется в современных протоколах (например, TLS, IPsec).
#
# Недостатки:
# - Требует уникального nonce для каждого сообщения.
#   Повторение nonce может привести к компрометации безопасности.
# - Более сложен в реализации по сравнению с другими режимами.
# - Может быть чувствителен к ошибкам в реализации аутентификации.

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Генерация ключа и nonce
key = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(key)
nonce = urandom(12)

# Шифрование
ciphertext = aesgcm.encrypt(nonce, "Секретное сообщение".encode("utf-8"), None)

# Дешифрование
plaintext = aesgcm.decrypt(nonce, ciphertext, None)

print("GCM ciphertext:", ciphertext)
print("GCM plaintext:", plaintext)


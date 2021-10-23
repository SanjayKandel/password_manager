import random
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_password():
    choices = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()/\~`[]"
    rand_password = [random.choice(choices) for i in range(25)]
    rand_password = "".join(rand_password)
    return rand_password.encode()


def encrypt(master_key, user_password):
    # we will get this main pass form data base
    salt = b'\xd0O\xb3\xeb\xa7\x87\x8dg!\x93\xf7\\\xd5\xb0\x15\xd6'
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                     salt=salt, iterations=100000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
    f = Fernet(key)
    encrypted = f.encrypt(user_password)
    return encrypted


def decrypt(master_key, encrypted_pass):
    salt = b'\xd0O\xb3\xeb\xa7\x87\x8dg!\x93\xf7\\\xd5\xb0\x15\xd6'
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                     salt=salt, iterations=100000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_pass)
    return decrypted.decode()

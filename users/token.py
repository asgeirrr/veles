import base64
import hashlib
from functools import partial

from cryptography.fernet import Fernet


def hash_password(password):
    """
    The hash of the password is used to encrypt and decrypt the FIO token at runtime.
    """
    return base64.b64encode(hashlib.md5(password.encode('utf-8')).hexdigest().encode('utf-8'))


def encrypt_or_decrypt_token(token, password, method_name='encrypt'):
    """
    The FIO token is encrypted in the database for security reasons.
    This function can be used to either encrypt or decrypt the token using a given password.
    """
    fernet = Fernet(hash_password(password))
    return getattr(fernet, method_name)(token.encode('ascii'))

encrypt_token = partial(encrypt_or_decrypt_token, method_name='encrypt')
decrypt_token = partial(encrypt_or_decrypt_token, method_name='decrypt')

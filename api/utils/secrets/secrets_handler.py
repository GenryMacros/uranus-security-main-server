import base64
import hashlib
import secrets

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization as crypto_serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


class SecretsHandler:
    @classmethod
    def calculate_hash(cls, hash_data: str, salt: str) -> str:
        hasher = hashlib.sha256()
        hasher.update(hash_data.encode('utf-8'))
        hasher.update(salt.encode('utf-8'))
        return hasher.hexdigest()

    @classmethod
    def generate_new_key_pair(cls):
        key_pair = rsa.generate_private_key(
            backend=default_backend(),
            public_exponent=65537,
            key_size=512)
        private_key = key_pair.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption())

        public_key = key_pair.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH)
        return public_key, private_key

    @classmethod
    def is_signature_valid(cls, public_key: bytes, signature: bytes, message: bytes) -> bool:
        pubkey = crypto_serialization.load_ssh_public_key(
            public_key, backend=default_backend())
        try:
            pubkey.verify(
                base64.b64decode(signature),
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256())
            return True
        except InvalidSignature:
            return False

    @classmethod
    def generate_salt(cls):
        return secrets.token_hex(5)

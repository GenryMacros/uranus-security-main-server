import base64
import hashlib
import secrets

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Signature import PKCS1_v1_5
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme


class SecretsHandler:
    KEY_SIZE = 2048

    @classmethod
    def calculate_hash(cls, hash_data: str, salt: str) -> str:
        hasher = hashlib.sha256()
        hasher.update(hash_data.encode('utf-8'))
        hasher.update(salt.encode('utf-8'))
        return hasher.hexdigest()

    @classmethod
    def generate_new_key_pair(cls):
        random_generator = Random.new().read
        key = RSA.generate(cls.KEY_SIZE, random_generator)
        public_key = str(key.public_key().exportKey(format='PEM'), "utf-8") \
            .replace('-----BEGIN PUBLIC KEY-----', '') \
            .replace('-----END PUBLIC KEY-----', '') \
            .replace('\n', '').replace(' ', '')
        private_key = str(key.exportKey(format='PEM'), "utf-8")
        return public_key, private_key

    @classmethod
    def is_signature_valid(cls, public_key: str, signature: bytes, message: bytes) -> bool:
        pubkey_decoded = base64.b64decode(public_key)
        rsa_pubkey = RSA.importKey(pubkey_decoded)
        verifier = PKCS115_SigScheme(rsa_pubkey)
        msg_hash = SHA256.new(message)
        try:
            verifier.verify(msg_hash, signature)
            return True
        except:
            return False

    @classmethod
    def sign_message(cls, message: bytes, private_key: str) -> str:
        msg_hash = SHA256.new(message)
        rsa_private_key = RSA.importKey(private_key)
        signer = PKCS1_v1_5.new(rsa_private_key)
        sig = signer.sign(msg_hash)
        return base64.b64encode(sig).decode('utf-8')

    @classmethod
    def cut_public_key(cls, public_key: str) -> str:
        return public_key.replace('-----BEGIN PUBLIC KEY-----', '') \
            .replace('-----END PUBLIC KEY-----', '') \
            .replace('\n', '').replace(' ', '')

    @classmethod
    def cut_private_key(cls, private_key: str) -> str:
        return private_key.replace('-----BEGIN RSA PRIVATE KEY-----', '') \
            .replace('-----END RSA PRIVATE KEY-----', '') \
            .replace('\n', '').replace(' ', '')

    @classmethod
    def generate_salt(cls):
        return secrets.token_hex(5)

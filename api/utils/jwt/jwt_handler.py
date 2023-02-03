import base64
import time

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from api.utils.jwt.schemas.jwt_schemas import JwtHeader, JwtBody, RefreshBody
from api.utils.secrets.secrets_handler import SecretsHandler


class JwtHandler:
    JWT_EXPIRATION_TIME = 0.5 * 60 * 60
    REFRESH_EXPIRATION_TIME = 7 * 24 * 60 * 60

    @classmethod
    def generate_new_jwt_pair(cls, user_id: int, client_first_name: str,
                              client_last_name: str, client_private: bytes):
        new_jwt = cls.generate_jwt(user_id=user_id,
                                   client_private=client_private,
                                   client_first_name=client_first_name,
                                   client_last_name=client_last_name,
                                   is_refresh=False)
        new_refresh = cls.generate_jwt(user_id=user_id,
                                       client_private=client_private,
                                       client_first_name=client_first_name,
                                       client_last_name=client_last_name,
                                       is_refresh=True)
        return new_jwt, new_refresh

    @classmethod
    def generate_jwt(cls, user_id: int,
                     client_first_name: str,
                     client_last_name: str,
                     client_private: bytes, is_refresh=False):
        header = JwtHeader.Schema().dumps(JwtHeader())
        if not is_refresh:
            body = JwtBody.Schema().dumps(
                JwtBody(
                    id=user_id,
                    first_name=client_first_name,
                    last_name=client_last_name,
                    expiration_date=(time.time() + cls.JWT_EXPIRATION_TIME)
                )
            )
        else:
            body = RefreshBody.Schema().dumps(
                RefreshBody(
                    id=user_id,
                    expiration_date=(time.time() + cls.REFRESH_EXPIRATION_TIME)
                )
            )
        header_encode = base64.b64encode(header.encode('utf-8'))
        body_encode = base64.b64encode(body.encode('utf-8'))

        signature_hash = f"{header_encode}.{body_encode}".encode('utf-8')
        client_private = load_pem_private_key(client_private, password=None)
        signature = client_private.sign(
            signature_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256())

        header_encode = header_encode.decode("utf-8")
        body_encode = body_encode.decode("utf-8")
        signature = base64.b64encode(signature).decode("utf-8")
        return f"{header_encode}.{str(body_encode)}.{str(signature)}"

    @classmethod
    def is_token_valid(cls, token: str, client_public_key: bytes):
        jwt_header, jwt_body, signature = token.split('.')
        pre_signed_message = f"{jwt_header.encode('utf-8')}.{jwt_body.encode('utf-8')}".encode('utf-8')
        is_signature_valid = SecretsHandler.is_signature_valid(
            public_key=client_public_key,
            signature=signature,
            message=pre_signed_message
        )
        return is_signature_valid

    @classmethod
    def retrieve_body_info_from_token_jwt(cls, token: str) -> JwtBody:
        jwt_header, jwt_body, signature = token.split('.')
        jwt_body = base64.b64decode(jwt_body).decode('utf-8')
        return JwtBody.Schema().loads(base64.b64decode(jwt_body).decode('utf-8'))

    @classmethod
    def retrieve_body_info_from_token_refresh(cls, token: str) -> RefreshBody:
        jwt_header, jwt_body, signature = token.split('.')
        jwt_body = base64.b64decode(jwt_body).decode('utf-8')
        return RefreshBody.Schema().loads(base64.b64decode(jwt_body).decode('utf-8'))

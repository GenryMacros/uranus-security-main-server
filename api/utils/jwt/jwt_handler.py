import base64
import time
from typing import Tuple

from api.utils.jwt.schemas.jwt_schemas import JwtHeader, JwtBody, RefreshBody
from api.utils.secrets.secrets_handler import SecretsHandler


class JwtHandler:
    JWT_EXPIRATION_TIME = 0.5 * 60 * 60
    REFRESH_EXPIRATION_TIME = 7 * 24 * 60 * 60

    @classmethod
    def generate_new_jwt_pair(cls, user_id: int, client_email: str, client_private: str) -> Tuple[str, str]:
        new_jwt = cls.generate_jwt(user_id=user_id,
                                   client_private=client_private,
                                   client_email=client_email,
                                   is_refresh=False)
        new_refresh = cls.generate_jwt(user_id=user_id,
                                       client_private=client_private,
                                       client_email=client_email,
                                       is_refresh=True)
        return new_jwt, new_refresh

    @classmethod
    def generate_jwt(cls, user_id: int,
                     client_private: str,
                     client_email: str,
                     is_refresh=False) -> str:
        header = JwtHeader.dumps(JwtHeader())
        if not is_refresh:
            body = JwtBody.dumps(
                JwtBody(
                    id=user_id,
                    email=client_email,
                    expiration_date=(time.time() + cls.JWT_EXPIRATION_TIME)
                )
            )
        else:
            body = RefreshBody.dumps(
                RefreshBody(
                    id=user_id,
                    expiration_date=(time.time() + cls.REFRESH_EXPIRATION_TIME)
                )
            )
        header_encode = base64.b64encode(header.encode('utf-8'))
        body_encode = base64.b64encode(body.encode('utf-8'))

        signature_hash = f"{header_encode}.{body_encode}".encode('utf-8')
        signature = SecretsHandler.sign_message(signature_hash, client_private)

        header_encode = header_encode.decode("utf-8")
        body_encode = body_encode.decode("utf-8")
        signature = base64.b64encode(signature).decode("utf-8")
        return f"{header_encode}.{str(body_encode)}.{str(signature)}"

    @classmethod
    def is_token_valid(cls, token: str, client_public_key: str) -> bool:
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
        return JwtBody.load(base64.b64decode(jwt_body).decode('utf-8'))

    @classmethod
    def retrieve_body_info_from_token_refresh(cls, token: str) -> RefreshBody:
        jwt_header, jwt_body, signature = token.split('.')
        jwt_body = base64.b64decode(jwt_body).decode('utf-8')
        return RefreshBody.load(base64.b64decode(jwt_body).decode('utf-8'))

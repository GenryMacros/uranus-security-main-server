import time

from api.exceptions.clients.exceptions import InvalidTokens, TokenIsExpired, InvalidCredentials, SignupFailed
from api.repositories.clients.clients_repository import ClientRepositoryInterface
from api.schemas.clients.clients_schemas import ClientCredentials, ClientSignup, ClientContactSchema, \
    ClientSecretSchema, ClientTokenRefresh, LoginResponse, ClientLocationSchema, ClientPersonalDataSchema
from api.utils.jwt.jwt_handler import JwtHandler
from api.utils.secrets.secrets_handler import SecretsHandler


class ClientService:

    def __init__(self, user_repository: ClientRepositoryInterface):
        self.user_repository = user_repository

    def login(self, credentials: ClientCredentials) -> LoginResponse:
        client = self.user_repository.get_client_by_username(credentials.login)
        client_pass_data = self.user_repository.get_client_password_data(client.id)
        credentials_password_hash = SecretsHandler.calculate_hash(credentials.password, client_pass_data.password_salt)
        if client_pass_data.password_hash != credentials_password_hash:
            raise InvalidCredentials()
        new_public_key, new_private_key = SecretsHandler.generate_new_key_pair()
        self.user_repository.update_secret(client.id, new_public_key, new_private_key)
        client_personal_data = self.user_repository.get_personal_data_by_id(client.id)
        new_jwt, new_refresh = JwtHandler.generate_new_jwt_pair(user_id=client.id,
                                                                client_first_name=client_personal_data.user_first_name,
                                                                client_last_name=client_personal_data.user_last_name,
                                                                client_private=new_private_key)
        return LoginResponse(
            id=client.id,
            public_key=new_public_key,
            auth_token=new_jwt,
            refresh_token=new_refresh,
        )

    def signup(self, signup_data: ClientSignup) -> None:
        new_client = None
        try:
            new_client = self.user_repository.add_new_client(signup_data.username)
            self.user_repository.add_new_client_personal_data(client_id=new_client.id,
                                                              first_name=signup_data.first_name,
                                                              last_name=signup_data.last_name)
            client_contact_schema = ClientContactSchema(email=signup_data.email,
                                                        phone=signup_data.phone,
                                                        telegram=signup_data.telegram)
            self.user_repository.add_new_client_contact(client_id=new_client.id,
                                                        client_contact=client_contact_schema)
            password_salt = SecretsHandler.generate_salt()
            pass_hash = SecretsHandler.calculate_hash(
                hash_data=signup_data.password,
                salt=password_salt
            )
            client_public, client_private = SecretsHandler.generate_new_key_pair()
            client_secret_schema = ClientSecretSchema(
                password_hash=pass_hash,
                password_salt=password_salt,
                user_private=client_private,
                user_public=client_public
            )
            self.user_repository.add_new_client_secret(client_id=new_client.id,
                                                       client_secret=client_secret_schema)
        except Exception as e:
            print(e)
            if new_client is not None:
                self.user_repository.delete_client(new_client.id)
            raise SignupFailed()

    def refresh_jwt(self, refresh_data: ClientTokenRefresh) -> ClientTokenRefresh:
        public, private = self.user_repository.get_client_keys(refresh_data.user_id)
        is_jwt_signature_valid = JwtHandler.is_token_valid(refresh_data.jwt, public)
        if not is_jwt_signature_valid:
            raise InvalidTokens()
        else:
            refresh_body_info = JwtHandler.retrieve_body_info_from_token_refresh(refresh_data.refresh)
            is_refresh_signature_valid = JwtHandler.is_token_valid(refresh_data.refresh, public)
            if not is_refresh_signature_valid:
                raise InvalidTokens()
            if refresh_body_info.expiration_date <= time.time():
                raise TokenIsExpired()

            jwt_body_info = JwtHandler.retrieve_body_info_from_token_jwt(refresh_data.jwt)
            new_jwt = JwtHandler.generate_jwt(
                user_id=jwt_body_info.id,
                client_first_name=jwt_body_info.last_name,
                client_last_name=jwt_body_info.last_name,
                client_private=private
            )
            return ClientTokenRefresh(
                user_id=refresh_data.user_id,
                jwt=new_jwt,
                refresh=refresh_data.refresh
            )

    def get_location_data(self, auth_data: str, client_id: int) -> ClientLocationSchema:
        token = auth_data[7:]
        self.check_token(token, client_id)
        client_location = self.user_repository.get_location_by_id(client_id)
        return ClientLocationSchema(
            country=client_location.country,
            city=client_location.city,
            addr=client_location.addr,
            ind=client_location.ind
        )

    def get_personal_data(self, auth_data: str, client_id: int) -> ClientPersonalDataSchema:
        token = auth_data[7:]
        self.check_token(token, client_id)
        client_data = self.user_repository.get_personal_data_by_id(client_id)
        return ClientPersonalDataSchema(
            user_first_name=client_data.user_first_name,
            user_last_name=client_data.user_last_name
        )

    def get_contact(self, auth_data: str, client_id: int) -> ClientContactSchema:
        token = auth_data[7:]
        self.check_token(token, client_id)
        client_contact = self.user_repository.get_contact_by_id(client_id)
        return ClientContactSchema(
            email=client_contact.email,
            phone=client_contact.phone,
            telegram=client_contact.telegram
        )

    def check_token(self, token: str, client_id: int):
        public = self.user_repository.get_client_public_key(client_id)
        is_token_signature_valid = JwtHandler.is_token_valid(token, public)
        if not is_token_signature_valid:
            raise InvalidTokens()
        token_body_info = JwtHandler.retrieve_body_info_from_token_jwt(token)
        if token_body_info.expiration_date <= time.time():
            raise TokenIsExpired()

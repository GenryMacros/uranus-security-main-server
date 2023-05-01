import enum
import time

from api.exceptions.clients.exceptions import InvalidTokens, TokenIsExpired, InvalidCredentials, SignupFailed, \
    TokenIsInvalid
from api.repositories.clients.clients_repository import ClientRepositoryInterface
from api.schemas.clients.clients_input import ClientCredentials, ClientSignup, ClientTokenRefresh
from api.schemas.clients.clients_output import LoginResponse, ClientSecretSchema, ClientLocationSchema, \
    ClientContactSchema, ClientsSignupResponse
from api.services.clients.clients_confirmator import ClientsConfirmator
from api.utils.jwt.jwt_handler import JwtHandler
from api.utils.secrets.secrets_handler import SecretsHandler


class ConfirmationMethod(enum.Enum):
    LINK = 0,
    SHORT_CODE = 1


class ClientService:
    TOKEN_EXPIRATION = 60 * 30

    def __init__(self, clients_repository: ClientRepositoryInterface):
        self.clients_repository = clients_repository
        self.confirmator = ClientsConfirmator()
        self.confirmation_method = ConfirmationMethod.SHORT_CODE

    def login(self, credentials: ClientCredentials) -> LoginResponse:
        client = self.clients_repository.get_client_by_username(credentials.username)
        client_pass_data = self.clients_repository.get_client_password_data(client.id)
        credentials_password_hash = SecretsHandler.calculate_hash(credentials.password, client_pass_data.password_salt)
        if client_pass_data.password_hash != credentials_password_hash:
            raise InvalidCredentials()
        new_public_key, new_private_key = SecretsHandler.generate_new_key_pair()
        self.clients_repository.update_secret(client.id, new_public_key, new_private_key)
        new_jwt, new_refresh = JwtHandler.generate_new_jwt_pair(user_id=client.id,
                                                                client_email=client.email,
                                                                client_private=new_private_key)
        return LoginResponse(
            id=client.id,
            public_key=SecretsHandler.cut_public_key(new_public_key),
            auth_token=new_jwt,
            refresh_token=new_refresh,
        )

    def signup(self, signup_data: ClientSignup) -> ClientsSignupResponse:
        new_client = None
        try:
            current_time = str(int(time.time()))
            new_client = self.clients_repository.add_new_client(signup_data.username,
                                                                signup_data.email,
                                                                current_time)
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
            self.clients_repository.add_new_client_secret(client_id=new_client.id,
                                                          client_secret=client_secret_schema,
                                                          password=signup_data.password)
            confirmation_token = self.__generate_confirmation_token(signup_data, new_client.id)
            self.confirmator.send_email_confirmation(confirmation_token, signup_data.email,
                                                     confirmation_method=self.confirmation_method)
            return ClientsSignupResponse(True, new_client.id)
        except Exception as e:
            if new_client is not None:
                self.clients_repository.delete_client(new_client.id)
            raise SignupFailed()

    def __generate_confirmation_token(self, signup_data: ClientSignup, client_id: int) -> str:
        if self.confirmation_method == ConfirmationMethod.SHORT_CODE:
            code = SecretsHandler.generate_salt(len_in_bytes=2)
            expiration_date = int(time.time()) + self.TOKEN_EXPIRATION
            self.clients_repository.add_confirmation_data(client_id, code, str(expiration_date))
            return code
        elif self.confirmation_method == ConfirmationMethod.LINK:
            return SecretsHandler.generate_temp_auth_token(signup_data.email,
                                                           self.clients_repository.get_client_public_key(1))
        else:
            raise NotImplementedError()

    def refresh_jwt(self, refresh_data: ClientTokenRefresh) -> ClientTokenRefresh:
        public, private = self.clients_repository.get_client_keys(refresh_data.user_id)
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
                client_email=jwt_body_info.email,
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
        client_location = self.clients_repository.get_location_by_id(client_id)
        return ClientLocationSchema(
            country=client_location.country,
            city=client_location.city,
            addr=client_location.addr,
            ind=client_location.ind
        )

    def get_contact(self, auth_data: str, client_id: int) -> ClientContactSchema:
        token = auth_data[7:]
        self.check_jwt_token(token, client_id)
        client_contact = self.clients_repository.get_contact_by_id(client_id)
        return ClientContactSchema(
            email=client_contact.email,
            phone=client_contact.phone,
            telegram=client_contact.telegram
        )

    def check_jwt_token(self, token: str, client_id: int) -> None:
        public = self.clients_repository.get_client_public_key(client_id)
        is_token_signature_valid = JwtHandler.is_token_valid(token, public)
        if not is_token_signature_valid:
            raise InvalidTokens()
        token_body_info = JwtHandler.retrieve_body_info_from_token_jwt(token)
        if token_body_info.expiration_date <= time.time():
            raise TokenIsExpired()

    def confirm_signup(self, confirmation_token: str, client_id: int) -> LoginResponse:
        if self.confirmation_method == ConfirmationMethod.LINK:
            self.__confirm_signup_link(confirmation_token)
        elif self.confirmation_method == ConfirmationMethod.SHORT_CODE:
            self.__confirm_signup_code(confirmation_token, client_id)
        else:
            raise NotImplementedError()

        self.clients_repository.set_as_confirmed_by_id(client_id)
        client_data = self.clients_repository.get_client_by_id(client_id)
        client_keys = self.clients_repository.get_client_keys(client_id)
        client_jwt, client_refresh = JwtHandler.generate_new_jwt_pair(client_id,
                                                                      client_data.email,
                                                                      client_keys[1])
        return LoginResponse(id=int(client_id),
                             public_key=SecretsHandler.cut_public_key(client_keys[0]),
                             auth_token=client_jwt,
                             refresh_token=client_refresh)

    def __confirm_signup_link(self, token: str):
        user_public_key = self.clients_repository.get_client_public_key(1)
        encoded_email = SecretsHandler.deserialize_token(token, user_public_key)
        client = self.clients_repository.get_client_by_email(encoded_email)
        if client is None:
            raise TokenIsInvalid()

    def __confirm_signup_code(self, token: str, client_id: int):
        conf_data = self.clients_repository.get_confirmation_data_by_id(client_id)
        conf_data_expiration = int(conf_data.expiration_date)
        if token != conf_data.confirmation_code:
            raise TokenIsInvalid()
        elif time.time() > conf_data_expiration:
            self.clients_repository.remove_confirmation_data(client_id)
            raise TokenIsExpired()
        self.clients_repository.remove_confirmation_data(client_id)

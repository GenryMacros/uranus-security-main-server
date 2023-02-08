from typing import Tuple

from api.exceptions.clients.exceptions import InvalidCredentials, ClientNotFound

from api.models.clients.clients_models import ClientSecret, Client, ClientPersonalData, ClientContact, ClientLocation
from api.repositories.clients.clients_data_verifier import ClientsDataVerifier
from api.repositories.db.mysql_db_context import AppDBConf
from api.schemas.clients.clients_schemas import ClientPasswordData, ClientContactSchema, ClientSecretSchema


class ClientRepositoryInterface:
    def get_client_by_username(self, username: str) -> Client:
        return None

    def get_client_by_id(self, client_id: int) -> Client:
        return None

    def get_personal_data_by_id(self, client_id: int) -> ClientPersonalData:
        return None

    def get_contact_by_id(self, client_id: int) -> ClientContact:
        return None

    def get_client_password_data(self, client_id: int) -> ClientPasswordData:
        return None

    def get_client_keys(self, client_id: int) -> Tuple[str, str]:
        return None

    def get_client_public_key(self, client_id: int) -> str:
        return None

    def get_location_by_id(self, client_id: int) -> ClientLocation:
        return None

    def update_secret(self, client_id: int, new_public_key: str, new_private_key: str) -> None:
        return None

    def add_new_client(self, username: str) -> Client:
        return None

    def add_new_client_personal_data(self, client_id: int,
                                     first_name: str, last_name: str) -> ClientPersonalData:
        return None

    def add_new_client_contact(self, client_id: int, client_contact: ClientContactSchema) -> ClientContact:
        return None

    def add_new_client_secret(self, client_id: int, client_secret: ClientSecretSchema, password: str) -> ClientSecret:
        return None

    def delete_client(self, client_id) -> None:
        return


class ClientRepository(ClientRepositoryInterface):

    def __init__(self, db_context=AppDBConf.DB_SESSION):
        self.db_context = db_context
        self.data_verifier = ClientsDataVerifier()

    def get_client_by_username(self, username: str) -> Client:
        self.data_verifier.verify_login(username)

        client = self.db_context.query(Client).filter(Client.username == username).first()
        if client is None:
            raise InvalidCredentials()
        return client

    def get_client_by_id(self, client_id: int) -> Client:
        client = self.db_context.query(Client).filter(Client.id == client_id).first()
        if client is None:
            raise ClientNotFound()
        return client

    def get_personal_data_by_id(self, client_id: int) -> ClientPersonalData:
        client_personal_data = self.db_context.query(ClientPersonalData).filter(ClientPersonalData.id == client_id).first()
        if client_personal_data is None:
            raise ClientNotFound()
        return client_personal_data

    def get_contact_by_id(self, client_id: int) -> ClientContact:
        client_contact = self.db_context.query(ClientContact).filter(ClientContact.id == client_id).first()
        if client_contact is None:
            raise ClientNotFound()
        return client_contact

    def get_client_password_data(self, client_id: int) -> ClientPasswordData:
        pass_data = self.db_context.query(ClientSecret).filter(ClientSecret.client_id == client_id).first()
        if pass_data is None:
            raise ClientNotFound()
        return ClientPasswordData(password_hash=pass_data.password_hash,
                                  password_salt=pass_data.password_salt)

    def get_client_keys(self, client_id: int) -> Tuple[str, str]:
        pass_data = self.db_context.query(ClientSecret).filter(ClientSecret.client_id == client_id).first()
        if pass_data is None:
            raise ClientNotFound()
        return pass_data.user_public, pass_data.user_private

    def get_client_public_key(self, client_id: int) -> str:
        pass_data = self.db_context.query(ClientSecret).filter(ClientSecret.client_id == client_id).first()
        if pass_data is None:
            raise ClientNotFound()
        return pass_data.user_public

    def get_client_location_data(self, client_id: int) -> ClientLocation:
        location_data = self.db_context.query(ClientLocation).filter(ClientLocation.client_id == client_id).first()
        if location_data is None:
            raise ClientNotFound()
        return location_data

    def update_secret(self, client_id: int, new_public_key: str, new_private_key: str) -> None:
        self.db_context.query(ClientSecret).filter(ClientSecret.client_id == client_id).update(
            {
                ClientSecret.user_private: new_private_key,
                ClientSecret.user_public: new_public_key
             },
            synchronize_session='fetch'
        )
        self.db_context.commit()

    def add_new_client(self, username: str) -> Client:
        self.data_verifier.verify_login(username)

        new_client = Client(
            username=username,
            is_deleted=False
        )
        self.db_context.add(new_client)
        self.db_context.commit()
        self.db_context.refresh(new_client)
        return new_client

    def add_new_client_personal_data(self, client_id: int,
                                     first_name: str, last_name: str) -> ClientPersonalData:
        self.data_verifier.verify_first_name(first_name)
        self.data_verifier.verify_last_name(last_name)

        new_client_personal = ClientPersonalData(
            client_id=client_id,
            user_first_name=first_name,
            user_last_name=last_name
        )
        self.db_context.add(new_client_personal)
        self.db_context.commit()
        self.db_context.refresh(new_client_personal)
        return new_client_personal

    def add_new_client_contact(self, client_id: int, client_contact_schema: ClientContactSchema) -> ClientContact:
        self.data_verifier.verify_contact(client_contact_schema)

        client_contact = ClientContact(
            client_id=client_id,
            email=client_contact_schema.email,
            phone=client_contact_schema.phone,
            telegram=client_contact_schema.telegram
        )
        self.db_context.add(client_contact)
        self.db_context.commit()
        self.db_context.refresh(client_contact)
        return client_contact

    def add_new_client_secret(self, client_id: int, client_secret: ClientSecretSchema, password: str) -> ClientSecret:
        self.data_verifier.verify_password(password)

        new_client_secret = ClientSecret(
            client_id=client_id,
            password_hash=client_secret.password_hash,
            password_salt=client_secret.password_salt,
            user_private=client_secret.user_private,
            user_public=client_secret.user_public
        )
        self.db_context.add(new_client_secret)
        self.db_context.commit()
        self.db_context.refresh(new_client_secret)
        return new_client_secret

    def delete_client(self, client_id) -> None:
        self.db_context.query(Client).filter(Client.id == client_id).delete()
        self.db_context.commit()

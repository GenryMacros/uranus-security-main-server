from typing import Tuple

from api.exceptions.clients.exceptions import InvalidCredentials, ClientNotFound, TokenIsInvalid

from api.models.clients.clients_models import ClientsSecrets, Clients, ClientsAdditionalContacts, ClientsLocations, \
    ClientsConfirmations
from api.repositories.clients.interfaces.iclients_repository import ClientRepositoryInterface
from api.repositories.db.mysql_db_context import AppDBConf
from api.schemas.clients.clients_output import ClientContactSchema, ClientSecretSchema
from api.schemas.clients.clients_schemas import ClientPasswordData


class ClientRepository(ClientRepositoryInterface):

    def __init__(self, db_context=AppDBConf.DB_SESSION):
        self.db_context = db_context

    def get_client_by_username(self, username: str) -> Clients:
        client = self.db_context.query(Clients).filter(Clients.username == username).first()
        if client is None:
            raise InvalidCredentials()
        return client

    def get_client_by_id(self, client_id: int) -> Clients:
        client = self.db_context.query(Clients).filter(Clients.id == client_id).first()
        if client is None:
            raise ClientNotFound()
        return client

    def get_contact_by_id(self, client_id: int) -> ClientsAdditionalContacts:
        client_contact = self.db_context.query(ClientsAdditionalContacts)\
            .filter(ClientsAdditionalContacts.id == client_id).first()
        if client_contact is None:
            raise ClientNotFound()
        return client_contact

    def get_client_password_data(self, client_id: int) -> ClientPasswordData:
        pass_data = self.db_context.query(ClientsSecrets).filter(ClientsSecrets.client_id == client_id).first()
        if pass_data is None:
            raise ClientNotFound()
        return ClientPasswordData(password_hash=pass_data.password_hash,
                                  password_salt=pass_data.password_salt)

    def get_client_keys(self, client_id: int) -> Tuple[str, str]:
        pass_data = self.db_context.query(ClientsSecrets).filter(ClientsSecrets.client_id == client_id).first()
        if pass_data is None:
            raise ClientNotFound()
        return pass_data.user_public, pass_data.user_private

    def get_client_public_key(self, client_id: int) -> str:
        pass_data = self.db_context.query(ClientsSecrets).filter(ClientsSecrets.client_id == client_id).first()
        if pass_data is None:
            raise ClientNotFound()
        return pass_data.user_public

    def get_client_by_email(self, email: str) -> Clients:
        client = self.db_context.query(Clients).filter(Clients.email == email).first()
        if client is None:
            raise ClientNotFound()
        return client

    def set_as_confirmed_by_id(self, client_id: int) -> None:
        self.db_context.query(Clients).filter(Clients.id == client_id).update(
            {
                Clients.is_confirmed: True
            }
        )
        self.db_context.commit()

    def get_client_location_data(self, client_id: int) -> ClientsLocations:
        location_data = self.db_context.query(ClientsLocations).filter(ClientsLocations.client_id == client_id).first()
        if location_data is None:
            raise ClientNotFound()
        return location_data

    def update_secret(self, client_id: int, new_public_key: str, new_private_key: str) -> None:
        self.db_context.query(ClientsSecrets).filter(ClientsSecrets.client_id == client_id).update(
            {
                ClientsSecrets.user_private: new_private_key,
                ClientsSecrets.user_public: new_public_key
             },
            synchronize_session='fetch'
        )
        self.db_context.commit()

    def add_new_client(self, username: str, email: str, signup_date: str) -> Clients:

        new_client = Clients(
            username=username,
            email=email,
            is_deleted=False,
            is_confirmed=False,
            signup_date=signup_date
        )
        self.db_context.add(new_client)
        self.db_context.commit()
        self.db_context.refresh(new_client)
        return new_client

    def add_new_client_contact(self, client_id: int, client_contact_schema: ClientContactSchema) -> ClientsAdditionalContacts:
        client_contact = ClientsAdditionalContacts(
            client_id=client_id,
            phone=client_contact_schema.phone,
            telegram=client_contact_schema.telegram
        )
        self.db_context.add(client_contact)
        self.db_context.commit()
        self.db_context.refresh(client_contact)
        return client_contact

    def add_new_client_secret(self, client_id: int, client_secret: ClientSecretSchema, password: str) -> ClientsSecrets:

        new_client_secret = ClientsSecrets(
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

    def add_confirmation_data(self, client_id: int, code: str, expiration_date: str) -> None:
        client_contact = ClientsConfirmations(
            client_id=client_id,
            confirmation_code=code,
            expiration_date=expiration_date
        )
        self.db_context.add(client_contact)
        self.db_context.commit()

    def get_confirmation_data_by_id(self, client_id: int) -> ClientsConfirmations:
        conf_data = self.db_context.query(ClientsConfirmations).filter(ClientsConfirmations.client_id == client_id).first()
        if conf_data is None:
            raise TokenIsInvalid()
        return conf_data

    def remove_confirmation_data(self, client_id: int) -> None:
        self.db_context.query(ClientsConfirmations).filter(ClientsConfirmations.client_id == client_id).delete()
        self.db_context.commit()

    def delete_client(self, client_id) -> None:
        self.db_context.query(Clients).filter(Clients.id == client_id).delete()
        self.db_context.commit()

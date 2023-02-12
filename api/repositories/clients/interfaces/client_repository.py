from typing import Tuple


from api.models.clients.clients_models import ClientsSecrets, Clients, ClientsAdditionalContacts, ClientsLocations
from api.schemas.clients.clients_output_schemas import ClientSecretSchema, ClientContactSchema
from api.schemas.clients.clients_schemas import ClientPasswordData


class ClientRepositoryInterface:
    def get_client_by_username(self, username: str) -> Clients:
        return Clients()

    def get_client_by_id(self, client_id: int) -> Clients:
        return Clients()

    def get_contact_by_id(self, client_id: int) -> ClientsAdditionalContacts:
        return ClientsAdditionalContacts()

    def get_client_password_data(self, client_id: int) -> ClientPasswordData:
        return ClientPasswordData()

    def get_client_keys(self, client_id: int) -> Tuple[str, str]:
        return "", ""

    def get_client_public_key(self, client_id: int) -> str:
        return ""

    def get_client_by_email(self, email: str) -> Clients:
        return None

    def set_as_confirmed_by_id(self, client_id: int) -> None:
        return None

    def get_location_by_id(self, client_id: int) -> ClientsLocations:
        return ClientsLocations()

    def update_secret(self, client_id: int, new_public_key: str, new_private_key: str) -> None:
        return None

    def add_new_client(self, username: str, email: str) -> Clients:
        return Clients()

    def add_new_client_contact(self, client_id: int, client_contact: ClientContactSchema) -> ClientsAdditionalContacts:
        return ClientsAdditionalContacts()

    def add_new_client_secret(self, client_id: int, client_secret: ClientSecretSchema, password: str) -> ClientsSecrets:
        return ClientsSecrets()

    def delete_client(self, client_id) -> None:
        return

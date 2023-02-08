from typing import Tuple


from api.models.clients.clients_models import ClientSecret, Client, ClientPersonalData, ClientContact, ClientLocation
from api.schemas.clients.clients_schemas import ClientPasswordData, ClientContactSchema, ClientSecretSchema


class ClientRepositoryInterface:
    def get_client_by_username(self, username: str) -> Client:
        return Client()

    def get_client_by_id(self, client_id: int) -> Client:
        return Client()

    def get_personal_data_by_id(self, client_id: int) -> ClientPersonalData:
        return ClientPersonalData()

    def get_contact_by_id(self, client_id: int) -> ClientContact:
        return ClientContact()

    def get_client_password_data(self, client_id: int) -> ClientPasswordData:
        return ClientPasswordData()

    def get_client_keys(self, client_id: int) -> Tuple[str, str]:
        return "", ""

    def get_client_public_key(self, client_id: int) -> str:
        return ""

    def get_location_by_id(self, client_id: int) -> ClientLocation:
        return ClientLocation()

    def update_secret(self, client_id: int, new_public_key: str, new_private_key: str) -> None:
        return None

    def add_new_client(self, username: str) -> Client:
        return Client()

    def add_new_client_personal_data(self, client_id: int,
                                     first_name: str, last_name: str) -> ClientPersonalData:
        return ClientPersonalData()

    def add_new_client_contact(self, client_id: int, client_contact: ClientContactSchema) -> ClientContact:
        return ClientContact()

    def add_new_client_secret(self, client_id: int, client_secret: ClientSecretSchema, password: str) -> ClientSecret:
        return ClientSecret()

    def delete_client(self, client_id) -> None:
        return

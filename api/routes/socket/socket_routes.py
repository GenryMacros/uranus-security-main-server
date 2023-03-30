from flask import Blueprint
from flask import request

from api.repositories.clients.clients_repository import ClientRepository
from api.schemas.clients.clients_input_schemas import ClientCredentials, ClientSignup, ClientTokenRefresh
from api.schemas.clients.clients_output_schemas import LoginResponse
from api.services.clients.clients_services import ClientService


socket_blueprint = Blueprint("socket_blueprint", __name__)
client_service = ClientService(ClientRepository())


@socket_blueprint.route('/socket/check_creds', methods=['POST'])
def login():
    request_data: ClientCredentials = ClientCredentials.load(request.get_json())

    response: LoginResponse = client_service.login(request_data)

    header = {'Content-Type': 'application/json'}
    return LoginResponse.dump(response), 200, header


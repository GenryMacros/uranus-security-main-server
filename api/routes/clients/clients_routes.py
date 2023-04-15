from flask import Blueprint
from flask import request

from api.repositories.clients.clients_repository import ClientRepository
from api.schemas.clients.clients_input import ClientCredentials, ClientSignup, ClientTokenRefresh
from api.schemas.clients.clients_output import LoginResponse
from api.schemas.default_response import DefaultResponse
from api.services.clients.clients_services import ClientService


users_blueprint = Blueprint("users_blueprint", __name__)
client_service = ClientService(ClientRepository())


@users_blueprint.route('/', methods=['GET'])
def check():
    return DefaultResponse(success=True).dump(), 200


@users_blueprint.route('/clients/login', methods=['POST'])
def login():
    request_data: ClientCredentials = ClientCredentials.load(request.get_json())

    response: LoginResponse = client_service.login(request_data)

    header = {'Content-Type': 'application/json'}
    return LoginResponse.dump(response), 200, header


@users_blueprint.route('/clients/signup', methods=['POST'])
def signup():
    request_data: ClientSignup = ClientSignup.load(request.get_json())

    response = client_service.signup(request_data)

    return response.dump(), 200


@users_blueprint.route('/clients/confirm', methods=['GET'])
def confirm():
    confirmation_token = request.args.get("token", None)
    client_id = int(request.args.get("id", None))

    response = client_service.confirm_signup(confirmation_token, client_id)
    header = {'Content-Type': 'application/json'}
    return response.dump(), 200, header


@users_blueprint.route('/clients/check_token', methods=['POST'])
def check_token():
    request_data: ClientCredentials = ClientCredentials.load(request.get_json())

    response: LoginResponse = client_service.login(request_data)

    header = {'Content-Type': 'application/json'}
    return LoginResponse.dump(response), 200, header


@users_blueprint.route('/clients/refresh', methods=['POST'])
def refresh_client_jwt():
    request_data: ClientTokenRefresh = ClientTokenRefresh.load(request.get_json())

    refresh_response = client_service.refresh_jwt(request_data)

    header = {'Content-Type': 'application/json'}
    return refresh_response.dump(), 200, header


@users_blueprint.route('/clients/location', methods=['GET'])
def get_client_location():
    authorization = request.headers.get("Authorization")
    client_id = request.args.get("client_id", None)

    if client_id is None:
        return "", 403, {'Content-Type': 'application/json'}
    client_location = client_service.get_location_data(authorization, int(client_id))

    header = {'Content-Type': 'application/json'}
    return client_location.dump(), 200, header


@users_blueprint.route('/clients/contact', methods=['GET'])
def get_client_contact():
    authorization = request.headers.get("Authorization")
    client_id = request.args.get("client_id", None)

    if client_id is None:
        return "", 403, {'Content-Type': 'application/json'}
    client_contact = client_service.get_contact(authorization, int(client_id))

    header = {'Content-Type': 'application/json'}
    return client_contact.dump(), 200, header

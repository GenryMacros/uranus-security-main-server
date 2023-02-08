from flask import Blueprint, jsonify
from flask import request

from api.repositories.clients.clients_repository import ClientRepository
from api.schemas.clients.clients_schemas import ClientCredentials, LoginResponse, ClientSignup, ClientTokenRefresh, \
    ClientLocationSchema, ClientContactSchema
from api.services.clients.clients_services import ClientService


logging_blueprint = Blueprint("logging_blueprint", __name__)
client_service = ClientService(ClientRepository())


@logging_blueprint.route('/users/login', methods=['POST'])
def login():
    request_data: ClientCredentials = ClientCredentials.Schema().load(request.get_json())

    response: LoginResponse = client_service.login(request_data)
    header = {'Content-Type': 'application/json'}
    return LoginResponse.Schema().dump(response), 200, header


@logging_blueprint.route('/users/register', methods=['POST'])
def register():
    request_data: ClientSignup = ClientSignup.Schema().load(request.get_json())
    client_service.signup(request_data)
    return jsonify({"success": True}), 200


@logging_blueprint.route('/users/refresh', methods=['POST'])
def refresh_client_jwt():
    request_data: ClientTokenRefresh = ClientTokenRefresh.Schema().load(request.get_json())
    refresh_response = client_service.refresh_jwt(request_data)
    header = {'Content-Type': 'application/json'}
    return ClientTokenRefresh.Schema().dump(refresh_response), 200, header


@logging_blueprint.route('/users/location', methods=['GET'])
def get_client_location():
    authorization = request.headers.get("Authorization")
    client_id = request.args.get("client_id", 0)
    client_location = client_service.get_location_data(authorization, client_id)
    header = {'Content-Type': 'application/json'}
    return ClientLocationSchema.Schema().dump(client_location), 200, header


@logging_blueprint.route('/users/contact', methods=['GET'])
def get_client_contact():
    authorization = request.headers.get("Authorization")
    client_id = request.args.get("client_id", 0)
    client_contact = client_service.get_contact(authorization, client_id)
    header = {'Content-Type': 'application/json'}
    return ClientContactSchema.Schema().dump(client_contact), 200, header

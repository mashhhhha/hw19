from flask import request, abort
from flask_restx import Namespace, Resource
from implemented import user_service
from service.auth import generate_tokens, approve_refresh_token

auth_ns = Namespace('/auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json

        username = req_json.get('username')
        password = req_json.get('password')
        role = req_json.get('role')

        if None in [username, password, role]:
            abort(401)

        tokens = generate_tokens(username, password, role)

        return tokens, 200

    def put(self):
        req_json = request.json

        refresh_token = req_json.get('refresh_token')

        tokens = approve_refresh_token(refresh_token)

        return tokens

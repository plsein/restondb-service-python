
from auth.auth import Auth
from services.service import Service
from flask_jwt_extended import jwt_required


class Routes:

    @classmethod
    def config(cls, app):

        @app.route("/")
        def index():
            return Service.index()

        @app.route("/oauth/token", methods=['POST'])
        def token():
            return Auth.oauth_token()

        @app.route("/graphql", methods=['POST'])
        @jwt_required()
        def graphql():
            return Service.graphql()

        @app.route("/api/select", methods=['POST'])
        @jwt_required()
        def select():
            return Service.select()

        @app.route("/api/add", methods=['POST'])
        @jwt_required()
        def add():
            return Service.add()

        @app.route("/api/edit", methods=['POST'])
        @jwt_required()
        def edit():
            return Service.edit()

        @app.route("/api/update", methods=['POST'])
        @jwt_required()
        def update():
            return Service.update()

        @app.route("/api/delete", methods=['POST'])
        @jwt_required()
        def delete():
            return Service.delete()

        @app.route("/api/remove", methods=['POST'])
        @jwt_required()
        def remove():
            return Service.remove()

        @app.route('/upload', methods=['POST'])
        @jwt_required()
        def upload():
            return Service.upload()

from api import Resource, abort, reqparse, auth, db, g
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema


class UserResource(Resource):
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id={user_id} not found")
        return user_schema.dump(user), 200

    @auth.login_required(role="admin")
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password")
        user_data = parser.parse_args()
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id={user_id} not found")
        user.username = user_data["username"]
        user.password = user_data.get("password") or user.password
        user.save()
        return user_schema.dump(user), 201

    @auth.login_required
    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if user == g.user:
            user_dict = user_schema.dump(user)
            user.delete()
            return user_dict, 200
        return f"QNote with id {user_id} not found", 404
        raise NotImplemented  # не реализовано!


class UsersListResource(Resource):
    def get(self):
        users = UserModel.query.all()
        return users_schema.dump(users), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        user_data = parser.parse_args()
        user = UserModel(**user_data)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        return user_schema.dump(user), 201

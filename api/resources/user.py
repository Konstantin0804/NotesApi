from api import Resource, abort, reqparse, auth, db, g
from api.models.user import UserModel
from api.models.note import NoteModel
from api.schemas.user import user_schema, users_schema
from api.schemas.note import note_schema, notes_schema


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
        user_data = parser.parse_args()
        user = UserModel.query.get(user_id)
        user.username = user_data["username"]
        user.save()
        return user_schema.dump(user), 200

    @auth.login_required
    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        author_id = user_id
        notes = NoteModel.query.get(author_id)
        user_dict = user_schema.dump(user)
        user.delete()
        notes.delete()
        return user_dict, 200



class UsersListResource(Resource):
    def get(self):
        users = UserModel.query.all()
        return users_schema.dump(users), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("role")
        user_data = parser.parse_args()
        user = UserModel(**user_data)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        return user_schema.dump(user), 201

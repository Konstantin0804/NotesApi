from api import Resource, abort, reqparse, auth, db, g
from api.models.user import UserModel
from api.models.note import NoteModel
from api.schemas.user import user_schema, users_schema, UserSchema, UserRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields


@doc(tags=['Users'])  # Декоратор для описания что делает данный класс в свагере
class UserResource(MethodResource):
    @doc(
        summary="Get user by id",
        description="Returns user",
        produces=[
            'application/json'
        ],
        params={'user_id': {'description': 'user id'}},
        responses={
            "200": {

                "description": "Return user",
                "content":
                    {"application/json": []}

            },
            "404": {
                "description": "User not found"
            }
        }
    )
    @marshal_with(UserSchema, code="User")
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id={user_id} not found")
        return user, 200


    @auth.login_required(role="admin")
    @doc(description='Edit user by id')
    @marshal_with(UserSchema)
    @use_kwargs({"username": fields.Str()})
    def put(self, user_id, **kwargs):
        user = UserModel.query.get(user_id)
        user.username = kwargs["username"]
        user.save()
        return user, 200


    @auth.login_required
    @marshal_with(UserSchema)
    @doc(description='Delete user by id')
    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        author_id = user_id
        notes = NoteModel.query.get(author_id)
        user_dict = user_schema.dump(user)
        user.delete()
        notes.delete()
        return user_dict, 200


@doc(tags=['Users'])
class UsersListResource(MethodResource):
    @marshal_with(UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users, 200

    @use_kwargs(UserRequestSchema, location='json')
    @marshal_with(UserSchema)
    def post(self, **kwargs):
        user = UserModel(**kwargs)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        return user, 201
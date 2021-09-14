from api import Resource, abort, reqparse, auth, db, g
from api.models.user import UserModel
from api.models.note import NoteModel
from api.schemas.user import user_schema, users_schema, UserSchema, UserRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields
import logging


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
    @doc(description='Edit user by id', security=[{"basicAuth": []}], summary="Edit user")
    @marshal_with(UserSchema)
    @use_kwargs({"username": fields.Str()})
    def put(self, user_id, **kwargs):
        user = UserModel.query.get(user_id)
        user.username = kwargs["username"]
        user.save()
        return user, 200


    @auth.login_required(role="admin")
    @marshal_with(UserSchema)
    @doc(description='Delete user by id', security=[{"basicAuth": []}], summary="Delete user")
    def delete(self, user_id):
        author_id = user_id
        user = UserModel.query.get(user_id)
        if not user:
            abort(400, error=f"User with user id:{user_id} not exist")
        notes = NoteModel.query.get(author_id)
        user_dict = user_schema.dump(user)
        user.delete()
        notes.delete()
        return user_dict, 200


@doc(tags=['Users'])
class UsersListResource(MethodResource):
    @marshal_with(UserSchema(many=True))
    @doc(description='Get all users', summary="Get users")
    def get(self):
        users = UserModel.query.all()
        return users, 200

    @use_kwargs(UserRequestSchema, location='json')
    @marshal_with(UserSchema)
    @doc(description='Post new user', summary="Post users")
    def post(self, **kwargs):
        user = UserModel(**kwargs)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        logging.info("User created") # поставил логирование отработка функции добавления нового автора
        return user, 201
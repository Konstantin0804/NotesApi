from api import ma
from api.models.user import UserModel
from api.schemas.file import FileSchema


#       schema        flask-restful
# object ------>  dict ----------> json


# Сериализация ответа(response)
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        # fields = ('id', 'username')

    id = ma.auto_field()
    username = ma.auto_field()
    is_staff = ma.auto_field()
    role = ma.auto_field()
    photo = ma.Nested(FileSchema())

    _links = ma.Hyperlinks({
        'self': ma.URLFor('userresource', values=dict(user_id="<id>")),
        'collection': ma.URLFor('userslistresource')
    })

class UserRequestSchema(ma.SQLAlchemySchema):
   class Meta:
       model = UserModel

   username = ma.Str()
   password = ma.Str()
   role = ma.Str()
   photo_id = ma.Integer(required=False)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Десериализация запроса(request)


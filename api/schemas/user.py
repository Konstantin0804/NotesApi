from api import ma
from api.models.user import UserModel


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

class UserRequestSchema(ma.SQLAlchemySchema):
   class Meta:
       model = UserModel

   username = ma.Str()
   password = ma.Str()
   role = ma.Str()

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Десериализация запроса(request)


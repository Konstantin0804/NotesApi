from api import ma
from api.models.tags import TagModel


#       schema        flask-restful
# object ------>  dict ----------> json


# Сериализация ответа(response)
class TagSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel
        # fields = ('id', 'username')

    id = ma.auto_field()
    name = ma.auto_field()

#class UserRequestSchema(ma.SQLAlchemySchema):
#  class Meta:
#       model = UserModel
#
#   username = ma.Str()
#   password = ma.Str()
#   role = ma.Str()

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)

# Десериализация запроса(request)


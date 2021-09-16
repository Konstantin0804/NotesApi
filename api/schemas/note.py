from api import ma
from api.models.note import NoteModel
from api.schemas.user import UserSchema
from api.schemas.tags import TagSchema


#       schema        flask-restful
# object ------>  dict ----------> json

class NoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = NoteModel

    id = ma.auto_field()
    text = ma.auto_field()
    private = ma.auto_field()
    archive = ma.auto_field()
    author = ma.Nested(UserSchema())
    tags = ma.Nested(TagSchema(many=True))

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

class NoteCreateSchema(ma.SQLAlchemySchema):
   class Meta:
       model = NoteModel

   text = ma.Str()
   private = ma.Str()

class NoteEditSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel
    text = ma.auto_field(required=False)
    private = ma.auto_field(required=False)

class NoteFilterchema(ma.SQLAlchemyAutoSchema):
    private = ma.Boolean(required=False)
    tag = ma.String(required=False)
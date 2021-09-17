from api import auth, abort, g, Resource, reqparse, api
from api.models.note import NoteModel
from api.models.tags import TagModel
from api.models.user import UserModel
from api.schemas.note import note_schema, notes_schema, NoteSchema, NoteEditSchema, NoteCreateSchema, NoteFilterchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields
from sqlalchemy.orm.exc import NoResultFound
from flask_babel import _


@doc(tags=['Notes'])
@api.resource('/notes/<int:note_id>') # вместо добавления этого обработчика в app.py можно делать так: через декоратор
class NoteResource(MethodResource):
    @auth.login_required
    @doc(description='Get notes by note id', summary="Get notes")
    @marshal_with(NoteSchema)
    def get(self, note_id):
        author = g.user
        try:
            note = NoteModel.get_all_for_user(author).filter_by(id=note_id).one()
            return note, 200
        except NoResultFound:
            abort(400, error=_("Note with id=%(note_id)s not found", note_id=note_id)) #так оборачивается для перевода с помощью babel


    @auth.login_required
    @doc(security=[{"basicAuth": []}], description='Edit users notes by note id', summary="Edit notes")
    @marshal_with(NoteSchema)
    @use_kwargs(NoteEditSchema)
    def put(self, note_id, **kwargs):
        author = g.user
        note = NoteModel.query.get(note_id)
        if kwargs.get("text") is not None:
            note.text = kwargs["text"]
        if kwargs.get("private") is not None:
            note.private = kwargs["private"]
        if not note:
            abort(400, error=f"note {note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        #note.text = note_data["text"]
        #note.private = note_data.get("private") or note.private
        note.save()
        return note, 200

    @auth.login_required
    @marshal_with(NoteSchema)
    @doc(security=[{"basicAuth": []}], description='Archive users notes by note id', summary="Archive notes")
    def delete(self, note_id):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(400, error=f"Note with id:{note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        note.delete()
        note.save()
        return note, 200

@doc(tags=['Notes'])
@api.resource('/notes/<int:note_id>')
class NoteRestoreResource(MethodResource):
    @auth.login_required
    @marshal_with(NoteSchema)
    @doc(security=[{"basicAuth": []}], description='Restore users notes by note id', summary="Restore notes")
    def put(self, note_id):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(400, error=f"Note with id:{note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        if note.archive:
            note.restore()
        else:
            return {}, 304
        return note, 200

@api.resource('/notes')
@doc(tags=['Notes'])
class NotesListResource(MethodResource):
    @auth.login_required
    @doc(description="Get user's notes", security=[{"basicAuth": []}], summary="Get notes")
    @marshal_with(NoteSchema(many=True))
    @use_kwargs(({"tags": fields.Str()}), location='query')
    def get(self, **kwargs):
        author = g.user
        notes = NoteModel.get_all_for_user(author)
        if kwargs.get("tags") is not None:
            notes = notes.filter(NoteModel.tags.any(name=kwargs['tags']))
        return notes, 200

    @auth.login_required
    @doc(description="Post new note", security=[{"basicAuth": []}], summary="Post notes")
    @use_kwargs(NoteCreateSchema)
    @marshal_with(NoteSchema)
    def post(self, **kwargs):
        author = g.user
        #parser = reqparse.RequestParser()      Заменил парсер reqparse на использование декоратора use_kwargs
        #parser.add_argument("text", required=True)
        #parser.add_argument("private", type=bool)
        #note_data = parser.parse_args()
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201

@api.resource('/notes/public')
@doc(tags=['Notes'])
class NotesPublicResource(MethodResource):
    @doc(description="Get all public notes", summary="Public notes")
    @marshal_with(NoteSchema(many=True))
    def get(self):
        notes = NoteModel.query.filter_by(private=0).filter_by(archive=False)
        return notes, 200

@api.resource('/notes/<note_id>/tags')
@doc(tags=['NotesTags'])
class NotesAddTagResource(MethodResource):
    @auth.login_required
    @doc(description="Put tags to note", security=[{"basicAuth": []}], summary="Put tags to notes")
    @use_kwargs({"tags": fields.List(fields.Int())}, location="json")
    @marshal_with(NoteSchema, code=200)
    def put(self, note_id, **kwargs):
        author = g.user
        note = NoteModel.query.get(note_id)
        if note.author != author:
            abort(403, error=f"Forbidden")
        for tag_id in kwargs["tags"]:
            tag = TagModel.query.get(tag_id)
            if tag.author != author.username:
                abort(403, error=f"Forbidden")
            note.tags.append(tag)
        note.save()
        return note, 200

    @auth.login_required
    @doc(description="Delete tags from notes", security=[{"basicAuth": []}], summary="Delete tags from notes")
    @use_kwargs({"tags": fields.List(fields.Int())}, location="json")
    @marshal_with(NoteSchema, code=200)
    def delete(self, note_id, **kwargs):
        note = NoteModel.query.get(note_id)
        for tag_id in kwargs["tags"]:
            tag = TagModel.query.get(tag_id)
            note.tags.remove(tag)
        note.save()
        return note, 200

@api.resource('/users/<int:user_id>/notes')
@doc(tags=['Notes'])
class NotesListByAuthorResource(MethodResource):
    @doc(description="Get notes by users", summary="Get notes by users")
    @marshal_with(NoteSchema(many=True))
    def get(self, user_id):
        UserModel.query.get_or_404(user_id, description="User not found") # Если будет введено не корректное user_id будет возвращена ошибка 404
        notes = NoteModel.query.filter_by(author_id=user_id).filter_by(private=0).filter_by(archive=False).all()
        return notes, 200


#@doc(tags=['Notes'])
#class NotesFilterResource(MethodResource):
#    @auth.login_required
#    @doc(description="Get all notes by tags", security=[{"basicAuth": []}], summary="Tags filter")
#    @marshal_with(NoteSchema(many=True), code=200)
#    @use_kwargs({"tag": fields.Str()}, location='query')
#    def get(self, **kwargs):
#        notes = NoteModel.query.filter(NoteModel.tags.any(name=kwargs["tag"])) #ANY выбирает все тэги которые подходят по д жтот фильтр
#        return notes, 200


#/notes/public/filter?username=<un>
#@doc(tags=['Notes'])
#class NotesPublicUserResource(MethodResource):
#    @doc(description="Get all public notes by users", summary="Public notes by user")
#    @marshal_with(NoteSchema(many=True), code=200)
#    @use_kwargs({"username": fields.Str()}, location='query')
#    def get(self, **kwargs):
#        notes = NoteModel.query.filter(NoteModel.author.has(username=kwargs["username"]), NoteModel.private==(False)) #
#        return notes, 200


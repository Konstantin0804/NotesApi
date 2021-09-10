from api import auth, abort, g, Resource, reqparse
from api.models.note import NoteModel
from api.schemas.note import note_schema, notes_schema, NoteSchema, NoteRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields


@doc(tags=['Notes'])
class NoteResource(MethodResource):
    @auth.login_required
    @doc(description='Get notes by user id')
    @marshal_with(NoteSchema)
    def get(self, note_id):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        return note, 200

    # FIXME Fix put like put in users
    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @marshal_with(NoteSchema)
    def put(self, note_id):
        author = g.user
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        parser.add_argument("private", type=bool)  # чтобы не передовался тип приватности в виде строки
        note_data = parser.parse_args()
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        note.text = note_data["text"]
        note.private = note_data.get("private") or note.private
        note.save()
        return note, 200

    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    def delete(self, note_id):
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id:{note_id} not found")
        note_dict = note_schema.dump(note)
        note.delete()
        return note_dict, 200

@doc(tags=['Notes'])
class NotesListResource(MethodResource):
    @auth.login_required
    @doc(description="Get user's notes", security=[{"basicAuth": []}], summary="Get notes")
    @marshal_with(NoteSchema(many=True))
    def get(self):
        author = g.user
        notes = NoteModel.query.filter_by(author_id=author.id)
        return notes, 200

    @auth.login_required
    @doc(description="Post new note", security=[{"basicAuth": []}], summary="Post notes")
    @use_kwargs({"text": fields.Str(), "private": fields.Boolean()})
    @marshal_with(NoteSchema)
    def post(self, **kwargs):
        author = g.user
        #parser = reqparse.RequestParser()
        #parser.add_argument("text", required=True)
        #parser.add_argument("private", type=bool)
        #note_data = parser.parse_args()
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201

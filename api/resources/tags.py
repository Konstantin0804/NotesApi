from api import auth, abort, g, Resource, reqparse, api
from api.models.tags import TagModel
from api.schemas.tags import tag_schema, tags_schema, TagSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields

@api.resource('/tags/<int:tag_id>')
@doc(tags=['Tags'])
class TagsResource(MethodResource):
    @marshal_with(TagSchema)
    @doc(description='Get tags by tag id', summary="Get Tag")
    def get(self, tag_id):
        tag = TagModel.query.get(tag_id)
        if not tag:
            abort(404, error=f"Tag with id={tag_id} not found")
        return tag, 200

    @auth.login_required
    @doc(description='Edit tags by id', security=[{"basicAuth": []}], summary="Edit tags")
    @marshal_with(TagSchema)
    @use_kwargs({"name": fields.Str()})
    def put(self, tag_id, **kwargs):
        author = g.user
        tag = TagModel.query.get(tag_id)
        if tag.author != author.username:
            abort(403, error=f"Forbidden")
        tag.name = kwargs["name"]
        tag.save()
        return tag, 200

    @auth.login_required
    @doc(security=[{"basicAuth": []}], description='Delete tags by id', summary="Delete tags")
    @marshal_with(TagSchema)
    def delete(self, tag_id):
        author = g.user
        tag = TagModel.query.get(tag_id)
        if tag.author != author.username:
            abort(403, error=f"Forbidden")
        if not tag:
            abort(404, error=f"Tag with id:{tag_id} not found")
        tag.delete()
        return tag, 200

@api.resource('/tags')
@doc(tags=['Tags'])
class TagsListResource(MethodResource):
    @auth.login_required
    @marshal_with(TagSchema(many=True))
    @doc(security=[{"basicAuth": []}], description='Get all tags by current user', summary="Get Tags")
    def get(self):
        author = g.user
        tags = TagModel.query.filter_by(author=author.username)
        return tags, 200

    @auth.login_required
    @use_kwargs({"name": fields.Str()})
    @marshal_with(TagSchema)
    @doc(security=[{"basicAuth": []}], description='Post new tags', summary="Post Tags")
    def post(self, **kwargs):
        author = g.user
        tag = TagModel(author=author.username, **kwargs)
        tag.save()
        return tag, 201


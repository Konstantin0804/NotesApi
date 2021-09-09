from api import auth, abort, g, Resource, reqparse
from api.models.tags import TagModel
from api.schemas.tags import tag_schema, tags_schema, TagSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields

@doc(tag=['Tags'])
class TagsResource(MethodResource):
    def get(self, tag_id):
        pass


@doc(tag=['Tags'])
class TagsListResource(MethodResource):
    @marshal_with(TagSchema(many=True))
    def get(self):
        tags = TagModel.query.all()
        return tags, 200

    @use_kwargs({"name": fields.Str()})
    @marshal_with(TagSchema)
    def get(self, **kwargs):
        tag = TagModel(**kwargs)
        tag.save()
        return tag, 200
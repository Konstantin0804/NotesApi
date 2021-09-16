from api import api, app, docs
from api.resources.note import NoteResource, NotesListResource, NotesPublicResource, NotesAddTagResource,  NoteRestoreResource
from api.resources.user import UserResource, UsersListResource
from api.resources.auth import TokenResource
from api.resources.tags import TagsResource, TagsListResource
from api.resources.file import UploadPictureResource
from config import Config
from flask import render_template, send_from_directory

@app.route('/uploads/<path:filename>')
def download_file(filename):
   # FIXME: добавить проверку есть ли такая директория и если нет то создать.
   return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE
api.add_resource(UsersListResource,
                 '/users')  # GET, POST
api.add_resource(UserResource,
                 '/users/<int:user_id>')  # GET, PUT, DELETE

api.add_resource(TokenResource,
                 '/auth/token')  # GET

#api.add_resource(NotesListResource,
#                 '/notes',  # GET, POST
#                 )
#api.add_resource(NoteResource,
#                 '/notes/<int:note_id>',  # GET, PUT, DELETE
#                 )
api.add_resource(NoteRestoreResource,
                 '/notes/<int:note_id>/restore',  # PUT
                 )
api.add_resource(NotesPublicResource,
                 '/notes/public',  # GET, PUT, DELETE
                 )
api.add_resource(TagsListResource,  #GET, POST
                 '/tags'
                 )
api.add_resource(TagsResource,  # GET, PUT, DELETE
                 '/tags/<int:tag_id>'
                 )
#api.add_resource(NotesFilterResource,  # GET
#                 '/notes/filter'
#                 )
api.add_resource(NotesAddTagResource,   #PUT
                 '/notes/<note_id>/tags'
                 )
#api.add_resource(NotesPublicUserResource,   #GET
#                 '/notes/public/filter'
#                 )

docs.register(UserResource)
docs.register(UsersListResource)
docs.register(NoteResource)
docs.register(NoteRestoreResource)
docs.register(NotesListResource)
docs.register(TagsListResource)
docs.register(TagsResource)
docs.register(NotesPublicResource)
docs.register(NotesAddTagResource)
docs.register(UploadPictureResource)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)

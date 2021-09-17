from api import api, app, docs
from api.resources.note import NoteResource, NotesListResource, NotesPublicResource, NotesAddTagResource,  NoteRestoreResource, NotesListByAuthorResource
from api.resources.user import UserResource, UsersListResource, UserFilterResource
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

docs.register(UserResource)
docs.register(UsersListResource)
docs.register(UserFilterResource)
docs.register(NoteResource)
docs.register(NoteRestoreResource)
docs.register(NotesListResource)
docs.register(NotesListByAuthorResource)
docs.register(TagsListResource)
docs.register(TagsResource)
docs.register(NotesPublicResource)
docs.register(NotesAddTagResource)
docs.register(UploadPictureResource)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)

from api import db
from api.models.user import UserModel


class TagModel(db.Model):
   __tablename__ = 'tag'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(255), unique=True, nullable=False)
   author = db.Column(db.String(255), db.ForeignKey(UserModel.username))

   def save(self):
      db.session.add(self)
      db.session.commit()

   def delete(self):
      db.session.delete(self)
      db.session.commit()

   def __repr__(self):
      return f"Tag [{self.name}]"
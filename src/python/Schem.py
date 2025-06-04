from flask_marshmallow import Marshmallow
from Mod import User, Quiz

ma = Marshmallow()

class UserSchema(ma.SQLAlchemyAutoSchema):
   class Meta:
       model = User
       include_fk = True

class QuizSchema(ma.SQLAlchemyAutoSchema):
   class Meta:
       model = Quiz
       include_fk = True

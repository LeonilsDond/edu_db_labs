from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Role(db.Model):
   __tablename__ = 'Role'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)

   users = db.relationship('User', backref='role', lazy=True)

class User(db.Model):
   __tablename__ = 'User'
   id = db.Column(db.Integer, primary_key=True)
   email = db.Column(db.String(255), unique=True, nullable=False)
   last_name = db.Column(db.String(100))
   first_name = db.Column(db.String(100))
   role_id = db.Column(db.Integer, db.ForeignKey('Role.id'))

   quiz_assignments = db.relationship('QuizAssignment', backref='user', lazy=True)
   answers = db.relationship('Answer', backref='user', lazy=True)
   reports = db.relationship('Report', backref='user', lazy=True)

class QuizCategory(db.Model):
   __tablename__ = 'quizCategory'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)

   quizzes = db.relationship('Quiz', backref='category', lazy=True)

class Quiz(db.Model):
   __tablename__ = 'Quiz'
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(255))
   description = db.Column(db.Text)
   start_date = db.Column(db.Date)
   end_date = db.Column(db.Date)
   status = db.Column(db.String(50))
   category_id = db.Column(db.Integer, db.ForeignKey('quizCategory.id'))

   assignments = db.relationship('QuizAssignment', backref='quiz', lazy=True)
   questions = db.relationship('Question', backref='quiz', lazy=True)
   answers = db.relationship('Answer', backref='quiz', lazy=True)
   module_links = db.relationship('Module_Quiz', backref='quiz', lazy=True)
   results = db.relationship('QuizResult', backref='quiz', lazy=True)

class QuizAssignment(db.Model):
   __tablename__ = 'QuizAssignment'
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
   quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))

class Question(db.Model):
   __tablename__ = 'Question'
   id = db.Column(db.Integer, primary_key=True)
   quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))
   text = db.Column(db.Text)
   question_type = db.Column(db.String(50))

   options = db.relationship('Option', backref='question', lazy=True)
   answers = db.relationship('Answer', backref='question', lazy=True)

class Option(db.Model):
   __tablename__ = 'Option'
   id = db.Column(db.Integer, primary_key=True)
   question_id = db.Column(db.Integer, db.ForeignKey('Question.id'))
   text = db.Column(db.Text)

   answers = db.relationship('Answer', backref='option', lazy=True)

class Answer(db.Model):
   __tablename__ = 'Answer'
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
   quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))
   question_id = db.Column(db.Integer, db.ForeignKey('Question.id'))
   option_id = db.Column(db.Integer, db.ForeignKey('Option.id'), nullable=True)
   text_answer = db.Column(db.Text, nullable=True)

class Course(db.Model):
   __tablename__ = 'Course'
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(255))
   description = db.Column(db.Text)
   duration_weeks = db.Column(db.Integer)

   modules = db.relationship('Module', backref='course', lazy=True)

class Module(db.Model):
   __tablename__ = 'Module'
   id = db.Column(db.Integer, primary_key=True)
   course_id = db.Column(db.Integer, db.ForeignKey('Course.id'))
   title = db.Column(db.String(255))
   content = db.Column(db.Text)

   module_quizzes = db.relationship('Module_Quiz', backref='module', lazy=True)

class Module_Quiz(db.Model):
   __tablename__ = 'Module_Quiz'
   module_id = db.Column(db.Integer, db.ForeignKey('Module.id'), primary_key=True)
   quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'), primary_key=True)

class QuizResult(db.Model):
   __tablename__ = 'quizResult'
   id = db.Column(db.Integer, primary_key=True)
   quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))
   respondent_count = db.Column(db.Integer)

   reports = db.relationship('Report', backref='quiz_result', lazy=True)

class Report(db.Model):
   __tablename__ = 'Report'
   id = db.Column(db.Integer, primary_key=True)
   quiz_result_id = db.Column(db.Integer, db.ForeignKey('quizResult.id'))
   user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
   format = db.Column(db.String(50))
   content = db.Column(db.Text)
   created_at = db.Column(db.Date)


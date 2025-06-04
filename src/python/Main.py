from flask import Flask, request, jsonify, render_template
from Mod import (
   db,
   Role, User, QuizCategory, Quiz, QuizAssignment,
   Question, Option, Answer, Course, Module,
   Module_Quiz, QuizResult, Report
)
from Schem import ma, UserSchema, QuizSchema
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

def seed_data():
   roles = [
       Role(id=1, name='Адміністратор'),
       Role(id=2, name='Експерт'),
       Role(id=3, name='Користувач'),
   ]
   db.session.bulk_save_objects(roles)

   users = [
       User(id=1, email='admin@osvita.ua', last_name='Шевченко', first_name='Тарас', role_id=1),
       User(id=2, email='expert@med.ua', last_name='Ковальчук', first_name='Олена', role_id=2),
       User(id=3, email='student@edu.ua', last_name='Мельник', first_name='Андрій', role_id=3),
   ]
   db.session.bulk_save_objects(users)

   categories = [
       QuizCategory(id=1, name='Освіта'),
       QuizCategory(id=2, name='Охорона здоров’я'),
       QuizCategory(id=3, name='Технології'),
   ]
   db.session.bulk_save_objects(categories)

   courses = [
       Course(id=1, title='Основи Python', description='Базовий курс з програмування мовою Python.', duration_weeks=6),
       Course(id=2, title='Цифрова грамотність', description='Курс для підвищення цифрової компетентності.', duration_weeks=4),
   ]
   db.session.bulk_save_objects(courses)

   modules = [
       Module(id=1, course_id=1, title='Змінні та типи даних', content='Теоретичні матеріали щодо типів змінних у Python.'),
       Module(id=2, course_id=1, title='Умовні оператори', content='Оператори if, elif, else.'),
       Module(id=3, course_id=2, title='Інтернет-безпека', content='Основи захисту персональних даних.'),
       Module(id=4, course_id=2, title='Електронні сервіси', content='Як користуватись державними онлайн-сервісами.'),
   ]
   db.session.bulk_save_objects(modules)

   quizzes = [
       Quiz(
           id=1,
           title='Перевірка знань з Python',
           description='Опитування для перевірки базових знань з Python.',
           start_date=date(2025, 6, 1),
           end_date=date(2025, 6, 15),
           status='Заплановано',
           category_id=3
       ),
       Quiz(
           id=2,
           title='Онлайн-безпека громадян',
           description='Оцінка обізнаності користувачів у сфері кібербезпеки.',
           start_date=date(2025, 6, 10),
           end_date=date(2025, 6, 20),
           status='Чернетка',
           category_id=2
       ),
   ]
   db.session.bulk_save_objects(quizzes)

   module_quizzes = [
       Module_Quiz(module_id=1, quiz_id=1),
       Module_Quiz(module_id=3, quiz_id=2),
   ]
   db.session.bulk_save_objects(module_quizzes)


   assignments = [
       QuizAssignment(id=1, user_id=2, quiz_id=1),
       QuizAssignment(id=2, user_id=3, quiz_id=2),
   ]
   db.session.bulk_save_objects(assignments)


   questions = [
       Question(id=1, quiz_id=1, text='Що таке змінна у Python?', question_type='single_choice'),
       Question(id=2, quiz_id=1, text='Оберіть правильні типи даних у Python:', question_type='multiple_choice'),
       Question(id=3, quiz_id=2, text='Як захистити свій пароль онлайн?', question_type='text'),
   ]
   db.session.bulk_save_objects(questions)

   options = [
       Option(id=1, question_id=1, text='Комірка для зберігання даних'),
       Option(id=2, question_id=1, text='Назва функції'),
       Option(id=3, question_id=2, text='int'),
       Option(id=4, question_id=2, text='str'),
       Option(id=5, question_id=2, text='html'),
   ]
   db.session.bulk_save_objects(options)


   answers = [
       Answer(id=1, user_id=2, quiz_id=1, question_id=1, option_id=1, text_answer=None),
       Answer(id=2, user_id=2, quiz_id=1, question_id=2, option_id=3, text_answer=None),
       Answer(id=3, user_id=2, quiz_id=1, question_id=2, option_id=4, text_answer=None),
       Answer(id=4, user_id=3, quiz_id=2, question_id=3, option_id=None,
              text_answer='Використовувати складні паролі та двофакторну автентифікацію'),
   ]
   db.session.bulk_save_objects(answers)


   results = [
       QuizResult(id=1, quiz_id=1, respondent_count=1),
       QuizResult(id=2, quiz_id=2, respondent_count=1),
   ]
   db.session.bulk_save_objects(results)


   reports = [
       Report(id=1, quiz_result_id=1, user_id=1,
              format='PDF', content='Звіт про проходження опитування з Python.', created_at=date(2025, 6, 16)),
       Report(id=2, quiz_result_id=2, user_id=1,
              format='DOCX', content='Звіт з опитування щодо безпеки в інтернеті.', created_at=date(2025, 6, 21)),
   ]
   db.session.bulk_save_objects(reports)


   db.session.commit()

with app.app_context():
   db.drop_all()
   db.create_all()
   seed_data()

user_schema = UserSchema()
users_schema = UserSchema(many=True)

quiz_schema = QuizSchema()
quizzes_schema = QuizSchema(many=True)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
   users = User.query.all()
   return users_schema.jsonify(users)

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
   user = User.query.get_or_404(id)
   return user_schema.jsonify(user)

@app.route('/users', methods=['POST'])
def create_user():
   data = request.json or {}
   try:
       if 'email' not in data or not data['email']:
           return jsonify({'error': 'Поле email є обовʼязковим'}), 400

       user = User(**data)
       db.session.add(user)
       db.session.commit()
       return user_schema.jsonify(user), 201

   except Exception as e:
       db.session.rollback()
       return jsonify({'error': str(e)}), 400

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
   user = User.query.get_or_404(id)
   data = request.json or {}
   try:
       for key, value in data.items():
           setattr(user, key, value)
       db.session.commit()
       return user_schema.jsonify(user)
   except Exception as e:
       db.session.rollback()
       return jsonify({'error': str(e)}), 400

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
   user = User.query.get_or_404(id)
   db.session.delete(user)
   db.session.commit()
   return jsonify({'message': 'User deleted'}), 200

@app.route('/quizzes', methods=['GET'])
def get_quizzes():
   quizzes = Quiz.query.all()
   return quizzes_schema.jsonify(quizzes)

@app.route('/quizzes/<int:id>', methods=['GET'])
def get_quiz(id):
   quiz = Quiz.query.get_or_404(id)
   return quiz_schema.jsonify(quiz)

@app.route('/quizzes', methods=['POST'])
def create_quiz():
   data = request.json or {}
   try:
       missing = []
       for f in ('title', 'start_date', 'end_date', 'category_id'):
           if f not in data or not data[f]:
               missing.append(f)
       if missing:
           return jsonify({'error': f"Відсутні обов'язкові поля: {', '.join(missing)}"}), 400

       try:
           data['start_date'] = date.fromisoformat(data['start_date'])
           data['end_date'] = date.fromisoformat(data['end_date'])
       except ValueError:
           return jsonify({'error': 'Неправильний формат дати. Має бути YYYY-MM-DD'}), 400

       quiz = Quiz(**data)
       db.session.add(quiz)
       db.session.commit()
       return quiz_schema.jsonify(quiz), 201

   except Exception as e:
       db.session.rollback()
       return jsonify({'error': str(e)}), 400


@app.route('/quizzes/<int:id>', methods=['PUT'])
def update_quiz(id):
   quiz = Quiz.query.get_or_404(id)
   data = request.json or {}
   try:
       if 'start_date' in data:
           try:
               data['start_date'] = date.fromisoformat(data['start_date'])
           except ValueError:
               return jsonify({'error': 'Неправильний формат start_date. Має бути YYYY-MM-DD'}), 400
       if 'end_date' in data:
           try:
               data['end_date'] = date.fromisoformat(data['end_date'])
           except ValueError:
               return jsonify({'error': 'Неправильний формат end_date. Має бути YYYY-MM-DD'}), 400


       for key, value in data.items():
           setattr(quiz, key, value)
       db.session.commit()
       return quiz_schema.jsonify(quiz)


   except Exception as e:
       db.session.rollback()
       return jsonify({'error': str(e)}), 400


@app.route('/quizzes/<int:id>', methods=['DELETE'])
def delete_quiz(id):
   quiz = Quiz.query.get_or_404(id)
   db.session.delete(quiz)
   db.session.commit()
   return jsonify({'message': 'Quiz deleted'}), 200




if __name__ == '__main__':
   app.run(debug=True)

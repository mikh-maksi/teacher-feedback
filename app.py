from numbers import Real
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from celery import Celery
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from flask import request, jsonify


# create the extension
# db = SQLAlchemy()
db = create_engine('postgresql+psycopg2://krgdfjhezazjek:b4d01edabab4b487a22a2694aa5f81f49d86c49b995f0ca498d356a0e7509dcf@ec2-54-170-90-26.eu-west-1.compute.amazonaws.com:5432/dcagfpkbfapf9d')
# create the app
app = Flask(__name__)

CORS(app, supports_credentials=True, allow_headers=True)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

base = declarative_base()

Session = sessionmaker(db)
session = Session()

@app.cli.command('db_create')
def db_create():
    base.metadata.create_all(db)
    print('Database created')


@app.cli.command('db_drop')
def db_drop():
    base.metadata.drop_all(db)
    print('Database dropped')

# configure the SQLite database, relative to the app instance folder
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://krgdfjhezazjek:b4d01edabab4b487a22a2694aa5f81f49d86c49b995f0ca498d356a0e7509dcf@ec2-54-170-90-26.eu-west-1.compute.amazonaws.com:5432/dcagfpkbfapf9d"
# initialize the app with the extension
# db.init_app(app)
# SQLALCHEMY_TRACK_MODIFICATIONS = False

ma = Marshmallow(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, unique=True, nullable=False)
#     email = db.Column(db.String)


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'telegram', 'login', 'role_id', 'password')

class Users(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    telegram = Column(Text, nullable=False)
    login = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    role_id = Column(Integer, nullable=False)


class Reports(base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    course = Column(String(80), nullable=False)
    grp = Column(String(80), nullable=False)
    lesson_type = Column(Integer, nullable=False)
    teacher = Column(String(50), nullable=False)
    lesson_theme = Column(String(50), nullable=False)
    lesson_duration = Column(Integer, nullable=False)
    lesson_date = Column(Date, nullable=False)
    homework_number = Column(Integer, nullable=False)
    lesson_total = Column(String(100), nullable=False)
    additional_materials = Column(String(100), nullable=False)
    program_comments = Column(String(100), nullable=False)



class ReportsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'course', 'grp', 'lesson_type', 'teacher', 'lesson_theme', 'lesson_duration', 'lesson_date', 'homework_number', 'lesson_total', 'additional_materials', 'program_comments')

reports_schema = ReportsSchema()
user_schema = UsersSchema()


@app.route('/test_report', methods=["GET"])
def create_reports1():
    report_course = 'some'
    if request.method == "GET":
        report_course = request.args.get('course')
    return report_course

@app.route('/get_parameters_test', methods=["GET"])
def create_reports2():
    if request.args.get('text') == None:
        text = ''
    else:
        text = request.args.get('text')
    if request.args.get('digits') == None:
        digits = 0
    else:
        digits = request.args.get('digits')
    return_out = "text: "+str(text)+" digits:"+str(digits)
    return return_out
    
    
@app.route('/get_report_test', methods=["GET"])
def create_reports_test():
    course = 'course'
    grp = 'grp'
    lesson_type = 1
    teacher = 'teacher'
    lesson_theme = 'theme'
    lesson_duration = 3
    lesson_date = '2022-10-17'
    homework_number = 8
    lesson_total = 'total'
    additional_materials = 'additon'
    program_comments = 'comments'
    # if request.method == "GET":
    #     course = request.args.get('course')
    #     grp = request.args.get('grp')
    #     lesson_type = request.args.get('lesson_type')
    #     teacher = request.args.get('teacher')
    #     lesson_theme = request.args.get('lesson_theme')
    #     lesson_duration = request.args.get('lesson_duration')
    #     lesson_date = request.args.get('lesson_date')
    #     homework_number = request.args.get('homework_number')
    #     lesson_total = request.args.get('lesson_total')
    #     additional_materials = request.args.get('additional_materials')
    #     program_comments = request.args.get('program_comments')

    report = Reports( course=course , grp=grp,
                lesson_type=lesson_type, teacher=teacher, lesson_theme=lesson_theme,lesson_duration=lesson_duration, lesson_date=lesson_date, homework_number=homework_number,  lesson_total=lesson_total, additional_materials=additional_materials, program_comments=program_comments)
    session.add(report)
    session.commit()
    test = session.query(Reports).filter_by(course=course).first()
    data = reports_schema.dump(test)
    print(data)


    return jsonify(data=data, message=f'Report {report.id} successfully registered'), 202


@app.route('/get_report', methods=["GET","POST"])
def create_reports():
    # course = 'course'
    # grp = 'grp'
    # lesson_type = 'type'
    # teacher = 'teacher'
    # lesson_theme = 'theme'
    # lesson_duration = 3
    # lesson_date = '2022-10-17'
    # homework_number = 8
    # lesson_total = 'total'
    # additional_materials = 'additon'
    # program_comments = 'comments'

    if request.method == "GET":
        if request.args.get('course') == None:
            course = ''
        else:
            course = request.args.get('course')
        
        if request.args.get('grp') == None:
            grp = ''
        else:
            grp = request.args.get('grp')
        
        if request.args.get('lesson_type') == None:
            lesson_type = 0
        else:
            lesson_type = request.args.get('lesson_type')

        if request.args.get('teacher') == None:
            teacher = ''
        else:
            teacher = request.args.get('teacher')

        if request.args.get('lesson_theme') == None:
            lesson_theme = ''
        else:
            lesson_theme = request.args.get('lesson_theme')

        if request.args.get('lesson_duration') == None:
            lesson_duration = 0
        else:
            lesson_duration = request.args.get('lesson_duration')
        
        if request.args.get('lesson_date') == None:
            lesson_date = '2000-01-01'
        else:
            lesson_date = request.args.get('lesson_date')
        
        if request.args.get('homework_number') == None:
            homework_number = 0
        else:
            homework_number = request.args.get('homework_number')
        
        if request.args.get('lesson_total') == None:
            lesson_total = ''
        else:
            lesson_total = request.args.get('lesson_total')

        if request.args.get('additional_materials') == None:
            additional_materials = ''
        else:
            additional_materials = request.args.get('additional_materials')

        if request.args.get('program_comments') == None:
            program_comments = ''
        else:
            program_comments = request.args.get('program_comments')


        report = Reports( course=course , grp=grp,
                lesson_type=lesson_type, teacher=teacher, lesson_theme=lesson_theme,lesson_duration=lesson_duration, lesson_date=lesson_date, homework_number=homework_number,  lesson_total=lesson_total, additional_materials=additional_materials, program_comments=program_comments)
        session.add(report)
        session.commit()
        test = session.query(Reports).filter_by(course=course).first()
        data = reports_schema.dump(test)
        print(data)

    if request.method == "POST":
        print("POST")
        try:
            course = request.form["course"]
            print(course)
        except:
            print('request')
        
        try:
            grp = request.form('grp')
            print(grp)
        except:
            print('grp')
        try:
            course = request.args('course')
            print(course)
        except:
            print('args')
        # if request.form["course"] == None:
        #     print("None")
        # else:
        #     course = request.form["course"]
        #     print(course)
        
        # grp = request.form["grp"]
        # lesson_type = request.form["lesson_type"]
        # teacher = request.form["teacher"]
        # lesson_theme = request.form["lesson_theme"]
        # lesson_duration = request.form["lesson_duration"]
        # lesson_date = request.form["lesson_date"]
        # homework_number = request.form["homework_number"]
        # lesson_total = request.form["lesson_total"]
        # additional_materials = request.form["additional_materials"]
        # program_comments = request.form["program_comments"]

        # report = Reports( course=course , grp=grp,
        #         lesson_type=lesson_type, teacher=teacher, lesson_theme=lesson_theme,lesson_duration=lesson_duration, lesson_date=lesson_date, homework_number=homework_number,  lesson_total=lesson_total, additional_materials=additional_materials, program_comments=program_comments)
        # session.add(report)
        # session.commit()
        # test = session.query(Reports).filter_by(course=course).first()
        # data = reports_schema.dump(test)
        # print(data)
        return "Post ok"
    return jsonify(data=data, message=f'Report {report.id} successfully registered'), 202

@app.route('/')
def main_template():
    return render_template('main.html')

@app.route('/reports')
def get_reports():
    reports_list = session.query(Reports).all()
    result = []
    for i in reports_list:
        report = reports_schema.dump(i)
        result.append(report)
    # try:
    #     backup.backup()
    # except:
    #     print('', end='')
    return jsonify(message='Successfully', reports=result)


@app.route("/create_user")
def create_user():
    user_name = 'user_name'
    user_telegram = 'user_telegram'
    user_login = 'user_login'
    user_password = 'user_password'
    user_role_id = 1
    user = Users(name=user_name, telegram=user_telegram,
            login=user_login, password=user_password, role_id=user_role_id)
    session.add(user)
    session.commit()
    test = session.query(Users).filter_by(name=user_name).first()
    data = user_schema.dump(test)
    return jsonify(data=data, message=f'User {user.id} successfully registered'), 202


@app.route('/users', methods=['GET'])
def get_users():
    users_list = session.query(Users).all()
    result = []
    for i in users_list:
        user = user_schema.dump(i)
        result.append(user)
    # try:
    #     backup.backup()
    # except:
    #     print('', end='')
    return jsonify(message='Successfully', users=result)


@app.route("/start")
def db_started():
    exchange = '[{"ccy":"USD","base_ccy":"UAH","buy":"39.90000","sale":"40.40000"},{"ccy":"EUR","base_ccy":"UAH","buy":"38.10000","sale":"39.10000"},{"ccy":"BTC","base_ccy":"USD","buy":"18153.0963","sale":"20063.9485"}]'

    return_message = "text out"
    return exchange

@app.route("/tmpl")
def tmpl_out():
    return_message = "text out"
    # return return_message
    return render_template('tmpl.html',text = return_message)


@app.route("/exchange")
def tmpl_exchange():
    exchange = [{"ccy":"USD","base_ccy":"UAH","buy":"39.90000","sale":"40.40000"},{"ccy":"EUR","base_ccy":"UAH","buy":"38.10000","sale":"39.10000"},{"ccy":"BTC","base_ccy":"USD","buy":"18153.0963","sale":"20063.9485"}]
    # return return_message
    return render_template('exchange.html',exchange = exchange)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, unique=True, nullable=False)
#     email = db.Column(db.String)

# @app.route("/user_create")
# def user_create():
#         user = User(
#             username='User Name',
#             email='User email',
#         )
#         db.session.add(user)
#         db.session.commit()
#         return "User created"

# @app.route("/db_create")
# def db_create():
#     db.create_all()

# with app.app_context():
#     db.create_all()

# @app.route("/users")
# def user_list():
#     users = db.session.execute(db.select(User).order_by(User.username)).scalars()
#     return render_template("user/list.html", users=users)

# @app.route("/users/create", methods=["GET", "POST"])
# def user_create():
#     if request.method == "POST":
#         user = User(
#             username=request.form["username"],
#             email=request.form["email"],
#         )
#         db.session.add(user)
#         db.session.commit()
#         return redirect(url_for("user_detail", id=user.id))

#     return render_template("user/create.html")

# @app.route("/user/<int:id>")
# def user_detail(id):
#     user = db.get_or_404(User, id)
#     return render_template("user/detail.html", user=user)

# @app.route("/user/<int:id>/delete", methods=["GET", "POST"])
# def user_delete(id):
#     user = db.get_or_404(User, id)

#     if request.method == "POST":
#         db.session.delete(user)
#         db.session.commit()
#         return redirect(url_for("user_list"))

#     return render_template("user/delete.html", user=user)
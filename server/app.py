# coding=utf-8
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from re import compile, fullmatch


regex = compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def isValid(email):
    if fullmatch(regex, email):
      return True
    else:
      return False

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    date_reg = db.Column(db.String(20))

    def __repr__(self):
        return '<User %r>' % self.nickname


class Auto(db.Model):
    __tablename__ = 'Auto'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    number = db.Column(db.String(20), unique=True)
    users_id = db.Column(db.String(20),  db.ForeignKey('User.id'))


    def __repr__(self):
        return '<Auto %r>' % self.name


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        delete = db.session.get(User, request.form['delete'])
        db.session.delete(delete)
        db.session.commit()
    items = User.query.order_by(User.id).all()
    return render_template('index.html', data=items)


@app.route('/UserEdit/<item_id>', methods=['POST', 'GET'])
def edit(item_id):
    if request.method == "POST":
        email = request.form['email']
        nickname = request.form['nickname']
        password = request.form['password']
        if isValid(email) == False or nickname=='':
            return render_template('UserEdit.html', data=db.session.get(User, item_id))
        value = db.session.get(User, item_id)
        value.email = email
        value.nickname = nickname
        value.password = password
        try:
            db.session.commit()
            return redirect('/')
        except:
            print('error')
            return render_template('UserEdit.html', data=db.session.get(User, item_id))
    else:
        return render_template('UserEdit.html', data=db.session.get(User, item_id))


@app.route('/auto',  methods=['POST', 'GET'])
def auto():
    if request.method == "POST":
        delete = db.session.get(Auto, request.form['delete'])
        db.session.delete(delete)
        db.session.commit()
    items = Auto.query.order_by(Auto.id).all()
    return render_template('auto.html', data = items)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        email = request.form['email']
        nickname = request.form['nickname']
        password = request.form['password']
        if isValid(email) == False or nickname=='':
            return redirect('/create')
        item = User(email=email, nickname=nickname, password=password, date_reg = str(date.today()))
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            print(item.email, item.nickname, item.password)
            return redirect('/create')
    else:
        return render_template('create.html')


@app.route('/GetAuto', methods=['POST', 'GET'])
def getTable():
    if request.method == "POST":
        name = request.form['name']
        number = request.form['number']
        id = request.form['id']
        if name == '' or number == '' or id == '':
            return 'error'
        item = Auto(name=name, number=number, users_id=db.session.get(User, id).id)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/auto')
        except:
            return 'Неверные входные данные'
    return render_template('GetAutoTable.html')


@app.route('/GetUser/<item_id>', methods=['POST', 'GET'])
def getUser(item_id):
    if request.method == "POST":
        item = request.form['User']
        if item =='':
            return render_template('GetUser.html', data=User.query.order_by(User.id).all())
        value = db.session.get(Auto, item_id)
        value.users_id = db.session.get(User, item).id
        try:
            db.session.commit()
            return redirect('/auto')
        except:
            return render_template('GetUser.html', data=User.query.order_by(User.id).all())
    return render_template('GetUser.html', data=User.query.order_by(User.id).all())


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    app.run(debug=False)
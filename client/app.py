from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from requests import post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class Firm(db.Model):
    __tablename__ = 'Firm'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class AutoSalon(db.Model):
    __tablename__ = 'AutoSalon'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    firma_id = db.Column(db.Integer,  db.ForeignKey('Firm.id'), nullable=False)

    def __repr__(self):
        return '<AutoSalon %r>' % self.name


class Auto(db.Model):
    __tablename__ = 'Auto'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    number = db.Column(db.String(20), unique=True, nullable=False)
    auto_market_id = db.Column(db.Integer,  db.ForeignKey('AutoSalon.id'), nullable=False)

    def __repr__(self):
        return '<Auto %r>' % self.name

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        delete = db.session.get(Firm, request.form['delete'])
        db.session.delete(delete)
        db.session.commit()
    items = Firm.query.order_by(Firm.id).all()
    return render_template('index.html', data=items)


@app.route('/CreateFirm', methods=['POST', 'GET'])
def CreateFirm():
    if request.method == "POST":
        name = request.form['name']
        if name =='':
            return redirect('/CreateFirm')
        item = Firm(name = name)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            print(item.name)
            return redirect('/CreateFirm')
    else:
        return render_template('CreateFirm.html')


@app.route('/AutoSalon', methods=['POST', 'GET'])
def AutoS():
    if request.method == "POST":
        delete = db.session.get(AutoSalon, request.form['delete'])
        db.session.delete(delete)
        db.session.commit()
    items = AutoSalon.query.order_by(AutoSalon.id).all()
    return render_template('AutoSalon.html', data=items)


@app.route('/CreateAutoSalon', methods=['POST', 'GET'])
def CreateAutoSalon():
    items = Firm.query.order_by(Firm.id).all()
    if request.method == "POST":
        name = request.form['name']
        firma_id = db.session.get(Firm, int(request.form['firma_id']))
        if name =='':
            return redirect('/CreateAutoSalon')
        item = AutoSalon(name=name, firma_id=firma_id.id)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/AutoSalon')
        except:
            return redirect('/CreateAutoSalon')
    else:
        return render_template('CreateAutoSalon.html', data=items)


@app.route('/Auto', methods=['POST', 'GET'])
def AutoTable():
    if request.method == "POST":
        delete = db.session.get(Auto, request.form['delete'])
        db.session.delete(delete)
        db.session.commit()
    items = Auto.query.order_by(Auto.id).all()
    return render_template('Auto.html', data=items)


@app.route('/CreateAuto', methods=['POST', 'GET'])
def CreateAuto():
    items = AutoSalon.query.order_by(AutoSalon.id).all()
    if request.method == "POST":
        name = request.form['name']
        number = request.form['number']
        auto_market_id = db.session.get(AutoSalon, int(request.form['auto_market_id']))
        if name =='' or number =='':
            return redirect('/CreateAuto')
        item = Auto(name=name, number=number, auto_market_id=auto_market_id.id)
        try:
            db.session.add(item)
            db.session.commit()
            data = {'name': name, 'number': number}
            post("http://127.0.0.1:5000/GetAutoTable", data=data)
            return redirect('/Auto')
        except:
            return redirect('/CreateAuto')
    else:
        return render_template('CreateAuto.html', data=items)


@app.route('/EditFirm/<int:item_id>', methods=['POST', 'GET'])
def FirmEdit(item_id):
    if request.method == "POST":
        name = request.form['name']
        item = db.session.get(Firm, item_id)
        if name =='':
            return redirect('/EditFirm/'+item_id)
        item.name = name
        try:
            db.session.commit()
            return redirect('/')
        except:
            print(item.email, item.nickname, item.password)
            return redirect('/EditFirm/'+item_id)
    else:
        return render_template('EditFirm.html', data=db.session.get(Firm, item_id))


@app.route('/EditAutoSalon/<int:item_id>', methods=['POST', 'GET'])
def EditAutoSalon(item_id):
    if request.method == "POST":
        name = request.form['name']
        firma_id = request.form['firma_id']
        item = db.session.get(AutoSalon, item_id)
        if name =='':
            return redirect('/EditAutoSalon/'+item_id)
        item.name = name
        item.firma_id = db.session.get(Firm, firma_id).id
        try:
            db.session.commit()
            return redirect('/AutoSalon')
        except:
            print(item.email, item.nickname, item.password)
            return redirect('/EditAutoSalon/'+item_id)
    else:
        return render_template('EditAutoSalon.html', data=db.session.get(AutoSalon, item_id), data2=Firm.query.order_by(Firm.id).all())


@app.route('/EditAuto/<int:item_id>', methods=['POST', 'GET'])
def EditAuto(item_id):
    if request.method == "POST":
        name = request.form['name']
        number = request.form['number']
        auto_market_id = request.form['auto_market_id']
        item = db.session.get(Auto, item_id)
        if name =='' or number=='':
            return redirect('/EditAuto/'+item_id)
        item.name = name
        item.number = number
        item.auto_market_id = db.session.get(AutoSalon, auto_market_id).id
        try:
            db.session.commit()
            return redirect('/Auto')
        except:
            print(item.email, item.nickname, item.password)
            return redirect('/EditAuto/'+item_id)
    else:
        return render_template('EditAuto.html', data=db.session.get(Auto, item_id), data2=AutoSalon.query.order_by(AutoSalon.id).all())


@app.route('/RestAuto/<int:item_id>', methods=['POST', 'GET'])
def postData(item_id):
    if request.method == "POST":
        name = db.session.get(Auto, request.form['id']).name
        number = db.session.get(Auto, request.form['id']).number
        id = item_id
        item = {'name':name,'number':number,'id':id}
        post('http://'+request.remote_addr+':5000/GetAuto', item)
        return redirect('http://127.0.0.1:5000/auto')
    return render_template('RestAuto.html', data =Auto.query.order_by(Auto.id).all(), item = item_id)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
    app.run(debug=False)
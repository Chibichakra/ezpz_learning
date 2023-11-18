from flask import Flask, request, session
from flask_login import LoginManager, login_user
from models import ExpandModel
from flask_bcrypt import Bcrypt 
from database import *
from forms import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Initialization step
with app.app_context():
    db.init_app(app)
    db.create_all()
    bcrypt = Bcrypt(app) 
    login_manager = LoginManager()
    login_manager.init_app(app)


@app.post('/api/register')
def register():
    json_data = request.get_json()
    form = RegistrationForm.from_json(json_data)
    if form.validate():
        username = json_data['username']
        password = json_data['password']
        hashed_password = bcrypt.generate_password_hash(password).decode() 

        user = User.query.filter(User.username == username).all()
        if user != []:
            return {'msg': 'User already exists!'}, 400

        
        db.session.add(User(id = uuid.uuid4(), username = username, password = hashed_password))
        db.session.commit()
    else:
        field, msg = list(form.errors.items())[0]
        return {'msg': f'{field}: {msg[0]}'}, 400


    return {'msg': 'User registered successfully!'}, 200

@app.post('/api/login')
def login():
    json_data = request.get_json()
    form = LoginForm.from_json(json_data)
    if form.validate():
        username = json_data['username']
        password = json_data['password']

        user = User.query.filter(User.username == username).all()
        if user == [] or bcrypt.check_password_hash(user[0].password, password) != True:
            return {'msg': 'Incorrect username or password!'}, 400

        login_user(user[0])

    else:
        field, msg = list(form.errors.items())[0]
        return {'msg': f'{field}: {msg[0]}'}, 400


    return {'msg': 'User logged in successfully!'}, 200

    

@app.post('/api/expand')
def expand():
    data = request.get_json()
    phrase = data.get('phrase', None)
    context = data.get('context', None)
    extra_context = data.get('extra_context', None)

    # Validations
    if phrase == None or context == None:
        return {'msg': 'Phrase and context required'}, 400

    model = ExpandModel(context = context, extra_context = extra_context)
    expanded = model.expand(phrase)

    return {'expanded': expanded}




if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
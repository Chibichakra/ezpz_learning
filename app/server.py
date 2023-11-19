from flask import Flask, request, session, render_template, redirect
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from models import ExpandModel
from flask_bcrypt import Bcrypt 
from database import *
from forms import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.environ["MYSQL_USER"]}:{os.environ["MYSQL_PASSWORD"]}@db:3306/{os.environ["MYSQL_DATABASE"]}'

# Initialization step
with app.app_context():
    db.init_app(app)
    db.create_all()
    bcrypt = Bcrypt(app) 
    login_manager = LoginManager()
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).one()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegistrationForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            hashed_password = bcrypt.generate_password_hash(password).decode()

         

            user = User.query.filter(User.email == email).all()
            if user != []:
                return render_template('register.html', error='User already exists!')

            db.session.add(User(email = email, password = password))
            db.session.commit()
        else:
            field, msg = list(form.errors.items())[0]
            return render_template('register.html', error=f'{field}: {msg[0]}')


    return redirect('login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data

            user = User.query.filter(User.email == email).all()
            # if user == [] or bcrypt.check_password_hash(user[0].password, password) != True:
            if user == [] or user[0].password != password:
                return render_template('login.html', msg='Incorrect email or password!')

            login_user(user[0])

        else:
            field, msg = list(form.errors.items())[0]
            return render_template('login.html', error=f'{field}: {msg[0]}')


    return redirect('/dashboard')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/chapter', methods=['GET'])
@login_required
def chapter():
    return render_template('chapter.html')

@app.route('/self', methods=['GET'])
@login_required
def chibi():
    return render_template('chibi.html')

    

@app.post('/api/expand')
@login_required
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
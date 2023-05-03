from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_TOKEN_LOCATION'] = ['query_string']
app.config['JWT_QUERY_STRING_NAME'] = 'access_token'
app.secret_key = secrets.token_hex(16)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    skills = db.relationship('Skill', backref='user', lazy=True)

# Skill model
class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    function = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, function, user_id):
        self.name = name
        self.function = function
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'function': self.function
        }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user:
            return render_template('login.html', message='User not found')

        if not check_password_hash(user.password, password):
            return render_template('login.html', message='Incorrect password')

        # Heslo je správné, vytvoříme access token
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token})

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect(url_for('login'))

# Dashboard route
@app.route('/dashboard')
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    skills = Skill.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', user=user, skills=skills)

@app.route('/add_skill', methods=['POST'])
@jwt_required()
def add_skill():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_skill = Skill(name=data['name'], function=data['function'], user_id=user_id)
    db.session.add(new_skill)
    db.session.commit()
    return jsonify(new_skill.serialize()), 201

@app.route('/remove_skill', methods=['POST'])
@jwt_required()
def remove_skill():
    data = request.get_json()

    if 'skill_id' not in data:
        return jsonify({'status': 'error', 'message': 'Missing skill_id'})

    user_id = get_jwt_identity()
    skill_id = data['skill_id']

    skill = Skill.query.filter_by(id=skill_id, user_id=user_id).first()
    if skill:
        db.session.delete(skill)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': f'Skill not found for skill_id: {skill_id}'})

def get_skill_by_id(skill_id):
    skill = Skill.query.filter_by(id=skill_id).first()
    if skill:
        return skill.serialize()
    else:
        return None

def update_skill(skill_id, name, function):
    skill = Skill.query.filter_by(id=skill_id).first()

    if not skill:
        return None

    skill.name = name
    skill.function = function
    db.session.commit()
    return skill.serialize()


@app.route('/get_skill', methods=['POST'])
@jwt_required()
def get_skill():
    data = request.get_json()
    skill_id = data.get('skill_id')

    if not skill_id:
        return jsonify({"status": "error", "message": "Skill ID is missing"}), 400

    skill = get_skill_by_id(skill_id)  # Zde nahraďte funkcí pro načtení dovednosti podle ID

    if skill:
        return jsonify({"status": "success", "skill": skill}), 200
    else:
        return jsonify({"status": "error", "message": "Skill not found"}), 404


@app.route('/edit_skill', methods=['POST'])
@jwt_required()
def edit_skill():
    data = request.get_json()
    name = data.get('name')
    function = data.get('function')
    skill_id = data.get('skill_id')

    if not all([name, function, skill_id]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    updated_skill = update_skill(skill_id, name, function)  # Zde nahraďte funkcí pro aktualizaci dovednosti

    if updated_skill:
        return jsonify({"status": "success", "skill": updated_skill}), 200
    else:
        return jsonify({"status": "error", "message": "Error updating skill"}), 500




if __name__ == '__main__':
    app.run(debug=False)

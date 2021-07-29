import os
from flask import Flask, jsonify, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from src.export_variables import export_envs

export_envs()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('database_url')
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

class Family_members_info(db.Model):
    member_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False) 
    last_name = db.Column(db.String, nullable=False) 
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer)
    phone_type = db.Column(db.String)

@app.route('/family-details')
def index():
    family_datas = []
    family_members = Family_members_info.query.all()
    for member in family_members:
        member_data = {
            "first_name" : member.first_name,
            "last_name" : member.last_name,
            "age" : member.age,
            "gender" : member.gender,
            "phone_number" : member.phone_number,
            "phone_type" : member.phone_type
        }
        family_datas.append(member_data)
    return jsonify(family_datas)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).one_or_none()
        if admin:
            if sha256_crypt.verify(password, admin.password):
                session['admin_id'] = admin.admin_id
                return redirect(url_for('family_member'))
    return render_template('login.html')

@app.route('/new_member', methods=['GET', 'POST'])
def family_member():
    if session.get('admin_id', None):
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            age = request.form['age']
            gender = request.form['gender']
            phone_number = request.form['phone_number']
            phone_type = request.form['phone_type']
            member = Family_members_info(
                first_name=first_name,last_name=last_name,
                age=age,gender=gender,phone_number=phone_number,
                phone_type=phone_type
            )
            db.session.add(member)
            db.session.commit()
            return "member added successful"
        return render_template('member.html')
    return redirect(url_for('admin_login'))

@app.route('/logout')
def logout():
    admin = session.get('admin_id', None)
    if admin:
        session.pop('admin_id', None)
    return redirect(url_for('admin_login'))

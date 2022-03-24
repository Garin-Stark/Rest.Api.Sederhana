#Kelompok Tugas WebService
#-Garin Irsyad Choriri 19090146 6D
#-Nurul Arifiah Gunarsih 19090085 6B
#----Login db----
#--Username & Password: 1234

from flask import Flask, jsonify, request,make_response
import os, random, string
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "poltek.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer')

class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    token = db.Column(db.String(225), unique=True, nullable=True, primary_key=False)
db.create_all()

@app.route('/add', methods=['POST'])
def add_user():
    print('Add username:')
    username = input()
    print('Add password:')
    password = input()
    data = User(username=username,password=password)
    db.session.add(data)
    db.session.commit()
    return 'Berhasil Menambahkan Data'

@app.route('/api/v1/login', methods=['POST'])
def auth():
    dataUsername = request.form.get('username')
    dataPassword = request.form.get('password')
    queryUsername = [data.username for data in User.query.all()]
    queryPassword = [data.password for data in User.query.all()]
    if dataUsername in queryUsername and dataPassword in queryPassword:
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return make_response(jsonify({"Token API":token}),200)
    return jsonify({"msg":"Mengambil Info Token Gagal"}) 

if __name__ == '__main__':
    app.run(debug=True, port=4000)
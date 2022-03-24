#6D/19090146/GarinIrsyadChoriri
#6B/19090085/NurulArifiahGunarsih
#----Login db----
#--Username & Password: 1234
from flask import Flask, jsonify, request,make_response
import os, random, string,os, random, string
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "poltek.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    token = db.Column(db.String(225), unique=True, nullable=True, primary_key=False)
db.create_all()

@app.route('/api/v1/login', methods=['POST'])
def auth():
    dataUsername = request.form.get('username')
    dataPassword = request.form.get('password')
    acc = dataUsername and dataPassword 
    if acc:
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        User.query.update({'token': token})
        db.session.commit()
        return make_response(jsonify({"Token API":token}),200)
    return jsonify({"msg":"Mengambil Info Token Gagal"}) 

@app.route('/api/v2/users/info', methods=['POST'])
def users_info():
    token = request.values.get('token')
    acc = User.query.filter_by(token=token).first()
    if acc:
        return acc.username 
    else:
        return 'salah input token'
        
if __name__ == '__main__':
    app.run(debug=True, port=4000)
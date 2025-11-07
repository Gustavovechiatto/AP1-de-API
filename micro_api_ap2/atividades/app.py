from flask import Flask
from flask_restx import Api
from database import db
from controllers_namespace import api as ns

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atividades.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app, doc='/docs', title='API Atividades')

api.add_namespace(ns, path='/atividades')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002)

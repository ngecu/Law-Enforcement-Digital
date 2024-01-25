from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .views import UserResource, IncidentResource

app = Flask(__name__)
print(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///occurrence_book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)

ma = Marshmallow(app)


api = Api(app)

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(IncidentResource, '/incidents', '/incidents/<int:incident_id>')


# Create tables
db.create_all()
app.run(debug=True)

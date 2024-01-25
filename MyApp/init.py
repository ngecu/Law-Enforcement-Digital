from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, marshal_with, fields
from flask import request, current_app as app
import jwt
from functools import wraps
import datetime
from .models import User, Incident, app,api,db
from .controllers import Register,Login,Protected,UpdateUser,IndividualUser,Incidents


api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Protected, '/protected')
api.add_resource(UpdateUser, '/update_user')
api.add_resource(IndividualUser, '/user/<int:user_id>')
api.add_resource(Incidents, '/incidents')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

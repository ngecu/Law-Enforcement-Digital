import jwt
from functools import wraps
import datetime
from flask_restful import Resource, marshal_with, fields
from flask import request, current_app as app
from .models import User, Incident, app,api,db

userFields = {
    'user_id': fields.Integer,
    'username': fields.String,
    'role': fields.String,
}

incidentFields = {
    'incident_id': fields.Integer,
    'name': fields.String,
    'accused': fields.String,
    'victim': fields.String,
    'reported_by': fields.String,
    'location': fields.String,
    'date': fields.String,
    'message': fields.String,
    'status': fields.String,
}


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            print("data is ", data)
            current_user = User.query.get(data["user_id"])
            print(current_user)

            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
        except jwt.ExpiredSignatureError:
            return {
                "message": "Token has expired",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except jwt.InvalidTokenError:
            return {
                "message": "Invalid token",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated




class Register(Resource):
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')  
        role = data.get('role', 'user')

     
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {"message": "Username already exists"}, 400

        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201


class Login(Resource):
    def post(self):
        data = request.json
        print(data)
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            # Create a JWT token
            token = jwt.encode({'user_id': user.user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                              app.config['SECRET_KEY'], algorithm='HS256')
            return {'token': token}

        return {'message': 'Invalid credentials'}, 401


class Protected(Resource):
    @marshal_with(userFields)
    @token_required
    def get(self, current_user):
        return current_user



class UpdateUser(Resource):
    @marshal_with(userFields)
    @token_required
    def put(self, current_user):
        data = request.json
        current_user.username = data.get('username', current_user.username)
        current_user.role = data.get('role', current_user.role)
        db.session.commit()
        return current_user



class IndividualUser(Resource):
    @marshal_with(userFields)
    @token_required
    def get(self, current_user, user_id):
        user = User.query.get(user_id)
        if user:
            return user
        return {'message': 'User not found'}, 404

    @token_required
    def delete(self, current_user, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}
        return {'message': 'User not found'}, 404


class Incidents(Resource):
    @marshal_with(incidentFields)
    @token_required
    def get(self,current_user):
        incidents = Incident.query.all()
        return incidents

    @marshal_with(incidentFields)
    @token_required
    def post(self,current_user):
        data = request.json
        incident = Incident(
            name=data['name'], accused=data['accused'], victim=data['victim'],
            reported_by=data['reported_by'], location=data['location'],
            date=data['date'], message=data['message'], status=data['status']
        )
        db.session.add(incident)
        db.session.commit()
        incidents = Incident.query.all()
        return incidents

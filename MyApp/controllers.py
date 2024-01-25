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

class AllUsers(Resource):
    @marshal_with(userFields)
    @token_required
    def get(self, current_user):
        print("current user is ",current_user)

        users = User.query.all()
        return users



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

    @marshal_with(userFields)
    @token_required
    def put(self, current_user,user_id):
        data = request.json
        username = data.get('username')
        password = data.get('password')  
        role = data.get('role', 'user')

        user = User.query.get(user_id)
        if user:
            user.username = username
            user.password = password
            user.role = role
            db.session.commit()
            return user
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
        name = data.get('name')
        existing_incident = Incident.query.filter_by(name=name).first()
        if existing_incident:
            return {"message": "Incident already exists"}, 400

        incident = Incident(
            name=data['name'], accused=data['accused'], victim=data['victim'],
            reported_by=data['reported_by'], location=data['location'],
            date=data['date'], message=data['message'], status=data['status']
        )
        db.session.add(incident)
        db.session.commit()
        return {"message": "Incident registered successfully"}, 201

class IndividualIncident(Resource):
    @marshal_with(incidentFields)
    @token_required
    def get(self, current_user, incident_id):
        incident = Incident.query.get(incident_id)
        if incident:
            return incident
        return {'message': 'Incident not found'}, 404

    @token_required
    def delete(self, current_user, incident_id):
        incident = Incident.query.get(incident_id)
        if incident:
            db.session.delete(incident)
            db.session.commit()
            return {'message': 'Incident deleted successfully'}
        return {'message': 'Incident not found'}, 404

    @marshal_with(incidentFields)
    @token_required
    def put(self, current_user, incident_id):
        data = request.json
        name = data.get('name')
        accused = data.get('accused')
        victim = data.get('victim')
        reported_by = data.get('reported_by')
        location = data.get('location')
        date = data.get('date')
        message = data.get('message')
        status = data.get('status')

        incident = Incident.query.get(incident_id)
        if incident:
            incident.name = name
            incident.accused = accused
            incident.victim = victim
            incident.reported_by = reported_by
            incident.location = location
            incident.date = date
            incident.message = message
            incident.status = status
            db.session.commit()
            return incident
        return {'message': 'Incident not found'}, 404
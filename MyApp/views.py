from flask_restful import Resource
from .models import User, Incident,db
from .schema import UserSchema, IncidentSchema
from flask import request

user_schema = UserSchema()
incident_schema = IncidentSchema()

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user_schema.dump(user)
            else:
                return {"message": "User not found"}, 404
        else:
            users = User.query.all()
            return user_schema.dump(users, many=True)

    def post(self):
        data = request.get_json()
        user = user_schema.load(data)
        # db.session.add(user)
        # db.session.commit()
        return user_schema.dump(user), 201

    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            data = request.get_json()
            user.username = data['username']
            user.role = data['role']
            db.session.commit()
            return user_schema.dump(user)
        else:
            return {"message": "User not found"}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, 200
        else:
            return {"message": "User not found"}, 404

class IncidentResource(Resource):
    def get(self, incident_id=None):
        if incident_id:
            incident = Incident.query.get(incident_id)
            if incident:
                return incident_schema.dump(incident)
            else:
                return {"message": "Incident not found"}, 404
        else:
            incidents = Incident.query.all()
            return incident_schema.dump(incidents, many=True)

    def post(self):
        data = request.get_json()
        incident = incident_schema.load(data)
        db.session.add(incident)
        db.session.commit()
        return incident_schema.dump(incident), 201

    def put(self, incident_id):
        incident = Incident.query.get(incident_id)
        if incident:
            data = request.get_json()
            incident.name = data['name']
            incident.accused = data['accused']
            incident.victim = data['victim']
            incident.reported_by = data['reported_by']
            incident.location = data['location']
            incident.date = data['date']
            incident.message = data['message']
            incident.status = data['status']
            db.session.commit()
            return incident_schema.dump(incident)
        else:
            return {"message": "Incident not found"}, 404

    def delete(self, incident_id):
        incident = Incident.query.get(incident_id)
        if incident:
            db.session.delete(incident)
            db.session.commit()
            return {"message": "Incident deleted successfully"}, 200
        else:
            return {"message": "Incident not found"}, 404
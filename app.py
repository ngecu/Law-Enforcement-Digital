from flask import Flask, jsonify, request, redirect, url_for, session, flash
import sqlite3
import os
from functools import wraps
import jwt

app = Flask(__name__)
SECRET_KEY = os.environ.get('SECRET_KEY') or 'abc123'
app.config['SECRET_KEY'] = SECRET_KEY

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
            print("data is ",data)
            conn = sqlite3.connect('occurrence_book.db')
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (data["user_id"],))
            current_user = cursor.fetchone()
            print(current_user)
            conn.close()

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

def create_user(username, password, role):
    print("I am creating user")
    conn = sqlite3.connect('occurrence_book.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)', (username, password, role))
    
    conn.commit()
    conn.close()



# Route for user registration
@app.route('/register', methods=['POST'])

def register_api():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data or 'role' not in data:
        return jsonify({'error': 'Invalid request format'}), 400

    username = data['username']
    password = data['password']
    role = data['role']

    create_user(username, password, role)
    return jsonify({'message': 'Registration successful!'}), 201

# Route for user login

@app.route('/login', methods=['POST'])
def login_api():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid request format'}), 400

    username = data['username']
    password = data['password']

    conn = sqlite3.connect('occurrence_book.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    conn.close()

    if user and password:
        user_dict = dict(user)
        # token should expire after 24 hrs
        user_dict["token"] = jwt.encode(
            {"user_id": user['user_id']},
            app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        return jsonify({
            "message": "Successfully Logged in",
            "data": user_dict
        }), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401



@app.route('/dashboard', methods=['GET'])
@token_required
def dashboard_api(current_user):

    conn = sqlite3.connect('occurrence_book.db')
    cursor = conn.cursor()

    # Example: Fetch incidents for the logged-in user
    cursor.execute('SELECT * FROM incidents')
    incidents = cursor.fetchall()

    conn.close()

    return jsonify({'incidents': incidents}), 200

@app.route('/add_incident', methods=['POST'])
@token_required
def add_incident_api(current_user):
    data = request.get_json()

    if not data or 'name' not in data or 'accused' not in data or 'victim' not in data \
            or 'reported_by' not in data or 'location' not in data or 'date' not in data \
            or 'message' not in data or 'status' not in data:
        return jsonify({'error': 'Invalid request format'}), 400

    name = data['name']
    accused = data['accused']
    victim = data['victim']
    reported_by = data['reported_by']
    location = data['location']
    date = data['date']
    message = data['message']
    status = data['status']

    conn = sqlite3.connect('occurrence_book.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO incidents (name, accused, victim, reported_by, location, date, message, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (name, accused, victim, reported_by, location, date, message, status))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Incident added successfully!'}), 201

@app.route('/update_incident/<int:incident_id>', methods=['PUT'])
@token_required
def update_incident_api(current_user,incident_id):
    data = request.get_json()
    print("data is ",data)

    if not data or 'name' not in data or 'accused' not in data or 'victim' not in data \
            or 'reported_by' not in data or 'location' not in data or 'date' not in data \
            or 'message' not in data or 'status' not in data:
        return jsonify({'error': 'Invalid request format'}), 400

    name = data['name']
    accused = data['accused']
    victim = data['victim']
    reported_by = data['reported_by']
    location = data['location']
    date = data['date']
    message = data['message']
    status = data['status']

    conn = sqlite3.connect('occurrence_book.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE incidents SET name=?, accused=?, victim=?, reported_by=?, location=?, date=?, message=?, status=? WHERE incident_id=?',
                   (name, accused, victim, reported_by, location, date, message, status, incident_id))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Incident updated successfully!'}), 200

@app.route('/delete_incident/<int:incident_id>', methods=['DELETE'])
@token_required
def delete_incident_api(current_user,incident_id):
    conn = sqlite3.connect('occurrence_book.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM incidents WHERE incident_id=?', (incident_id,))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Incident deleted successfully!'}), 200


@app.route('/incident/<int:incident_id>', methods=['GET'])
@token_required
def get_incident_api(current_user,incident_id):
    conn = sqlite3.connect('occurrence_book.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM incidents WHERE incident_id = ?', (incident_id,))
    incident = cursor.fetchone()

    conn.close()

    if incident:
        return jsonify({'incident': incident}), 200
    else:
        return jsonify({'error': 'Incident not found'}), 404
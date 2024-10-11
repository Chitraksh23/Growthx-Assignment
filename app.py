from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['assignment_portal']
users = db['users']
assignments = db['assignments']
# Serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')
# Register User
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if users.find_one({'username': data['username']}):
        return jsonify({'error': 'User already exists'}), 400
    password_hash = generate_password_hash(data['password'])
    users.insert_one({
        'username': data['username'],
        'password': password_hash,
        'role': data['role']  # 'admin' or 'user'
    })
    return jsonify({'message': 'User registered successfully'})
# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = users.find_one({'username': data['username']})
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Invalid credentials'}), 400
    return jsonify({'message': f'Welcome {user["username"]}', 'role': user['role']})
# Upload Assignment (User)
@app.route('/upload', methods=['POST'])
def upload_assignment():
    data = request.json
    assignments.insert_one({
        'userId': data['userId'],
        'task': data['task'],
        'admin': data['admin'],
        'status': 'pending'
    })
    return jsonify({'message': 'Assignment uploaded successfully'})
# Get Admins List
@app.route('/admins', methods=['GET'])
def get_admins():
    admin_list = users.find({'role': 'admin'}, {'_id': 0, 'username': 1})
    return jsonify(list(admin_list))
# View Assignments (Admin)
@app.route('/assignments', methods=['GET'])
def view_assignments():
    admin = request.args.get('admin')
    admin_assignments = assignments.find({'admin': admin})
    response = [{
        'id': str(assignment['_id']),
        'userId': assignment['userId'],
        'task': assignment['task'],
        'status': assignment['status']
    } for assignment in admin_assignments]
    return jsonify(response)
# Accept or Reject Assignment
@app.route('/assignments/<id>/<action>', methods=['POST'])
def modify_assignment(id, action):
    if action not in ['accept', 'reject']:
        return jsonify({'error': 'Invalid action'}), 400
    assignment = assignments.find_one({'_id': ObjectId(id)})
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404

    assignments.update_one({'_id': ObjectId(id)}, {'$set': {'status': action}})
    return jsonify({'message': f'Assignment {action}ed successfully'})
if __name__ == '__main__':
    app.run(debug=True)

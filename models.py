from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['assignment_portal']
# Collections
users = db['users']
admins = db['admins']
assignments = db['assignments']

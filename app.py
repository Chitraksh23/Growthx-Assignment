from flask import Flask
from routes import user_routes, admin_routes
from flask_jwt_extended import JWTManager
app = Flask(__name__)
# Configurations
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)
# Register Blueprints
app.register_blueprint(user_routes)
app.register_blueprint(admin_routes)
if __name__ == "__main__":
    app.run(debug=True)

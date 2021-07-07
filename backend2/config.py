from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from routes import theme

from database.db import initialize_db

app = Flask(__name__, template_folder="template")
app.config["JWT_SECRET_KEY"] = "super-secret"

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config["MONGODB_SETTINGS"] = {"host": "mongodb://localhost:27017/Users"}
initialize_db(app)

app.register_blueprint(theme)

from flask import Flask
from flask_cors import CORS
from config import Config
from models import db, Contact
from routes import main
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)
Swagger(app)  # Initialiser Flasgger

app.register_blueprint(main)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Bienvenue dans ton application CRM !"

if __name__ == '__main__':
    app.run(debug=True)
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

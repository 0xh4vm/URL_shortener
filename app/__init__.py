from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_socketio import SocketIO
from config import Config
from app.jinja_functions import *


db = SQLAlchemy()
migrate = Migrate()
# socketio = SocketIO()

def register_blueprints(app):
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin/')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    # socketio.init_app(app, message_queue="redis://")

    register_blueprints(app)

    app.jinja_env.globals.update(randomword=randomword)

    return app
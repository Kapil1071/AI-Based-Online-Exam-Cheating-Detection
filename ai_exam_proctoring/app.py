from routes.monitor_routes import monitor_bp
from routes.auth_routes import login_manager
from routes.home_routes import home_bp

from flask import Flask

from database.db import db
from config import Config

from routes.auth_routes import auth_bp
from routes.exam_routes import exam_bp
from routes.detection_routes import detection_bp
from routes.admin_routes import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    app.register_blueprint(home_bp)
    app.register_blueprint(monitor_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(detection_bp)
    app.register_blueprint(admin_bp)

    return app


app = create_app()

if __name__ == "__main__":
    import os
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")

import os
from urllib.parse import quote_plus

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    db_password = quote_plus(os.getenv("DB_PASSWORD", ""))

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://"
        f"{os.getenv('DB_USER')}:{db_password}"
        f"@{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '3306')}/"
        f"{os.getenv('DB_NAME')}"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes import api
    app.register_blueprint(api)

    @app.route("/health")
    def health():
        return {
            "status": "success",
            "message": "Financial Risk & Fraud Detection API is running"
        }

    return app
import json
import os
from msilib import schema
from pathlib import Path

from flask import Flask
from flask_migrate import Migrate

from api import api
from api.config import config
from api.models import db


def create_app():
    """アプリケーションインスタンスを作成する関数"""
    """戻り値はインスタンスapp"""
    config_name = os.environ.get("CONFIG", "local")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config_json_path = Path(__file__).parent / "config" / "json-schemas"
    for p in config_json_path.glob("*.json"):
        with open(p) as f:
            json_name = p.stem
            schmea = json.load(f)
        app.config[json_name] = schema
    db.init_app(app)
    return app


app = create_app()
# DBマイグレーションの作成
Migrate(app, db)

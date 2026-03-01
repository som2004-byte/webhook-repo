from flask import Flask
from app.webhook.routes import webhook_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(webhook_blueprint)
    return app

#demo setup for webhook receiver
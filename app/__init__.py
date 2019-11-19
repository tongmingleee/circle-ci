import os

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

from app import routes
from app.health import health


def create_app():
    app = Flask(__name__)
    app.config["SENTRY_DSN"] = os.environ.get("SENTRY_DSN")

    # initialize sentry
    sentry_sdk.init(dsn=app.config["SENTRY_DSN"], integrations=[FlaskIntegration()])

    # register blueprints
    app.register_blueprint(health.bp)
    app.register_blueprint(routes.bp)
    return app

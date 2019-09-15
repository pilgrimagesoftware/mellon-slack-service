__author__ = "Paul Schifferer <paul@schifferers.net>"

from flask import Flask, make_response, render_template, g
# from flask_locale import Locale, _
import logging
import os
from mellon_common import constants, exceptions
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
# from prometheus_flask_exporter import PrometheusMetrics
import dotenv
import json
from mellon_app_core import helpers as core_helpers
from . import routes
from .routes import identity, main, status


def create_app():
    # Define the WSGI application object
    app = Flask(__name__)

    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    core_helpers.setup_app(app=app,
                           env_path=env_path,
                           blueprint_modules=[routes.blueprint])

    return app

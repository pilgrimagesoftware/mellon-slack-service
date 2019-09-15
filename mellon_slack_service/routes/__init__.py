__author__ = "Paul Schifferer <paul@schifferers.net>"

from flask import Blueprint, make_response, render_template, g
import json

# Define the blueprint: 'slack', set its url prefix: app.url/slack
blueprint = Blueprint("slack", __name__, url_prefix="/slack")
# metrics = g["metrics"]

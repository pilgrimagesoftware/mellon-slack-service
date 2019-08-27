__author__ = "Paul Schifferer <paul@schifferers.net>"

# Import flask dependencies
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for,
)

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
# from app import db
from app.core import worker
from app.mod_slack import helpers

# Import other modules
import json
import logging


# Define the blueprint: 'slack', set its url prefix: app.url/github
slack = Blueprint("slack", __name__, url_prefix="/slack")


# Set the route and accepted methods
@slack.route("/interact", methods=["POST"])
def interact():
    logging.debug(f"/interact request: {request.form}")

    r = {"text": f"Done."}

    try:
        payload = json.loads(request.form["payload"])
        logging.debug(f"payload: {payload}")
        # worker.merge_pull_request(payload)
    except:
        logging.exception(
            "Error while trying to process button interaction from Slack."
        )

    return json.dumps(r)


@slack.route("/events", methods=["POST"])
def events():
    logging.debug(f"/events request: {request.json}")

    r = {}

    try:
        payload = request.json
        logging.debug(f"payload: {payload}")

        # check for event API setup challenge
        challenge = payload.get("challenge")
        if challenge:
            r = {"challenge": f"{challenge}"}
        else:

            helpers.validate_request(payload)

    except:
        logging.exception(
            "Error while trying to process button interaction from Slack."
        )

    return json.dumps(r)

__author__ = "Paul Schifferer <paul@schifferers.net>"

from flask import Blueprint, current_app, request
import json
from . import helpers

# Define the blueprint: 'slack', set its url prefix: app.url/github
blueprint = Blueprint("slack", __name__, url_prefix="/slack")

# Set the route and accepted methods
@blueprint.route("/interact", methods=["POST"])
def interact():
    current_app.logger.debug(f"/interact request: {request.form}")

    r = {"text": f"Done."}

    try:
        payload = json.loads(request.form["payload"])
        current_app.logger.debug(f"payload: {payload}")
        # worker.merge_pull_request(payload)
    except:
        current_app.logger.exception(
            "Error while trying to process button interaction from Slack."
        )

    return json.dumps(r)


@blueprint.route("/events", methods=["POST"])
def events():
    current_app.logger.debug(f"/events request: {request.json}")

    r = {}

    try:
        payload = request.json
        current_app.logger.debug(f"payload: {payload}")

        # check for event API setup challenge
        challenge = payload.get("challenge")
        if challenge:
            r = {"challenge": f"{challenge}"}
        else:

            helpers.validate_request(payload)

    except:
        current_app.logger.exception(
            "Error while trying to process button interaction from Slack."
        )

    return json.dumps(r)

__author__ = "Paul Schifferer <paul@schifferers.net>"

from flask import Blueprint, make_response, render_template, g, current_app, request
import json
from . import blueprint
from .. import helpers

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

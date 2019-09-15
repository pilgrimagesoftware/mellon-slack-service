__author__ = "Paul Schifferer <paul@schifferers.net>"

from flask import Blueprint, make_response, render_template, g, current_app, request
import json
from . import blueprint


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

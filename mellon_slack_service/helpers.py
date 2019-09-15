__author__ = "Paul Schifferer <paul@schifferers.net>"

from flask import current_app
from mellon_common import exceptions


def validate_request(request):
    # check app ID
    app_id = request.get("api_app_id")
    if app_id is None or app_id != config.SLACK_APP_ID:
        raise exceptions.InvalidAppIDException()


def is_mention(message_tokens):
    current_app.logger.debug("Checking if message tokens contain a mention.")
    if len(message_tokens) == 0:
        current_app.logger.debug("No message tokens provided for mention check.")
        return False
    first_token = message_tokens[0].strip()
    result = re.match("^\\<\\@(\\S+)\\>\\S*$", first_token)
    current_app.logger.debug("result: {}".format(result))
    if result is None:
        current_app.logger.debug(
            "Regular expression match for user ID failed for token '{}'.".format(
                first_token
            )
        )
        return False
    user_id = result.group(1)
    current_app.logger.debug("user_id: {}".format(user_id))
    return user_id == my_identity


def is_im(event):
    current_app.logger.debug("Checking if event is on an IM channel.")
    if event is None or type(event) is not dict:
        current_app.logger.debug(
            "Event provided for IM check was empty or not a dictionary."
        )
        return False
    if "channel" in event and "user" in event and "text" in event:
        channel_id = event["channel"]
        user_id = event["user"]
        text = event["text"]

        # list of (channel_id, user_id) tuples
        im_channels = load_im_channels()
        current_app.logger.debug("im_channels: {}".format(im_channels))

        for c, u in im_channels:
            if channel_id == c and user_id == u:
                current_app.logger.debug("Found a matching IM channel with the user.")
                return True

    return False

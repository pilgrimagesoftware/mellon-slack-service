__author__ = "Paul Schifferer <paul@schifferers.net>"

from flask import current_app
from slack import WebClient
from mellon_common import constants
import os


class SlackBot(object):
    client = None
    user_cache = {}

    def __init__(self):
        self.client = WebClient(
            token=os.environ[constants.SLACK_BOT_OAUTH_ACCESS_TOKEN_ENV]
        )
        current_app.logger.debug(f"client={self.client}")

    def get_users(self):
        response = self.client.api_call("users.list")
        current_app.logger.debug(f"response={type(response)}, {response}")

        # if "members" in response:
        try:
            for m in response["members"]:
                current_app.logger.debug(f"m={m}")

                uid = m["id"]
                if m["is_bot"] or m["deleted"]:
                    current_app.logger.info(f"Skipping bot or deleted user {uid}.")
                    continue
                self.user_cache[uid] = {"user_name": m}

            current_app.logger.debug(f"user_cache: {self.user_cache}")
            current_app.logger.info(
                f"Loaded {len(self.user_cache)} user(s) from Slack."
            )
            return True
        except:
            current_app.logger.exception(
                f"Unexpected response from users.list call: {response}"
            )
            return False

    def find_user_id_for(self, user_name):
        current_app.logger.debug(f"user_cache: {self.user_cache}")
        for uid, user in self.user_cache.items():
            if user["user_name"] == user_name:
                return uid

        return None

    def send_message(self, user, message, attachments=None):
        current_app.logger.debug(f"user: {user}, message: {message}")

        # get user ID
        user_id = self.find_user_id_for(user)
        if user_id is None:
            # refresh the user list if the user wasn't found, just in case they're new
            self.get_users()
            user_id = self.find_user_id_for(user)
        if user_id is None:
            current_app.logger.error(f"User not found for username '{user}'")
            return

        # send message
        response = self.client.api_call("conversations.open", users=[user_id])
        if "channel" in response and "id" in response["channel"]:
            channel_id = str(response["channel"]["id"])
        else:
            current_app.logger.error(
                f"Unexpected response from conversations.open call: {response}"
            )
            return

        response = self.client.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=message,
            attachments=attachments,
        )
        if "ok" in response and response["ok"]:
            current_app.logger.info(f"Message sent to user {user}.")
            return True
        else:
            current_app.logger.error(
                f"Failed to send message to user {user}: {response}"
            )
            return False

    # def load_members(self):
    #     current_app.logger.info("Requesting team member list...")
    #     members = self.client.api_call("users.list")
    #     current_app.logger.info("Got {} members.".format(len(members)))

    #     name_to_user_id_map = {}
    #     user_id_to_name_map = {}

    #     for m in members:
    #         if "name" in m and "id" in m:
    #             name = m.get("name")
    #             user_id = m.get("id")
    #             name_to_user_id_map[name] = user_id
    #             user_id_to_name_map[user_id] = name

    #     return members, name_to_user_id_map, user_id_to_name_map

    def load_im_channels(self):
        current_app.logger.info("Requesting IM channels...")
        c = self.client.api_call("im.list")
        current_app.logger.debug("IM channels: {}".format(c))

        if "ims" not in c:
            return []
        channels = c["ims"]

        ims = []
        for im in channels:
            if "id" in im and "user" in im:
                t = (im["id"], im["user"])
                ims.append(t)

        return ims

    def load_identity(self):
        current_app.logger.info("Requesting auth.test to get user identity...")
        info = self.client.api_call("auth.test")
        current_app.logger.debug("info: {}".format(info))
        return info.get("user_id")

    def get_user(self, user_id):
        current_app.logger.debug("Getting user for ID {}".format(user_id))
        user = self.user_cache.get(user_id)
        current_app.logger.debug("user: {}".format(user))
        if user is not None:
            current_app.logger.debug("Returning cached user: {}".format(user))
            return user

        current_app.logger.info("Requesting user info for ID {}...".format(user_id))
        info = self.client.api_call("users.info", user=user_id)
        current_app.logger.debug("info: {}".format(info))
        if "user" in info:
            user = info["user"]
            user_cache[user_id] = user
            return user

        return None

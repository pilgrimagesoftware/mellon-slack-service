__author__ = "Paul Schifferer <paul@schifferers.net>"


from slack import WebClient
from app.common import constants
import os
import logging


class SlackBot(object):
    client = None
    user_cache = {}

    def __init__(self):
        self.client = WebClient(
            token=os.environ[constants.SLACK_BOT_OAUTH_ACCESS_TOKEN_ENV]
        )
        logging.debug(f"client={self.client}")

    def get_users(self):
        response = self.client.api_call("users.list")
        logging.debug(f"response={type(response)}, {response}")

        # if "members" in response:
        try:
            for m in response["members"]:
                logging.debug(f"m={m}")

                uid = m["id"]
                if m["is_bot"] or m["deleted"]:
                    logging.info(f"Skipping bot or deleted user {uid}.")
                    continue
                self.user_cache[uid] = {"user_name": m}

            logging.debug(f"user_cache: {self.user_cache}")
            logging.info(f"Loaded {len(self.user_cache)} user(s) from Slack.")
            return True
        except:
            logging.exception(f"Unexpected response from users.list call: {response}")
            return False

    def find_user_id_for(self, user_name):
        logging.debug(f"user_cache: {self.user_cache}")
        for uid, user in self.user_cache.items():
            if user["user_name"] == user_name:
                return uid

        return None

    def send_message(self, user, message, attachments=None):
        logging.debug(f"user: {user}, message: {message}")

        # get user ID
        user_id = self.find_user_id_for(user)
        if user_id is None:
            # refresh the user list if the user wasn't found, just in case they're new
            self.get_users()
            user_id = self.find_user_id_for(user)
        if user_id is None:
            logging.error(f"User not found for username '{user}'")
            return

        # send message
        response = self.client.api_call("conversations.open", users=[user_id])
        if "channel" in response and "id" in response["channel"]:
            channel_id = str(response["channel"]["id"])
        else:
            logging.error(
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
            logging.info(f"Message sent to user {user}.")
            return True
        else:
            logging.error(f"Failed to send message to user {user}: {response}")
            return False

    # def load_members(self):
    #     logging.info("Requesting team member list...")
    #     members = self.client.api_call("users.list")
    #     logging.info("Got {} members.".format(len(members)))

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
        logging.info("Requesting IM channels...")
        c = self.client.api_call("im.list")
        logging.debug("IM channels: {}".format(c))

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
        logging.info("Requesting auth.test to get user identity...")
        info = self.client.api_call("auth.test")
        logging.debug("info: {}".format(info))
        return info.get("user_id")

    def get_user(self, user_id):
        logging.debug("Getting user for ID {}".format(user_id))
        user = self.user_cache.get(user_id)
        logging.debug("user: {}".format(user))
        if user is not None:
            logging.debug("Returning cached user: {}".format(user))
            return user

        logging.info("Requesting user info for ID {}...".format(user_id))
        info = self.client.api_call("users.info", user=user_id)
        logging.debug("info: {}".format(info))
        if "user" in info:
            user = info["user"]
            user_cache[user_id] = user
            return user

        return None

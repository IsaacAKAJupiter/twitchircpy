class Message():

    """
    Class used for storing information sent from the PRIVMSG command from the IRC.
    Created for ease of use for the user.
    Should not be manually created in most cases.

    Parameters
    ==========
    channel -> :str:
        The channel that the message got sent to.
    user -> :str:
        The user's name that sent the message.
    content -> :str:
        The content of the message that got sent.
        AKA what the user sent to the channel.
    params -> :dict<str, str>:
        A dictionary of parameters sent with the IRC command.
        Note, key: "has_me" indicates if the user used /me.
    """

    def __init__(self, channel, user, content, params):
        self.channel = channel
        self.user = user
        self.content = content
        self.badges = params["badges"] if "badges" in params else None
        self.bits = int(params["bits"]) if "bits" in params else None
        self.color = params["color"] if "color" in params else None
        self.display_name = params["display-name"] if "display-name" in params else None
        self.emotes = params["emotes"] if "emotes" in params else None
        self.id = params["id"] if "id" in params else None
        self.mod = int(params["mod"]) if "mod" in params else None
        self.room_id = int(params["room-id"]) if "room-id" in params else None
        self.tmi_sent_ts = int(
            params["tmi-sent-ts"]) if "tmi-sent-ts" in params else None
        self.user_id = int(params["user-id"]) if "user-id" in params else None
        self.has_me = params["has_me"]

    def __repr__(self):
        return f"Message(channel: {self.channel}, user: {self.user}, content: {self.content})"


class Info(Message):

    """
    This class is the exact same as class:Message: except with a different name.
    Created for simpler command usage.
    Should not be manually created in most cases.
    """

    def __repr__(self):
        return f"Info(channel: {self.channel}, user: {self.user}, content: {self.content})"

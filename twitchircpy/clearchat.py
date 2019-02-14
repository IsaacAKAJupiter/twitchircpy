class ClearChat():

    """
    Class used for storing information sent from the CLEARCHAT command from the IRC.
    CLEARCHAT is the IRC command for someone being banned from a channel or from a chat being cleared.
    Note, Twitch occasionally does not send the ban reason even if it should.
    Should not be manually created in most cases.

    Parameters
    ==========
    channel -> :str:
        The channel that CLEARCHAT got sent to.
    user -> :str: | :None:
        The user that got banned.
        Can be :None: if it was a chat being cleared. 
    params -> :dict<str, str>:
        A dictionary of parameters sent with the command.
        These parameters are:
            ban_duration (length of ban),
            ban_reason (reason for ban),
            room_id (chatroom that got cleared),
            target_msg_id (message that got deleted when someone got banned?)
            tmi_sent_ts (Unix time (Epoch time) that the chat got cleared)
    """

    def __init__(self, channel, user = None, params = None):
        self.channel = channel
        self.user = user
        self.ban_duration = int(params["ban-duration"]) if "ban-duration" in params else "Permanent" if self.user else None
        self.ban_reason = params["ban-reason"] if "ban-reason" in params else None
        self.room_id = int(params["room-id"]) if "room-id" in params else None
        self.target_msg_id = params["target-msg-id"] if "target-msg-id" in params else None
        self.tmi_sent_ts = int(params["tmi-sent-ts"]) if "tmi-sent-ts" in params else None

    def __repr__(self):
        return f"ClearChat(channel: {self.channel}, user: {self.user}, duration: {self.ban_duration}, reason: {self.ban_reason})"

    def to_ban(self):
        return Ban(self.channel, self.user, [self.ban_duration, self.ban_reason])

class Ban(ClearChat):

    """
    This class is the exact same as class:ClearChat: except with a different name.
    Created for CLEARCHAT commands which are specifically for bans.
    Should not be manually created in most cases.
    """

    def __repr__(self):
        return f"Ban(channel: {self.channel}, user: {self.user}, duration: {self.ban_duration}, reason: {self.ban_reason})"
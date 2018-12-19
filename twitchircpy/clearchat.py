class ClearChat():

    """
    Class used for storing information sent from the CLEARCHAT command from the IRC.
    CLEARCHAT is the IRC command for someone being banned from a channel.
    Note, Twitch occasionally does not send the ban reason even if it should.
    Should not be manually created.

    Parameters
    ==========
    channel -> :str:
        The Twitch channel name that CLEARCHAT got sent to.
    user -> :str:
        The user that got banned.
        This is the user's display name.
    params -> :dict<str, str>:
        A dictionary of parameters sent with the command.
        These parameters are:
            ban_duration (length of ban),
            ban_reason (reason for ban)
    """

    def __init__(self, channel, user, params):
        self.channel = channel
        self.user = user
        self.ban_duration = params["ban-duration"] if "ban_duration" in params else "Permanent"
        self.ban_reason = params["ban-reason"] if "ban-reason" in params else None

    def __repr__(self):
        return f"ClearChat(channel: {self.channel}, user: {self.user}, duration: {self.ban_duration}, reason: {self.ban_reason})"

    def to_ban(self):
        return Ban(self.channel, self.user, [self.ban_duration, self.ban_reason])

class Ban(ClearChat):

    """
    This class is the exact same as class:ClearChat: except with a different name.
    Created for users who might prefer seeing/using Ban instead of ClearChat.
    Should not be manually created.
    """

    def __repr__(self):
        return f"Ban(channel: {self.channel}, user: {self.user}, duration: {self.ban_duration}, reason: {self.ban_reason})"
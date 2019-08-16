class JoinChannel():

    """
    Class used for storing information sent from the JOIN command from the IRC.
    Used for when a user joins a channel.
    Note, usually sent in chunks.
    Should not be manually created in most cases.

    Parameters
    ==========
    user -> :str:
        The user's name that joined the channel.
    channel -> :str:
        The channel that the user joined.
    """

    def __init__(self, user, channel):
        self.user = user
        self.channel = channel

    def __repr__(self):
        return f"JoinChannel(user: {self.user}, channel: {self.channel})"

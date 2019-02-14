class Mode():

    """
    Class used for storing information sent from the MODE command from the IRC.
    Used for when a user gains/loses moderator status in a channel.
    Note, usually sent in chunks and usually users who have been moderators for a while/lost it a while ago.
    Use for real-time moderation gain/loss knowing the above note.
    Should not be manually created in most cases.
    
    Parameters
    ==========
    channel -> :str:
        The channel that the user gained/lost moderator status in.
    user -> :str:
        The user's name that gained/lost moderator status.
    gain -> :bool:
        Whether or not the user gained moderator status.
        True if gained, False if lost.
    """

    def __init__(self, channel, user, gain):
        self.channel = channel
        self.user = user
        self.gain = gain
    
    def __repr__(self):
        return f"Mode(channel: {self.channel}, user: {self.user}, gain: {self.gain})"
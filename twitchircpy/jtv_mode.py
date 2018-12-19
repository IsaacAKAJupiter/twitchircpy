class Mode():

    """
    Class used for storing information sent from the MODE command from the IRC.
    Used for when a user loses gains/loses moderator status in a channel.
    Note, usually sent in chunks and usually users who have been moderators for a while/lost it a while ago.
    Use for real-time moderation gain/loss knowing the above note.
    Should not be manually created.
    
    Parameters
    ==========
    channel -> :str:
        The channel that the user gained/lost moderator status.
        This is the channel's name/handle.
    user -> :str:
        The user that gained/lost moderator status.
        This is the user's name.
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
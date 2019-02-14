class PartChannel():

    """
    Class used for storing information sent from the PART command from the IRC.
    Used for when a user parts a channel.
    Note, usually sent in chunks.
    Should not be manually created in most cases.
    
    Parameters
    ==========
    user -> :str:
        The user's name that parted the channel.
    channel -> :str:
        The channel that the user parted.
    """

    def __init__(self, user, channel):
        self.user = user
        self.channel = channel

    def __repr__(self):
        return f"PartChannel(user: {self.user}, channel: {self.channel})"
class HostTarget():

    """
    Class used for storing information sent from the HOSTTARGET command from the IRC.
    Used for when a channel starts or stops host mode.
    Should not be manually created.
    
    Parameters
    ==========
    target -> :str:
        The target Twitch channel that got hosted/unhosted.
        This is the channel's name/handle.
    channel -> :str:
        The Twitch channel name that started/stopped hosting.
    viewers -> Optional[:int: | :None:]
        The amount of viewers watching the host.
        Can be None if not sent by Twitch.
    """

    def __init__(self, target, channel, viewers = None):
        self.target = target
        self.channel = channel
        self.viewers = viewers

    def __repr__(self):
        return f"HostTarget(channel: {self.channel}, target: {self.target}, viewers: {self.viewers})"
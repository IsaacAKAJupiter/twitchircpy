class RoomState():

    """
    Class used for storing information sent from the ROOMSTATE command from the IRC.
    Used for when a room setting is changed.
    Note, all parameters could be :None: since when testing, Twitch would not send some parameters occasionally.
    Should not be manually created in most cases.

    Parameters
    ==========
    broadcaster_lang -> Optional[:str: | :None:]
        Chat language when broadcaster language mode is enabled.
        Could be :None: if a language is not set.
        Examples: en (English) and fi (Finnish).
    emote_only -> Optional[:int: | :None:]
        Whether or not emote-only chat is enabled.
        Possible values: 0 (disabled) and 1 (enabled).
    followers_only -> Optional[:int: | :None:]
        Whether or not followers-only chat is enabled.
        Possible values: -1 (disabled) and 0 (any followers).
        Also could be a non-negative int, meaning users that
        have been following for at least the specific amount
        of minutes can chat.
    r9k -> Optional[:int: | :None:]
        Whether or not R9K mode is enabled.
        Possible values: 0 (disabled) and 1 (enabled).
        If enabled, messages with more than 9 characters must
        be unique.
    slow -> Optional[:int: | :None:]
        Number of seconds chatters without moderator privileges
        have to wait between sending messages.
    subs_only -> Optional[:int: | :None:]
        Whether or not subscribers-only chat is enabled.
        Possible values: 0 (disabled) and 1 (enabled).
    """

    def __init__(self, params):
        self.broadcaster_lang = params["broadcaster-lang"] if "broadcaster-lang" in params else None
        self.emote_only = int(params["emote-only"]
                              ) if "emote-only" in params else None
        self.followers_only = int(
            params["followers-only"]) if "followers-only" in params else None
        self.r9k = int(params["r9k"]) if "r9k" in params else None
        self.slow = int(params["slow"]) if "slow" in params else None
        self.subs_only = int(params["subs-only"]
                             ) if "subs-only" in params else None
        self.channel = params["channel"] if "channel" in params else None

    def __repr__(self):
        return f"RoomState(channel: {self.channel})"

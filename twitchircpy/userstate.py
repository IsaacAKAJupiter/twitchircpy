class UserState:

    """
    Class used for storing information sent from the USERSTATE command from the IRC.
    USERSTATE is the IRC command for when a user joins a channel or sends a message to a channel.
    From testing, it's sporadic for when it sends. Assume it sends once per user.
    Should not be manually created.

    Parameters
    ==========
    params -> :dict<str, str>:
        A dictionary of parameters sent with the command.
        Note, most parameters can be :None: as well as :str:.
        These parameters include:
            badges (chat badges and versions of each badge),
            channel (channel user joined/sent a message to),
            color (user's chat color),
            display_name (user's display name),
            emotes (user's emote set),
            mod (1 if moderator, 0 if not)
    """

    def __init__(self, params):
        self.badges = params["badges"] if "badges" in params else None
        self.channel = params["channel"] if "channel" in params else None
        self.color = params["color"] if "color" in params else None
        self.display_name = params["display-name"] if "display-name" in params else None
        self.emotes = params["emotes"] if "emotes" in params else None
        self.mod = params["mod"] if "mod" in params else None

    def __repr__(self):
        return f"UserState(channel: {self.channel}, user: {self.display_name})"


class GlobalUserState(UserState):

    """
    This class is the very similar to class:UserState: except with a different name, a few more parameters and sent from the GLOBALUSERSTATE command instead of USERSTATE.
    Not completely sure what this is used for, since I never received it during testing. Assume it is for Twitch staff/admins.
    Note, channel will always be :None: and emotes will always be :None:.
    Should not be manually created.

    New "params" Parameters
    =======================
    emote_sets (emotes belonging to one or more emote sets.),\n
    user_id (the user's ID)
    """

    def __init__(self, params):
        super().__init__(params)
        self.emote_sets = params["emote-sets"] if "emote-sets" in params else None
        self.user_id = params["user-id"] if "user-id" in params else None
        self.channel = None
        self.emotes = None

    def __repr__(self):
        return f"GlobalUserState(user: {self.display_name})"
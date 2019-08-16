class ClearMsg():

    """
    Class used for storing information sent from the CLEARMSG command from the IRC.
    CLEARMSG is the IRC command for a single message being removed/cleared.
    Should not be manually created in most cases.

    Parameters
    ==========
    channel -> :str:
        The channel that CLEARMSG got sent to.
    message -> :str:
        The message that got removed/cleared.
    params -> :dict<str, str>:
        A dictionary of parameters sent with the command.
        These parameters are:
            login (name of the user who sent the message),
            target_msg_id (UUID of the message)
    """

    def __init__(self, channel, message, params):
        self.channel = channel
        self.message = message
        self.login = params["login"] if "login" in params else None
        self.target_msg_id = params["target-msg-id"] if "target-msg-id" in params else None

    def __repr__(self):
        return f"ClearMsg(channel: {self.channel}, message: {self.message}, login: {self.login}, target_msg_id: {self.target_msg_id})"

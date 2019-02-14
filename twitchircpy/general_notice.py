class Notice():

    """
    Class used for storing information sent from the NOTICE command from the IRC.
    Used for general notices from Twitch.
    Example: A channel's chat goes into slow mode.
    Should not be manually created in most cases.
    
    Parameters
    ==========
    msg_id -> :str:
        The message ID string for the notice.
        All msg_id's can be found at the link below.
        https://dev.twitch.tv/docs/irc/msg-id/
    channel -> :str:
        The channel that NOTICE got sent to.
    room -> :str: | :None:
        The chat room that NOTICE got sent to.
        Can be :None: if the notice is just for a channel.
        A channel can have multiple chat rooms, so this is incase
        one of the chat rooms got sent a notice.
        More chat room information below. (First Paragraph)
        https://dev.twitch.tv/docs/irc/chat-rooms/#overview
    message -> :str:
        The message sent by Twitch.
        AKA the full description of the notice.
    """

    def __init__(self, msg_id, channel, room, message):
        self.msg_id = msg_id
        self.channel = channel
        self.room = room
        self.message = message

    def __repr__(self):
        return f"Notice(msg_id: {self.msg_id}, channel: {self.channel}, room: {self.room}, message: {self.message})"
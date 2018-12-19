class JoinChatRoom():

    """
    Class used for storing information sent from the JOIN command from the IRC.
    Similar to class:JoinChannel:, except with chat rooms.
    Note, usually sent in chunks.
    Should not be manually created.
    
    Parameters
    ==========
    user -> :str:
        The user's name that joined the chat room.
    chatroom -> :str:
        The Twitch channel's chat room that the user joined.
    channel_id -> :int:
        The Twitch channel's ID.
    """

    def __init__(self, user, chatroom, channel_id):
        self.user = user
        self.chatroom = chatroom
        self.channel_id = channel_id

    def __repr__(self):
        return f"JoinChatRoom(user: {self.user}, chatroom: {self.chatroom}, channel_id: {self.channel_id})"
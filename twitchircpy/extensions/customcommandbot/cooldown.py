import twitchircpy

class ChatCommandCooldown(twitchircpy.Cooldown):

    """
    This class is the very similar to class:Cooldown: except with a different name and an extra parameter.
    Note, command_id is always going to be :None: since chat commands do not have an interal ID.
    Should not be manually created.

    New Parameter
    =============
    name -> :str:
        The name of the chat command.
        Used for partial identification along with channel.
    """

    def __init__(self, name, channel, time, command_id=None):
        super().__init__(command_id, channel, time)
        self.name = name

    def __repr__(self):
        return f"ChatCommandCooldown(name: {self.name}, channel: {self.channel}, time: {self.time})"
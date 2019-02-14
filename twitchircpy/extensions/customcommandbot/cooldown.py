import twitchircpy

class ChatCommandCooldown(twitchircpy.Cooldown):

    """
    This class is the very similar to class:Cooldown: except with an extra parameter.
    Note, command_id is always going to be :None: since chat commands do not have an interal ID.
    Should not be manually created in most cases.

    New Parameters
    ==============
    name -> :str:
        The name of the chat command.
        Used for partial identification along with channel.
    aliases -> :list<str>: | :None:
        Aliases for the chat command.
        Used to help with command identification.
        Can be :None: if there are no aliases.
    """

    def __init__(self, name, aliases, channel, time, command_id=None):
        super().__init__(command_id, channel, time)
        self.name = name
        self.aliases = aliases

    def __repr__(self):
        return f"ChatCommandCooldown(name: {self.name}, aliases: {self.aliases}, channel: {self.channel}, time: {self.time})"
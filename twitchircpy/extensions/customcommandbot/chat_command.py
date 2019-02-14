class ChatCommand():

    """
    Class used for storing information about a chat command.
    Should not be manually created in most cases.

    Parameters
    ==========
    name -> :str:
        The name of the chat command.
        Used for partial identification along with channel.
    channel -> :str:
        The channel name/handle that the chat command can be used in.
        Used for partial identification along with name.
    cooldown -> :int:
        The cooldown for the chat command.
    permission -> :str:
        The permission for the chat command.
        Used for checking whether a user can use it or not.
    response -> :str:
        The full response for the chat command.
        This includes unformatted variables.
    variables -> :list<str>:
        All of the variables found in the chat command.
    aliases -> Optional[:list<str>: | :None:]
        All of the aliases for the chat command.
    count -> Optional[:int: | :None:]
        Amount of times the chat command was used.
        This will increase upon chat command use.
        :None: if no count variable found in chat command.
    timeuntil -> Optional[:datetime: | :None:]
        Amount of time until a specified datetime.
        Can be :None: if no datetime specified.
    timesince -> Optional[:datetime: | :None:]
        Amount of time since a specified datetime.
        Can be :None: if no datetime specified.
    """

    def __init__(self, name, channel, cooldown, permission, response, variables, aliases=None, count = None, timeuntil = None, timesince = None):
        self.name = name
        self.response = response
        self.channel = channel
        self.cooldown = cooldown
        self.permission = permission
        self.variables = variables
        self.aliases = aliases
        self.count = count
        self.timeuntil = timeuntil
        self.timesince = timesince

    def __repr__(self):
        return f"ChatCommand(name: {self.name}, response: {self.response}, channel: {self.channel}, cooldown: {self.cooldown}, permission: {self.permission}, aliases: {self.aliases})"
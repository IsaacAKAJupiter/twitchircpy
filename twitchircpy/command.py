class Command():

    """
    Class used for storing information about a command.
    Should not be manually created in most cases.

    Parameters
    ==========
    command_id -> :int:
        The internal ID of the command.
    name -> :str:
        The name of the command.
        AKA the name of the function of the command.
    cog -> :class:
        The actual class of the cog containing the command.
    function -> :function:
        The function object of the command.
        Used for calling the command.
    cooldown -> :int: | :None:
        The cooldown amount for the command in seconds.
        Can be :None: if there is no cooldown.
    aliases -> Optional[:list<str>: | :None:]
        List of aliases for the command.
        Can be :None: if there are no aliases.
    """

    def __init__(self, command_id, name, cog, function, cooldown, aliases=None, last_used=None):
        self.id = command_id
        self.name = name
        self.cog = cog
        self.function = function
        self.cooldown = cooldown
        self.aliases = aliases
        self.last_used = last_used

    @property
    def description(self):
        return self.function.__doc__

    def __repr__(self):
        return f"Command(name: {self.name}, aliases={self.aliases}, cog: {self.cog})"

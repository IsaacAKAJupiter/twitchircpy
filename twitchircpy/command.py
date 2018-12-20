class Command():

    """
    Class used for storing information about a command.
    Should not be manually created.

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
        The cooldown amount for the command.
        Can be None if there is no cooldown.
    """

    def __init__(self, command_id, name, cog, function, cooldown):
        self.id = command_id
        self.name = name
        self.cog = cog
        self.function = function
        self.cooldown = cooldown

    @property
    def description(self):
        return self.function.__doc__

    def __repr__(self):
        return f"Command(name: {self.name}, cog: {self.cog})"
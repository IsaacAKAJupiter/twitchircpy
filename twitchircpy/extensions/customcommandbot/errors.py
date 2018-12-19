class ChatCommandError():

    """
    This class is used for storing information about errors dealing with chat commands.
    Should not be manually created in most cases.
    
    Parameters
    ==========
    command -> :str:
        This is the name of the chat command.
    channel -> :str:
        The Twitch channel name that the error occured in.
    error -> :str:
        This is the actual error message.
    """

    def __init__(self, command, user, channel, error):
        self.command = command
        self.user = user
        self.channel = channel
        self.error = error

    def __repr__(self):
        return f"ChatCommandError(command: {self.command}, user: {self.user}, channel: {self.channel}, error: {self.error})"

class VariableError():

    """
    This class is used for storing information about errors dealing with variables.
    Should not be manually created in most cases.
    
    Parameters
    ==========
    variable -> :str:
        This is the name of the variable.
    error -> :str:
        This is the actual error message.
    """

    def __init__(self, variable, error):
        self.variable = variable
        self.error = error
    
    def __repr__(self):
        return f"VariableError(variable: {self.variable}, error: {self.error}"
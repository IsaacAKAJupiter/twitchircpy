class ChatCommandError():

    """
    This class is used for storing information about errors dealing with chat commands.
    Should not be manually created in most cases.

    Parameters
    ==========
    command -> :str:
        Name of the chat command that raised an error.
    user -> :str:
        Name of the user that fired the chat command when it raised an error.
    channel -> :str:
        The channel that the error occurred in.
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
        Name of the variable that raised an error.
    error -> :str:
        This is the actual error message.
    """

    def __init__(self, variable, error):
        self.variable = variable
        self.error = error

    def __repr__(self):
        return f"VariableError(variable: {self.variable}, error: {self.error}"

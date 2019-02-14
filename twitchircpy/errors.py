class CommandError():

    """
    This class is used for storing information about errors dealing with commands.
    Should not be manually created in most cases.
    
    Parameters
    ==========
    command -> :Command:
        This is the actual command object that raised an error.
    user -> :str:
        The user that attempted to use the command when it raised an error.
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
        return f"CommandError(command: {self.command}, user: {self.user}, channel: {self.channel}, error: {self.error})"

class CooldownError(CommandError):

    """
    This class is the exact same as class:CommandError: except with a different name and only fired when the command error is for cooldowns.
    Created for an easier understanding of the error.
    Should not be manually created in most cases.
    """

    def __repr__(self):
        return f"CooldownError(command: {self.command}, user: {self.user}, channel: {self.channel}, error: {self.error})"

class SilencedError():
    
    """
    This class is used for storing information about errors dealing with silenced commands.
    Usually occurs upon an attempt to run a command that was silenced.
    Should not be manually created in most cases.

    Parameters
    ==========
    command -> :Command:
        The command object that was silenced.
    user -> :str:
        The user that attempted to fire the silenced command.
    channel -> :str:
        The channel that the command attempted to fire in.
    error -> :str:
        This is the actual error message.
    """

    def __init__(self, command, user, channel, error):
        self.command = command
        self.user = user
        self.channel = channel
        self.error = error

    def __repr__(self):
        return f"SilencedError(command: {self.command}, user: {self.user}, channel: {self.channel}, error: {self.error})"

class DecoratorError():

    """
    This class is used for storing information about errors dealing with decorators.
    Usually occurs upon using the "@bot.check()" decorator with custom checks.
    Should not be manually created in most cases.
    
    Parameters
    ==========
    function -> :function:
        The function that raised an error.
        Used to track the error that occurred.
    error -> :str:
        This is the actual error message.
    """

    def __init__(self, function, error):
        self.function = function
        self.error = error

    def __repr__(self):
        return f"DecoratorError(function: {self.function}, error: {self.error})"

class CogError():

    """
    This class is used for storing information about errors dealing with cogs.
    Usually occurs upon creating/adding cogs.
    Should not be manually created in most cases.
    
    Parameters
    ==========
    cog -> :str:
        The name of the cog that raised an error.
    error -> :str:
        This is the actual error message.
    """

    def __init__(self, cog, error):
        self.cog = cog
        self.error = error

    def __repr__(self):
        return f"CogError(cog: {self.cog}, error: {self.error})"

class EventError():

    """
    This class is used for storing information about errors dealing with events.
    Usually occurs upon using an event incorrectly.
    Note, this does not fire upon attempting to use an event that does not exist. Instead, a warning is sent.
    Should not be manually created in most cases.
    
    Parameters
    ==========
    event -> :str:
        The name of the event that raised an error.
    error -> :str:
        This is the actual error message.
    """

    def __init__(self, event, error):
        self.event = event
        self.error = error

    def __repr__(self):
        return f"EventError(event: {self.event}, error: {self.error})"

class TimedMessageError():

    """
    This class is used for storing information about errors dealing with timed messages.
    Usually occurs upon function failure when firing a timed message.
    Should not be manually created in most cases.
    
    Parameters
    ==========
    timed_message -> :str: | :None:
        The name of the timed_message that raised an error.
        Could be :None: if an error occurred upon creation.
    error -> :str:
        This is the actual error message.
    """

    def __init__(self, timed_message, error):
        self.timed_message = timed_message
        self.error = error

    def __repr__(self):
        return f"TimedMessageError(timed_message: {self.timed_message}, error: {self.error})"

class CommonError():

    """
    This class is used for storing information about non-specified errors.
    Usually occurs upon using Twitch chat commands, like ".color".
    Should not be manually created in most cases.
    
    Parameters
    ==========
    error -> :str:
        This is the actual error message.
    """

    def __init__(self, error):
        self.error = error
    
    def __repr__(self):
        return f"CommonError(error: {self.error})"
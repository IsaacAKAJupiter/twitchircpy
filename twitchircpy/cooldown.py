class Cooldown():

    """
    Class for holding information about a command on cooldown.
    Should not be manually created in most cases.

    Parameters
    ==========
    command_id -> :int:
        This is the internal ID for the command on cooldown.
    channel -> :str:
        The channel that the command entered cooldown in.
        Used to enable cooldowns per channel for commands.
    time -> :int:
        The current cooldown, in seconds, the command has left.
        A dynamic variable that gets decreased every second.
    """

    def __init__(self, command_id, channel, time):
        self.command_id = command_id
        self.channel = channel
        self.time = time

    def __repr__(self):
        return f"Cooldown(command_id: {self.command_id}, channel: {self.channel}, time: {self.time})"

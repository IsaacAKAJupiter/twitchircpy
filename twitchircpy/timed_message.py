import time as ptime

class TimedMessage():

    """
    Class used for storing information about timed messages added to the class:Bot:.
    Used for easily storing many timed messages within the class:Bot:.
    Should not be manually created. Instead use the method: "add_timed_message" of class:Bot:.
    Raises TypeError for incorrect types on constructor (__init__). 
    
    Parameters
    ==========
    name -> :str:
        The name of the timed message.
        Used for partial identification along with channel.
    required_chats -> :int:
        This is the amount of chat messages required to activate.
        AKA this amount, or more, messages have to pass before
        the timed message will activate.
    channel -> :str:
        The Twitch channel name that the timed message houses.
        Used for partial identification along with name.
    time -> :int:
        The time to wait in between attempting to activate.
        This time will reset if required_chats not met.
    function -> :function:
        The function that the timed message fires upon activation.
    """

    def __init__(self, name, required_chats, channel, time, function):
        if type(required_chats) != int or required_chats <= 0:
            raise TypeError("required_chats has to be a positive integer which is also greater than 0.")
        if type(time) != int or time <= 0:
            raise TypeError("time has to be a positive integer which is also greater than 0.")

        self.name = name
        self.required_chats = required_chats
        self.channel = channel
        self.time = time
        self.function = function
        self.last_called = ptime.time()
        self.current_chats = 0

    def __repr__(self):
        return f"TimedMessage(name: {self.name}, channel: {self.channel}, function: {self.function})"
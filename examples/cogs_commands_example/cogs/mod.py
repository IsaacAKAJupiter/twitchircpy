from twitchircpy import bot

class Mod():

    def __init__(self, bot):
        self.bot = bot

    @bot.command
    @bot.ismoderator # The class:Bot: has built-in decorators for command checks. This one is for checking if the user is a moderator.
    @bot.issubscriber # This one is for checking if the user is a subscriber. Only mods that are subs can use this command (and broadcaster).
    def modulus(self, info, number1, number2): # This command has to be given 2 parameters. Example: "!modulus 2 4" in chat.
        """Gets the modulus of the 2 given numbers."""
        try:
            number1 = int(number1)
            number2 = int(number2)
        except ValueError:
            self.bot.send_message(info.channel, "Please send 2 numbers for me to mod.")
        else:
            self.bot.send_message(info.channel, str(number1 % number2))

def setup(bot):
    bot.add_commands(Mod(bot)) # In this cog, the class is called "Mod" so I
    # instantiated a new object using the class, passing the class:Bot: object as a parameter.
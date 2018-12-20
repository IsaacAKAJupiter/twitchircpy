from twitchircpy import bot

class General():

    def __init__(self, bot): # This init needs to include a parameter for the class:Bot:. This is to allow class:Bot: methods to be used within commands.
        self.bot = bot

    def has_me(self, info, *args): # Define a custom check. Using the *args (doesn't have to be named args but has to include *) since checks send
        return info.has_me         # every parameter given. This ensures it doesn't break when given extra parameters by the user firing it from chat.

    @bot.command # Create the command with the command function from the import at line 1.
    @bot.cooldown(5) # Add a cooldown to the command (in seconds).
    def copy(self, info, *message): #Each command must include self and info for parameters. The rest are whatever the user sends in chat after the command.
        """Copies the user's message.""" # This is the docstring of the command. You can retrieve this through the description property of a command object.
        self.bot.send_message(info.channel, " ".join(message))

    @bot.command
    @bot.check(has_me) # Use a check (defined at like 8-9) to see if the user included /me in their message.
    def me(self, info):
        """Useless command for mixing /me and commands."""
        self.bot.me(info.channel, f"{info.user} is using /me BabyRage")

def setup(bot): # A setup function needs to be in every cog added to the bot. This allows the library to initalize the commands internally.
    bot.add_commands(General(bot)) # The only piece of code that would need to be changed is creating the instance of the class.
    # In this cog, the class is called "General" so I instantiated a new object using the class, passing the class:Bot: object as a parameter.
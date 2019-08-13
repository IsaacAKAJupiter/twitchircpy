import twitchircpy

"""Example of how to use commands. Take a look at the files within cogs directory for more information."""

bot = twitchircpy.Bot("oauth", "nick", "!", "jups", True)
cogs = ["cogs.general", "cogs.mod"]   # Gets each cog from the cogs directory.
bot.add_cogs(cogs) # Add the cogs and initialize the commands.
                   # Commands are handled internally, no other necessary initialization.

@bot.event # Takes the bot object created at line 4 and hooks to an event.
def on_connect(): # Fires when the bot has connected to all of the given channels.
    print("Command bot connected.")
    print(f"nickname: {bot.nick}")
    print(f"channels connected to: {bot.channels}")
    print(f"commands: {[c.name for c in bot.commands]}") # Creating a list of commands with just their name instead of their object.
    print(f"cogs: {bot.cogs}") # Just printing the cog object. This shows name and where they are located.

@bot.event
def command_fired(info, command): # Fires when a command runs successfully. Useful for keeping track of how many times a command was used.
    print(f"User: {info.user}")
    print(f"Channel: {info.channel}")
    print(f"Command: {command.name}")

@bot.event
def on_error(error): # Fires when an error occurs within the class:Bot:. This could be a command execution failure or user decorator fail, etc.
    print(error)     # Useful to include since the class:Bot: doesn't raise script-stopping exceptions except for on class:Bot: initialization.

bot.start() # Start the bot AFTER defining all events and commands.

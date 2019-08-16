from twitchircpy.extensions import customcommandbot

"""Small example of how to use chat commands. Please note, these commands are not saved and therefore will reset upon restart."""

bot = customcommandbot.CustomCommandBot("oauth", "nick", "!", "jups", True)


@bot.event  # Takes the bot object created at line 4 and hooks to an event.
def on_connect():  # Fires when the bot has connected to all of the given channels.
    print("Connected.")
    print(f"nickname: {bot.nick}")
    print(f"channels connected to: {bot.channels}")


@bot.event
def chatcommand_created(command):  # Fires when a chat command was created.
    print(command)


@bot.event
# Fires when a chat command was removed/deleted.
def chatcommand_removed(command):
    print(command)


@bot.event
# Fires when a chat command was edited. Sends the old command before the edit, and the new command after the edit.
def chatcommand_edited(old, new):
    print(old)
    print(new)


@bot.event
# Fires when a chat command runs successfully. Useful for keeping track of how many times a chat command was used.
def chatcommand_fired(info, command):
    print(info)
    print(command)


# Create a custom variable for chat commands. Note, you can also have parameters for the variable. Example: !addcommand !custom {custom param1 param2}
def custom_variable(info, param1, param2):
    return param1 + param2


# Initialize the custom variable for the chat command.
bot.add_variable("custom", custom_variable)

bot.start()  # Start the bot AFTER defining all events.

import twitchircpy

"""Example of using timed messages."""

bot = twitchircpy.Bot("oauth", "nick", "!", "jups", True)


@bot.event  # Takes the bot object created at line 4 and hooks to an event.
def on_connect():  # Fires when the bot has connected to all of the given channels.
    print("Connected.")
    print(f"nickname: {bot.nick}")
    print(f"channels connected to: {bot.channels}")


# Create custom function for the timed message. Note, this sends class:Bot: as first parameter for function definition outside the main file.
def timed_github(bot, timed_message):
    bot.send_message(timed_message.channel,
                     "https://github.com/IsaacAKAJupiter/twitchircpy")


class Example():  # You can also create timed message with methods.
    # This method will fire from the timed message defined on line 23.
    def example_method(self, bot, timed_message):
        bot.send_message(timed_message.channel,
                         "This is an example timed message.")


# Enable timed messages and start the internal loop. Note, this must be before "start()" method.
bot.start_timed_messages()
# Add timed message with name "Github", requires at least 5 chat messages to pass before firing,
bot.add_timed_message("GitHub", 5, "jups", 60, timed_github)
# send to channel "jups", try to fire every 60 seconds, with the function "timed_github".
bot.add_timed_message("Example", 2, "jups", 120, Example().example_method)

bot.start()  # Start the bot AFTER defining all events and timed messages.

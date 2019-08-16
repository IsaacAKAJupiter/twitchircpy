import twitchircpy

"""Example of deleting messages, timing users out and banning users."""

bot = twitchircpy.Bot("oauth", "nick", "!", "jups", True)

warnings = {}


@bot.event  # Takes the bot object created at line 4 and hooks to an event.
def on_connect():  # Fires when the bot has connected to all of the given channels.
    print("Delete bot connected.")
    print(f"nickname: {bot.nick}")
    print(f"channels connected to: {bot.channels}")


@bot.event
# Fires when a message is sent to any of the connected channels.
def on_message(message):
    # Checks if the user used /me and was not a moderator.
    if message.has_me and not "moderator/1" in message.badges:
        # Delete the message with unique ID.
        bot.delete(message.channel, message.id)
        if not message.user in warnings:
            warnings[message.user] = 1
        else:
            warnings[message.user] += 1

        if warnings[message.user] > 3:
            bot.timeout(message.channel, message.user, 20 *
                        warnings[message.user], "Stop using /me in chat!")

        if warnings[message.user] > 20:
            bot.ban(message.channel, message.user,
                    "You used /me too many times.")


bot.start()  # Start the bot AFTER defining all events.

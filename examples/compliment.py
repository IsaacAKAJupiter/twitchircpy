import twitchircpy
import random

"""Short example of how you can use events to compliment a random chatter."""

bot = twitchircpy.Bot("oauth", "nick", "!", "jups", True)

# Since you cannot get a list of all the viewers with the Twitch IRC, we're going to create it ourselves.
chatters = []
compliments = ["you look great today!", "I like your username!",
               "you're a smart cookie.", "I appreciate you", "you deserve a hug right now."]


@bot.event  # Takes the bot object created at line 4 and hooks to an event.
def on_connect():  # Fires when the bot has connected to all of the given channels.
    print("Compliment bot connected.")
    print(f"nickname: {bot.nick}")
    print(f"channels connected to: {bot.channels}")


@bot.event
# Fires when a message is sent to any of the connected channels.
def on_message(message):
    if not message.user in chatters:
        chatters.append(message.user)

    if message.content.startswith("!compliment"):
        if chatters:
            chatter = chatters[random.randint(0, len(chatters) - 1)]
            compliment = compliments[random.randint(0, len(compliments) - 1)]
            bot.send_message(message.channel, f"@{chatter}, {compliment}")


bot.start()  # Start the bot AFTER defining all events.

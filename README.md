# twitchircpy

twitchircpy is a wrapper for the Twitch IRC used for creating chat bots.

## Installing
  
Installing from pypi:

```
pip3 install twitchircpy
```

Installing from source:

```
pip3 install git+https://github.com/IsaacAKAJupiter/twitchircpy.git
```

## Small Example

```py
import twitchircpy

bot = twitchircpy.Bot("oauth", "nick", "!", "jups", True)

@bot.event
def on_connect():
    print("Connected!)
    
@bot.event
def on_message(message):
    if "HeyGuys" in message.content:
        bot.send_message(message.channel, f"@{message.user} HeyGuys")
        
@bot.event
def on_sub(sub):
    bot.send_message(sub.channel, f"Thank you @{sub.login} for subbing!"

bot.start()
```

You can find examples in the examples directory.

## Library Requirements

Good news! This library only uses built-in Python libraries.

## Python Version

Tested with Python 3.7.1
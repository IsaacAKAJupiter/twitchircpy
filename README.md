# twitchircpy
[![PyPI](https://img.shields.io/pypi/v/twitchircpy.svg)](https://pypi.python.org/pypi/twitchircpy/)
[![PyPI](https://img.shields.io/pypi/pyversions/twitchircpy.svg)](https://pypi.python.org/pypi/twitchircpy/)

twitchircpy is a wrapper for the Twitch IRC used for creating chat bots.

## Installing
  
Installing from pypi:

```
pip install twitchircpy
```

Installing from source:

```
pip install git+https://github.com/IsaacAKAJupiter/twitchircpy.git
```

You might have to install with these commands if the above installs for Python 2.

```
pip3 install twitchircpy
pip3 install git+https://github.com/IsaacAKAJupiter/twitchircpy.git
```

## Updating

Check out this [link](https://packaging.python.org/tutorials/installing-packages/#upgrading-packages "https://packaging.python.org/tutorials/installing-packages/#upgrading-packages") for more information about updating PyPI (pip) packages.

## Small Example

```py
import twitchircpy

bot = twitchircpy.Bot("oauth", "nick", "!", "jups", True)

@bot.event
def on_connect():
    print("Connected!")
    
@bot.event
def on_message(message):
    if "HeyGuys" in message.content:
        bot.send_message(message.channel, f"@{message.user} HeyGuys")
        
@bot.event
def on_sub(sub):
    bot.send_message(sub.channel, f"Thank you @{sub.login} for subbing!")

bot.start()
```

You can find examples in the examples directory.

## Library Requirements

Good news! This library only uses built-in Python libraries.

## Python Version

Tested with Python 3.7.1.

## Discord

Please join the [Discord](https://discord.gg/yxzp7JU "https://discord.gg/yxzp7JU") if you need help with the library or just want to chat!

"""
Twitch IRC Wrapper

Extension: CustomCommandBot.

This extension is for dynamically adding commands to the bot via the Twitch chat.
"""

from .customcommandbot import CustomCommandBot
from .chat_command import ChatCommand
from .errors import ChatCommandError, VariableError
from .cooldown import ChatCommandCooldown
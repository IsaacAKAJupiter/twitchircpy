import re
import inspect
import os
import datetime
import math

import twitchircpy
from twitchircpy import bot

from .chat_command import ChatCommand
from .variable import Variable
from .errors import ChatCommandError, VariableError
from .cooldown import ChatCommandCooldown

class CustomCommandBot(twitchircpy.bot.Bot):

    """
    Class used as an additional layer of commands through Twitch chat.
    Used for dynamic chat commands defined through Twitch chat.
    Does not save chat commands on termination, so only recommended to those with a database or knowledge of Python's File I/O.
    Since this inherits class:Bot: and is simply an extension, this requires the same parameters as class:Bot:.
    Raises TypeError for incorrect types on class:Bot: constructor (super().__init__).

    Parameters
    ==========
    oauth -> :str:
        The OAuth token for the Twitch account being used.
        Format: oauth:asdasd234asd234ad234asds23
        Note, this is not an actual OAuth Token.
    nick -> :str:
        The nickname (nick) must be your Twitch username/handle.
    prefix -> :str:
        The prefix is used for the bot's commands.
        These commands are added with cogs.
        Mandatory since there is no default prefix.
    channel -> :str: | :list<str>:
        Channel is the username(s) of the Twitch channel(s) 
        that the bot will end up joining.
        :str: for single channel.
        :list<str>: for multiple channels.
    reconnect -> :bool:
        Reconnect is for responding to Twitch's IRC Ping.
        Also for responding to Twitch's IRC Reconnect.
        This should be True on most occasions.
        Could be False if using for temporary bot.
    """

    def __init__(self, oath, nick, prefix, channel, reconnect):
        super().__init__(oath, nick, prefix, channel, reconnect)
        self.chat_commands = []
        self.variables = []
        self._chat_command_permissions = ["user", "moderator", "subscriber", "admin", "bits", "broadcaster", "global_mod", "staff", "turbo"]

        self._append_builtins()
        self._append_variables()
        self._append_events()

    def __repr__(self):
        return f"CustomCommandBot(nick: {self.nick}, prefix: {self._prefix})"

    ###################################
    #            VARIABLES            #
    ###################################

    def _check_variable(self, var):
        for variable in self.variables:
            if var == variable.name:
                return True
        
        return False

    def _get_variable(self, var):
        for variable in self.variables:
            if var == variable.name:
                return variable
        
        return None

    def _get_variables_from_message(self, message):
        # Get all the variables.
        all_vars = []
        all_starts = []
        amount_of_starts = 0
        for index, letter in enumerate(message):
            if letter == "{" and message[index - 1] != "\\":
                all_starts.append(index)
                amount_of_starts += 1
            elif letter == "}" and message[index - 1] != "\\":
                appended = message[all_starts[amount_of_starts - 1]:index + 1]
                all_vars.append(appended)
                all_starts.remove(all_starts[amount_of_starts - 1])
                amount_of_starts -= 1
        
        # Make sure that all the variables are actually variables, if not, remove from list.
        # Also if they are variables, turn them into dynamicvariable objects.
        return_vars = []
        for var in all_vars:
            if " " in var:
                # If there is a space, then there is at least 1 param.
                just_params = var.split(" ", 1)
                var_name = just_params[0][1:]
                just_params = just_params[1][:-1]
                # Have exceptions for built-in variables.
                exceptions = ["timesince", "timeuntil"]
                if not var_name in exceptions:
                    if " " in just_params:
                        amount_of_starts = 0
                        last_param = 0
                        actual_params = []
                        for index, letter in enumerate(just_params):
                            if letter == "{" and just_params[index - 1] != "\\":
                                amount_of_starts += 1
                            elif letter == "}" and just_params[index - 1] != "\\":
                                amount_of_starts -= 1
                            elif letter == " " and amount_of_starts <= 0:
                                actual_params.append(just_params[last_param:index])
                                last_param = index

                        if not actual_params:
                            actual_params = [just_params]
                    else:
                        actual_params = [just_params]
                else:
                    try:
                        actual_params = [datetime.datetime.fromisoformat(just_params)]
                    except Exception:
                        raise ValueError("Incorrect datetime format. Please use ISO format. Example: 2019-05-05T13:00:00-05:00 == May 5th 2019, 1:00AM EST.")
            else:
                var_name = var[1:-1]
                actual_params = None
            if self._check_variable(var_name):
                return_vars.append(self._get_variable(var_name).to_dynamic(actual_params))

        return return_vars

    def _format_response(self, info, command):
        # Check if the user sent any params.
        if " " in info.content:
            params = info.content.split(" ")
            params.remove(params[0])

        variables = command.variables.copy()

        return_string = command.response

        for var in variables:
            # Using a try-except since the users function could error.
            try:
                # Since you can remove variables, just check if the variable still exists.
                if self._check_variable(var.name):
                    if "params" in locals():
                        if var.params:
                            return_func = var.function(command, info, *var.params, *params)
                        else:
                            return_func = var.function(command, info, *params)
                    else:
                        if var.params:
                            return_func = var.function(command, info, *var.params)
                        else:
                            return_func = var.function(command, info)
                else:
                    continue
            except Exception as e:
                self._call_event("on_error", VariableError(var.name, f"An error occured when running the variable's function. Raised: {e}"))
                return None

            # Check if the user returned a non-string.
            if not isinstance(return_func, str):
                self._call_event("on_error", VariableError(var.name, f"An error occured when running the variable's function. Raised: Function must return a string."))
                return None

            regex = r"{" + re.escape(var.name) + r".*?}"

            for v in variables:
                if v != var and v.params and v.name not in ["timesince", "timeuntil"]:
                    for index, param in enumerate(v.params):  
                        if f"{{{var.name}" in param and not "\\{" in param:
                            v.params[index] = re.sub(regex, return_func, v.params[index])
            
            return_string = re.sub(regex, return_func, return_string)
                
        # Remove all the \ from the escaped curly braces.
        return_string = re.sub(r"\\({)|\\(})", "\\1\\2", return_string)
        return return_string

    def add_variable(self, name, function):
        """
        This method is for adding a custom variable to the class:CustomCommandBot:.
        Note, the function must return a str object.
        """

        if inspect.isfunction(function) and isinstance(name, str):
            self.variables.append(Variable(name, function))
        else:
            self._call_event("on_error", VariableError(name, "An error occured when creating a variable. The name must be a string and the function must be a function."))

    def remove_variable(self, name):
        """
        This method is for removing a custom variable to the class:CustomCommandBot: via name.
        """

        unremovable_variables = ["user", "channel", "count", "timeuntil", "timesince"]
        if name in unremovable_variables:
            self._call_event("on_error", VariableError(name, "You cannot remove this variable."))
        
        # Actually remove it.
        for variable in self.variables:
            if variable.name == name:
                self.variables.remove(variable)

    def _append_variables(self):
        self.variables.append(Variable("user", self._user_variable))
        self.variables.append(Variable("channel", self._channel_variable))
        self.variables.append(Variable("count", self._count_variable))
        self.variables.append(Variable("timeuntil", self._timeuntil_variable))
        self.variables.append(Variable("timesince", self._timesince_variable))

    def _user_variable(self, command, info):
        return info.user

    def _channel_variable(self, command, info):
        return info.channel

    def _count_variable(self, command, info):
        if not command.count:
            command.count = 1
        else:
            command.count += 1
        return str(command.count)

    def _totalseconds_to_dhms(self, total_seconds):
        total_minutes = total_seconds / 60
        seconds = math.fmod(total_seconds, 60)
        total_hours = total_minutes / 60
        minutes = math.fmod(total_minutes, 60)
        days = total_hours / 24
        hours = math.fmod(total_hours, 24)

        days = int(days)
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)

        return_string = ""
        return_string += f"{days} days, " if days > 1 or days < 1 and not days == 0 else f"{days} day, " if days == 1 else ""
        return_string += f"{hours} hours, " if hours > 1 or hours < 1 and not hours == 0 else f"{hours} hour, " if hours == 1 else ""
        return_string += f"{minutes} minutes, " if minutes > 1 or minutes < 1 and not minutes == 0 else f"{minutes} minute, " if minutes == 1 else ""
        return_string += f"{seconds} seconds." if seconds > 1 or seconds < 1 and not seconds == 0 else f"{seconds} second." if seconds == 1 else ""
        return return_string

    def _timeuntil_variable(self, command, info, until = None, *args):
        if not until:
            raise ValueError("Missing parameter in timeuntil variable.")
        if isinstance(until, str):
            try:
                until = datetime.datetime.fromisoformat(until)
            except Exception:
                raise ValueError(f"User input of \"{until}\" not in ISO time format. You might've forgotten to put the timeuntil parameter when creating the chat command.")
        difference = until - datetime.datetime.now(tz=until.tzinfo)
        total_seconds = int(difference.total_seconds())
        return self._totalseconds_to_dhms(total_seconds)

    def _timesince_variable(self, command, info, since = None, *args):
        if not since:
            raise ValueError("Missing parameter in timesince variable.")
        if isinstance(since, str):
            try:
                since = datetime.datetime.fromisoformat(since)
            except Exception:
                raise ValueError(f"User input of \"{since}\" not in ISO time format. You might've forgotten to put the timesince parameter when creating the chat command.")
        difference = datetime.datetime.now(tz=since.tzinfo) - since
        total_seconds = int(difference.total_seconds())
        return self._totalseconds_to_dhms(total_seconds)

    ###################################
    #          CHAT COMMANDS          #
    ###################################

    def _run_chat_command(self, info):
        command = info.content.split(" ")[0]
        if self._check_chat_command(command, info.channel):
            command_o = self._get_chat_command(command, info.channel)
            cooldown_o = self._check_chat_command_cooldown(command, info.channel)
            if not cooldown_o:
                if self._check_chat_command_permission(info, command_o):
                    formatted_response = self._format_response(info, command_o)
                    if formatted_response:
                        self.send_message(info.channel, formatted_response)
                        self._call_event("chatcommand_fired", info, command_o)
                        self.cooldowns.append(ChatCommandCooldown(command_o.name, info.channel, command_o.cooldown))
                else:
                    self._call_event("on_error", ChatCommandError(command, info.user, info.channel, f"User does not have permission to use this command."))
            else:
                self._call_event("on_error", ChatCommandError(command, info.user, info.channel, f"Command is on cooldown for another {cooldown_o.time} seconds."))
    
    def _check_chat_command(self, command, channel):
        for c in self.chat_commands:
            if c.name == command and c.channel == channel:
                return True

        return False

    def _get_chat_command(self, command, channel):
        for c in self.chat_commands:
            if c.name == command and c.channel == channel:
                return c

        return None

    def _check_chat_command_cooldown(self, command, channel):
        for cooldown in self.cooldowns:
            if isinstance(cooldown, ChatCommandCooldown):
                if cooldown.name == command and cooldown.channel == channel:
                    return cooldown
        
        return None

    def _check_chat_command_permission(self, info, command):
        # If permission is user, return True.
        if command.permission == "user":
            return True
        
        # Check for mod.
        if command.permission == "moderator":
            if "moderator/1" in info.badges or "broadcaster/1" in info.badges:
                return True

        # Check for sub.
        if command.permission == "subscriber":
            if "subscriber/1" in info.badges or "broadcaster/1" in info.badges:
                return True

        # Check for broadcaster.
        if command.permission == "broadcaster":
            if "broadcaster/1" in info.badges:
                return True

        # Check for bits.
        if command.permission == "bits":
            if "bits/" in info.badges or "broadcaster/1" in info.badges:
                return True

        # Check for admin.
        if command.permission == "admin":
            if "admin/1" in info.badges or "broadcaster/1" in info.badges:
                return True

        # Check for global mod.
        if command.permission == "globalmod":
            if "global_mod/1" in info.badges or "broadcaster/1" in info.badges:
                return True

        # Check for staff.
        if command.permission == "staff":
            if "staff/1" in info.badges or "broadcaster/1" in info.badges:
                return True
        
        # Check for turbo.
        if command.permission == "turbo":
            if "turbo/1" in info.badges or "broadcaster/1" in info.badges:
                return True

        return False

    def _add_chat_command(self, channel, command, *response, edit=False, cooldown=None, permission=None, count=None, timeuntil=None, timesince=None):
        # Check if it exists.
        if self._get_chat_command(command, channel):
            return False, "Command already exists.", None

        if len(command) > 256:
            return False, "Command length too long. Please choose a command name under 256 characters.", None

        try:
            default_cooldown = 30
            default_permission = "user"

            response = list(response)
            
            # Check for custom params for cooldown, permission, etc.
            removed_params = []
            for param in response:
                # Check for cooldown.
                if param.startswith("--cooldown="):
                    cooldown = param.split("=")[1]
                    removed_params.append(param)
                    continue
                # Check for permission.
                if param.startswith("--permission="):
                    permission = param.split("=")[1]
                    if not permission in self._chat_command_permissions:
                        return False, "Incorrect permission.", None
                    removed_params.append(param)
                    continue

            # Remove all custom params.
            for param in removed_params:
                response.remove(param)
            
            if not isinstance(cooldown, int):
                cooldown = int(cooldown) if cooldown and cooldown.isdigit() else default_cooldown

            if not permission:
                permission = default_permission

            response = " ".join(response)

            chat_command = ChatCommand(command, channel, cooldown, permission, response, self._get_variables_from_message(response), count, timeuntil, timesince)
            self.chat_commands.append(chat_command)
            if not edit:
                self._call_event("chatcommand_created", chat_command)
            return True, None, response
        except Exception as e:
            return False, e, None

    def _remove_chat_command(self, channel, command_name, edit=False):
        for command in self.chat_commands:
            if command.name == command_name:
                if not edit:
                    self._call_event("chatcommand_removed", command)
                self.chat_commands.remove(command)
                return True, None
        
        return False, "Command not found."

    @bot.ismoderator
    def _add_command(self, info, command, *response):
        success, error, response = self._add_chat_command(info.channel, command, *response)
        if not success:
            self._call_event("on_error", ChatCommandError("addcommand", info.user, info.channel, f"An error occured when creating the command: {command}. Raised: {error}"))

    @bot.ismoderator
    def _remove_command(self, info, command):
        success, error = self._remove_chat_command(info.channel, command)
        if not success:
            self._call_event("on_error", ChatCommandError("removecommand", info.user, info.channel, f"An error occured when removing the command: {command}. Raised: {error}"))

    @bot.ismoderator
    def _edit_command(self, info, command, *response):
        if self._check_chat_command(command, info.channel):
            success, response = self._edit_chat_command(info, command, *response)
            if success:
                self._call_event("chatcommand_edited", self._get_chat_command(command, info.channel))
                return True

        self._call_event("on_error", ChatCommandError("editcommand", info.user, info.channel, f"An error occured when attempting to edit the command: {command}. Error: {response}"))
        return False

    def _edit_chat_command(self, info, command_name, *response):
        command = self._get_chat_command(command_name, info.channel)
        success, error = self._remove_chat_command(info, command_name)
        if success:
            success, error, response = self._add_chat_command(info.channel, command_name, *response, edit=True, cooldown=command.cooldown, permission=command.permission, count=command.count, timeuntil=command.timeuntil, timesince=command.timesince)
            if success:
                return True, response
        
        return False, error
    
    ###################################
    #            OVERRIDE             #
    ###################################

    def _read_message(self, message):
        _, params, message_data = self._read_default(message)
        info = twitchircpy.Info(message_data[1].split("#")[1][:-1], message_data[1].split("!")[0], message_data[2], params)
        self._run_chat_command(info)
        return twitchircpy.Message(message_data[1].split("#")[1][:-1], message_data[1].split("!")[0], message_data[2], params), info

    ###################################
    #              MISC               #
    ###################################

    def _append_builtins(self):
        self._builtin_commands.append(twitchircpy.Command(len(self.commands), "addcommand", self, "_add_command", None))
        self._builtin_commands.append(twitchircpy.Command(len(self.commands), "removecommand", self, "_remove_command", None))
        self._builtin_commands.append(twitchircpy.Command(len(self.commands), "editcommand", self, "_edit_command", None))
    
    def _append_events(self):
        events_len = len(self.events)
        self.events.append(twitchircpy.Event(events_len, "chatcommand_created", 1))
        self.events.append(twitchircpy.Event(events_len + 1, "chatcommand_edited", 1))
        self.events.append(twitchircpy.Event(events_len + 2, "chatcommand_removed", 1))
        self.events.append(twitchircpy.Event(events_len + 3, "chatcommand_fired", 2))
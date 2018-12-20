import socket
import importlib
import inspect
import warnings
import threading
import sys
import re
import time
from functools import wraps

from .command import Command
from .event import Event
from .message import Message, Info
from .userstate import UserState, GlobalUserState
from .usernotice import UserNotice, Sub, ReSub, SubGift, AnonSubGift, Raid, Ritual
from .roomstate import RoomState
from .join_channel import JoinChannel
from .join_chatroom import JoinChatRoom
from .part_channel import PartChannel
from .jtv_mode import Mode
from .cooldown import Cooldown
from .errors import CommandError, CooldownError, DecoratorError, CogError, EventError, CommonError, TimedMessageError
from .clearchat import ClearChat, Ban
from .clearmsg import ClearMsg
from .general_notice import Notice
from .hosttarget import HostTarget
from .timed_message import TimedMessage

###################################
#            DECORATORS           #
###################################

def command(func):
    """
    This decorator is for marking specific functions as a command.
    """

    func._decorators = "command"
    return func

def cooldown(time):
    """
    This decorator is for allowing specific functions to have a cooldown.
    """

    def _dec_cooldown(func):
        if not isinstance(time, int):
            warnings.warn("Cooldown must be an int.")
            return
        func._cooldown = time
        return func
    return _dec_cooldown

def ismoderator(func):
    """
    This decorator is for allowing only moderators (and the broadcaster) to use the specific command.
    """

    @wraps(func)
    def _dec_ismod(*args, **kwargs):
        if len(args) > 1:
            if isinstance(args[1], Info):
                if "moderator/1" in args[1].badges or "broadcaster/1" in args[1].badges:
                    return func(*args, **kwargs)
        if len(args) > 1:
            if inspect.isclass(type(args[0])):
                if not isinstance(args[0], Bot):
                    args[0].bot._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} was not a mod. Command used: {func.__name__}"))
                else:
                    args[0]._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} was not a mod. Command used: {func.__name__}"))
            return
    return _dec_ismod

def issubscriber(func):
    """
    This decorator is for allowing only subscribers (and the broadcaster) to use the specific command.
    """

    @wraps(func)
    def _dec_issub(*args, **kwargs):
        if len(args) > 1:
            if isinstance(args[1], Info):
                if "subscriber/1" in args[1].badges or "broadcaster/1" in args[1].badges:
                    return func(*args, **kwargs)
        if len(args) > 1:
            if inspect.isclass(type(args[0])):
                if not isinstance(args[0], Bot):
                    args[0].bot._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} was not a subscriber. Command used: {func.__name__}"))
                else:
                    args[0]._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} was not a subscriber. Command used: {func.__name__}"))
            return
    return _dec_issub

def isbroadcaster(func):
    """
    This decorator is for allowing only the broadcaster to use the specific command.
    """

    @wraps(func)
    def _dec_isbroadcaster(*args, **kwargs):
        if len(args) > 1:
            if isinstance(args[1], Info):
                if "broadcaster/1" in args[1].badges:
                    return func(*args, **kwargs)
        if len(args) > 1:
            if inspect.isclass(type(args[0])):
                if not isinstance(args[0], Bot):
                    args[0].bot._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} was not the broadcaster. Command used: {func.__name__}"))
                else:
                    args[0]._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} was not the broadcaster. Command used: {func.__name__}"))
            return
    return _dec_isbroadcaster

def isbits(func):
    """
    This decorator is for allowing only users that cheer within the command (and the broadcaster) to use the specific command.
    """
    
    @wraps(func)
    def _dec_isbits(*args, **kwargs):
        if len(args) > 1:
            if isinstance(args[1], Info):
                if "bits/" in args[1].badges or "broadcaster/1" in args[1].badges:
                    return func(*args, **kwargs)
        if len(args) > 1:
            if inspect.isclass(type(args[0])):
                if not isinstance(args[0], Bot):
                    args[0].bot._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} did not include bits. Command used: {func.__name__}"))
                else:
                    args[0]._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} did not include bits. Command used: {func.__name__}"))
            return
    return _dec_isbits
    
def isadmin(func):
    """
    This decorator is for allowing only admins (and the broadcaster) to use the specific command.
    """

    @wraps(func)
    def _dec_isadmin(*args, **kwargs):
        if len(args) > 1:
            if isinstance(args[1], Info):
                if "admin/1" in args[1].badges or "broadcaster/1" in args[1].badges:
                    return func(*args, **kwargs)
        if len(args) > 1:
            if inspect.isclass(type(args[0])):
                if not isinstance(args[0], Bot):
                    args[0].bot._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} was not an admin. Command used: {func.__name__}"))
                else:
                    args[0]._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} was not an admin. Command used: {func.__name__}"))
            return
    return _dec_isadmin

def isglobalmod(func):
    """
    This decorator is for allowing only global moderators (and the broadcaster) to use the specific command.
    """
    
    @wraps(func)
    def _dec_isglobalmod(*args, **kwargs):
        if len(args) > 1:
            if isinstance(args[1], Info):
                if "global_mod/1" in args[1].badges or "broadcaster/1" in args[1].badges:
                    return func(*args, **kwargs)
        if len(args) > 1:
            if inspect.isclass(type(args[0])):
                if not isinstance(args[0], Bot):
                    args[0].bot._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} was not a global mod. Command used: {func.__name__}"))
                else:
                    args[0]._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} was not a global mod. Command used: {func.__name__}"))
            return
    return _dec_isglobalmod

def isstaff(func):
    """
    This decorator is for allowing only staff (and the broadcaster) to use the specific command.
    """

    @wraps(func)
    def _dec_isstaff(*args, **kwargs):
        if len(args) > 1:
            if isinstance(args[1], Info):
                if "staff/1" in args[1].badges or "broadcaster/1" in args[1].badges:
                    return func(*args, **kwargs)
        if len(args) > 1:
            if inspect.isclass(type(args[0])):
                if not isinstance(args[0], Bot):
                    args[0].bot._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} was not a staff member. Command used: {func.__name__}"))
                else:
                    args[0]._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} was not a staff member. Command used: {func.__name__}"))
            return
    return _dec_isstaff

def isturbo(func):
    """
    This decorator is for allowing only turbo members (and the broadcaster) to use the specific command.
    Note, this does not work for Prime members.
    """

    @wraps(func)
    def _dec_isturbo(*args, **kwargs):
        if len(args) > 1:
            if isinstance(args[1], Info):
                if "turbo/1" in args[1].badges or "broadcaster/1" in args[1].badges:
                    return func(*args, **kwargs)
        if len(args) > 1:
            if inspect.isclass(type(args[0])):
                if not isinstance(args[0], Bot):
                    args[0].bot._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} was not turbo. Command used: {func.__name__}"))
                else:
                    args[0]._call_event("on_error", DecoratorError(func, f"Command check failed, {args[1].display_name} was not turbo. Command used: {func.__name__}"))
            return
    return _dec_isturbo

def check(check_func):
    """
    This decorator is for creating custom checks for your commands.
    \nThe decorator will always send all of the arguments and keyword arguments to the check function.
    \nTo use this decorator, provide a function as the parameter to the decorator. This function must return True or False, else it will error.
    \nIf the function returns True, it will allow the user to use the command, else if it returns False, it will not allow the user to use the command.
    """

    def _func_check(func):
        @wraps(func)
        def _dec_check(*args, **kwargs):
            if not inspect.isfunction(check_func):
                if len(args) > 1 and inspect.isclass(type(args[0])):
                    if not isinstance(args[0], Bot):
                        args[0].bot._call_event("on_error", DecoratorError(func, f"@bot.check() has to have a function as a parameter."))
                    else:
                        args[0]._call_event("on_error", DecoratorError(func, f"@bot.check() has to have a function as a parameter."))
                return
            try:
                func_val = check_func(*args, **kwargs)
            except Exception as e:
                if len(args) > 1 and inspect.isclass(type(args[0])):
                    if not isinstance(args[0], Bot):
                        args[0].bot._call_event("on_error", DecoratorError(func, f"@bot.check() tried to call the function: {check_func.__name__} but the function raised this exception: {e}."))
                    else:
                        args[0]._call_event("on_error", DecoratorError(func, f"@bot.check() tried to call the function: {check_func.__name__} but the function raised this exception: {e}."))
                return
            else:
                if func_val is False:
                    if len(args) > 1 and inspect.isclass(type(args[0])):
                        if not isinstance(args[0], Bot):
                            args[0].bot._call_event("on_error", DecoratorError(func, f"Command check failed. User {args[1].display_name} failed the check: {check_func.__name__}. Command used: {func.__name__}"))
                        else:
                            args[0]._call_event("on_error", DecoratorError(func, f"Command check failed. User {args[1].display_name} failed the check: {check_func.__name__}. Command used: {func.__name__}"))
                    return
                elif func_val is True:
                    return func(*args, **kwargs)
                else:
                    if len(args) > 1 and inspect.isclass(type(args[0])):
                        if not isinstance(args[0], Bot):
                            args[0].bot._call_event("on_error", DecoratorError(func, f"The return function for @bot.check() needs to return either True or False. Return function name: {check_func.__name__}."))
                        else:
                            args[0]._call_event("on_error", DecoratorError(func, f"The return function for @bot.check() needs to return either True or False. Return function name: {check_func.__name__}."))
                    return
        return _dec_check
    return _func_check

class Bot():

    """
    Main class used for interaction with the Twitch IRC.
    Used to interact with Twitch Chat with commands, events and timed messages.
    Responsible for sending and receiving IRC commands from/to Twitch.
    Raises TypeError for incorrect types on constructor (__init__).

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
    
    def __init__(self, oauth, nick, prefix, channel, reconnect):
        # Check if the required types are given.
        if not isinstance(prefix, str):
            raise TypeError("Prefix must be a string.")
        if not isinstance(oauth, str):
            raise TypeError("OAuth must be a string.")
        if not isinstance(channel, str) and not isinstance(channel, list):
            raise TypeError("Channel must either be a string (only 1 channel) or list (multiple channels or 1 channel with single item list).")
        if not isinstance(nick, str):
            raise TypeError("Nickname (nick) must be a string.")
        if not isinstance(reconnect, bool):
            raise TypeError("Reconnect must be a boolean (bool).")

        self.oauth = oauth
        self._prefix = prefix
        self.nick = nick
        self.channels = [channel] if isinstance(channel, str) else channel
        self.reconnect = reconnect
        self.cogs = []
        self.commands = []
        self.events = []
        self._callbacks = {}
        self.cooldowns = []
        self.timed_messages = []
        self._builtin_commands = []
        self._timed_messages_enabled = False
        self._socket = None
        self._read_buffer = ""
        self._RECV_AMOUNT = 1024
        self.running = False
        self.thread = None
        self.cd_thread = None
        self.td_thread = None

        self._define_events()
        self._define_builtin_commands()

    def __repr__(self):
        return f"Bot(nick: {self.nick}, prefix: {self._prefix})"

    ###################################
    #            PROPERTY             #
    ###################################

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, p):
        if not isinstance(p, str):
            warnings.warn("Prefix has to be a string.")
            return
        self._prefix = p

    ###################################
    #             SOCKET              #
    ###################################

    def _set_socket(self, s):
        self._socket = s

    def _connect(self, host, port):
        if self._socket:
            self._socket.connect((host, port))
        else:
            raise ValueError("Couldn't connect, bot doesn't have a socket.")

    def _receive(self):
        try:
            self._read_buffer = self._read_buffer + self._socket.recv(self._RECV_AMOUNT).decode("utf-8")
        except UnicodeDecodeError:
            return None
        else:
            temp = self._read_buffer.split("\r\n")
            self._read_buffer = temp.pop()
            return temp

    def _send_socket_message(self, message):
        self._socket.send(f"{message}\r\n".encode("utf-8"))

    def _open_socket(self):
        self._set_socket(socket.socket())
        self._connect("irc.chat.twitch.tv", 6667)
        self._send_socket_message(f"PASS {self.oauth}")
        self._send_socket_message(f"NICK {self.nick}")
        self._send_socket_message("CAP REQ :twitch.tv/commands")
        self._send_socket_message("CAP REQ :twitch.tv/tags")
        self._send_socket_message("CAP REQ :twitch.tv/membership")

    # Called when bot starts to join all channels.
    def _join_room(self):
        for channel in self.channels:
            if not isinstance(channel, str):
                raise ValueError("One of the channels that was requested to join was not of type string.")

            self._send_socket_message(f"JOIN #{channel}")

            read_buffer = ""
            loading = True
            while loading:
                read_buffer = read_buffer + self._socket.recv(self._RECV_AMOUNT).decode("utf-8")
                temp = read_buffer.split("\n")
                read_buffer = temp.pop()

                for line in temp:
                    if "JOIN" in line:
                        join = self._read_join(line)
                        self._call_event("channel_join", join)

                    if "End of /NAMES list" in line:
                        loading = False

        self._call_event("on_connect")

    # Used to dynamically join a new channel.
    def join_channel(self, channel):
        """
        This method is used to allow the class:Bot: to dynamically join a channel whilst running.
        """

        self._send_socket_message(f"JOIN #{channel}")

        read_buffer = ""
        loading = True
        while loading:
            read_buffer = read_buffer + self._socket.recv(self._RECV_AMOUNT).decode("utf-8")
            temp = read_buffer.split("\n")
            read_buffer = temp.pop()

            for line in temp:
                if "JOIN" in line:
                    join = self._read_join(line)
                    self._call_event("channel_join", join)
                    
                if "End of /NAMES list" in line:
                    loading = False
        
        self.channels.append(channel)

    def part_channel(self, channel):
        """
        This method is used to allow the class:Bot: to dynamically part from a channel whilst running.
        """

        self._send_socket_message(f"PART #{channel}")
        self.channels.remove(channel)

    ###################################
    #              LOOP               #
    ###################################
        
    def start(self):
        """
        Use this method to start the class:Bot:
        This method is to be used after defining all of your events/timed messages/commands/etc (at the end of your main file).
        """

        self._open_socket()
        self._join_room()

        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.cd_thread = threading.Thread(target=self._run_cooldown)
        self.thread.start()
        self.cd_thread.start()

    def start_timed_messages(self):
        """
        This method is used to allow the class:Bot: to be able to use timed messages.
        \nUse this method before "add_timed_message" else it will error.
        \nTo stop using timed messages, use "stop_timed_messages".
        """

        self.td_thread = threading.Thread(target=self._run_timed_messages)
        # Need self.running = True in both this and run so it runs if called before bot.run()
        self.running = True
        self._timed_messages_enabled = True
        self.td_thread.start()
    
    def _run(self):
        while self.running:
            # Receive from Twitch, then send to main_read() function.
            temp = self._receive()
            if temp:
                for line in temp:
                    self._main_read(line)
        
    def _run_cooldown(self):
        while self.running:
            time.sleep(1)
            
            for cooldown in self.cooldowns:
                cooldown.time -= 1
                if cooldown.time <= 0:
                    self.cooldowns.remove(cooldown)

    def _run_timed_messages(self):
        while self.running and self._timed_messages_enabled:
            time.sleep(1)

            for message in self.timed_messages:
                if time.time() - message.last_called > message.time:
                    message.last_called = time.time()
                    if message.current_chats >= message.required_chats:
                        try:
                            message.function(self, message)
                        except Exception as e:
                            self._call_event("on_error", TimedMessageError(message.name, f"Error when calling timed_message. Error: {e}"))
                        message.current_chats = 0

    def stop(self):
        """
        This method is to completely stop the class:Bot:.
        """

        self.running = False
        self._socket.close()

    ###################################
    #         TIMED_MESSAGES          #
    ###################################

    def disable_timed_messages(self):
        """
        This method is for disabling the ability of class:Bot: to use timed messages.
        \nTo allow timed messages again, use "start_timed_messages".
        """

        self._timed_messages_enabled = False

    def _check_for_timed_message(self, name, channel):
        for tm in self.timed_messages:
            if tm.name == name and tm.channel == channel:
                return True
        
        return False

    def add_timed_message(self, name, required_chats, channel, time, function):
        """
        This method is to add a timed message to the class:Bot:.
        """

        if self._timed_messages_enabled:
            if inspect.isfunction(function) or inspect.ismethod(function):
                if not self._check_for_timed_message(name, channel):
                    self.timed_messages.append(TimedMessage(name, required_chats, channel, time, function))
                else:
                    self._call_event("on_error", TimedMessageError(None, f"Timed Message with name: \"{name}\" already exists for channel: \"{channel}\"."))
            else:
                self._call_event("on_error", TimedMessageError(None, "Function must be a function or a method (class function)."))
        else:
            self._call_event("on_error", TimedMessageError(None, "Timed Messages Disabled. Please use bot.start_timed_messages() to start it."))

    def remove_timed_message(self, name, channel):
        """
        This method is for removing a timed message via a name from the class:Bot:.
        """

        removed = []
        for tm in self.timed_messages:
            if tm.name == name and tm.channel == channel:
                removed.append(tm)

        for remove in removed:
            self.timed_messages.remove(remove)
    
    def _handle_timed_messages(self, message):
        for tm in self.timed_messages:
            if tm.channel == message.channel:
                tm.current_chats += 1

    ###################################
    #             EVENTS              #
    ###################################

    def _define_events(self):
        self.events.append(Event(0, "on_message", 1))
        self.events.append(Event(1, "on_usernotice", 1))
        self.events.append(Event(2, "on_userstate", 1))
        self.events.append(Event(3, "on_connect", 0))
        self.events.append(Event(4, "on_roomstate", 1))
        self.events.append(Event(5, "dynamic_prefix", 1))
        self.events.append(Event(6, "chatroom_join", 1))
        self.events.append(Event(7, "channel_join", 1))
        self.events.append(Event(8, "on_part", 1))
        self.events.append(Event(9, "on_mode", 1))
        self.events.append(Event(10, "on_error", 1))
        self.events.append(Event(11, "on_cheer", 1))
        self.events.append(Event(12, "on_clearchat", 1))
        self.events.append(Event(13, "on_ban", 1))
        self.events.append(Event(14, "on_clearmsg", 1))
        self.events.append(Event(15, "on_globaluserstate", 1))
        self.events.append(Event(16, "on_notice", 1))
        self.events.append(Event(17, "on_hosttarget", 1))
        self.events.append(Event(18, "on_host", 1))
        self.events.append(Event(19, "on_sub", 1))
        self.events.append(Event(20, "on_resub", 1))
        self.events.append(Event(21, "on_subgift", 1))
        self.events.append(Event(22, "on_anonsubgift", 1))
        self.events.append(Event(23, "on_raid", 1))
        self.events.append(Event(24, "on_ritual", 1))
        self.events.append(Event(25, "on_charity", 1))
        self.events.append(Event(26, "on_submysterygift", 1))
        self.events.append(Event(27, "command_fired", 2))
    
    def _get_event(self, event_name):
        for event in self.events:
            if event.name == event_name:
                return event

    def _call_event(self, event_name, *args):
        if self._callbacks and event_name in self._callbacks:
            return self._callbacks[event_name](*args)

    def event(self, func):
        """
        This method is for accessing an event from class:Bot:.
        \nHas to be used as a decorator for a function.
        """

        event = self._get_event(func.__name__)
        if event:
            f_args = len(inspect.getargspec(func).args)
            if f_args != event.args:
                warnings.warn(f"Event \"{event.name}\" does not have correct number of parameters. {event.args} needed; {f_args} given.")
                return
            self._callbacks[func.__name__] = func
        else:
            warnings.warn(f"Event \"{func.__name__}\" does not exist.")

    ###################################
    #            MESSAGES             #
    ###################################
        
    def send_message(self, channel, message):
        """
        This method is for sending a message to a channel.
        """

        message_final = f"PRIVMSG #{channel} :{message}\r\n"
        self._socket.send(message_final.encode("utf-8"))

    def _main_read(self, line):
        # Check if Twitch sent a reconnect notice.
        # Not sure if this is the correct format, most-likely the same as PING, will fix if not the case.
        if line == "RECONNECT :tmi.twitch.tv" and self.reconnect:
            # Might need to wait here, docs do not have much information about this and have no example.
            # For now, just reconnect to all the current channels the bot should be connected to.
            self._join_room()
            return

        # Check if Twitch sent a ping.
        if line == "PING :tmi.twitch.tv" and self.reconnect:
            self._send_socket_message("PONG :tmi.twitch.tv")
            return

        #USERNOTICE.
        if f":tmi.twitch.tv USERNOTICE #" in line:
            usernotice = self._read_usernotice(line)
            self._call_event("on_usernotice", usernotice)
            if hasattr(usernotice, f"to_{usernotice.msg_id}"):
                self._call_event(f"on_{usernotice.msg_id}", getattr(usernotice, f"to_{usernotice.msg_id}")())
            else:
                self._call_event("on_error", CommonError(f"Twitch sent an unknown type of USERNOTICE: \"{usernotice.msg_id}\". Please submit a new issue to https://github.com/IsaacAKAJupiter/twitchircpy/issues including \"USERNOTICE\", \"{usernotice.msg_id}\" and \"{line}\" somewhere in the title or comment."))
            return

        #USERSTATE.
        if f":tmi.twitch.tv USERSTATE #" in line:
            userstate = self._read_userstate(line)
            self._call_event("on_userstate", userstate)
            return

        #GLOBALUSERSTATE.
        if f":tmi.twitch.tv GLOBALUSERSTATE" in line:
            globaluserstate = self._read_globaluserstate(line)
            self._call_event("on_globaluserstate", globaluserstate)
            return

        #ROOMSTATE.
        if ":tmi.twitch.tv ROOMSTATE #" in line:
            roomstate = self._read_roomstate(line)
            self._call_event("on_roomstate", roomstate)
            return

        #JOIN.
        if ".tmi.twitch.tv JOIN #" in line:
            join = self._read_join(line)
            if "#chatrooms" in line:
                self._call_event("chatroom_join", join)
            else:
                self._call_event("channel_join", join)
            return

        #PART.
        if ".tmi.twitch.tv PART #" in line:
            part = self._read_part(line)
            self._call_event("on_part", part)
            return

        #jtv MODE.
        if "jtv MODE #" in line:
            mode = self._read_mode(line)
            self._call_event("on_mode", mode)
            return

        #CLEARCHAT.
        if ":tmi.twitch.tv CLEARCHAT #" in line:
            clearchat = self._read_clearchat(line)
            self._call_event("on_clearchat", clearchat)
            self._call_event("on_ban", clearchat.to_ban())
            return

        #CLEARMSG.
        if ":tmi.twitch.tv CLEARMSG #" in line:
            clearmsg = self._read_clearmsg(line)
            self._call_event("on_clearmsg", clearmsg)
            return

        #NOTICE.
        if ":tmi.twitch.tv NOTICE #" in line:
            notice = self._read_notice(line)
            self._call_event("on_notice", notice)
            return

        #HOSTTARGET.
        if ":tmi.twitch.tv HOSTTARGET #" in line:
            hosttarget = self._read_hosttarget(line)
            self._call_event("on_hosttarget", hosttarget)
            self._call_event("on_host", hosttarget)
            return

        #PRIVMSG.
        if ".tmi.twitch.tv PRIVMSG #" in line:
            message, info = self._read_message(line)
            if message.bits:
                self._call_event("on_cheer", message)
            self._call_event("on_message", message)

            #Handle timed_messages.
            self._handle_timed_messages(message)

            #Handle commands.
            self._handle_commands(info)
        else:
            warnings.warn(f"When recieving data from Twitch, this got read wrong or got sent incorrectly by Twitch: \"{line}\"")

    def _read_default(self, message):
        splitspace = message.split(" ", 1)
        if splitspace[0].startswith("@"):
            splitspace[0] = splitspace[0][1:]
        message_data = splitspace[1].split(":", 2)
        split_user = splitspace[0].split(";")
        params = {}
        for s in split_user:
            ss = s.split("=")
            params[ss[0]] = ss[1]

        # Check for /me if it's PRIVMSG.
        if ".tmi.twitch.tv PRIVMSG #" in message:
            if "\u0001ACTION " in message_data[2]:
                params["has_me"] = True
                message_data[2] = message_data[2].split("\u0001")[1].replace("ACTION ", "")
            else:
                params["has_me"] = False

        return splitspace, params, message_data

    def _read_message(self, message):
        #BITS EX -> @badges=subscriber/0;bits=100;color=#0000FF;display-name=Atomic_2k;emotes=;flags=;id=1aea1e31-adce-45f1-972d-20a45b5e18bf;mod=0;room-id=90020006;subscriber=1;tmi-sent-ts=1542937782028;turbo=0;user-id=161329917;user-type= :atomic_2k!atomic_2k@atomic_2k.tmi.twitch.tv PRIVMSG #tsm_viss :kappa100
        _, params, message_data = self._read_default(message)
        return Message(message_data[1].split("#")[1][:-1], message_data[1].split("!")[0], message_data[2], params), Info(message_data[1].split("#")[1][:-1], message_data[1].split("!")[0], message_data[2], params)

    def _read_usernotice(self, message):
        #RESUB WITH MESSAGE -> @badges=subscriber/6;color=#36B319;display-name=DuckDuckLion;emotes=;flags=;id=efc65d23-12e8-4144-a419-b6fa50dab762;login=duckducklion;mod=0;msg-id=resub;msg-param-months=11;msg-param-sub-plan-name=Channel\sSubscription\s(vissgames);msg-param-sub-plan=1000;room-id=90020006;subscriber=1;system-msg=DuckDuckLion\sjust\ssubscribed\swith\sa\sTier\s1\ssub.\sDuckDuckLion\ssubscribed\sfor\s11\smonths\sin\sa\srow!;tmi-sent-ts=1542938148985;turbo=0;user-id=161337488;user-type= :tmi.twitch.tv USERNOTICE #tsm_viss :Black Friday was the first BR
        #GIFT -> @badges=subscriber/12,premium/1;color=#0000FF;display-name=gamblebamble;emotes=;flags=;id=fb2994c2-765b-4077-b7d5-a3081b300424;login=gamblebamble;mod=0;msg-id=subgift;msg-param-months=1;msg-param-origin-id=b5\sc0\sba\s23\s7f\sd9\sf1\s05\sf9\se0\s62\sfb\s14\s20\s4e\s5c\s80\s9c\sf3\s1e;msg-param-recipient-display-name=KnifeWound;msg-param-recipient-id=160154219;msg-param-recipient-user-name=knifewound;msg-param-sender-count=100;msg-param-sub-plan-name=Channel\sSubscription\s(vissgames);msg-param-sub-plan=1000;room-id=90020006;subscriber=1;system-msg=gamblebamble\sgifted\sa\sTier\s1\ssub\sto\sKnifeWound!\sThey\shave\sgiven\s100\sGift\sSubs\sin\sthe\schannel!;tmi-sent-ts=1542938555193;turbo=0;user-id=95464062;user-type= :tmi.twitch.tv USERNOTICE #tsm_viss
        #PRIME -> @badges=subscriber/0,turbo/1;color=#FF0000;display-name=xMAYZILLAx;emotes=;flags=;id=4f99520d-d07f-4250-9f59-a2e66aa7d811;login=xmayzillax;mod=0;msg-id=sub;msg-param-months=1;msg-param-sub-plan-name=Channel\sSubscription\s(vissgames);msg-param-sub-plan=Prime;room-id=90020006;subscriber=1;system-msg=xMAYZILLAx\sjust\ssubscribed\swith\sTwitch\sPrime!;tmi-sent-ts=1542938662653;turbo=1;user-id=189813901;user-type= :tmi.twitch.tv USERNOTICE #tsm_viss
        #NORMAL SUB -> @badges=subscriber/0;color=#0000FF;display-name=DemNades;emotes=;flags=;id=2b4240c9-95f6-405f-b4f6-9e941336752e;login=demnades;mod=0;msg-id=sub;msg-param-months=1;msg-param-sub-plan-name=Channel\sSubscription\s(vissgames);msg-param-sub-plan=1000;room-id=90020006;subscriber=1;system-msg=DemNades\sjust\ssubscribed\swith\sa\sTier\s1\ssub!;tmi-sent-ts=1542939145123;turbo=0;user-id=55216234;user-type= :tmi.twitch.tv USERNOTICE #tsm_viss
        splitspace, params, message_data = self._read_default(message)
        channel = splitspace[1].split("#")[1]
        if " :" in channel:
            channel = channel.split(" :")[0]
        params["channel"] = channel
        if len(message_data) > 2:
            params["message"] = message_data[2]
        return UserNotice(params)

    def _read_userstate(self, message):
        #EX -> @badges=;color=;display-name=JupiKD;emote-sets=0;mod=0;subscriber=0;user-type= :tmi.twitch.tv USERSTATE #dan_rll
        splitspace, params, _ = self._read_default(message)
        params["channel"] = splitspace[1].split("#")[1]
        return UserState(params)

    def _read_globaluserstate(self, message):
        #EX -> @badges=staff/1;color=#0D4200;display-name=dallas;emote-sets=0,33,50,237,793,2126,3517,4578,5569,9400,10337,12239;turbo=0;user-id=1337;user-type=admin :tmi.twitch.tv GLOBALUSERSTATE
        _, params, _ = self._read_default(message)
        return GlobalUserState(params)

    def _read_roomstate(self, message):
        #EX -> @broadcaster-lang=;emote-only=0;followers-only=-1;r9k=0;rituals=0;room-id=79095817;slow=0;subs-only=0 :tmi.twitch.tv ROOMSTATE #jups
        #EX2 -> @room-id=79095817;subs-only=1 :tmi.twitch.tv ROOMSTATE #jups
        splitspace, params, _ = self._read_default(message)
        params["channel"] = splitspace[1].split("#")[1]
        return RoomState(params)

    def _read_join(self, message):
        #CHANNEL -> :jupikd!jupikd@jupikd.tmi.twitch.tv JOIN #dan_rll
        #CHATROOM -> :ronni!ronni@ronni.tmi.twitch.tv JOIN #chatrooms:44322889:04e762ec-ce8f-4cbc-b6a3-ffc871ab53da
        if "#chatrooms" in message:
            colons = message.split(":")
            return JoinChatRoom(colons[1].split("!")[0], colons[3], int(colons[2]))
        else:
            return JoinChannel(message.split("!")[0][1:], message.split("#")[1])

    def _read_part(self, message):
        #EX -> :jupikd!jupikd@jupikd.tmi.twitch.tv PART #jups
        return PartChannel(message.split("!")[0][1:], message.split("#")[1])

    def _read_mode(self, message):
        #EX -> :jtv MODE #jups +o jupikd
        right_split = message.split("#")[1].split(" ")
        return Mode(right_split[0], right_split[2], True if "+o" in right_split[1] else False)

    def _read_clearchat(self, message):
        #EX -> @ban-reason=Follow\sthe\srules :tmi.twitch.tv CLEARCHAT #dallas :ronni
        _, params, message_data = self._read_default(message)
        return ClearChat(message_data[1].split(" ")[2][1:], message_data[2], params)

    def _read_clearmsg(self, message):
        #EX -> @login=jups;target-msg-id=5c709d48-1122-4a1c-af61-d0b920372a66 :tmi.twitch.tv CLEARMSG #jups :yeet
        _, params, message_data = self._read_default(message)
        return ClearMsg(message_data[1].split(" ")[2][1:], message_data[2], params)

    def _read_notice(self, message):
        #EX -> @msg-id=slow_off :tmi.twitch.tv NOTICE #chatrooms:44322889:04e762ec-ce8f-4cbc-b6a3-ffc871ab53da :This room is no longer in slow mode.
        _, params, message_data = self._read_default(message)
        if "#chatrooms:" in message:
            chatroom = message_data[3] if not " " in message_data[3] else message_data[3][:-1]
            return Notice(params["msg-id"], message_data[2], chatroom, message_data[4])
        else:
            return Notice(params["msg-id"], message_data[1].split(" ")[2][1:], None, message_data[2])

    def _read_hosttarget(self, message):
        # Start -> :tmi.twitch.tv HOSTTARGET #hosting_channel <channel> [<number-of-viewers>]
        # Stop -> :tmi.twitch.tv HOSTTARGET #hosting_channel :- [<number-of-viewers>]
        splitspace = message.split(" ")
        target = splitspace[3]
        if ":-" in target:
            target = None
        elif ":" in target:
            target = target[1:]
        viewer_bracket = splitspace[4].replace("[", "").replace("]", "")
        viewer_regex = re.search(r"\d*", splitspace[4])
        viewers = None
        if splitspace[4] == "-":
            viewers = None
        elif "[" in splitspace[4] and "]" in splitspace[4] and viewer_bracket != "":
            viewers = viewer_bracket
        elif viewer_regex != None:
            viewers = int(viewer_regex.string)
        return HostTarget(target, splitspace[2][1:], viewers)

    ###################################
    #              COGS               #
    ###################################

    def get_cog(self, cog_name):
        """
        This method is for getting a specific cog loaded in the class:Bot:.
        """

        for cog in self.cogs:
            if cog.__name__ == cog_name:
                return cog

        return None

    def _get_class_in_cog(self, cog):
        return inspect.getmembers(cog, inspect.isclass)[0][1]

    def add_cog(self, cog):
        """
        This method is the main way of adding commands into the class:Bot: via cogs.
        \nCogs are just classes containing mainly commands.
        \nIf you are having issues using cogs, please refer to the wiki on the GitHub page.
        \nhttps://github.com/IsaacAKAJupiter/twitchircpy/wiki
        """

        try:
            cog_o = importlib.import_module(cog)
        except ModuleNotFoundError:
            if self._socket:
                self._call_event("on_error", CogError(cog, f"An error occured when trying to import the cog."))
            else:
                warnings.warn(f"An error occured when importing cog: {cog}. This is a warning and not a class:Bot: error since it raised before \"run()\" was called.")
            return

        self.cogs.append(cog_o)
        if self._check_for_valid_cog(cog_o) == False:
            self._call_event("on_error", CogError(cog, f"Attempt to add cog failed. Missing valid setup function."))
            self.remove_cog(cog)
        else:
            getattr(cog_o, "setup")(self)

    def add_cogs(self, cogs):
        """
        This method is for adding multiple cogs via a list.
        """

        for cog in cogs:
            self.add_cog(cog)

    def remove_cog(self, cog):
        """
        This method is for removing a cog from the class:Bot:.
        """

        for c in self.cogs:
            if c.__name__ == cog:
                self.cogs.remove(c)
                self._remove_commands(c.__name__)
                del sys.modules[c.__name__]
                del c
                return

    def remove_cogs(self, cogs):
        """
        This method is for removing multiple cogs from the class:Bot: via a list.
        """

        removed = []
        for c in self.cogs:
            if c.__name__ in cogs:
                removed.append(c)

        for remove in removed:
            self.cogs.remove(remove)
            self._remove_commands(remove.__name__)
            del sys.modules[remove.__name__]
            del remove

    def reload_cog(self, cog):
        """
        This method is for reloading a cog within the class:Bot:.
        \nUsed for dynamic chat commands without restarting the class:Bot:.
        """

        self.remove_cog(cog)
        self.add_cog(cog)

    def reload_cogs(self, cogs):
        """
        This method is for reloading all cogs within the class:Bot:.
        """

        for cog in cogs:
            self.remove_cog(cog)
            self.add_cog(cog)

    def _check_for_valid_cog(self, cog):
        members = inspect.getmembers(cog)

        for member in members:
            if member[0] == "setup":
                return True

        return False

    def add_commands(self, cclass):
        """
        This method is used within the "setup" function within a cog.
        \nUsage:\n
        \nPass a new object of the cog class as the parameter. Example below if your cog class was "General".
        \ndef setup(bot):
        \n    bot.add_commands(General(bot))
        """

        classmembers = inspect.getmembers(cclass.__class__, inspect.isfunction)
        for i in classmembers:
            # Check for command.
            if "_decorators" in dir(i[1]) and "_cooldown" in dir(i[1]):
                if i[1]._decorators == "command":
                    self.commands.append(Command(len(self.commands), i[0], cclass, i[1], i[1]._cooldown))
            elif "_decorators" in dir(i[1]) and not "_cooldown" in dir(i[1]):
                if i[1]._decorators == "command":
                    self.commands.append(Command(len(self.commands), i[0], cclass, i[1], None)) 

    def _remove_commands(self, cog_name):
        removed = []
        for command in self.commands:
            if command.cog.__module__ == cog_name:
                removed.append(command)

        for remove in removed:
            self.commands.remove(remove)

    ###################################
    #            COMMANDS             #
    ###################################

    # Builtin command functions.

    def _define_builtin_commands(self):
        #self._builtin_commands.append(Command(len(self.commands), "thonking", self, "_builtin_thonking", None))
        pass

    def _check_builtin_command(self, command):
        for c in self._builtin_commands:
            if c.name == command:
                return True
    
        return False

    def _get_builtin_command(self, command):
        for c in self._builtin_commands:
            if c.name == command:
                return c
        
        return None

    # Normal command functions.

    def _handle_commands(self, info):
        prefix = self._call_event("dynamic_prefix", info)
        prefix = self._prefix if not prefix else prefix
        if not isinstance(prefix, str):
            self._call_event("on_error", EventError("dynamic_prefix", "This callback must return a string as the prefix."))
            prefix = self._prefix 

        if info.content.startswith(prefix):
            args = info.content.split(" ")
            command = args[0][1:]
            del args[0]
            self._run_command(command, info, args)

    def get_command(self, command):
        """
        This method is used for getting a command via name.
        """

        for c in self.commands:
            if c.name == command:
                return c
        
        return None

    def check_command(self, command):
        """
        This method is used for checking if a command exists with the given name.
        """

        for c in self.commands:
            if c.name == command:
                return True
    
        return False

    def _check_command_in_cooldown(self, c_id, channel):
        for cooldown in self.cooldowns:
            if cooldown.command_id == c_id and cooldown.channel == channel:
                return cooldown

        return None

    def _run_command(self, command, info, args):
        # Builtin commands.
        if self._check_builtin_command(command) == True:
            command_o = self._get_builtin_command(command)
            cooldown_o = self._check_command_in_cooldown(command_o.id, info.channel)
            if not cooldown_o:
                getattr(self, command_o.function)(info, *args)

        # Actual commands from cogs.
        if self.check_command(command) == True:
            command_o = self.get_command(command)
            cooldown_o = self._check_command_in_cooldown(command_o.id, info.channel)
            if not cooldown_o:
                try:
                    command_o.function(command_o.cog, info, *args) if args else command_o.function(command_o.cog, info)
                except TypeError as e:
                    self._call_event("on_error", CommandError(command_o, info.user, info.channel, f"Error running function -> TypeError: {e}"))
                    return
                # Add cooldown if command has it.
                if command_o.cooldown:
                    self._add_cooldown(command_o, info.channel)
                # Call event for command_fired.
                self._call_event("command_fired", info, command_o)
            else:
                self._call_event("on_error", CooldownError(command_o, info.user, info.channel, f"Command on cooldown, please wait {cooldown_o.time} seconds."))

    def _add_cooldown(self, command, channel):
        self.cooldowns.append(Cooldown(command.id, channel, command.cooldown))

    # Actual chat commands.
    def ban(self, channel, user, reason = None):
        """
        This is the built-in Twitch chat command for banning a user.
        \nEquivalent to:
        \nbot.send_message(channel, f".ban {user} {reason}")
        \nOr:
        \nbot.send_message(channel, f".ban {user}")
        """

        if reason:
            self.send_message(channel, f".ban {user} {reason}")
        else:
            self.send_message(channel, f".ban {user}")

    def unban(self, channel, user):
        """
        This is the built-in Twitch chat command for unbanning a user.
        \nEquivalent to:
        \nbot.send_message(channel, f".unban {user}")
        """

        self.send_message(channel, f".unban {user}")

    def whisper(self, channel, user, message):
        """
        This is the built-in Twitch chat command for whispering a user.
        \nEquivalent to:
        \nbot.send_message(channel, f".w {user} {message}")
        """

        self.send_message(channel, f".w {user} {message}")

    def w(self, channel, user, message):
        """
        This is the built-in Twitch chat command for whispering a user.
        \nEquivalent to:
        \nbot.send_message(channel, f".w {user} {message}")
        """

        self.send_message(channel, f".w {user} {message}")

    def me(self, channel, message):
        """
        This is the built-in Twitch chat command for /me.
        \nEquivalent to:
        \nbot.send_message(channel, f".me {message}")
        """

        self.send_message(channel, f".me {message}")

    def color(self, channel, color):
        """
        This is the built-in Twitch chat command for changing the color of the bots chat color.
        \nNote, if you are having issues with this method, try writing /help color in a Twitch chat to get the specifics how this command works.
        \nEquivalent to:
        \nbot.send_message(channel, f".color {color}")
        """

        colors = ["Blue", "BlueViolet", "CadetBlue", "Chocolate", "Coral", "DodgerBlue", "Firebrick", "GoldenRod", "Green", "HotPink", "OrangeRed", "Red", "SeaGreen", "SpringGreen", "YellowGreen"]
        if re.search(r"^(#)[A-Fa-f0-9]+$", color) or color in colors:
            self.send_message(channel, f".color {color}")
        else:
            self._call_event("on_error", CommonError("Color given is neither a HEX code nor a string color predefined by Twitch."))

    def commercial(self, channel, length = None):
        """
        This is the built-in Twitch chat command for running a commercial.
        \nEquivalent to:
        \nbot.send_message(channel, f".commercial {length}")
        \nOr:
        \nbot.send_message(channel, ".commercial")
        """

        if length and length.isdigit():
            self.send_message(channel, f".commercial {length}")
        else:
            self.send_message(channel, ".commercial")

    def timeout(self, channel, user, length = 600, reason = None):
        """
        This is the built-in Twitch chat command for timing out a user.
        \nEquivalent to:
        \nbot.send_message(channel, f".timeout {user} {length} {reason}")
        \nOr:
        \nbot.send_message(channel, f".timeout {user} {length}")
        """

        if reason:
            self.send_message(channel, f".timeout {user} {length} {reason}")
        elif not reason:
            self.send_message(channel, f".timeout {user} {length}")

    def untimeout(self, channel, user):
        """
        This is the built-in Twitch chat command for untiming out a user.
        \nEquivalent to:
        \nbot.send_message(channel, f".untimeout {user}")
        """

        self.send_message(channel, f".untimeout {user}")

    def slow(self, channel, amount = None):
        """
        This is the built-in Twitch chat command for enabling slow mode for a chat.
        \nEquivalent to:
        \nbot.send_message(channel, f".slow {amount}")
        \nOr:
        \nbot.send_message(channel, ".slow")
        """
        
        if amount:
            self.send_message(channel, f".slow {amount}")
        else:
            self.send_message(channel, ".slow")

    def slowoff(self, channel):
        """
        This is the built-in Twitch chat command for disabling slow mode for a chat.
        \nEquivalent to:
        \nbot.send_message(channel, ".slowoff")
        """

        self.send_message(channel, ".slowoff")

    def r9kbeta(self, channel):
        """
        This is the built-in Twitch chat command for enabling R9K mode for a chat.
        \nEquivalent to:
        \nbot.send_message(channel, ".r9kbeta")
        """

        self.send_message(channel, ".r9kbeta")

    def r9kbetaoff(self, channel):
        """
        This is the built-in Twitch chat command for disabling R9K mode for a chat.
        \nEquivalent to:
        \nbot.send_message(channel, ".r9kbetaoff")
        """

        self.send_message(channel, ".r9kbetaoff")

    def emoteonly(self, channel):
        """
        This is the built-in Twitch chat command for enabling emote-only mode for a chat.
        \nEquivalent to:
        \nbot.send_message(channel, ".emoteonly")
        """

        self.send_message(channel, ".emoteonly")

    def emoteonlyoff(self, channel):
        """
        This is the built-in Twitch chat command for disabling emote-only mode for a chat.
        \nEquivalent to:
        \nbot.send_message(channel, ".emoteonlyoff")
        """

        self.send_message(channel, ".emoteonlyoff")

    def clear(self, channel):
        """
        This is the built-in Twitch chat command for clearing chat.
        \nEquivalent to:
        \nbot.send_message(channel, ".clear")
        """

        self.send_message(channel, ".clear")

    def subscribers(self, channel):
        """
        This is the built-in Twitch chat command for enabling subscribers-only mode for a chat.
        \nEquivalent to:
        \nbot.send_message(channel, ".subscribers")
        """

        self.send_message(channel, ".subscribers")

    def subscribersoff(self, channel):
        """
        This is the built-in Twitch chat command for disabling subscribers-only mode for a chat.
        \nEquivalent to:
        \nbot.send_message(channel, ".subscribersoff")
        """

        self.send_message(channel, ".subscribersoff")

    def followers(self, channel, duration = None):
        """
        This is the built-in Twitch chat command for enabling followers-only mode for a chat.
        \nNote: {duration} is the length a user must have been following for to be able to chat. Leaving it :None: will allow all followers to chat.
        \nEquivalent to:
        \nbot.send_message(channel, f".followers {duration}")
        \nOr:
        \nbot.send_message(channel, ".followers")
        """

        if duration:
            self.send_message(channel, f".followers {duration}")
        else:
            self.send_message(channel, ".followers")

    def followersoff(self, channel):
        """
        This is the built-in Twitch chat command for disabling followers-only mode for a chat.
        \nEquivalent to:
        \nbot.send_message(channel, ".followersoff")
        """

        self.send_message(channel, ".followersoff")

    def delete(self, channel, message_id):
        """
        This is an IRC command for removing a single message from chat.
        \nEquivalent to:
        \nbot.send_message(channel, f".delete {message_id}")
        """

        self.send_message(channel, f".delete {message_id}")
class UserNotice():

    """
    Class used for storing information sent from the USERNOTICE command from the IRC.
    Used for notifying for subs, resubs, gifted subs, anonymous gifted subs, mystery gifted subs, raids, rituals and charity events.
    Charity is not in the documentation for Twitch IRC, not sure if it is for every charity event Twitch does.
    Worked for charity event occuring from December 12-27, 2018, with #charity cheering.
    Should not be manually created in most cases.

    Parameters
    ==========
    params -> :dict<str, str>:
        Holds every parameter that Twitch sends from USERNOTICE.
        Note, most parameters can be :None:.
        For more information, check out my wiki for this. https://github.com/IsaacAKAJupiter/twitchircpy/wiki/API-Reference#usernotice
    """

    def __init__(self, params):
        self.badges = params["badges"] if "badges" in params else None
        self.color = params["color"] if "color" in params else None
        self.display_name = params["display-name"] if "display-name" in params else None
        self.channel = params["channel"] if "channel" in params else None
        self.emotes = params["emotes"] if "emotes" in params else None
        self.id = params["id"] if "id" in params else None
        self.login = params["login"] if "login" in params else None
        self.message = params["message"] if "message" in params else None
        self.mod = int(params["mod"]) if "mod" in params else None
        self.msg_id = params["msg-id"] if "msg-id" in params else None
        self.msg_param_cumulative_months = int(
            params["msg-param-cumulative-months"]) if "msg-param-cumulative-months" in params else None
        self.msg_param_displayName = params["msg-param-displayName"] if "msg-param-displayName" in params else None
        self.msg_param_login = params["msg-param-login"] if "msg-param-login" in params else None
        self.msg_param_months = int(
            params["msg-param-months"]) if "msg-param-months" in params else None
        self.msg_param_recipient_display_name = params[
            "msg-param-recipient-display-name"] if "msg-param-recipient-display-name" in params else None
        self.msg_param_recipient_id = int(
            params["msg-param-recipient-id"]) if "msg-param-recipient-id" in params and params["msg-param-recipient-id"] else None
        self.msg_param_recipient_user_name = params[
            "msg-param-recipient-user-name"] if "msg-param-recipient-user-name" in params else None
        self.msg_param_should_share_streak = int(
            params["msg-param-should-share-streak"]) if "msg-param-should-share-streak" in params else None
        self.msg_param_streak_months = int(
            params["msg-param-streak-months"]) if "msg-param-streak-months" in params else None
        self.msg_param_sub_plan = params["msg-param-sub-plan"] if "msg-param-sub-plan" in params else None
        self.msg_param_sub_plan_name = params["msg-param-sub-plan-name"] if "msg-param-sub-plan-name" in params else None
        self.msg_param_viewerCount = int(
            params["msg-param-viewerCount"]) if "msg-param-viewerCount" in params and params["msg-param-viewerCount"] else None
        self.msg_param_ritual_name = params["msg-param-ritual-name"] if "msg-param-ritual-name" in params else None
        self.room_id = int(params["room-id"]) if "room-id" in params else None
        self.system_msg = params["system-msg"] if "system-msg" in params else None
        self.tmi_sent_ts = int(
            params["tmi-sent-ts"]) if "tmi-sent-ts" in params else None
        self.user_id = int(params["user-id"]) if "user-id" in params else None
        self.msg_param_charity_days_remaining = int(
            params["msg-param-charity-days-remaining"]) if "msg-param-charity-days-remaining" in params else None
        self.msg_param_charity_hashtag = params[
            "msg-param-charity-hashtag"] if "msg-param-charity-hashtag" in params else None
        self.msg_param_charity_hours_remaining = int(
            params["msg-param-charity-hours-remaining"]) if "msg-param-charity-hours-remaining" in params else None
        self.msg_param_charity_learn_more = params[
            "msg-param-charity-learn-more"] if "msg-param-charity-learn-more" in params else None
        self.msg_param_charity_name = params["msg-param-charity-name"] if "msg-param-charity-name" in params else None
        self.msg_param_total = float(
            params["msg-param-total"]) if "msg-param-total" in params else None

    def __repr__(self):
        return f"UserNotice(channel: {self.channel}, user: {self.display_name}, type: {self.msg_id})"

    def get_params(self):
        return {"badges": self.badges, "color": self.color, "display-name": self.display_name, "channel": self.channel, "emotes": self.emotes, "id": self.id, "login": self.login, "message": self.message, "mod": self.mod, "msg-id": self.msg_id, "msg-param-displayName": self.msg_param_displayName, "msg-param-login": self.msg_param_login, "msg-param-months": self.msg_param_months, "msg-param-recipient-display-name": self.msg_param_recipient_display_name, "msg-param-recipient-id": self.msg_param_recipient_id, "msg-param-recipient-user-name": self.msg_param_recipient_user_name, "msg-param-ritual-name": self.msg_param_ritual_name, "msg-param-sub-plan": self.msg_param_sub_plan, "msg-param-sub-plan-name": self.msg_param_sub_plan_name, "msg-param-viewerCount": self.msg_param_viewerCount, "room-id": self.room_id, "system-msg": self.system_msg, "tmi-sent-ts": self.tmi_sent_ts, "user-id": self.user_id}

    def to_sub(self):
        return Sub(self.get_params())

    def to_resub(self):
        return ReSub(self.get_params())

    def to_subgift(self):
        return SubGift(self.get_params())

    def to_anonsubgift(self):
        return AnonSubGift(self.get_params())

    def to_raid(self):
        return Raid(self.get_params())

    def to_ritual(self):
        return Ritual(self.get_params())

    def to_charity(self):
        return Charity(self.get_params())

    def to_submysterygift(self):
        return SubMysteryGift(self.get_params())


class Sub(UserNotice):

    """
    This class is the exact same as class:UserNotice: except with a different name.
    Created for specific msg_id of sub.
    Should not be manually created in most cases.
    """

    def __repr__(self):
        return f"Sub(channel: {self.channel}, user: {self.display_name})"


class ReSub(UserNotice):

    """
    This class is the exact same as class:UserNotice: except with a different name.
    Created for specific msg_id of resub.
    Should not be manually created in most cases.
    """

    def __repr__(self):
        return f"ReSub(channel: {self.channel}, user: {self.display_name}, months: {self.msg_param_months})"


class SubGift(UserNotice):

    """
    This class is the exact same as class:UserNotice: except with a different name.
    Created for specific msg_id of subgift.
    Should not be manually created in most cases.
    """

    def __repr__(self):
        return f"SubGift(channel: {self.channel}, user: {self.display_name})"


class AnonSubGift(UserNotice):

    """
    This class is the exact same as class:UserNotice: except with a different name.
    Created for specific msg_id of anonsubgift.
    Should not be manually created in most cases.
    """

    def __repr__(self):
        return f"AnonSubGift(channel: {self.channel}, user: {self.display_name})"


class Raid(UserNotice):

    """
    This class is the exact same as class:UserNotice: except with a different name.
    Created for specific msg_id of raid.
    Should not be manually created in most cases.
    """

    def __repr__(self):
        return f"Raid(channel: {self.channel}, user: {self.msg_param_displayName}, viewers: {self.msg_param_viewerCount})"


class Ritual(UserNotice):

    """
    This class is the exact same as class:UserNotice: except with a different name.
    Created for specific msg_id of ritual.
    Should not be manually created in most cases.
    """

    def __repr__(self):
        return f"Ritual(channel: {self.channel}, user: {self.display_name}, ritual name: {self.msg_param_ritual_name})"


class Charity(UserNotice):

    """
    This class is the exact same as class:UserNotice: except with a different name.
    Created for specific msg_id of charity.
    Should not be manually created in most cases.
    """

    def __repr__(self):
        return f"Charity(charity: {self.msg_param_charity_name}, charity learn more: {self.msg_param_charity_learn_more}, total: {self.msg_param_total})"


class SubMysteryGift(UserNotice):

    """
    This class is the exact same as class:UserNotice: except with a different name.
    Created for specific msg_id of submysterygift.
    Should not be manually created in most cases.
    """

    def __repr__(self):
        return f"SubMysteryGift(channel: {self.channel}, user: {self.display_name})"

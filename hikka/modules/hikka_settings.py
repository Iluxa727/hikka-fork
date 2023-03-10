# ÂŠī¸ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# đ https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# đ https://www.gnu.org/licenses/agpl-3.0.html

import logging
import os
import random

import hikkatl
from hikkatl.tl.functions.channels import JoinChannelRequest
from hikkatl.tl.functions.messages import (
    GetDialogFiltersRequest,
    UpdateDialogFilterRequest,
)
from hikkatl.tl.types import Message
from hikkatl.utils import get_display_name

from .. import loader, log, main, utils
from .._internal import fw_protect, restart
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)

ALL_INVOKES = [
    "clear_entity_cache",
    "clear_fulluser_cache",
    "clear_fullchannel_cache",
    "clear_perms_cache",
    "clear_cache",
    "reload_core",
    "inspect_cache",
    "inspect_modules",
]


@loader.tds
class HikkaSettingsMod(loader.Module):
    """Advanced settings for Hikka Userbot"""

    strings = {
        "name": "HikkaSettings",
        "watchers": (
            "<emoji document_id=5424885441100782420>đ</emoji>"
            " <b>Watchers:</b>\n\n<b>{}</b>"
        ),
        "no_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>No arguments"
            " specified</b>"
        ),
        "invoke404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Internal debug method"
            "</b> <code>{}</code> <b>not found, ergo can't be invoked</b>"
        ),
        "module404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Module</b>"
            " <code>{}</code> <b>not found</b>"
        ),
        "invoke": (
            "<emoji document_id=5215519585150706301>đ</emoji> <b>Invoked internal debug"
            " method</b> <code>{}</code>\n\n<emoji"
            " document_id=5784891605601225888>đĩ</emoji> <b>Result:\n{}</b>"
        ),
        "invoking": (
            "<emoji document_id=5213452215527677338>âŗ</emoji> <b>Invoking internal"
            " debug method</b> <code>{}</code> <b>of</b> <code>{}</code><b>...</b>"
        ),
        "mod404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Watcher {} not"
            " found</b>"
        ),
        "disabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>Watcher {} is now"
            " <u>disabled</u></b>"
        ),
        "enabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>Watcher {} is now"
            " <u>enabled</u></b>"
        ),
        "args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>You need to specify"
            " watcher name</b>"
        ),
        "user_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick for this user"
            " is now {}</b>"
        ),
        "no_cmd": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Please, specify"
            " command to toggle NoNick for</b>"
        ),
        "cmd_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick for"
            "</b> <code>{}</code> <b>is now {}</b>"
        ),
        "cmd404": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Command not found</b>"
        ),
        "inline_settings": "âī¸ <b>Here you can configure your Hikka settings</b>",
        "confirm_update": (
            "đ§­ <b>Please, confirm that you want to update. Your userbot will be"
            " restarted</b>"
        ),
        "confirm_restart": "đ <b>Please, confirm that you want to restart</b>",
        "suggest_fs": "â Suggest FS for modules",
        "do_not_suggest_fs": "đĢ Suggest FS for modules",
        "use_fs": "â Always use FS for modules",
        "do_not_use_fs": "đĢ Always use FS for modules",
        "btn_restart": "đ Restart",
        "btn_update": "đ§­ Update",
        "close_menu": "đ Close menu",
        "custom_emojis": "â Custom emojis",
        "no_custom_emojis": "đĢ Custom emojis",
        "suggest_subscribe": "â Suggest subscribe to channel",
        "do_not_suggest_subscribe": "đĢ Suggest subscribe to channel",
        "private_not_allowed": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>This command must be"
            " executed in chat</b>"
        ),
        "nonick_warning": (
            "Warning! You enabled NoNick with default prefix! "
            "You may get muted in Hikka chats. Change prefix or "
            "disable NoNick!"
        ),
        "reply_required": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Reply to a message"
            " of user, which needs to be added to NoNick</b>"
        ),
        "deauth_confirm": (
            "â ī¸ <b>This action will fully remove Hikka from this account and can't be"
            " reverted!</b>\n\n<i>- Hikka chats will be removed\n- Session will be"
            " terminated and removed\n- Hikka inline bot will be removed</i>"
        ),
        "deauth_confirm_step2": (
            "â ī¸ <b>Are you really sure you want to delete Hikka?</b>"
        ),
        "deauth_yes": "I'm sure",
        "deauth_no_1": "I'm not sure",
        "deauth_no_2": "I'm uncertain",
        "deauth_no_3": "I'm struggling to answer",
        "deauth_cancel": "đĢ Cancel",
        "deauth_confirm_btn": "đĸ Delete",
        "uninstall": "đĸ <b>Uninstalling Hikka...</b>",
        "uninstalled": (
            "đĸ <b>Hikka uninstalled. Web interface is still active, you can add another"
            " account</b>"
        ),
        "cmd_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick is enabled"
            " for these commands:</b>\n\n{}"
        ),
        "user_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick is enabled"
            " for these users:</b>\n\n{}"
        ),
        "chat_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick is enabled"
            " for these chats:</b>\n\n{}"
        ),
        "nothing": (
            "<emoji document_id=5427052514094619126>đ¤ˇââī¸</emoji> <b>Nothing to"
            " show...</b>"
        ),
        "privacy_leak": (
            "â ī¸ <b>This command gives access to your Hikka web interface. It's not"
            " recommended to run it in public group chats. Consider using it in <a"
            " href='tg://openmessage?user_id={}'>Saved messages</a>. Type"
            "</b> <code>{}proxypass force_insecure</code> <b>to ignore this warning</b>"
        ),
        "privacy_leak_nowarn": (
            "â ī¸ <b>This command gives access to your Hikka web interface. It's not"
            " recommended to run it in public group chats. Consider using it in <a"
            " href='tg://openmessage?user_id={}'>Saved messages</a>.</b>"
        ),
        "opening_tunnel": "đ <b>Opening tunnel to Hikka web interface...</b>",
        "tunnel_opened": "đ <b>Tunnel opened. This link is valid for about 1 hour</b>",
        "web_btn": "đ Web interface",
        "btn_yes": "đ¸ Open anyway",
        "btn_no": "đģ Cancel",
        "lavhost_web": (
            "âī¸ <b>This link leads to your Hikka web interface on lavHost</b>\n\n<i>đĄ"
            " You'll need to authorize using lavHost credentials, specified on"
            " registration</i>"
        ),
        "disable_debugger": "â Debugger enabled",
        "enable_debugger": "đĢ Debugger disabled",
    }

    strings_ru = {
        "watchers": (
            "<emoji document_id=5424885441100782420>đ</emoji>"
            " <b>ĐĄĐŧĐžŅŅĐ¸ŅĐĩĐģĐ¸:</b>\n\n<b>{}</b>"
        ),
        "mod404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĄĐŧĐžŅŅĐ¸ŅĐĩĐģŅ {} ĐŊĐĩ"
            " ĐŊĐ°ĐšĐ´ĐĩĐŊ</b>"
        ),
        "disabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>ĐĄĐŧĐžŅŅĐ¸ŅĐĩĐģŅ {} ŅĐĩĐŋĐĩŅŅ"
            " <u>Đ˛ŅĐēĐģŅŅĐĩĐŊ</u></b>"
        ),
        "enabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>ĐĄĐŧĐžŅŅĐ¸ŅĐĩĐģŅ {} ŅĐĩĐŋĐĩŅŅ"
            " <u>Đ˛ĐēĐģŅŅĐĩĐŊ</u></b>"
        ),
        "args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐŖĐēĐ°ĐļĐ¸ Đ¸ĐŧŅ"
            " ŅĐŧĐžŅŅĐ¸ŅĐĩĐģŅ</b>"
        ),
        "user_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>ĐĄĐžŅŅĐžŅĐŊĐ¸Đĩ NoNick Đ´ĐģŅ"
            " ŅŅĐžĐŗĐž ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ: {}</b>"
        ),
        "no_cmd": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>ĐŖĐēĐ°ĐļĐ¸ ĐēĐžĐŧĐ°ĐŊĐ´Ņ, Đ´ĐģŅ"
            " ĐēĐžŅĐžŅĐžĐš ĐŊĐ°Đ´Đž Đ˛ĐēĐģŅŅĐ¸ŅŅ\\Đ˛ŅĐēĐģŅŅĐ¸ŅŅ NoNick</b>"
        ),
        "cmd_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>ĐĄĐžŅŅĐžŅĐŊĐ¸Đĩ NoNick Đ´ĐģŅ"
            "</b> <code>{}</code><b>: {}</b>"
        ),
        "cmd404": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>ĐĐžĐŧĐ°ĐŊĐ´Đ° ĐŊĐĩ ĐŊĐ°ĐšĐ´ĐĩĐŊĐ°</b>"
        ),
        "inline_settings": "âī¸ <b>ĐĐ´ĐĩŅŅ ĐŧĐžĐļĐŊĐž ŅĐŋŅĐ°Đ˛ĐģŅŅŅ ĐŊĐ°ŅŅŅĐžĐšĐēĐ°ĐŧĐ¸ Hikka</b>",
        "confirm_update": "đ§­ <b>ĐĐžĐ´ŅĐ˛ĐĩŅĐ´Đ¸ŅĐĩ ĐžĐąĐŊĐžĐ˛ĐģĐĩĐŊĐ¸Đĩ. ĐŽĐˇĐĩŅĐąĐžŅ ĐąŅĐ´ĐĩŅ ĐŋĐĩŅĐĩĐˇĐ°ĐŗŅŅĐļĐĩĐŊ</b>",
        "confirm_restart": "đ <b>ĐĐžĐ´ŅĐ˛ĐĩŅĐ´Đ¸ŅĐĩ ĐŋĐĩŅĐĩĐˇĐ°ĐŗŅŅĐˇĐēŅ</b>",
        "suggest_fs": "â ĐŅĐĩĐ´ĐģĐ°ĐŗĐ°ŅŅ ŅĐžŅŅĐ°ĐŊĐĩĐŊĐ¸Đĩ ĐŧĐžĐ´ŅĐģĐĩĐš",
        "do_not_suggest_fs": "đĢ ĐŅĐĩĐ´ĐģĐ°ĐŗĐ°ŅŅ ŅĐžŅŅĐ°ĐŊĐĩĐŊĐ¸Đĩ ĐŧĐžĐ´ŅĐģĐĩĐš",
        "use_fs": "â ĐŅĐĩĐŗĐ´Đ° ŅĐžŅŅĐ°ĐŊŅŅŅ ĐŧĐžĐ´ŅĐģĐ¸",
        "do_not_use_fs": "đĢ ĐŅĐĩĐŗĐ´Đ° ŅĐžŅŅĐ°ĐŊŅŅŅ ĐŧĐžĐ´ŅĐģĐ¸",
        "btn_restart": "đ ĐĐĩŅĐĩĐˇĐ°ĐŗŅŅĐˇĐēĐ°",
        "btn_update": "đ§­ ĐĐąĐŊĐžĐ˛ĐģĐĩĐŊĐ¸Đĩ",
        "close_menu": "đ ĐĐ°ĐēŅŅŅŅ ĐŧĐĩĐŊŅ",
        "custom_emojis": "â ĐĐ°ŅŅĐžĐŧĐŊŅĐĩ ŅĐŧĐžĐ´ĐˇĐ¸",
        "no_custom_emojis": "đĢ ĐĐ°ŅŅĐžĐŧĐŊŅĐĩ ŅĐŧĐžĐ´ĐˇĐ¸",
        "suggest_subscribe": "â ĐŅĐĩĐ´ĐģĐ°ĐŗĐ°ŅŅ ĐŋĐžĐ´ĐŋĐ¸ŅĐēŅ ĐŊĐ° ĐēĐ°ĐŊĐ°Đģ",
        "do_not_suggest_subscribe": "đĢ ĐŅĐĩĐ´ĐģĐ°ĐŗĐ°ŅŅ ĐŋĐžĐ´ĐŋĐ¸ŅĐēŅ ĐŊĐ° ĐēĐ°ĐŊĐ°Đģ",
        "private_not_allowed": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Đ­ŅŅ ĐēĐžĐŧĐ°ĐŊĐ´Ņ ĐŊŅĐļĐŊĐž"
            " Đ˛ŅĐŋĐžĐģĐŊŅŅŅ Đ˛ ŅĐ°ŅĐĩ</b>"
        ),
        "_cls_doc": "ĐĐžĐŋĐžĐģĐŊĐ¸ŅĐĩĐģŅĐŊŅĐĩ ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸ Hikka",
        "nonick_warning": (
            "ĐĐŊĐ¸ĐŧĐ°ĐŊĐ¸Đĩ! ĐĸŅ Đ˛ĐēĐģŅŅĐ¸Đģ NoNick ŅĐž ŅŅĐ°ĐŊĐ´Đ°ŅŅĐŊŅĐŧ ĐŋŅĐĩŅĐ¸ĐēŅĐžĐŧ! "
            "ĐĸĐĩĐąŅ ĐŧĐžĐŗŅŅ ĐˇĐ°ĐŧŅŅŅĐ¸ŅŅ Đ˛ ŅĐ°ŅĐ°Ņ Hikka. ĐĐˇĐŧĐĩĐŊĐ¸ ĐŋŅĐĩŅĐ¸ĐēŅ Đ¸ĐģĐ¸ "
            "ĐžŅĐēĐģŅŅĐ¸ ĐŗĐģĐžĐąĐ°ĐģŅĐŊŅĐš NoNick!"
        ),
        "reply_required": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐŅĐ˛ĐĩŅŅ ĐŊĐ° ŅĐžĐžĐąŅĐĩĐŊĐ¸Đĩ"
            " ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ, Đ´ĐģŅ ĐēĐžŅĐžŅĐžĐŗĐž ĐŊŅĐļĐŊĐž Đ˛ĐēĐģŅŅĐ¸ŅŅ NoNick</b>"
        ),
        "deauth_confirm": (
            "â ī¸ <b>Đ­ŅĐž Đ´ĐĩĐšŅŅĐ˛Đ¸Đĩ ĐŋĐžĐģĐŊĐžŅŅŅŅ ŅĐ´Đ°ĐģĐ¸Ņ Hikka Ņ ŅŅĐžĐŗĐž Đ°ĐēĐēĐ°ŅĐŊŅĐ°! ĐĐŗĐž ĐŊĐĩĐģŅĐˇŅ"
            " ĐžŅĐŧĐĩĐŊĐ¸ŅŅ</b>\n\n<i>- ĐŅĐĩ ŅĐ°ŅŅ, ŅĐ˛ŅĐˇĐ°ĐŊĐŊŅĐĩ Ņ Hikka ĐąŅĐ´ŅŅ ŅĐ´Đ°ĐģĐĩĐŊŅ\n- ĐĄĐĩŅŅĐ¸Ņ"
            " Hikka ĐąŅĐ´ĐĩŅ ŅĐąŅĐžŅĐĩĐŊĐ°\n- ĐĐŊĐģĐ°ĐšĐŊ ĐąĐžŅ Hikka ĐąŅĐ´ĐĩŅ ŅĐ´Đ°ĐģĐĩĐŊ</i>"
        ),
        "deauth_confirm_step2": "â ī¸ <b>ĐĸŅ ŅĐžŅĐŊĐž ŅĐ˛ĐĩŅĐĩĐŊ, ŅŅĐž ŅĐžŅĐĩŅŅ ŅĐ´Đ°ĐģĐ¸ŅŅ Hikka?</b>",
        "deauth_yes": "Đ¯ ŅĐ˛ĐĩŅĐĩĐŊ",
        "deauth_no_1": "Đ¯ ĐŊĐĩ ŅĐ˛ĐĩŅĐĩĐŊ",
        "deauth_no_2": "ĐĐĩ ŅĐžŅĐŊĐž",
        "deauth_no_3": "ĐĐĩŅ",
        "deauth_cancel": "đĢ ĐŅĐŧĐĩĐŊĐ°",
        "deauth_confirm_btn": "đĸ ĐŖĐ´Đ°ĐģĐ¸ŅŅ",
        "uninstall": "đĸ <b>ĐŖĐ´Đ°ĐģŅŅ Hikka...</b>",
        "uninstalled": (
            "đĸ <b>Hikka ŅĐ´Đ°ĐģĐĩĐŊĐ°. ĐĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅ Đ˛ŅĐĩ ĐĩŅĐĩ Đ°ĐēŅĐ¸Đ˛ĐĩĐŊ, ĐŧĐžĐļĐŊĐž Đ´ĐžĐąĐ°Đ˛Đ¸ŅŅ Đ´ŅŅĐŗĐ¸Đĩ"
            " Đ°ĐēĐēĐ°ŅĐŊŅŅ!</b>"
        ),
        "cmd_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick Đ˛ĐēĐģŅŅĐĩĐŊ Đ´ĐģŅ"
            " ŅŅĐ¸Ņ ĐēĐžĐŧĐ°ĐŊĐ´:</b>\n\n{}"
        ),
        "user_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick Đ˛ĐēĐģŅŅĐĩĐŊ Đ´ĐģŅ"
            " ŅŅĐ¸Ņ ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģĐĩĐš:</b>\n\n{}"
        ),
        "chat_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick Đ˛ĐēĐģŅŅĐĩĐŊ Đ´ĐģŅ"
            " ŅŅĐ¸Ņ ŅĐ°ŅĐžĐ˛:</b>\n\n{}"
        ),
        "nothing": (
            "<emoji document_id=5427052514094619126>đ¤ˇââī¸</emoji> <b>ĐĐĩŅĐĩĐŗĐž"
            " ĐŋĐžĐēĐ°ĐˇŅĐ˛Đ°ŅŅ...</b>"
        ),
        "privacy_leak": (
            "â ī¸ <b>Đ­ŅĐ° ĐēĐžĐŧĐ°ĐŊĐ´Đ° Đ´Đ°ĐĩŅ Đ´ĐžŅŅŅĐŋ Đē Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅŅ Hikka. ĐĐĩ Đ˛ŅĐŋĐžĐģĐŊĐĩĐŊĐ¸Đĩ Đ˛"
            " ĐŋŅĐąĐģĐ¸ŅĐŊŅŅ ŅĐ°ŅĐ°Ņ ŅĐ˛ĐģŅĐĩŅŅŅ ŅĐŗŅĐžĐˇĐžĐš ĐąĐĩĐˇĐžĐŋĐ°ŅĐŊĐžŅŅĐ¸. ĐŅĐĩĐ´ĐŋĐžŅŅĐ¸ŅĐĩĐģŅĐŊĐž Đ˛ŅĐŋĐžĐģĐŊŅŅŅ"
            " ĐĩĐĩ Đ˛ <a href='tg://openmessage?user_id={}'>ĐĐˇĐąŅĐ°ĐŊĐŊŅŅ ŅĐžĐžĐąŅĐĩĐŊĐ¸ŅŅ</a>."
            " ĐŅĐŋĐžĐģĐŊĐ¸</b> <code>{}proxypass force_insecure</code> <b>ŅŅĐžĐąŅ ĐžŅĐēĐģŅŅĐ¸ŅŅ"
            " ŅŅĐž ĐŋŅĐĩĐ´ŅĐŋŅĐĩĐļĐ´ĐĩĐŊĐ¸Đĩ</b>"
        ),
        "privacy_leak_nowarn": (
            "â ī¸ <b>Đ­ŅĐ° ĐēĐžĐŧĐ°ĐŊĐ´Đ° Đ´Đ°ĐĩŅ Đ´ĐžŅŅŅĐŋ Đē Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅŅ Hikka. ĐĐĩ Đ˛ŅĐŋĐžĐģĐŊĐĩĐŊĐ¸Đĩ Đ˛"
            " ĐŋŅĐąĐģĐ¸ŅĐŊŅŅ ŅĐ°ŅĐ°Ņ ŅĐ˛ĐģŅĐĩŅŅŅ ŅĐŗŅĐžĐˇĐžĐš ĐąĐĩĐˇĐžĐŋĐ°ŅĐŊĐžŅŅĐ¸. ĐŅĐĩĐ´ĐŋĐžŅŅĐ¸ŅĐĩĐģŅĐŊĐž Đ˛ŅĐŋĐžĐģĐŊŅŅŅ"
            " ĐĩĐĩ Đ˛ <a href='tg://openmessage?user_id={}'>ĐĐˇĐąŅĐ°ĐŊĐŊŅŅ ŅĐžĐžĐąŅĐĩĐŊĐ¸ŅŅ</a>.</b>"
        ),
        "opening_tunnel": "đ <b>ĐŅĐēŅŅĐ˛Đ°Ņ ŅĐžĐŊĐŊĐĩĐģŅ Đē Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅŅ Hikka...</b>",
        "tunnel_opened": (
            "đ <b>ĐĸĐžĐŊĐŊĐĩĐģŅ ĐžŅĐēŅŅŅ. Đ­ŅĐ° ŅŅŅĐģĐēĐ° ĐąŅĐ´ĐĩŅ Đ°ĐēŅĐ¸Đ˛ĐŊĐ° ĐŊĐĩ ĐąĐžĐģĐĩĐĩ ŅĐ°ŅĐ°</b>"
        ),
        "web_btn": "đ ĐĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅ",
        "btn_yes": "đ¸ ĐŅĐĩ ŅĐ°Đ˛ĐŊĐž ĐžŅĐēŅŅŅŅ",
        "btn_no": "đģ ĐĐ°ĐēŅŅŅŅ",
        "lavhost_web": (
            "âī¸ <b>ĐĐž ŅŅĐžĐš ŅŅŅĐģĐēĐĩ ŅŅ ĐŋĐžĐŋĐ°Đ´ĐĩŅŅ Đ˛ Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅ Hikka ĐŊĐ°"
            " lavHost</b>\n\n<i>đĄ ĐĸĐĩĐąĐĩ ĐŊŅĐļĐŊĐž ĐąŅĐ´ĐĩŅ Đ°Đ˛ŅĐžŅĐ¸ĐˇĐžĐ˛Đ°ŅŅŅŅ, Đ¸ŅĐŋĐžĐģŅĐˇŅŅ Đ´Đ°ĐŊĐŊŅĐĩ,"
            " ŅĐēĐ°ĐˇĐ°ĐŊĐŊŅĐĩ ĐŋŅĐ¸ ĐŊĐ°ŅŅŅĐžĐšĐēĐĩ lavHost</i>"
        ),
        "disable_debugger": "â ĐŅĐģĐ°Đ´ŅĐ¸Đē Đ˛ĐēĐģŅŅĐĩĐŊ",
        "enable_debugger": "đĢ ĐŅĐģĐ°Đ´ŅĐ¸Đē Đ˛ŅĐēĐģŅŅĐĩĐŊ",
    }

    strings_fr = {
        "watchers": (
            "<emoji document_id=5424885441100782420>đ</emoji>"
            " <b>Les observateurs:</b>\n\n<b>{}</b>"
        ),
        "mod404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>L'observateur {} n'est"
            " pas trouvÃŠ</b>"
        ),
        "disabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>L'observateur {} est"
            " maintenant <u>dÃŠsactivÃŠ</u></b>"
        ),
        "enabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>L'observateur {} est"
            " maintenant <u>activÃŠ</u></b>"
        ),
        "args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Indiquez le nom"
            " de l'observateur</b>"
        ),
        "user_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>L'ÃŠtat de NoNick pour"
            " cet utilisateur: {}</b>"
        ),
        "no_cmd": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Indiquez la commande"
            " pour laquelle vous souhaitez activer\\dÃŠsactiver NoNick</b>"
        ),
        "cmd_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>L'ÃŠtat de NoNick"
            " pour</b> <code>{}</code><b>: {}</b>"
        ),
        "cmd404": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Commande non"
            " trouvÃŠe</b>"
        ),
        "inline_settings": "âī¸ <b>Vous pouvez gÃŠrer les paramÃ¨tres Hikka ici</b>",
        "confirm_update": (
            "đ§­ <b>Confirmez la mise Ã  jour. L'utilisateur-bot sera redÃŠmarrÃŠ</b>"
        ),
        "confirm_restart": "đ <b>Confirmez le redÃŠmarrage</b>",
        "suggest_fs": "â SuggÃŠrer l'enregistrement des modules",
        "do_not_suggest_fs": "đĢ SuggÃŠrer l'enregistrement des modules",
        "use_fs": "â Toujours enregistrer les modules",
        "do_not_use_fs": "đĢ Toujours enregistrer les modules",
        "btn_restart": "đ RedÃŠmarrer",
        "btn_update": "đ§­ Mise Ã  jour",
        "close_menu": "đ Fermer le menu",
        "custom_emojis": "â ÃmoticÃ´nes personnalisÃŠes",
        "no_custom_emojis": "đĢ ÃmoticÃ´nes personnalisÃŠes",
        "suggest_subscribe": "â SuggÃŠrer l'abonnement au canal",
        "do_not_suggest_subscribe": "đĢ SuggÃŠrer l'abonnement au canal",
        "private_not_allowed": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Vous devez exÃŠcuter"
            " cette commande dans un chat</b>"
        ),
        "_cls_doc": "ParamÃ¨tres supplÃŠmentaires Hikka",
        "nonick_warning": (
            "Attention! Vous avez activÃŠ NoNick avec le prÃŠfixe standard! "
            "Vous pouvez ÃĒtre mutÃŠ dans les chats Hikka. Changez le prÃŠfixe ou "
            "dÃŠsactivez NoNick global!"
        ),
        "reply_required": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>RÃŠpondez au message"
            " de l'utilisateur pour lequel vous devez activer NoNick</b>"
        ),
        "deauth_confirm": (
            "â ī¸ <b>Cette action supprimera complÃ¨tement Hikka de ce compte! Il ne peut"
            " pas ÃĒtre annulÃŠ</b>\n\n<i>- Toutes les conversations liÃŠes Ã  Hikka seront"
            " supprimÃŠes\n- La session Hikka sera rÃŠinitialisÃŠe\n- Le bot en ligne"
            " Hikka sera supprimÃŠ</i>"
        ),
        "deauth_confirm_step2": "â ī¸ <b>Ãtes-vous sÃģr de vouloir supprimer Hikka?</b>",
        "deauth_yes": "Je suis sÃģr",
        "deauth_no_1": "Je ne suis pas sÃģr",
        "deauth_no_2": "Pas vraiment",
        "deauth_no_3": "Non",
        "deauth_cancel": "đĢ Annuler",
        "deauth_confirm_btn": "đĸ Supprimer",
        "uninstall": "đĸ <b>Je supprime Hikka...</b>",
        "uninstalled": (
            "đĸ <b>Hikka a ÃŠtÃŠ supprimÃŠ. L'interface Web est toujours active, vous"
            " pouvez ajouter d'autres comptes!</b>"
        ),
        "cmd_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick est activÃŠ pour"
            " ces commandes:</b>\n\n{}"
        ),
        "user_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick est activÃŠ"
            " pour ces utilisateurs:</b>\n\n{}"
        ),
        "chat_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick est activÃŠ"
            " pour ces groupes:</b>\n\n{}"
        ),
        "nothing": (
            "<emoji document_id=5427052514094619126>đ¤ˇââī¸</emoji> <b>Rien Ã "
            " montrer...</b>"
        ),
        "privacy_leak": (
            "â ī¸ <b>Cette commande donne accÃ¨s Ã  l'interface web de Hikka. L'exÃŠcution"
            " dans les groupes est une menace pour la sÃŠcuritÃŠ. PrÃŠfÃŠrez l'exÃŠcution"
            " dans <a href='tg://openmessage?user_id={}'>Messages favoris</a>."
            " ExÃŠcutez</b> <code>{}proxypass force_insecure</code> <b>pour dÃŠsactiver"
            " cette alerte</b>"
        ),
        "privacy_leak_nowarn": (
            "â ī¸ <b>Cette commande donne accÃ¨s Ã  l'interface web de Hikka. L'exÃŠcution"
            " dans les groupes est une menace pour la sÃŠcuritÃŠ. PrÃŠfÃŠrez l'exÃŠcution"
            " dans <a href='tg://openmessage?user_id={}'>Messages favoris</a>.</b>"
        ),
        "opening_tunnel": (
            "đ <b>Ouverture du tunnel vers l'interface web de Hikka...</b>"
        ),
        "tunnel_opened": (
            "đ <b>Tunnel ouvert. Ce lien ne sera actif que pendant une heure</b>"
        ),
        "web_btn": "đ Interface web",
        "btn_yes": "đ¸ Ouvrir quand mÃĒme",
        "btn_no": "đģ Fermer",
        "lavhost_web": (
            "âī¸ <b>En cliquant sur ce lien, tu accÃ¨deras Ã  l'interface web de Hikka"
            " sur lavHost</b>\n\n<i>đĄ Tu devras t'authentifier avec les donnÃŠes"
            " spÃŠcifiÃŠes lors de la configuration de lavHost</i>"
        ),
        "disable_debugger": "â DÃŠbogueur activÃŠ",
        "enable_debugger": "đĢ DÃŠbogueur dÃŠsactivÃŠ",
    }

    strings_it = {
        "watchers": (
            "<emoji document_id=5424885441100782420>đ</emoji>"
            " <b>Guardiani:</b>\n\n<b>{}</b>"
        ),
        "mod404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Il guardiano {} non"
            " Ã¨ stato trovato</b>"
        ),
        "disabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>Il guardiano {} Ã¨"
            " <u>disabilitato</u></b>"
        ),
        "enabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>Il guardiano {} Ã¨"
            " <u>abilitato</u></b>"
        ),
        "args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Specifica il nome del"
            " guardiano</b>"
        ),
        "user_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Stato di NoNick per"
            " questo utente: {}</b>"
        ),
        "no_cmd": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Specifica il comando"
            " per cui vuoi abilitare\\disabilitare NoNick</b>"
        ),
        "cmd_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Stato di NoNick per"
            "</b> <code>{}</code><b>: {}</b>"
        ),
        "cmd404": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Comando non"
            " trovato</b>"
        ),
        "inline_settings": "âī¸ <b>Qui puoi gestire le impostazioni di Hikka</b>",
        "confirm_update": "đ§­ <b>Conferma l'aggiornamento. Il bot verrÃ  riavviato</b>",
        "confirm_restart": "đ <b>Conferma il riavvio</b>",
        "suggest_fs": "â Suggerisci il salvataggio dei moduli",
        "do_not_suggest_fs": "đĢ Suggerisci il salvataggio dei moduli",
        "use_fs": "â Salva sempre i moduli",
        "do_not_use_fs": "đĢ Salva sempre i moduli",
        "btn_restart": "đ Riavvia",
        "btn_update": "đ§­ Aggiorna",
        "close_menu": "đ Chiudi il menu",
        "custom_emojis": "â Emoji personalizzate",
        "no_custom_emojis": "đĢ Emoji personalizzati",
        "suggest_subscribe": "â Suggest subscribe to channel",
        "do_not_suggest_subscribe": "đĢ Non suggerire l'iscrizione al canale",
        "private_not_allowed": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Questo comando deve"
            " essere eseguito in un gruppo</b>"
        ),
        "_cls_doc": "Impostazioni aggiuntive di Hikka",
        "nonick_warning": (
            "Attenzione! Hai abilitato NoNick con il prefisso predefinito! "
            "Puoi essere mutato nei gruppi di Hikka. Modifica il prefisso o "
            "disabilita NoNick!"
        ),
        "reply_required": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Rispondi al messaggio"
            " di un utente per cui vuoi abilitare NoNick</b>"
        ),
        "deauth_confirm": (
            "â ī¸ <b>Questa azione rimuoverÃ  completamente Hikka da questo account! Non"
            " puÃ˛ essere annullata</b>\n\n<i>- Tutte le chat associate a Hikka saranno"
            " rimosse\n- La sessione Hikka verrÃ  annullata\n- Il bot inline Hikka verrÃ "
            " rimosso</i>"
        ),
        "deauth_confirm_step2": "â ī¸ <b>Sei sicuro di voler rimuovere Hikka?</b>",
        "deauth_yes": "Sono sicuro",
        "deauth_no_1": "Non sono sicuro",
        "deauth_no_2": "Non esattamente",
        "deauth_no_3": "No",
        "deauth_cancel": "đĢ Annulla",
        "deauth_confirm_btn": "đĸ Rimuovi",
        "uninstall": "đĸ <b>Rimuovo Hikka...</b>",
        "uninstalled": (
            "đĸ <b>Hikka Ã¨ stata rimossa. L'interfaccia web Ã¨ ancora attiva, puoi"
            " aggiungere altri account!</b>"
        ),
        "cmd_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick abilitato"
            " per queste comandi:</b>\n\n{}"
        ),
        "user_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick abilitato"
            " per questi utenti:</b>\n\n{}"
        ),
        "chat_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick abilitato"
            " per queste chat:</b>\n\n{}"
        ),
        "nothing": (
            "<emoji document_id=5427052514094619126>đ¤ˇââī¸</emoji> <b>Niente"
            " da mostrare...</b>"
        ),
        "privacy_leak": (
            "â ī¸ <b>Questo comando dÃ  accesso all'interfaccia web di Hikka. La sua"
            " esecuzione in chat pubbliche Ã¨ un pericolo per la sicurezza. E' meglio"
            " eseguirla in <a href='tg://openmessage?user_id={}'>Messaggi"
            " Preferiti</a>. Esegui</b> <code>{}proxypass force_insecure</code> <b>per"
            " disattivare questo avviso</b>"
        ),
        "privacy_leak_nowarn": (
            "â ī¸ <b>Questo comando dÃ  accesso all'interfaccia web di Hikka. La sua"
            " esecuzione in chat pubbliche Ã¨ un pericolo per la sicurezza. E' meglio"
            " eseguirla in <a href='tg://openmessage?user_id={}'>Messaggi"
            " Preferiti</a>.</b>"
        ),
        "opening_tunnel": (
            "đ <b>Sto aprendo il tunnel all'interfaccia web di Hikka...</b>"
        ),
        "tunnel_opened": (
            "đ <b>Tunnel aperto. Questo link sarÃ  attivo per un massimo di un ora</b>"
        ),
        "web_btn": "đ Interfaccia web",
        "btn_yes": "đ¸ Comunque apri",
        "btn_no": "đģ Chiudi",
        "lavhost_web": (
            "âī¸ <b>Collegandoti a questo link entrerai nell'interfaccia web di Hikka su"
            " lavHost</b>\n\n<i>đĄ Dovrai autenticarti utilizzando le credenziali"
            " impostate su lavHost</i>"
        ),
        "disable_debugger": "â Debugger abilitato",
        "enable_debugger": "đĢ Debugger disabilitato",
    }

    strings_de = {
        "watchers": (
            "<emoji document_id=5424885441100782420>đ</emoji>"
            " <b>Beobachter:</b>\n\n<b>{}</b>"
        ),
        "mod404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Beobachter {} nicht"
            "gefunden</b>"
        ),
        "disabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>Watcher {} ist jetzt"
            " <u>aus</u></b>"
        ),
        "enabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>Watcher {} ist jetzt"
            " <u>aktiviert</u></b>"
        ),
        "arg": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Bitte geben Sie einen"
            " Namen einHausmeister</b>"
        ),
        "user_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick-Status fÃŧr"
            " dieser Benutzer: {}</b>"
        ),
        "no_cmd": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Geben Sie einen Befehl"
            " anwas NoNick aktivieren/\\deaktivieren sollte</b>"
        ),
        "cmd_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick-Status fÃŧr"
            "</b> <code>{}</code><b>: {}</b>"
        ),
        "cmd404": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Befehl nicht"
            " gefunden</b>"
        ),
        "inline_settings": (
            "âī¸ <b>Hier kÃļnnen Sie Ihre Hikka-Einstellungen verwalten</b>"
        ),
        "confirm_update": (
            "đ§­ <b>BestÃ¤tige das Update. Der Userbot wird neu gestartet</b>"
        ),
        "confirm_restart": "đ <b>Neustart bestÃ¤tigen</b>",
        "suggest_fs": "â Speichermodule vorschlagen",
        "do_not_suggest_fs": "đĢ Speichermodule vorschlagen",
        "use_fs": "â Module immer speichern",
        "do_not_use_fs": "đĢ Module immer speichern",
        "btn_restart": "đ Neustart",
        "btn_update": "đ§­ Aktualisieren",
        "close_menu": "đ MenÃŧ schlieÃen",
        "custom_emojis": "â Benutzerdefinierte Emojis",
        "no_custom_emojis": "đĢ Benutzerdefinierte Emojis",
        "suggest_subscribe": "â Kanalabonnement vorschlagen",
        "do_not_suggest_subscribe": "đĢ Kanalabonnement vorschlagen",
        "private_not_allowed": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Dieser Befehl benÃļtigt"
            "im Chat ausfÃŧhren</b>"
        ),
        "_cls_doc": "Erweiterte Hikka-Einstellungen",
        "nonick_warning": (
            "Achtung! Sie haben NoNick mit dem Standard-PrÃ¤fix eingefÃŧgt!Sie sind"
            " mÃļglicherweise in Hikka-Chats stummgeschaltet. Ãndern Sie das PrÃ¤fix oder"
            " schalten Sie das globale NoNick aus!"
        ),
        "reply_required": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Auf Nachricht"
            " antwortenBenutzer soll NoNick aktivieren</b>"
        ),
        "deauth_confirm": (
            "â ī¸ <b>Diese Aktion wird Hikka vollstÃ¤ndig von diesem Konto entfernen! Er"
            " kann nichtAbbrechen</b>\n\n<i>- Alle Hikka-bezogenen Chats werden"
            " gelÃļscht\n- SitzungHikka wird zurÃŧckgesetzt\n- Hikkas Inline-Bot wird"
            " gelÃļscht</i>"
        ),
        "deauth_confirm_step2": (
            "â ī¸ <b>Sind Sie sicher, dass Sie Hikka deinstallieren mÃļchten?</b>"
        ),
        "deauth_yes": "Ich bin sicher",
        "deauth_no_1": "Ich bin mir nicht sicher",
        "deauth_no_2": "Nicht sicher",
        "deauth_no_3": "Nein",
        "deauth_cancel": "đĢ Abbrechen",
        "deauth_confirm_btn": "đĸ LÃļschen",
        "uninstall": "đĸ <b>Hikka wird deinstalliert...</b>",
        "uninstalled": (
            "đĸ <b>Hikka wurde entfernt. Die WeboberflÃ¤che ist noch aktiv, andere kÃļnnen"
            " hinzugefÃŧgt werdenKonten!</b>"
        ),
        "cmd_nn_liste": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick aktiviert fÃŧr"
            " diese Befehle:</b>\n\n{}"
        ),
        "user_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick aktiviert fÃŧr"
            " diese Benutzer:</b>\n\n{}"
        ),
        "chat_nn_liste": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick aktiviert fÃŧr"
            " diese Chats:</b>\n\n{}"
        ),
        "nothing": (
            "<emoji document_id=5427052514094619126>đ¤ˇââī¸</emoji> <b>Nichtszeigen...</b>"
        ),
        "privacy_leak": (
            "â ī¸ <b>Dieser Befehl ermÃļglicht den Zugriff auf die Hikka-WeboberflÃ¤che."
            " Seine AusfÃŧhrung inÃffentliche Chats sind ein Sicherheitsrisiko. Am"
            " besten durchfÃŧhren es in <a href='tg://openmessage?user_id={}'>Empfohlene"
            " Nachrichten</a>.FÃŧhren Sie</b> <code>{}proxypass force_insecure</code><b>"
            " zum Deaktivieren ausDies ist eine Warnung</b>"
        ),
        "privacy_leak_nowarn": (
            "â ī¸ <b>Dieser Befehl ermÃļglicht den Zugriff auf die Hikka-WeboberflÃ¤che."
            " Seine AusfÃŧhrung inÃffentliche Chats sind ein Sicherheitsrisiko. Am"
            " besten durchfÃŧhren sie in <a"
            " href='tg://openmessage?user_id={}'>Empfohlene Nachrichten</a>.</b>"
        ),
        "opening_tunnel": "đ <b>Ãffne einen Tunnel zur Hikka-WeboberflÃ¤che...</b>",
        "tunnel_opened": (
            "đ <b>Der Tunnel ist offen. Dieser Link ist nicht lÃ¤nger als eine Stunde"
            " aktiv</b>"
        ),
        "web_btn": "đ Webinterface",
        "btn_yes": "đ¸ Trotzdem geÃļffnet",
        "btn_no": "đģ SchlieÃen",
        "lavhost_web": (
            "âī¸ <b>Dieser Link fÃŧhrt Sie zur Hikka-WeboberflÃ¤che auf"
            " lavHost</b>\n\n<i>đĄ Sie mÃŧssen sich mit Ihren Zugangsdaten anmelden,"
            "beim Setzen von lavHost angegeben</i>"
        ),
        "disable_debugger": "â Debugger aktiviert",
        "enable_debugger": "đĢ Debugger deaktiviert",
    }

    strings_tr = {
        "watchers": (
            "<emoji document_id=5424885441100782420>đ</emoji>"
            " <b>Ä°zleyiciler:</b>\n\n<b>{}</b>"
        ),
        "mod404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Ä°zleyici {} deÄil"
            " bulundu</b>"
        ),
        "disabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>Ä°zleyici {} Åimdi"
            " <u>kapalÄą</u></b>"
        ),
        "enabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>Ä°zleyici {} Åimdi"
            " <u>etkin</u></b>"
        ),
        "arg": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>LÃŧtfen bir ad girin"
            "bekÃ§i</b>"
        ),
        "user_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick durumu iÃ§in"
            " bu kullanÄącÄą: {}</b>"
        ),
        "no_cmd": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Bir komut belirtin"
            "hangisi NoNick'i etkinleÅtirmeli/devre dÄąÅÄą bÄąrakmalÄądÄąr</b>"
        ),
        "cmd_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick durumu iÃ§in"
            "</b> <code>{}</code><b>: {}</b>"
        ),
        "cmd404": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Komut bulunamadÄą</b>"
        ),
        "inline_settings": "âī¸ <b>Buradan Hikka ayarlarÄąnÄązÄą yÃļnetebilirsiniz</b>",
        "confirm_update": (
            "đ§­ <b>GÃŧncellemeyi onaylayÄąn. KullanÄącÄą robotu yeniden baÅlatÄąlacak</b>"
        ),
        "confirm_restart": "đ <b>Yeniden baÅlatmayÄą onayla</b>",
        "suggest_fs": "â Kaydetme modÃŧlleri Ãļner",
        "do_not_suggest_fs": "đĢ ModÃŧllerin kaydedilmesini Ãļner",
        "use_fs": "â ModÃŧlleri her zaman kaydet",
        "do_not_use_fs": "đĢ ModÃŧlleri her zaman kaydet",
        "btn_restart": "đ Yeniden BaÅlat",
        "btn_update": "đ§­ GÃŧncelle",
        "close_menu": "đ MenÃŧyÃŧ kapat",
        "custom_emojis": "â Ãzel emojiler",
        "no_custom_emojis": "đĢ Ãzel Emojiler",
        "suggest_subscribe": "â Kanal aboneliÄi Ãļner",
        "do_not_suggest_subscribe": "đĢ Kanal aboneliÄi Ãļner",
        "private_not_allowed": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Bu komut gerekiyor"
            " sohbette yÃŧrÃŧt</b>"
        ),
        "_cls_doc": "GeliÅmiÅ Hikka AyarlarÄą",
        "nonick_warning": (
            "Dikkat! NoNick'i standart Ãļnekle eklediniz!"
            "Hikka sohbetlerinde sesiniz kapatÄąlmÄąÅ olabilir. Ãn eki deÄiÅtirin veya "
            "kÃŧresel NoNick'i kapatÄąn!"
        ),
        "reply_required": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>MesajÄą yanÄątla"
            "NoNick'i etkinleÅtirmek iÃ§in kullanÄącÄą</b>"
        ),
        "deauth_confirm": (
            "â ī¸ <b>Bu iÅlem Hikka'yÄą bu hesaptan tamamen kaldÄąracak! Yapamaz"
            "iptal</b>\n\n<i>- Hikka ile ilgili tÃŧm sohbetler silinecek\n- Oturum"
            " Hikka sÄąfÄąrlanacak\n- Hikka'nÄąn satÄąr iÃ§i botu silinecek</i>"
        ),
        "deauth_confirm_step2": (
            "â ī¸ <b>Hikka'yÄą kaldÄąrmak istediÄinizden emin misiniz?</b>"
        ),
        "deauth_yes": "Eminim",
        "deauth_no_1": "Emin deÄilim",
        "deauth_no_2": "Emin deÄilim",
        "deauth_no_3": "HayÄąr",
        "deauth_cancel": "đĢ Ä°ptal",
        "deauth_confirm_btn": "đĸ Sil",
        "uninstall": "đĸ <b>Hikka'yÄą KaldÄąrÄąlÄąyor...</b>",
        "uninstalled": (
            "đĸ <b>Hikka kaldÄąrÄąldÄą. Web arayÃŧzÃŧ hala aktif, baÅkalarÄą eklenebilir"
            "hesaplar!</b>"
        ),
        "cmd_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick iÃ§in"
            " etkinleÅtirildi bu komutlar:</b>\n\n{}"
        ),
        "user_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick iÃ§in"
            " etkinleÅtirildi bu kullanÄącÄąlar:</b>\n\n{}"
        ),
        "chat_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick iÃ§in"
            " etkinleÅtirildi bu sohbetler:</b>\n\n{}"
        ),
        "nothing": (
            "<emoji document_id=5427052514094619126>đ¤ˇââī¸</emoji> <b>HiÃ§bir Åey"
            "gÃļster...</b>"
        ),
        "privacy_leak": (
            "â ī¸ <b>Bu komut, Hikka web arayÃŧzÃŧne eriÅim saÄlar. YÃŧrÃŧtÃŧlmesiGenel"
            " sohbetler bir gÃŧvenlik riskidir. Tercihen gerÃ§ekleÅtirin <a"
            " href='tg://openmessage?user_id={}'>Ãne ÃÄąkan Mesajlar</a> iÃ§inde.Devre"
            " dÄąÅÄą bÄąrakmak iÃ§in</b> <code>{}proxypass force_insecure</code><b>"
            " Ã§alÄąÅtÄąrÄąnbu bir uyarÄądÄąr</b>"
        ),
        "privacy_leak_nowarn": (
            "â ī¸ <b>Bu komut, Hikka web arayÃŧzÃŧne eriÅim saÄlar. YÃŧrÃŧtÃŧlmesi"
            "Genel sohbetler bir gÃŧvenlik riskidir. Tercihen gerÃ§ekleÅtirin"
            " onu <a href='tg://openmessage?user_id={}'>Ãne ÃÄąkan Mesajlar</a>'da.</b>"
        ),
        "disable_debugger": "â Hata ayÄąklayÄącÄą etkin",
        "enable_debugger": "đĢ Hata AyÄąklayÄącÄą devre dÄąÅÄą",
    }

    strings_uz = {
        "watchers": (
            "<emoji document_id=5424885441100782420>đ</emoji>"
            " <b>Kuzatuvchilar:</b>\n\n<b>{}</b>"
        ),
        "mod404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Kuzuvchi {} emas"
            " topildi</b>"
        ),
        "disabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>Kuzatuvchi {} hozir"
            " <u>o'chirilgan</u></b>"
        ),
        "enabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>Kuzatuvchi {} hozir"
            " <u>yoqilgan</u></b>"
        ),
        "args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Iltimos, nom kiriting"
            "qorovul</b>"
        ),
        "user_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick holati uchun"
            " bu foydalanuvchi: {}</b>"
        ),
        "no_cmd": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Buyruqni belgilang"
            "bu NoNickni yoqish/o'chirish kerak</b>"
        ),
        "cmd_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick holati uchun"
            "</b> <code>{}</code><b>: {}</b>"
        ),
        "cmd404": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Buyruq topilmadi</b>"
        ),
        "inline_settings": (
            "âī¸ <b>Bu yerda siz Hikka sozlamalaringizni boshqarishingiz mumkin</b>"
        ),
        "confirm_update": (
            "đ§­ <b>Yangilanishni tasdiqlang. Userbot qayta ishga tushiriladi</b>"
        ),
        "confirm_restart": "đ <b>Qayta ishga tushirishni tasdiqlang</b>",
        "suggest_fs": "â Modullarni saqlashni taklif qilish",
        "do_not_suggest_fs": "đĢ Modullarni saqlashni taklif qilish",
        "use_fs": "â Modullarni doimo saqlash",
        "do_not_use_fs": "đĢ Har doim modullarni saqlang",
        "btn_restart": "đ Qayta ishga tushirish",
        "btn_update": "đ§­ Yangilash",
        "close_menu": "đ Menyuni yopish",
        "custom_emojis": "â Maxsus emojilar",
        "no_custom_emojis": "đĢ Maxsus kulgichlar",
        "suggest_subscribe": "â Kanalga obuna bo'lishni taklif qilish",
        "do_not_suggest_subscribe": "đĢ Kanalga obuna bo'lishni taklif qilish",
        "private_not_allowed": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Bu buyruq kerak"
            " chatda bajarish</b>"
        ),
        "_cls_doc": "Kengaytirilgan Hikka sozlamalari",
        "nonick_warning": (
            "Diqqat! NoNickni standart prefiks bilan kiritdingiz!Hikka chatlarida"
            " ovozingiz o'chirilgan bo'lishi mumkin. Prefiksni o'zgartiring yoki global"
            " NoNickni o'chiring!"
        ),
        "reply_required": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Xatga javob berish"
            "foydalanuvchi NoNick</b>ni yoqish uchun"
        ),
        "deauth_confirm": (
            "â ī¸ <b>Bu amal Hikkani ushbu hisobdan butunlay olib tashlaydi! U qila"
            " olmaydiBekor qilish</b>\n\n<i>- Hikka bilan bog'liq barcha chatlar"
            " o'chiriladi\n- Sessiya Hikka qayta tiklanadi\n- Hikkaning ichki boti"
            " o'chiriladi</i>"
        ),
        "deauth_confirm_step2": (
            "â ī¸ <b>Haqiqatan ham Hikkani o'chirib tashlamoqchimisiz?</b>"
        ),
        "deauth_yes": "Ishonchim komil",
        "deauth_no_1": "Imonim yo'q",
        "deauth_no_2": "Ishonasiz",
        "deauth_no_3": "Yo'q",
        "deauth_cancel": "đĢ Bekor qilish",
        "deauth_confirm_btn": "đĸ O'chirish",
        "uninstall": "đĸ <b>Hikka o'chirilmoqda...</b>",
        "uninstalled": (
            "đĸ <b>Hikka o'chirildi. Veb-interfeys hali ham faol, boshqalarni qo'shish"
            " mumkinhisoblar!</b>"
        ),
        "cmd_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick yoqilgan"
            " bu buyruqlar:</b>\n\n{}"
        ),
        "user_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick yoqilgan"
            " bu foydalanuvchilar:</b>\n\n{}"
        ),
        "chat_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick yoqilgan"
            " bu chatlar:</b>\n\n{}"
        ),
        "nothing": (
            "<emoji document_id=5427052514094619126>đ¤ˇââī¸</emoji> <b>Hech narsa"
            "ko'rsatish...</b>"
        ),
        "privacy_leak": (
            "â ī¸ <b>Ushbu buyruq Hikka veb-interfeysiga kirish imkonini beradi. Uning"
            " bajarilishiOmmaviy chatlar xavfsizlikka xavf tug'diradi. Afzal bajaring"
            " Bu <a href='tg://openmessage?user_id={}'>Taniqli xabarlar</a>da.O'chirish"
            " uchun</b> <code>{}proxypass force_insecure</code><b>ni ishga tushiring bu"
            " ogohlantirish</b>"
        ),
        "privacy_leak_nowarn": (
            "â ī¸ <b>Ushbu buyruq Hikka veb-interfeysiga kirish imkonini beradi. Uning"
            " bajarilishiOmmaviy chatlar xavfsizlikka xavf tug'diradi. Afzal bajaring u"
            " <a href='tg://openmessage?user_id={}'>Mazkur xabarlarda</a>.</b>"
        ),
        "opening_tunnel": "đ <b>Hikka veb-interfeysiga tunnel ochilmoqda...</b>",
        "tunnel_opened": (
            "đ <b>Tunnel ochiq. Bu havola bir soatdan ko'p bo'lmagan vaqt davomida faol"
            " bo'ladi</b>"
        ),
        "web_btn": "đ Veb interfeysi",
        "btn_yes": "đ¸ Baribir ochiq",
        "btn_no": "đģ Yopish",
        "lavhost_web": (
            "âī¸ <b>Ushbu havola sizni Hikka veb-interfeysiga olib boradi"
            " lavHost</b>\n\n<i>đĄ Hisob ma'lumotlaringizdan foydalanib tizimga"
            " kirishingiz kerak,lavHost</i>ni sozlashda ko'rsatilgan"
        ),
        "disable_debugger": "â Debugger yoqilgan",
        "enable_debugger": "đĢ Debugger o'chirilgan",
    }

    strings_es = {
        "watchers": (
            "<emoji document_id=5424885441100782420>đ</emoji>"
            " <b>Los espectadores:</b>\n\n<b>{}</b>"
        ),
        "mod404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>El espectador {} no"
            " encontrado</b>"
        ),
        "disabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>El espectador {} ahora"
            " <u>desactivado</u></b>"
        ),
        "enabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>El espectador {} ahora"
            " <u>activado</u></b>"
        ),
        "args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Indica el nombre"
            " del espectador</b>"
        ),
        "user_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>El estado de NoNick"
            " para este usuario: {}</b>"
        ),
        "no_cmd": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>Indica el comando,"
            " para el que se debe habilitar\\deshabilitar NoNick</b>"
        ),
        "cmd_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>El estado de NoNick"
            " para</b> <code>{}</code><b>: {}</b>"
        ),
        "cmd404": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>El comando no se"
            " encuentra</b>"
        ),
        "inline_settings": (
            "âī¸ <b>AquÃ­ puedes administrar las configuraciones de Hikka</b>"
        ),
        "confirm_update": (
            "đ§­ <b>Confirma la actualizaciÃŗn. El usuario del bot se reiniciarÃĄ</b>"
        ),
        "confirm_restart": "đ <b>Confirma el reinicio</b>",
        "suggest_fs": "â Sugerir guardar mÃŗdulos",
        "do_not_suggest_fs": "đĢ Sugerir guardar mÃŗdulos",
        "use_fs": "â Guardar mÃŗdulos siempre",
        "do_not_use_fs": "đĢ Guardar mÃŗdulos siempre",
        "btn_restart": "đ Reiniciar",
        "btn_update": "đ§­ ActualizaciÃŗn",
        "close_menu": "đ Cerrar menÃē",
        "custom_emojis": "â Emojis personalizados",
        "no_custom_emojis": "đĢ Emojis personalizados",
        "suggest_subscribe": "â Sugerir suscribirse al canal",
        "do_not_suggest_subscribe": "đĢ Sugerir suscribirse al canal",
        "private_not_allowed": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Debes ejecutar este"
            " comando en un chat</b>"
        ),
        "_cls_doc": "ConfiguraciÃŗn adicional de Hikka",
        "nonick_warning": (
            "ÂĄAtenciÃŗn! ÂĄHas activado NoNick con el prefijo predeterminado! "
            "Pueden silenciarte en los chats de Hikka. ÂĄCambie el prefijo o "
            "desactive NoNick globalmente!"
        ),
        "reply_required": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Responde al mensaje"
            " del usuario al que desea activar NoNick</b>"
        ),
        "deauth_confirm": (
            "â ī¸ <b>ÂĄEsta acciÃŗn eliminarÃĄ completamente Hikka de esta cuenta! No se"
            " puede deshacer</b>\n\n<i>- Todos los chats vinculados a Hikka serÃĄn"
            " eliminados\n- La sesiÃŗn de Hikka se restablecerÃĄ\n- El bot de lÃ­nea de"
            " Hikka se eliminarÃĄ</i>"
        ),
        "deauth_confirm_step2": (
            "â ī¸ <b>ÂŋEstÃĄs seguro de que quieres eliminar Hikka?</b>"
        ),
        "deauth_yes": "Estoy seguro",
        "deauth_no_1": "No estoy seguro",
        "deauth_no_2": "No es cierto",
        "deauth_no_3": "No",
        "deauth_cancel": "đĢ Cancelar",
        "deauth_confirm_btn": "đĸ Eliminar",
        "uninstall": "đĸ <b>Eliminando Hikka...</b>",
        "uninstalled": (
            "đĸ <b>Hikka eliminada. La interfaz web sigue activa, ÂĄpuedes agregar otras"
            " cuentas!</b>"
        ),
        "cmd_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick activado para"
            " estos comandos:</b>\n\n{}"
        ),
        "user_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick activado para"
            " estos usuarios:</b>\n\n{}"
        ),
        "chat_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick activado para"
            " estos chats:</b>\n\n{}"
        ),
        "nothing": (
            "<emoji document_id=5427052514094619126>đ¤ˇââī¸</emoji> <b>Nada"
            " para mostrar...</b>"
        ),
        "privacy_leak": (
            "â ī¸ <b>Este comando da acceso al interfaz web de Hikka. Su ejecuciÃŗn en"
            " chats pÃēblicos es una amenaza para la seguridad. Es preferible ejecutarlo"
            " en <a href='tg://openmessage?user_id={}'>Mensajes Favoritos</a>."
            " Ejecute</b> <code>{}proxypass force_insecure</code> <b>para desactivar"
            " este aviso</b>"
        ),
        "privacy_leak_nowarn": (
            "â ī¸ <b>Este comando da acceso al interfaz web de Hikka. Su ejecuciÃŗn en"
            " chats pÃēblicos es una amenaza para la seguridad. Es preferible ejecutarlo"
            " en <a href='tg://openmessage?user_id={}'>Mensajes Favoritos</a>.</b>"
        ),
        "opening_tunnel": "đ <b>Abriendo tÃēnel al interfaz web de Hikka...</b>",
        "tunnel_opened": (
            "đ <b>TÃēnel abierto. Esta enlace estarÃĄ activo no mÃĄs de una hora</b>"
        ),
        "web_btn": "đ Interfaz Web",
        "btn_yes": "đ¸ De todas formas, abrir",
        "btn_no": "đģ Cerrar",
        "lavhost_web": (
            "âī¸ <b>En este enlace entrarÃĄs al interfaz web de Hikka en"
            " lavHost</b>\n\n<i>đĄ NecesitarÃĄs autorizarte con los datos"
            " indicados en la configuraciÃŗn de lavHost</i>"
        ),
        "disable_debugger": "â Depurador activado",
        "enable_debugger": "đĢ Depurador desactivado",
    }

    strings_kk = {
        "watchers": (
            "<emoji document_id=5424885441100782420>đ</emoji>"
            " <b>ŌĐ°ŅĐ°ŅŅŅĐģĐ°Ņ:</b>\n\n<b>{}</b>"
        ),
        "mod404": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ŌĐ°ŅĐ°ŅŅŅ {} ĐļĐžŌ"
            " ŅĐ°ĐąŅĐģĐ´Ņ</b>"
        ),
        "disabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>ŌĐ°ĐˇŅŅ {} ĐąĐ°ŌŅĐģĐ°ŅŅŅŅŅ"
            " <u>ĶŠŅŅŅŅ</u></b>"
        ),
        "enabled": (
            "<emoji document_id=5424885441100782420>đ</emoji> <b>ŌĐ°ĐˇŅŅ {} ĐąĐ°ŌŅĐģĐ°ŅŅŅŅŅ"
            " <u>ŌĐžŅŅĐģŌĐ°ĐŊ</u></b>"
        ),
        "args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐŅŅĐŊ ĐĩĐŊĐŗŅĐˇŅŌŖŅĐˇ"
            "ŌĐ°ĐŧŌĐžŅŅŅ</b>"
        ),
        "user_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick ĐēŌ¯ĐšŅ Ō¯ŅŅĐŊ"
            " ĐąŌąĐģ ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅ: {}</b>"
        ),
        "no_cmd": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>ĐĶŅĐŧĐĩĐŊĐ´Ņ ĐēĶŠŅŅĐĩŅŅŌŖŅĐˇ"
            "ĐžĐģ NoNick</b>ŌĐžŅŅ/ĶŠŅŅŅŅ ĐēĐĩŅĐĩĐē"
        ),
        "cmd_nn": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick ĐēŌ¯ĐšŅ Ō¯ŅŅĐŊ"
            "</b> <code>{}</code><b>: {}</b>"
        ),
        "cmd404": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>ĐĶŅĐŧĐĩĐŊ ŅĐ°ĐąŅĐģĐŧĐ°Đ´Ņ</b>"
        ),
        "inline_settings": "âī¸ <b>ĐŅŅĐŊĐ´Đ° Hikka ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐģĐĩŅŅĐŊ ĐąĐ°ŅŌĐ°ŅŅŌĐ° ĐąĐžĐģĐ°Đ´Ņ</b>",
        "confirm_update": "đ§­ <b>ĐĐ°ŌŖĐ°ŅŅŅĐ´Ņ ŅĐ°ŅŅĐ°ŌŖŅĐˇ. Userbot ŌĐ°ĐšŅĐ° ŅŅĐēĐĩ ŌĐžŅŅĐģĐ°Đ´Ņ</b>",
        "confirm_restart": "đ <b>ŌĐ°ĐšŅĐ° ŌĐžŅŅĐ´Ņ ŅĐ°ŅŅĐ°Ņ</b>",
        "suggest_fs": "â ĐĄĐ°ŌŅĐ°Ņ ĐŧĐžĐ´ŅĐģŅĐ´ĐĩŅŅĐŊ ŌąŅŅĐŊŅ",
        "do_not_suggest_fs": "đĢ ĐĄĐ°ŌŅĐ°Ņ ĐŧĐžĐ´ŅĐģŅĐ´ĐĩŅŅĐŊ ŌąŅŅĐŊŅ",
        "use_fs": "â ĐĐžĐ´ŅĐģŅĐ´ĐĩŅĐ´Ņ ĶŅŌĐ°ŅĐ°ĐŊ ŅĐ°ŌŅĐ°Ņ",
        "do_not_use_fs": "đĢ ĶŅŌĐ°ŅĐ°ĐŊ ĐŧĐžĐ´ŅĐģŅĐ´ĐĩŅĐ´Ņ ŅĐ°ŌŅĐ°",
        "btn_restart": "đ ŌĐ°ĐšŅĐ° ŅŅĐēĐĩ ŌĐžŅŅ",
        "btn_update": "đ§­ ĐĐ°ŌŖĐ°ŅŅŅ",
        "close_menu": "đ ĐĶĐˇŅŅĐ´Ņ ĐļĐ°ĐąŅ",
        "custom_emojis": "â ĐŅĐŊĐ°ĐšŅ ŅĐŧĐžĐ´ĐˇĐ¸ĐģĐĩŅ",
        "no_custom_emojis": "đĢ ĐŅĐŊĐ°ŅĐģŅ ŅĐŧĐžĐ´ĐˇĐ¸ĐģĐĩŅ",
        "suggest_subscribe": "â ĐŅĐŊĐ°ŌĐ° ĐļĐ°ĐˇŅĐģŅĐ´Ņ ŌąŅŅĐŊŅ",
        "do_not_suggest_subscribe": "đĢ ĐŅĐŊĐ°ŌĐ° ĐļĐ°ĐˇŅĐģŅĐ´Ņ ŌąŅŅĐŊŅ",
        "private_not_allowed": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐŌąĐģ ĐŋĶŅĐŧĐĩĐŊ ŌĐ°ĐļĐĩŅ"
            " ŅĐ°ŅŅĐ° ĐžŅŅĐŊĐ´Đ°Ņ</b>"
        ),
        "_cls_doc": "ŌĐžŅŅĐŧŅĐ° Hikka ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐģĐĩŅŅ",
        "nonick_warning": (
            "ĐĐ°ĐˇĐ°Ņ Đ°ŅĐ´Đ°ŅŅŌŖŅĐˇ! ĐĄŅĐˇ ŅŅĐ°ĐŊĐ´Đ°ŅŅŅŅ ĐŋŅĐĩŅĐ¸ĐēŅĐŋĐĩĐŊ NoNick ŌĐžŅŅŅŌŖŅĐˇ!"
            "Hikka ŅĐ°ŅŅĐ°ŅŅĐŊĐ´Đ°ŌŅ Đ´ŅĐąŅŅŅŌŖŅĐˇ ĶŠŅŅŅŅĐģŅŅ ĐŧŌ¯ĐŧĐēŅĐŊ. ĐŅĐĩŅĐ¸ĐēŅŅŅ ĶŠĐˇĐŗĐĩŅŅŅŌŖŅĐˇ ĐŊĐĩĐŧĐĩŅĐĩ "
            "ĐļĐ°ŌģĐ°ĐŊĐ´ŅŌ NoNick ĶŠŅŅŅŅŌŖŅĐˇ!"
        ),
        "reply_required": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĨĐ°ĐąĐ°ŅŌĐ° ĐļĐ°ŅĐ°Đŋ ĐąĐĩŅŅ"
            "NoNick</b>ŌĐžŅĐ°ŅŅĐŊ ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅ"
        ),
        "deauth_confirm": (
            "â ī¸ <b>ĐŌąĐģ ĶŅĐĩĐēĐĩŅ ĐĨĐ¸ĐēĐēĐ°ĐŊŅ ĐžŅŅ ĐĩŅĐĩĐŋŅŅĐē ĐļĐ°ĐˇĐąĐ°Đ´Đ°ĐŊ ŅĐžĐģŅŌŅĐŧĐĩĐŊ ĐļĐžŅĐ´Ņ! ĐĐģ ĐŧŌ¯ĐŧĐēŅĐŊ"
            " ĐĩĐŧĐĩŅĐąĐ°Ņ ŅĐ°ŅŅŅ</b>\n\n<i>- ĐĨĐ¸ĐēĐēĐ°ŌĐ° ŌĐ°ŅŅŅŅŅ ĐąĐ°ŅĐģŅŌ ŅĐ°ŅŅĐ°Ņ ĐļĐžĐšŅĐģĐ°Đ´Ņ\n- ĐĄĐĩĐ°ĐŊŅ"
            " ĐĨĐ¸ĐēĐēĐ° ŌĐ°ĐģĐŋŅĐŊĐ° ĐēĐĩĐģŅŅŅŅĐģĐĩĐ´Ņ\n- ĐĨĐ¸ĐēĐēĐ°ĐŊŅŌŖ ĐēŅŅŅŅŅŅŅŅĐģĐŗĐĩĐŊ ĐąĐžŅŅ ĐļĐžĐšŅĐģĐ°Đ´Ņ</i>"
        ),
        "deauth_confirm_step2": "â ī¸ <b>ĐĄŅĐˇ ŅŅĐŊŅĐŧĐĩĐŊ ĐĨĐ¸ĐēĐēĐ°ĐŊŅ ĐļĐžĐšŌŅŌŖŅĐˇ ĐēĐĩĐģĐĩ ĐŧĐĩ?</b>",
        "deauth_yes": "ĐĐĩĐŊ ŅĐĩĐŊŅĐŧĐ´ŅĐŧŅĐŊ",
        "deauth_no_1": "ĐĐĩĐŊ ŅĐĩĐŊŅĐŧĐ´Ņ ĐĩĐŧĐĩŅĐŋŅĐŊ",
        "deauth_no_2": "ĐĐ°ŌŅŅ ĐĩĐŧĐĩŅ",
        "deauth_no_3": "ĐĐžŌ",
        "deauth_cancel": "đĢ ĐĐžĐģĐ´ŅŅĐŧĐ°Ņ",
        "deauth_confirm_btn": "đĸ ĐĐžŅ",
        "uninstall": "đĸ <b>Hikka ĐļĐžĐšŅĐģŅĐ´Đ°...</b>",
        "uninstalled": (
            "đĸ <b>Hikka ĐļĐžĐšŅĐģĐ´Ņ. ĐĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅ ĶĐģŅ ĐąĐĩĐģŅĐĩĐŊĐ´Ņ, ĐąĐ°ŅŌĐ°ĐģĐ°ŅŅĐŊ ŌĐžŅŅŌĐ° ĐąĐžĐģĐ°Đ´Ņ"
            "ŅĐžŅŅĐ°Ņ!</b>"
        ),
        "cmd_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick Ō¯ŅŅĐŊ ŌĐžŅŅĐģŌĐ°ĐŊ"
            " ĐŧŅĐŊĐ° ĐŋĶŅĐŧĐĩĐŊĐ´ĐĩŅ:</b>\n\n{}"
        ),
        "user_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick Ō¯ŅŅĐŊ ŌĐžŅŅĐģŌĐ°ĐŊ"
            " ĐŧŅĐŊĐ° ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅĐģĐ°Ņ:</b>\n\n{}"
        ),
        "chat_nn_list": (
            "<emoji document_id=5469791106591890404>đĒ</emoji> <b>NoNick Ō¯ŅŅĐŊ ŌĐžŅŅĐģŌĐ°ĐŊ"
            " ĐŧŅĐŊĐ° ŅĐ°ŅŅĐ°Ņ:</b>\n\n{}"
        ),
        "nothing": (
            "<emoji document_id=5427052514094619126>đ¤ˇââī¸</emoji> <b>ĐŅŅĐĩŌŖĐĩ"
            "ĐēĶŠŅŅĐĩŅŅ...</b>"
        ),
        "privacy_leak": (
            "â ī¸ <b>ĐŌąĐģ ĐŋĶŅĐŧĐĩĐŊ Hikka Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅŅĐŊĐĩ ŌĐžĐģ ĐļĐĩŅĐēŅĐˇŅĐŗĐĩ ĐŧŌ¯ĐŧĐēŅĐŊĐ´ŅĐē ĐąĐĩŅĐĩĐ´Ņ."
            " ĐĐŊŅŌŖ ĐžŅŅĐŊĐ´Đ°ĐģŅŅĐŊĐ´Đ°ĐŅŅŌ ŅĐ°ŅŅĐ°Ņ - ŌĐ°ŅŅĐŋŅŅĐˇĐ´ŅĐēĐēĐĩ ŌĐ°ŅŅĐŋ ŅĶŠĐŊĐ´ŅŅĐĩĐ´Ņ. ĐĐ°ŌŅŅŅĐ°Ō"
            " ĐžŅŅĐŊĐ´Đ°ŌŖŅĐˇ ĐžĐģ <a href='tg://openmessage?user_id={}'>ĐĸĐ°ŌŖĐ´Đ°ŅĐģŅ ŅĐ°ĐąĐ°ŅĐģĐ°Ņ</a>"
            " ŅŅŅĐŊĐ´Đĩ.Ķ¨ŅŅŅŅ Ō¯ŅŅĐŊ</b> <code>{}proxypass force_insecure</code> <b>ŅŅĐēĐĩ"
            " ŌĐžŅŅŌŖŅĐˇ ĐąŌąĐģ ĐĩŅĐēĐĩŅŅŅ</b>"
        ),
        "privacy_leak_nowarn": (
            "â ī¸ <b>ĐŌąĐģ ĐŋĶŅĐŧĐĩĐŊ Hikka Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅŅĐŊĐĩ ŌĐžĐģ ĐļĐĩŅĐēŅĐˇŅĐŗĐĩ ĐŧŌ¯ĐŧĐēŅĐŊĐ´ŅĐē ĐąĐĩŅĐĩĐ´Ņ."
            " ĐĐŊŅŌŖ ĐžŅŅĐŊĐ´Đ°ĐģŅŅĐŊĐ´Đ°ĐŅŅŌ ŅĐ°ŅŅĐ°Ņ - ŌĐ°ŅŅĐŋŅŅĐˇĐ´ŅĐēĐēĐĩ ŌĐ°ŅŅĐŋ ŅĶŠĐŊĐ´ŅŅĐĩĐ´Ņ. ĐĐ°ŌŅŅŅĐ°Ō"
            " ĐžŅŅĐŊĐ´Đ°ŌŖŅĐˇ ĐžĐģ <a href='tg://openmessage?user_id={}'>ĐĸĐ°ŌŖĐ´Đ°ŅĐģŅ"
            " ŅĐ°ĐąĐ°ŅĐģĐ°ŅĐ´Đ°</a>.</b>"
        ),
        "opening_tunnel": "đ <b>ĐŅŅayu ŅŅĐŊĐŊĐĩĐģŅ ĐĨĐ¸ĐēĐēĐ° Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅŅĐŊĐĩ...</b>",
        "tunnel_opened": (
            "đ <b>ĐĸŅĐŊĐŊĐĩĐģŅ Đ°ŅŅŌ. ĐŌąĐģ ŅŅĐģŅĐĩĐŧĐĩ ĐąŅŅ ŅĐ°ŌĐ°ŅŅĐ°ĐŊ Đ°ŅŅŅŌ ĐĩĐŧĐĩŅ ĐąĐĩĐģŅĐĩĐŊĐ´Ņ ĐąĐžĐģĐ°Đ´Ņ</b>"
        ),
        "web_btn": "đ ĐĐĩĐą Đ¸ĐŊŅĐĩŅŅĐĩĐšŅŅ",
        "btn_yes": "đ¸ ĶĐšŅĐĩŅŅŅ Đ°ŅŅŌŖŅĐˇ",
        "btn_no": "đģ ĐĐ°ĐąŅ",
        "lavhost_web": (
            "âī¸ <b>ĐŌąĐģ ŅŅĐģŅĐĩĐŧĐĩ ŅŅĐˇĐ´Ņ Hikka Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅŅĐŊĐĩ Đ°ĐŋĐ°ŅĐ°Đ´Ņ"
            " lavHost</b>\n\n<i>đĄ ĐĄŅĐˇĐŗĐĩ ŅŅŅĐēĐĩĐģĐŗŅ Đ´ĐĩŅĐĩĐēŅĐĩŅŅĐŊ ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅĐŋ ĐēŅŅŅ ŌĐ°ĐļĐĩŅ,"
            "lavHost</i> ĐžŅĐŊĐ°ŅŅ ĐēĐĩĐˇŅĐŊĐ´Đĩ ĐēĶŠŅŅĐĩŅŅĐģĐŗĐĩĐŊ"
        ),
        "disable_debugger": "â ĐŅĐģĐ°Đ´ŅĐ¸Đē ŌĐžŅŅĐģŌĐ°ĐŊ",
        "enable_debugger": "đĢ ĐĸŌ¯ĐˇĐĩŅŅ ŌŌąŅĐ°ĐģŅ ĶŠŅŅŅŅĐģĐŗĐĩĐŊ",
    }

    def get_watchers(self) -> tuple:
        return [
            str(watcher.__self__.__class__.strings["name"])
            for watcher in self.allmodules.watchers
            if watcher.__self__.__class__.strings is not None
        ], self._db.get(main.__name__, "disabled_watchers", {})

    async def _uninstall(self, call: InlineCall):
        await call.edit(self.strings("uninstall"))

        async with self._client.conversation("@BotFather") as conv:
            for msg in [
                "/deletebot",
                f"@{self.inline.bot_username}",
                "Yes, I am totally sure.",
            ]:
                await fw_protect()
                m = await conv.send_message(msg)
                r = await conv.get_response()

                logger.debug(">> %s", m.raw_text)
                logger.debug("<< %s", r.raw_text)

                await fw_protect()

                await m.delete()
                await r.delete()

        async for dialog in self._client.iter_dialogs(
            None,
            ignore_migrated=True,
        ):
            if (
                dialog.name
                in {
                    "hikka-logs",
                    "hikka-onload",
                    "hikka-assets",
                    "hikka-backups",
                    "hikka-acc-switcher",
                    "silent-tags",
                }
                and dialog.is_channel
                and (
                    dialog.entity.participants_count == 1
                    or dialog.entity.participants_count == 2
                    and dialog.name in {"hikka-logs", "silent-tags"}
                )
                or (
                    self._client.loader.inline.init_complete
                    and dialog.entity.id == self._client.loader.inline.bot_id
                )
            ):
                await fw_protect()
                await self._client.delete_dialog(dialog.entity)

        await fw_protect()

        folders = await self._client(GetDialogFiltersRequest())

        if any(folder.title == "hikka" for folder in folders):
            folder_id = max(
                folders,
                key=lambda x: x.id,
            ).id
            await fw_protect()
            await self._client(UpdateDialogFilterRequest(id=folder_id))

        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.CRITICAL)

        await fw_protect()

        await self._client.log_out()

        restart()

    async def _uninstall_confirm_step_2(self, call: InlineCall):
        await call.edit(
            self.strings("deauth_confirm_step2"),
            utils.chunks(
                list(
                    sorted(
                        [
                            {
                                "text": self.strings("deauth_yes"),
                                "callback": self._uninstall,
                            },
                            *[
                                {
                                    "text": self.strings(f"deauth_no_{i}"),
                                    "action": "close",
                                }
                                for i in range(1, 4)
                            ],
                        ],
                        key=lambda _: random.random(),
                    )
                ),
                2,
            )
            + [
                [
                    {
                        "text": self.strings("deauth_cancel"),
                        "action": "close",
                    }
                ]
            ],
        )

    @loader.owner
    @loader.command(
        ru_doc="ĐŖĐ´Đ°ĐģĐ¸ŅŅ Hikka",
        fr_doc="DÃŠsinstaller Hikka",
        it_doc="Disinstalla Hikka",
        de_doc="Hikka deinstallieren",
        tr_doc="Hikka'yÄą kaldÄąr",
        uz_doc="Hikka'ni o'chirish",
        es_doc="Desinstalar Hikka",
        kk_doc="Hikka'ĐŊŅ ĐļĐžŅ",
    )
    async def uninstall_hikka(self, message: Message):
        """Uninstall Hikka"""
        await self.inline.form(
            self.strings("deauth_confirm"),
            message,
            [
                {
                    "text": self.strings("deauth_confirm_btn"),
                    "callback": self._uninstall_confirm_step_2,
                },
                {"text": self.strings("deauth_cancel"), "action": "close"},
            ],
        )

    @loader.command(
        ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ Đ°ĐēŅĐ¸Đ˛ĐŊŅĐĩ ŅĐŧĐžŅŅĐ¸ŅĐĩĐģĐ¸",
        fr_doc="Afficher les observateurs actifs",
        it_doc="Mostra i guardatori attivi",
        de_doc="Aktive Beobachter anzeigen",
        tr_doc="Etkin gÃļzlemcileri gÃļster",
        uz_doc="Faol ko'rib chiqqanlarni ko'rsatish",
        es_doc="Mostrar observadores activos",
        kk_doc="ĐĐĩĐģŅĐĩĐŊĐ´Ņ ĐēĶŠĐˇĐ´ĐĩŅĐ´Ņ ĐēĶŠŅŅĐĩŅŅ",
    )
    async def watchers(self, message: Message):
        """List current watchers"""
        watchers, disabled_watchers = self.get_watchers()
        watchers = [
            f"âģī¸ {watcher}"
            for watcher in watchers
            if watcher not in list(disabled_watchers.keys())
        ]
        watchers += [f"đĸ {k} {v}" for k, v in disabled_watchers.items()]
        await utils.answer(
            message, self.strings("watchers").format("\n".join(watchers))
        )

    @loader.command(
        ru_doc="<module> - ĐĐēĐģŅŅĐ¸ŅŅ/Đ˛ŅĐēĐģŅŅĐ¸ŅŅ ŅĐŧĐžŅŅĐ¸ŅĐĩĐģŅ Đ˛ ŅĐĩĐēŅŅĐĩĐŧ ŅĐ°ŅĐĩ",
        fr_doc="<module> - Activer / dÃŠsactiver l'observateur dans ce chat",
        it_doc="<module> - Abilita/disabilita il guardatore nel gruppo corrente",
        de_doc="<module> - Aktiviere/Deaktiviere Beobachter in diesem Chat",
        tr_doc="<module> - Bu sohbetteki gÃļzlemciyi etkinleÅtirin/devre dÄąÅÄą bÄąrakÄąn",
        uz_doc="<module> - Joriy suhbatda ko'rib chiqqanlarni yoqish/yopish",
        es_doc="<module> - Habilitar / deshabilitar observador en este chat",
        kk_doc="<module> - ĐŌąĐģ ŅĶŠĐšĐģĐĩŅŅĐ´Đĩ ĐēĶŠĐˇĐ´ĐĩŅĐ´Ņ ŌĐžŅŅ/ĶŠŅŅŅŅ",
    )
    async def watcherbl(self, message: Message):
        """<module> - Toggle watcher in current chat"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("args"))
            return

        watchers, disabled_watchers = self.get_watchers()

        if args.lower() not in map(lambda x: x.lower(), watchers):
            await utils.answer(message, self.strings("mod404").format(args))
            return

        args = next((x.lower() == args.lower() for x in watchers), False)

        current_bl = [
            v for k, v in disabled_watchers.items() if k.lower() == args.lower()
        ]
        current_bl = current_bl[0] if current_bl else []

        chat = utils.get_chat_id(message)
        if chat not in current_bl:
            if args in disabled_watchers:
                for k in disabled_watchers:
                    if k.lower() == args.lower():
                        disabled_watchers[k].append(chat)
                        break
            else:
                disabled_watchers[args] = [chat]

            await utils.answer(
                message,
                self.strings("disabled").format(args) + " <b>in current chat</b>",
            )
        else:
            for k in disabled_watchers.copy():
                if k.lower() == args.lower():
                    disabled_watchers[k].remove(chat)
                    if not disabled_watchers[k]:
                        del disabled_watchers[k]
                    break

            await utils.answer(
                message,
                self.strings("enabled").format(args) + " <b>in current chat</b>",
            )

        self._db.set(main.__name__, "disabled_watchers", disabled_watchers)

    @loader.command(
        ru_doc=(
            "<ĐŧĐžĐ´ŅĐģŅ> - ĐŖĐŋŅĐ°Đ˛ĐģĐĩĐŊĐ¸Đĩ ĐŗĐģĐžĐąĐ°ĐģŅĐŊŅĐŧĐ¸ ĐŋŅĐ°Đ˛Đ¸ĐģĐ°ĐŧĐ¸ ŅĐŧĐžŅŅĐ¸ŅĐĩĐģŅ\n"
            "ĐŅĐŗŅĐŧĐĩĐŊŅŅ:\n"
            "[-c - ŅĐžĐģŅĐēĐž Đ˛ ŅĐ°ŅĐ°Ņ]\n"
            "[-p - ŅĐžĐģŅĐēĐž Đ˛ ĐģŅ]\n"
            "[-o - ŅĐžĐģŅĐēĐž Đ¸ŅŅĐžĐ´ŅŅĐ¸Đĩ]\n"
            "[-i - ŅĐžĐģŅĐēĐž Đ˛ŅĐžĐ´ŅŅĐ¸Đĩ]"
        ),
        fr_doc=(
            "<module> - GÃŠrer les rÃ¨gles globales de l'observateur\n"
            "Arguments:\n"
            "[-c - uniquement dans les chats]\n"
            "[-p - uniquement dans les messages privÃŠs]\n"
            "[-o - uniquement sortant]\n"
            "[-i - uniquement entrant]"
        ),
        it_doc=(
            "<module> - Gestisci le regole globali del guardatore\n"
            "Argomenti:\n"
            "[-c - solo nei gruppi]\n"
            "[-p - solo nei messaggi privati]\n"
            "[-o - solo in uscita]\n"
            "[-i - solo in entrata]"
        ),
        de_doc=(
            "<module> - Verwalte globale Beobachterregeln\n"
            "Argumente:\n"
            "[-c - Nur in Chats]\n"
            "[-p - Nur in privaten Chats]\n"
            "[-o - Nur ausgehende Nachrichten]\n"
            "[-i - Nur eingehende Nachrichten]"
        ),
        tr_doc=(
            "<module> - Genel gÃļzlemci kurallarÄąnÄą yÃļnetin\n"
            "ArgÃŧmanlar:\n"
            "[-c - YalnÄązca sohbetlerde]\n"
            "[-p - YalnÄązca Ãļzel sohbetlerde]\n"
            "[-o - YalnÄązca giden mesajlar]\n"
            "[-i - YalnÄązca gelen mesajlar]"
        ),
        uz_doc=(
            "<module> - Umumiy ko'rib chiqqan qoidalarni boshqarish\n"
            "Argumentlar:\n"
            "[-c - Faqat suhbatlarda]\n"
            "[-p - Faqat shaxsiy suhbatlarda]\n"
            "[-o - Faqat chiqarilgan xabarlar]\n"
            "[-i - Faqat kelgan xabarlar]"
        ),
        es_doc=(
            "<module> - Administre las reglas del observador global\n"
            "Argumentos:\n"
            "[-c - Solo en chats]\n"
            "[-p - Solo en chats privados]\n"
            "[-o - Solo mensajes salientes]\n"
            "[-i - Solo mensajes entrantes]"
        ),
        kk_doc=(
            "<module> - ŌĐžŌĐ°ĐŧĐ´ŅŌ ĐēĶŠĐˇĐ´ĐĩŅĐ´Ņ ĐąĐ°ŅŌĐ°ŅŅ\n"
            "ĐŅĐŗŅĐŧĐĩĐŊŅŅĐĩŅ:\n"
            "[-c - ĐĸĐĩĐē ŅĶŠĐšĐģĐĩŅŅĐ´Đĩ]\n"
            "[-p - ĐĸĐĩĐē ŅĐ°ŅŅĐ¸ ŅĶŠĐšĐģĐĩŅŅĐ´Đĩ]\n"
            "[-o - ĐĸĐĩĐē ŅŅŌĐ°ŅŅĐģŌĐ°ĐŊ ŅĐ°ĐąĐ°ŅĐģĐ°Ņ]\n"
            "[-i - ĐĸĐĩĐē ĐēĐĩĐģĐŗĐĩĐŊ ŅĐ°ĐąĐ°ŅĐģĐ°Ņ]"
        ),
    )
    async def watchercmd(self, message: Message):
        """<module> - Toggle global watcher rules
        Args:
        [-c - only in chats]
        [-p - only in pm]
        [-o - only out]
        [-i - only incoming]"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings("args"))

        chats, pm, out, incoming = False, False, False, False

        if "-c" in args:
            args = args.replace("-c", "").replace("  ", " ").strip()
            chats = True

        if "-p" in args:
            args = args.replace("-p", "").replace("  ", " ").strip()
            pm = True

        if "-o" in args:
            args = args.replace("-o", "").replace("  ", " ").strip()
            out = True

        if "-i" in args:
            args = args.replace("-i", "").replace("  ", " ").strip()
            incoming = True

        if chats and pm:
            pm = False
        if out and incoming:
            incoming = False

        watchers, disabled_watchers = self.get_watchers()

        if args.lower() not in [watcher.lower() for watcher in watchers]:
            return await utils.answer(message, self.strings("mod404").format(args))

        args = [watcher for watcher in watchers if watcher.lower() == args.lower()][0]

        if chats or pm or out or incoming:
            disabled_watchers[args] = [
                *(["only_chats"] if chats else []),
                *(["only_pm"] if pm else []),
                *(["out"] if out else []),
                *(["in"] if incoming else []),
            ]
            self._db.set(main.__name__, "disabled_watchers", disabled_watchers)
            await utils.answer(
                message,
                self.strings("enabled").format(args)
                + f" (<code>{disabled_watchers[args]}</code>)",
            )
            return

        if args in disabled_watchers and "*" in disabled_watchers[args]:
            await utils.answer(message, self.strings("enabled").format(args))
            del disabled_watchers[args]
            self._db.set(main.__name__, "disabled_watchers", disabled_watchers)
            return

        disabled_watchers[args] = ["*"]
        self._db.set(main.__name__, "disabled_watchers", disabled_watchers)
        await utils.answer(message, self.strings("disabled").format(args))

    @loader.command(
        ru_doc="ĐĐēĐģŅŅĐ¸ŅŅ NoNick Đ´ĐģŅ ĐžĐŋŅĐĩĐ´ĐĩĐģĐĩĐŊĐŊĐžĐŗĐž ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ",
        fr_doc="Activer NoNick pour un utilisateur spÃŠcifique",
        it_doc="Abilita NoNick per un utente specifico",
        de_doc="Aktiviere NoNick fÃŧr einen bestimmten Benutzer",
        tr_doc="Belirli bir kullanÄącÄą iÃ§in NoNick'i etkinleÅtirin",
        uz_doc="Belgilangan foydalanuvchi uchun NoNickni yoqish",
        es_doc="Habilitar NoNick para un usuario especÃ­fico",
        kk_doc="ĐĐĩĐģĐŗŅĐģĐĩĐŊĐŗĐĩĐŊ ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅ Ō¯ŅŅĐŊ NoNick ŅŌ¯ŅĐģĐĩĐŊĐ´ŅŅŅĐģĐŗĐĩĐŊ",
    )
    async def nonickuser(self, message: Message):
        """Allow no nickname for certain user"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("reply_required"))
            return

        u = reply.sender_id
        if not isinstance(u, int):
            u = u.user_id

        nn = self._db.get(main.__name__, "nonickusers", [])
        if u not in nn:
            nn += [u]
            nn = list(set(nn))  # skipcq: PTC-W0018
            await utils.answer(message, self.strings("user_nn").format("on"))
        else:
            nn = list(set(nn) - {u})
            await utils.answer(message, self.strings("user_nn").format("off"))

        self._db.set(main.__name__, "nonickusers", nn)

    @loader.command(
        ru_doc="ĐĐēĐģŅŅĐ¸ŅŅ NoNick Đ´ĐģŅ ĐžĐŋŅĐĩĐ´ĐĩĐģĐĩĐŊĐŊĐžĐŗĐž ŅĐ°ŅĐ°",
        fr_doc="Activer NoNick pour un chat spÃŠcifique",
        it_doc="Abilita NoNick per una chat specifica",
        de_doc="Aktiviere NoNick fÃŧr einen bestimmten Chat",
        tr_doc="Belirli bir sohbet iÃ§in NoNick'i etkinleÅtirin",
        uz_doc="Belgilangan suhbat uchun NoNickni yoqish",
        es_doc="Habilitar NoNick para un chat especÃ­fico",
        kk_doc="ĐĐĩĐģĐŗŅĐģĐĩĐŊĐŗĐĩĐŊ ŅĶŠĐšĐģĐĩŅŅ Ō¯ŅŅĐŊ NoNick ŅŌ¯ŅĐģĐĩĐŊĐ´ŅŅŅĐģĐŗĐĩĐŊ",
    )
    async def nonickchat(self, message: Message):
        """Allow no nickname in certain chat"""
        if message.is_private:
            await utils.answer(message, self.strings("private_not_allowed"))
            return

        chat = utils.get_chat_id(message)

        nn = self._db.get(main.__name__, "nonickchats", [])
        if chat not in nn:
            nn += [chat]
            nn = list(set(nn))  # skipcq: PTC-W0018
            await utils.answer(
                message,
                self.strings("cmd_nn").format(
                    utils.escape_html((await message.get_chat()).title),
                    "on",
                ),
            )
        else:
            nn = list(set(nn) - {chat})
            await utils.answer(
                message,
                self.strings("cmd_nn").format(
                    utils.escape_html((await message.get_chat()).title),
                    "off",
                ),
            )

        self._db.set(main.__name__, "nonickchats", nn)

    @loader.command(
        ru_doc="ĐĐēĐģŅŅĐ¸ŅŅ NoNick Đ´ĐģŅ ĐžĐŋŅĐĩĐ´ĐĩĐģĐĩĐŊĐŊĐžĐš ĐēĐžĐŧĐ°ĐŊĐ´Ņ",
        fr_doc="Activer NoNick pour une commande spÃŠcifique",
        it_doc="Abilita NoNick per un comando specifico",
        de_doc="Aktiviere NoNick fÃŧr einen bestimmten Befehl",
        tr_doc="Belirli bir komut iÃ§in NoNick'i etkinleÅtirin",
        uz_doc="Belgilangan buyruq uchun NoNickni yoqish",
        es_doc="Habilitar NoNick para un comando especÃ­fico",
        kk_doc="ĐĐĩĐģĐŗŅĐģĐĩĐŊĐŗĐĩĐŊ ĐēĐžĐŧĐŧĐ°ĐŊĐ´Đ° Ō¯ŅŅĐŊ NoNick ŅŌ¯ŅĐģĐĩĐŊĐ´ŅŅŅĐģĐŗĐĩĐŊ",
    )
    async def nonickcmdcmd(self, message: Message):
        """Allow certain command to be executed without nickname"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_cmd"))
            return

        if args not in self.allmodules.commands:
            await utils.answer(message, self.strings("cmd404"))
            return

        nn = self._db.get(main.__name__, "nonickcmds", [])
        if args not in nn:
            nn += [args]
            nn = list(set(nn))
            await utils.answer(
                message,
                self.strings("cmd_nn").format(
                    self.get_prefix() + args,
                    "on",
                ),
            )
        else:
            nn = list(set(nn) - {args})
            await utils.answer(
                message,
                self.strings("cmd_nn").format(
                    self.get_prefix() + args,
                    "off",
                ),
            )

        self._db.set(main.__name__, "nonickcmds", nn)

    @loader.command(
        ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ ŅĐŋĐ¸ŅĐžĐē Đ°ĐēŅĐ¸Đ˛ĐŊŅŅ NoNick ĐēĐžĐŧĐ°ĐŊĐ´",
        fr_doc="Afficher la liste des commandes NoNick actives",
        it_doc="Mostra la lista dei comandi NoNick attivi",
        de_doc="Zeige eine Liste der aktiven NoNick Befehle",
        tr_doc="Etkin NoNick komutlarÄąnÄąn listesini gÃļster",
        uz_doc="Yoqilgan NoNick buyruqlar ro'yxatini ko'rsatish",
        es_doc="Mostrar una lista de comandos NoNick activos",
        kk_doc="ŌĐžŅŅĐģŌĐ°ĐŊ NoNick ĐēĐžĐŧĐŧĐ°ĐŊĐ´Đ°ĐģĐ°Ņ ŅŅĐˇŅĐŧŅĐŊ ĐēĶŠŅŅĐĩŅŅ",
    )
    async def nonickcmds(self, message: Message):
        """Returns the list of NoNick commands"""
        if not self._db.get(main.__name__, "nonickcmds", []):
            await utils.answer(message, self.strings("nothing"))
            return

        await utils.answer(
            message,
            self.strings("cmd_nn_list").format(
                "\n".join(
                    [
                        f"âĢī¸ <code>{self.get_prefix()}{cmd}</code>"
                        for cmd in self._db.get(main.__name__, "nonickcmds", [])
                    ]
                )
            ),
        )

    @loader.command(
        ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ ŅĐŋĐ¸ŅĐžĐē Đ°ĐēŅĐ¸Đ˛ĐŊŅŅ NoNick ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģĐĩĐš",
        fr_doc="Afficher la liste des utilisateurs NoNick actifs",
        it_doc="Mostra la lista degli utenti NoNick attivi",
        de_doc="Zeige eine Liste der aktiven NoNick Benutzer",
        tr_doc="Etkin NoNick kullanÄącÄąlarÄąnÄąn listesini gÃļster",
        uz_doc="Yoqilgan NoNick foydalanuvchilar ro'yxatini ko'rsatish",
        es_doc="Mostrar una lista de usuarios NoNick activos",
        kk_doc="ŌĐžŅŅĐģŌĐ°ĐŊ NoNick ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅĐģĐ°Ņ ŅŅĐˇŅĐŧŅĐŊ ĐēĶŠŅŅĐĩŅŅ",
    )
    async def nonickusers(self, message: Message):
        """Returns the list of NoNick users"""
        users = []
        for user_id in self._db.get(main.__name__, "nonickusers", []).copy():
            try:
                user = await self._client.get_entity(user_id)
            except Exception:
                self._db.set(
                    main.__name__,
                    "nonickusers",
                    list(
                        (
                            set(self._db.get(main.__name__, "nonickusers", []))
                            - {user_id}
                        )
                    ),
                )

                logger.warning("User %s removed from nonickusers list", user_id)
                continue

            users += [
                'âĢī¸ <b><a href="tg://user?id={}">{}</a></b>'.format(
                    user_id,
                    utils.escape_html(get_display_name(user)),
                )
            ]

        if not users:
            await utils.answer(message, self.strings("nothing"))
            return

        await utils.answer(
            message,
            self.strings("user_nn_list").format("\n".join(users)),
        )

    @loader.command(
        ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ ŅĐŋĐ¸ŅĐžĐē Đ°ĐēŅĐ¸Đ˛ĐŊŅŅ NoNick ŅĐ°ŅĐžĐ˛",
        fr_doc="Afficher la liste des chats NoNick actifs",
        it_doc="Mostra la lista dei gruppi NoNick attivi",
        de_doc="Zeige eine Liste der aktiven NoNick Chats",
        tr_doc="Etkin NoNick sohbetlerinin listesini gÃļster",
        uz_doc="Yoqilgan NoNick suhbatlar ro'yxatini ko'rsatish",
        es_doc="Mostrar una lista de chats NoNick activos",
        kk_doc="ŌĐžŅŅĐģŌĐ°ĐŊ NoNick ŅĶŠĐšĐģĐĩŅŅŅŅĐģĐĩŅ ŅŅĐˇŅĐŧŅĐŊ ĐēĶŠŅŅĐĩŅŅ",
    )
    async def nonickchats(self, message: Message):
        """Returns the list of NoNick chats"""
        chats = []
        for chat in self._db.get(main.__name__, "nonickchats", []):
            try:
                chat_entity = await self._client.get_entity(int(chat))
            except Exception:
                self._db.set(
                    main.__name__,
                    "nonickchats",
                    list(
                        (set(self._db.get(main.__name__, "nonickchats", [])) - {chat})
                    ),
                )

                logger.warning("Chat %s removed from nonickchats list", chat)
                continue

            chats += [
                'âĢī¸ <b><a href="{}">{}</a></b>'.format(
                    utils.get_entity_url(chat_entity),
                    utils.escape_html(get_display_name(chat_entity)),
                )
            ]

        if not chats:
            await utils.answer(message, self.strings("nothing"))
            return

        await utils.answer(
            message,
            self.strings("user_nn_list").format("\n".join(chats)),
        )

    async def inline__setting(self, call: InlineCall, key: str, state: bool = False):
        if callable(key):
            key()
            hikkatl.extensions.html.CUSTOM_EMOJIS = not main.get_config_key(
                "disable_custom_emojis"
            )
        else:
            self._db.set(main.__name__, key, state)

        if key == "no_nickname" and state and self.get_prefix() == ".":
            await call.answer(
                self.strings("nonick_warning"),
                show_alert=True,
            )
        else:
            await call.answer("Configuration value saved!")

        await call.edit(
            self.strings("inline_settings"),
            reply_markup=self._get_settings_markup(),
        )

    async def inline__update(
        self,
        call: InlineCall,
        confirm_required: bool = False,
    ):
        if confirm_required:
            await call.edit(
                self.strings("confirm_update"),
                reply_markup=[
                    {"text": "đĒ Update", "callback": self.inline__update},
                    {"text": "đĢ Cancel", "action": "close"},
                ],
            )
            return

        await call.answer("You userbot is being updated...", show_alert=True)
        await call.delete()
        await self.invoke("update", "-f", peer="me")

    async def inline__restart(
        self,
        call: InlineCall,
        confirm_required: bool = False,
    ):
        if confirm_required:
            await call.edit(
                self.strings("confirm_restart"),
                reply_markup=[
                    {"text": "đ Restart", "callback": self.inline__restart},
                    {"text": "đĢ Cancel", "action": "close"},
                ],
            )
            return

        await call.answer("You userbot is being restarted...", show_alert=True)
        await call.delete()
        await self.invoke("restart", "-f", peer="me")

    def _get_settings_markup(self) -> list:
        return [
            [
                (
                    {
                        "text": "â NoNick",
                        "callback": self.inline__setting,
                        "args": (
                            "no_nickname",
                            False,
                        ),
                    }
                    if self._db.get(main.__name__, "no_nickname", False)
                    else {
                        "text": "đĢ NoNick",
                        "callback": self.inline__setting,
                        "args": (
                            "no_nickname",
                            True,
                        ),
                    }
                ),
                (
                    {
                        "text": "â Grep",
                        "callback": self.inline__setting,
                        "args": (
                            "grep",
                            False,
                        ),
                    }
                    if self._db.get(main.__name__, "grep", False)
                    else {
                        "text": "đĢ Grep",
                        "callback": self.inline__setting,
                        "args": (
                            "grep",
                            True,
                        ),
                    }
                ),
                (
                    {
                        "text": "â InlineLogs",
                        "callback": self.inline__setting,
                        "args": (
                            "inlinelogs",
                            False,
                        ),
                    }
                    if self._db.get(main.__name__, "inlinelogs", True)
                    else {
                        "text": "đĢ InlineLogs",
                        "callback": self.inline__setting,
                        "args": (
                            "inlinelogs",
                            True,
                        ),
                    }
                ),
            ],
            [
                (
                    {
                        "text": self.strings("do_not_suggest_fs"),
                        "callback": self.inline__setting,
                        "args": (
                            "disable_modules_fs",
                            False,
                        ),
                    }
                    if self._db.get(main.__name__, "disable_modules_fs", False)
                    else {
                        "text": self.strings("suggest_fs"),
                        "callback": self.inline__setting,
                        "args": (
                            "disable_modules_fs",
                            True,
                        ),
                    }
                )
            ],
            [
                (
                    {
                        "text": self.strings("use_fs"),
                        "callback": self.inline__setting,
                        "args": (
                            "permanent_modules_fs",
                            False,
                        ),
                    }
                    if self._db.get(main.__name__, "permanent_modules_fs", False)
                    else {
                        "text": self.strings("do_not_use_fs"),
                        "callback": self.inline__setting,
                        "args": (
                            "permanent_modules_fs",
                            True,
                        ),
                    }
                ),
            ],
            [
                (
                    {
                        "text": self.strings("suggest_subscribe"),
                        "callback": self.inline__setting,
                        "args": (
                            "suggest_subscribe",
                            False,
                        ),
                    }
                    if self._db.get(main.__name__, "suggest_subscribe", True)
                    else {
                        "text": self.strings("do_not_suggest_subscribe"),
                        "callback": self.inline__setting,
                        "args": (
                            "suggest_subscribe",
                            True,
                        ),
                    }
                ),
            ],
            [
                (
                    {
                        "text": self.strings("no_custom_emojis"),
                        "callback": self.inline__setting,
                        "args": (
                            lambda: main.save_config_key(
                                "disable_custom_emojis", False
                            ),
                        ),
                    }
                    if main.get_config_key("disable_custom_emojis")
                    else {
                        "text": self.strings("custom_emojis"),
                        "callback": self.inline__setting,
                        "args": (
                            lambda: main.save_config_key("disable_custom_emojis", True),
                        ),
                    }
                ),
            ],
            [
                (
                    {
                        "text": self.strings("disable_debugger"),
                        "callback": self.inline__setting,
                        "args": lambda: self._db.set(log.__name__, "debugger", False),
                    }
                    if self._db.get(log.__name__, "debugger", False)
                    else {
                        "text": self.strings("enable_debugger"),
                        "callback": self.inline__setting,
                        "args": (lambda: self._db.set(log.__name__, "debugger", True),),
                    }
                ),
            ],
            [
                {
                    "text": self.strings("btn_restart"),
                    "callback": self.inline__restart,
                    "args": (True,),
                },
                {
                    "text": self.strings("btn_update"),
                    "callback": self.inline__update,
                    "args": (True,),
                },
            ],
            [{"text": self.strings("close_menu"), "action": "close"}],
        ]

    @loader.owner
    @loader.command(
        ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸",
        fr_doc="Afficher les paramÃ¨tres",
        it_doc="Mostra le impostazioni",
        de_doc="Zeige die Einstellungen",
        tr_doc="AyarlarÄą gÃļster",
        uz_doc="Sozlamalarni ko'rsatish",
        es_doc="Mostrar configuraciÃŗn",
        kk_doc="ĐĐ°ĐŋŅĐ°ŅĐģĐ°ŅĐ´Ņ ĐēĶŠŅŅĐĩŅŅ",
    )
    async def settings(self, message: Message):
        """Show settings menu"""
        await self.inline.form(
            self.strings("inline_settings"),
            message=message,
            reply_markup=self._get_settings_markup(),
        )

    @loader.owner
    @loader.command(
        ru_doc="ĐŅĐēŅŅŅŅ ŅĐžĐŊĐŊĐĩĐģŅ Đē Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅŅ Hikka",
        fr_doc="Ouvrir un tunnel vers l'interface web de Hikka",
        it_doc="Apri il tunnel al web interface di Hikka",
        de_doc="Ãffne einen Tunnel zum Hikka Webinterface",
        tr_doc="Hikka Web ArayÃŧzÃŧne bir tÃŧnel aÃ§",
        uz_doc="Hikka veb-interfeysi uchun tunel ochish",
        es_doc="Abrir un tÃēnel al interfaz web de Hikka",
        kk_doc="Hikka Đ˛ĐĩĐą-Đ¸ĐŊŅĐĩŅŅĐĩĐšŅŅĐŊĐĩ ŅŅĐŊĐĩĐģŅ Đ°ŅŅ",
    )
    async def weburl(self, message: Message, force: bool = False):
        """Opens web tunnel to your Hikka web interface"""
        if "LAVHOST" in os.environ:
            form = await self.inline.form(
                self.strings("lavhost_web"),
                message=message,
                reply_markup={
                    "text": self.strings("web_btn"),
                    "url": await main.hikka.web.get_url(proxy_pass=False),
                },
                gif="https://t.me/hikari_assets/28",
            )
            return

        if (
            not force
            and not message.is_private
            and "force_insecure" not in message.raw_text.lower()
        ):
            try:
                if not await self.inline.form(
                    self.strings("privacy_leak_nowarn").format(self._client.tg_id),
                    message=message,
                    reply_markup=[
                        {
                            "text": self.strings("btn_yes"),
                            "callback": self.weburl,
                            "args": (True,),
                        },
                        {"text": self.strings("btn_no"), "action": "close"},
                    ],
                    gif="https://i.gifer.com/embedded/download/Z5tS.gif",
                ):
                    raise Exception
            except Exception:
                await utils.answer(
                    message,
                    self.strings("privacy_leak").format(
                        self._client.tg_id,
                        self.get_prefix(),
                    ),
                )

            return

        if force:
            form = message
            await form.edit(
                self.strings("opening_tunnel"),
                reply_markup={"text": "đ Wait...", "data": "empty"},
                gif=(
                    "https://i.gifer.com/origin/e4/e43e1b221fd960003dc27d2f2f1b8ce1.gif"
                ),
            )
        else:
            form = await self.inline.form(
                self.strings("opening_tunnel"),
                message=message,
                reply_markup={"text": "đ Wait...", "data": "empty"},
                gif=(
                    "https://i.gifer.com/origin/e4/e43e1b221fd960003dc27d2f2f1b8ce1.gif"
                ),
            )

        url = await main.hikka.web.get_url(proxy_pass=True)

        await form.edit(
            self.strings("tunnel_opened"),
            reply_markup={"text": self.strings("web_btn"), "url": url},
            gif="https://t.me/hikari_assets/48",
        )

    @loader.loop(interval=1, autostart=True)
    async def loop(self):
        obj = self.allmodules.get_approved_channel
        if not obj:
            return

        channel, event = obj

        try:
            await self._client(JoinChannelRequest(channel))
        except Exception:
            logger.exception("Failed to join channel")
            event.status = False
            event.set()
        else:
            event.status = True
            event.set()

    def _get_all_IDM(self, module: str):
        return {
            getattr(getattr(self.lookup(module), name), "name", name): getattr(
                self.lookup(module), name
            )
            for name in dir(self.lookup(module))
            if getattr(getattr(self.lookup(module), name), "is_debug_method", False)
        }

    @loader.command()
    async def invokecmd(self, message: Message):
        """<module or `core` for built-in methods> <method> - Only for debugging purposes. DO NOT USE IF YOU'RE NOT A DEVELOPER"""
        args = utils.get_args_raw(message)
        if not args or len(args.split()) < 2:
            await utils.answer(message, self.strings("no_args"))
            return

        module = args.split()[0]
        method = args.split(maxsplit=1)[1]

        if module != "core" and not self.lookup(module):
            await utils.answer(message, self.strings("module404").format(module))
            return

        if (
            module == "core"
            and method not in ALL_INVOKES
            or module != "core"
            and method not in self._get_all_IDM(module)
        ):
            await utils.answer(message, self.strings("invoke404").format(method))
            return

        message = await utils.answer(
            message, self.strings("invoking").format(method, module)
        )
        result = ""

        if module == "core":
            if method == "clear_entity_cache":
                result = (
                    f"Dropped {len(self._client._hikka_entity_cache)} cache records"
                )
                self._client._hikka_entity_cache = {}
            elif method == "clear_fulluser_cache":
                result = (
                    f"Dropped {len(self._client._hikka_fulluser_cache)} cache records"
                )
                self._client._hikka_fulluser_cache = {}
            elif method == "clear_fullchannel_cache":
                result = (
                    f"Dropped {len(self._client._hikka_fullchannel_cache)} cache"
                    " records"
                )
                self._client._hikka_fullchannel_cache = {}
            elif method == "clear_perms_cache":
                result = f"Dropped {len(self._client._hikka_perms_cache)} cache records"
                self._client._hikka_perms_cache = {}
            elif method == "clear_cache":
                result = (
                    f"Dropped {len(self._client._hikka_entity_cache)} entity cache"
                    " records\nDropped"
                    f" {len(self._client._hikka_fulluser_cache)} fulluser cache"
                    " records\nDropped"
                    f" {len(self._client._hikka_fullchannel_cache)} fullchannel cache"
                    " records"
                )
                self._client._hikka_entity_cache = {}
                self._client._hikka_fulluser_cache = {}
                self._client._hikka_fullchannel_cache = {}
                self._client.hikka_me = await self._client.get_me()
            elif method == "reload_core":
                core_quantity = await self.lookup("loader").reload_core()
                result = f"Reloaded {core_quantity} core modules"
            elif method == "inspect_cache":
                result = (
                    "Entity cache:"
                    f" {len(self._client._hikka_entity_cache)} records\nFulluser cache:"
                    f" {len(self._client._hikka_fulluser_cache)} records\nFullchannel"
                    f" cache: {len(self._client._hikka_fullchannel_cache)} records"
                )
            elif method == "inspect_modules":
                result = (
                    "Loaded modules: {}\nLoaded core modules: {}\nLoaded user"
                    " modules: {}"
                ).format(
                    len(self.allmodules.modules),
                    sum(
                        module.__origin__.startswith("<core")
                        for module in self.allmodules.modules
                    ),
                    sum(
                        not module.__origin__.startswith("<core")
                        for module in self.allmodules.modules
                    ),
                )
        else:
            result = await self._get_all_IDM(module)[method](message)

        await utils.answer(
            message,
            self.strings("invoke").format(method, utils.escape_html(result)),
        )

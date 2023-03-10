# ÂŠī¸ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# đ https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# đ https://www.gnu.org/licenses/agpl-3.0.html

import ast
import contextlib
import functools
import typing
from math import ceil

from hikkatl.tl.types import Message

from .. import loader, translations, utils
from ..inline.types import InlineCall

# Everywhere in this module, we use the following naming convention:
# `obj_type` of non-core module = False
# `obj_type` of core module = True
# `obj_type` of library = "library"


@loader.tds
class HikkaConfigMod(loader.Module):
    """Interactive configurator for Hikka Userbot"""

    strings = {
        "name": "HikkaConfig",
        "choose_core": "âī¸ <b>Choose a category</b>",
        "configure": "âī¸ <b>Choose a module to configure</b>",
        "configure_lib": "đĻ <b>Choose a library to configure</b>",
        "configuring_mod": (
            "âī¸ <b>Choose config option for mod</b> <code>{}</code>\n\n<b>Current"
            " options:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĻ <b>Choose config option for library</b> <code>{}</code>\n\n<b>Current"
            " options:</b>\n\n{}"
        ),
        "configuring_option": (
            "âī¸ <b>Configuring option</b> <code>{}</code> <b>of mod"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Default: {}</b>\n\n<b>Current:"
            " {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĻ <b>Configuring option</b> <code>{}</code> <b>of library"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Default: {}</b>\n\n<b>Current:"
            " {}</b>\n\n{}"
        ),
        "option_saved": (
            "<emoji document_id=5318933532825888187>âī¸</emoji> <b>Option"
            "</b> <code>{}</code> <b>of module</b> <code>{}</code><b>"
            " saved!</b>\n<b>Current: {}</b>"
        ),
        "option_saved_lib": (
            "<emoji document_id=5431736674147114227>đĻ</emoji> <b>Option"
            "</b> <code>{}</code> <b>of library</b> <code>{}</code><b>"
            " saved!</b>\n<b>Current: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>Option</b> <code>{}</code> <b>of module</b> <code>{}</code> <b>has"
            " been reset to default</b>\n<b>Current: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>Option</b> <code>{}</code> <b>of library</b> <code>{}</code> <b>has"
            " been reset to default</b>\n<b>Current: {}</b>"
        ),
        "args": "đĢ <b>You specified incorrect args</b>",
        "no_mod": "đĢ <b>Module doesn't exist</b>",
        "no_option": "đĢ <b>Configuration option doesn't exist</b>",
        "validation_error": "đĢ <b>You entered incorrect config value.\nError: {}</b>",
        "try_again": "đ Try again",
        "typehint": "đĩī¸ <b>Must be a{eng_art} {}</b>",
        "set": "set",
        "set_default_btn": "âģī¸ Reset default",
        "enter_value_btn": "âī¸ Enter value",
        "enter_value_desc": "âī¸ Enter new configuration value for this option",
        "add_item_desc": "âī¸ Enter item to add",
        "remove_item_desc": "âī¸ Enter item to remove",
        "back_btn": "đ Back",
        "close_btn": "đģ Close",
        "add_item_btn": "â Add item",
        "remove_item_btn": "â Remove item",
        "show_hidden": "đ¸ Show value",
        "hide_value": "đ Hide value",
        "builtin": "đ° Built-in",
        "external": "đ¸ External",
        "libraries": "đĻ Libraries",
    }

    strings_ru = {
        "choose_core": "âī¸ <b>ĐŅĐąĐĩŅĐ¸ ĐēĐ°ŅĐĩĐŗĐžŅĐ¸Ņ</b>",
        "configure": "âī¸ <b>ĐŅĐąĐĩŅĐ¸ ĐŧĐžĐ´ŅĐģŅ Đ´ĐģŅ ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸</b>",
        "configure_lib": "đĻ <b>ĐŅĐąĐĩŅĐ¸ ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēŅ Đ´ĐģŅ ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸</b>",
        "configuring_mod": (
            "âī¸ <b>ĐŅĐąĐĩŅĐ¸ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅ Đ´ĐģŅ ĐŧĐžĐ´ŅĐģŅ</b> <code>{}</code>\n\n<b>ĐĸĐĩĐēŅŅĐ¸Đĩ"
            " ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĻ <b>ĐŅĐąĐĩŅĐ¸ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅ Đ´ĐģŅ ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸</b> <code>{}</code>\n\n<b>ĐĸĐĩĐēŅŅĐ¸Đĩ"
            " ĐŊĐ°ŅŅŅĐžĐšĐēĐ¸:</b>\n\n{}"
        ),
        "configuring_option": (
            "âī¸ <b>ĐŖĐŋŅĐ°Đ˛ĐģĐĩĐŊĐ¸Đĩ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐžĐŧ</b> <code>{}</code> <b>ĐŧĐžĐ´ŅĐģŅ"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>ĐĄŅĐ°ĐŊĐ´Đ°ŅŅĐŊĐžĐĩ:"
            " {}</b>\n\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĻ <b>ĐŖĐŋŅĐ°Đ˛ĐģĐĩĐŊĐ¸Đĩ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐžĐŧ</b> <code>{}</code> <b>ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>ĐĄŅĐ°ĐŊĐ´Đ°ŅŅĐŊĐžĐĩ:"
            " {}</b>\n\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>\n\n{}"
        ),
        "option_saved": (
            "<emoji document_id=5318933532825888187>âī¸</emoji> <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ"
            "</b> <code>{}</code> <b>ĐŧĐžĐ´ŅĐģŅ</b> <code>{}</code><b>"
            " ŅĐžŅŅĐ°ĐŊĐĩĐŊ!</b>\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>"
        ),
        "option_saved_lib": (
            "<emoji document_id=5431736674147114227>đĻ</emoji> <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ"
            "</b> <code>{}</code> <b>ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸</b> <code>{}</code><b>"
            " ŅĐžŅŅĐ°ĐŊĐĩĐŊ!</b>\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ</b> <code>{}</code> <b>ĐŧĐžĐ´ŅĐģŅ</b> <code>{}</code><b>"
            " ŅĐąŅĐžŅĐĩĐŊ Đ´Đž ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Ņ ĐŋĐž ŅĐŧĐžĐģŅĐ°ĐŊĐ¸Ņ</b>\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ</b> <code>{}</code> <b>ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸</b> <code>{}</code><b>"
            " ŅĐąŅĐžŅĐĩĐŊ Đ´Đž ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Ņ ĐŋĐž ŅĐŧĐžĐģŅĐ°ĐŊĐ¸Ņ</b>\n<b>ĐĸĐĩĐēŅŅĐĩĐĩ: {}</b>"
        ),
        "_cls_doc": "ĐĐŊŅĐĩŅĐ°ĐēŅĐ¸Đ˛ĐŊŅĐš ĐēĐžĐŊŅĐ¸ĐŗŅŅĐ°ŅĐžŅ Hikka",
        "args": "đĢ <b>ĐĸŅ ŅĐēĐ°ĐˇĐ°Đģ ĐŊĐĩĐ˛ĐĩŅĐŊŅĐĩ Đ°ŅĐŗŅĐŧĐĩĐŊŅŅ</b>",
        "no_mod": "đĢ <b>ĐĐžĐ´ŅĐģŅ ĐŊĐĩ ŅŅŅĐĩŅŅĐ˛ŅĐĩŅ</b>",
        "no_option": "đĢ <b>ĐŖ ĐŧĐžĐ´ŅĐģŅ ĐŊĐĩŅ ŅĐ°ĐēĐžĐŗĐž ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Ņ ĐēĐžĐŊŅĐ¸ĐŗĐ°</b>",
        "validation_error": (
            "đĢ <b>ĐĐ˛ĐĩĐ´ĐĩĐŊĐž ĐŊĐĩĐēĐžŅŅĐĩĐēŅĐŊĐžĐĩ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ ĐēĐžĐŊŅĐ¸ĐŗĐ°.\nĐŅĐ¸ĐąĐēĐ°: {}</b>"
        ),
        "try_again": "đ ĐĐžĐŋŅĐžĐąĐžĐ˛Đ°ŅŅ ĐĩŅĐĩ ŅĐ°Đˇ",
        "typehint": "đĩī¸ <b>ĐĐžĐģĐļĐŊĐž ĐąŅŅŅ {}</b>",
        "set": "ĐŋĐžŅŅĐ°Đ˛Đ¸ŅŅ",
        "set_default_btn": "âģī¸ ĐĐŊĐ°ŅĐĩĐŊĐ¸Đĩ ĐŋĐž ŅĐŧĐžĐģŅĐ°ĐŊĐ¸Ņ",
        "enter_value_btn": "âī¸ ĐĐ˛ĐĩŅŅĐ¸ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ",
        "enter_value_desc": "âī¸ ĐĐ˛ĐĩĐ´Đ¸ ĐŊĐžĐ˛ĐžĐĩ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ ŅŅĐžĐŗĐž ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐ°",
        "add_item_desc": "âī¸ ĐĐ˛ĐĩĐ´Đ¸ ŅĐģĐĩĐŧĐĩĐŊŅ, ĐēĐžŅĐžŅŅĐš ĐŊŅĐļĐŊĐž Đ´ĐžĐąĐ°Đ˛Đ¸ŅŅ",
        "remove_item_desc": "âī¸ ĐĐ˛ĐĩĐ´Đ¸ ŅĐģĐĩĐŧĐĩĐŊŅ, ĐēĐžŅĐžŅŅĐš ĐŊŅĐļĐŊĐž ŅĐ´Đ°ĐģĐ¸ŅŅ",
        "back_btn": "đ ĐĐ°ĐˇĐ°Đ´",
        "close_btn": "đģ ĐĐ°ĐēŅŅŅŅ",
        "add_item_btn": "â ĐĐžĐąĐ°Đ˛Đ¸ŅŅ ŅĐģĐĩĐŧĐĩĐŊŅ",
        "remove_item_btn": "â ĐŖĐ´Đ°ĐģĐ¸ŅŅ ŅĐģĐĩĐŧĐĩĐŊŅ",
        "show_hidden": "đ¸ ĐĐžĐēĐ°ĐˇĐ°ŅŅ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ",
        "hide_value": "đ ĐĄĐēŅŅŅŅ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ",
        "builtin": "đ° ĐŅŅŅĐžĐĩĐŊĐŊŅĐĩ",
        "external": "đ¸ ĐĐŊĐĩŅĐŊĐ¸Đĩ",
        "libraries": "đĻ ĐĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ¸",
    }

    strings_fr = {
        "choose_core": "âī¸ <b>choisissez la catÃŠgorie</b>",
        "configure": "âī¸ <b>Choisissez le module Ã  configurer</b>",
        "configure_lib": "đĻ <b>Choisissez la bibliothÃ¨que Ã  configurer</b>",
        "configuring_mod": (
            "âī¸ <b>Choisissez le paramÃ¨tre pour le module</b>"
            " <code>{}</code>\n\n<b>Actuellement rÃŠglages:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĻ <b>Choisissez le paramÃ¨tre pour la bibliothÃ¨que</b>"
            " <code>{}</code>\n\n<b>Actuellement rÃŠglages:</b>\n\n{}"
        ),
        "configuring_option": (
            "âī¸ <b>ContrÃ´le des paramÃ¨tres</b> <code>{}</code> <b>module"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Standard:"
            " {}</b>\n\n<b>Actuelle: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĻ <b>ContrÃ´le des paramÃ¨tres</b> <code>{}</code> <b>library"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Standard:"
            " {}</b>\n\n<b>Actuelle: {}</b>\n\n{}"
        ),
        "option_saved": (
            "<emoji document_id=5318933532825888187>âī¸</emoji> <b>ParamÃ¨tre"
            "</b> <code>{}</code> <b>module</b> <code>{}</code><b>"
            " enregistrÃŠ!</b>\n<b>Actuelle: {}</b>"
        ),
        "option_saved_lib": (
            "<emoji document_id=5431736674147114227>đĻ</emoji> <b>ParamÃ¨tre"
            "</b> <code>{}</code> <b>library</b> <code>{}</code><b>"
            " enregistrÃŠ!</b>\n<b>Actuelle: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>ParamÃ¨tre</b> <code>{}</code> <b>module</b> <code>{}</code><b>"
            " rÃŠinitialisÃŠ Ã  la valeur par dÃŠfaut</b>\n<b>Actuelle: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>ParamÃ¨tre</b> <code>{}</code> <b>de la librairie</b>"
            " <code>{}</code><b> rÃŠinitialisÃŠ Ã  sa valeur par dÃŠfaut</b>\n<b>Actuel:"
            " {}</b>"
        ),
        "_cls_doc": "Configuration interactive Hikka",
        "args": "đĢ <b>Vous avez spÃŠcifiÃŠ des arguments incorrects</b>",
        "no_mod": "đĢ <b>Le module n'existe pas</b>",
        "no_option": "đĢ <b>Le module n'a pas de paramÃ¨tre</b>",
        "validation_error": (
            "đĢ <b>Vous avez entrÃŠ une valeur de configuration incorrecte.\nErreur:"
            " {}</b>"
        ),
        "try_again": "đ Essayez Ã  nouveau",
        "typehint": "đĩī¸ <b>Doit ÃĒtre {}</b>",
        "set": "mettre",
        "set_default_btn": "âģī¸ Valeur par dÃŠfaut",
        "enter_value_btn": "âī¸ Entrer une valeur",
        "enter_value_desc": "âī¸ Entrez une nouvelle valeur pour ce paramÃ¨tre",
        "add_item_desc": "âī¸ Entrez l'ÃŠlÃŠment Ã  ajouter",
        "remove_item_desc": "âī¸ Entrez l'ÃŠlÃŠment Ã  supprimer",
        "back_btn": "đ Retour",
        "close_btn": "đģ Fermer",
        "add_item_btn": "â Ajouter un ÃŠlÃŠment",
        "remove_item_btn": "â Supprimer un ÃŠlÃŠment",
        "show_hidden": "đ¸ Afficher la valeur",
        "hide_value": "đ Masquer la valeur",
        "builtin": "đ° IntÃŠgrÃŠ",
        "external": "đ¸ Externe",
        "libraries": "đĻ BibliothÃ¨ques",
    }

    strings_it = {
        "choose_core": "âī¸ <b>Scegli la categoria</b>",
        "configure": "âī¸ <b>Scegli il modulo da configurare</b>",
        "configure_lib": "đĻ <b>Scegli la libreria da configurare</b>",
        "configuring_mod": (
            "âī¸ <b>Scegli il parametro per il modulo</b> <code>{}</code>\n\n<b>Attuale"
            " configurazione:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĻ <b>Scegli il parametro per la libreria</b> <code>{}</code>\n\n<b>Attuale"
            " configurazione:</b>\n\n{}"
        ),
        "configuring_option": (
            "âī¸ <b>Configurazione dell'opzione</b> <code>{}</code> <b>del"
            " modulo</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Standard:"
            " {}</b>\n\n<b>Attuale: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĻ <b>Configurazione dell'opzione</b> <code>{}</code> <b>della"
            " libreria</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Standard:"
            " {}</b>\n\n<b>Attuale: {}</b>\n\n{}"
        ),
        "option_saved": (
            "<emoji document_id=5318933532825888187>âī¸</emoji> <b>Opzione"
            "</b> <code>{}</code> <b>del modulo</b> <code>{}</code><b>"
            " salvata!</b>\n<b>Attuale: {}</b>"
        ),
        "option_saved_lib": (
            "<emoji document_id=5431736674147114227>đĻ</emoji> <b>Opzione"
            "</b> <code>{}</code> <b>della libreria</b> <code>{}</code><b>"
            " salvata!</b>\n<b>Attuale: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>Opzione</b> <code>{}</code> <b>del modulo</b> <code>{}</code><b>"
            " resettata al valore di default</b>\n<b>Attuale: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>Opzione</b> <code>{}</code> <b>della libreria</b> <code>{}</code><b>"
            " resettata al valore di default</b>\n<b>Attuale: {}</b>"
        ),
        "_cls_doc": "Configuratore interattivo di Hikka",
        "args": "đĢ <b>Hai fornito argomenti non validi</b>",
        "validation_error": (
            "đĢ <b>Hai fornito un valore di configurazione non valido.\nErrore: {}</b>"
        ),
        "try_again": "đ Riprova",
        "typehint": "đĩī¸ <b>Dovrebbe essere {}</b>",
        "set": "impostare",
        "set_default_btn": "âģī¸ Imposta valore di default",
        "enter_value_btn": "âī¸ Inserisci valore",
        "enter_value_desc": "âī¸ Inserisci il nuovo valore di questo parametro",
        "add_item_desc": "âī¸ Inserisci l'elemento che vuoi aggiungere",
        "remove_item_desc": "âī¸ Inserisci l'elemento che vuoi rimuovere",
        "back_btn": "đ Indietro",
        "close_btn": "đģ Chiudi",
        "add_item_btn": "â Aggiungi elemento",
        "remove_item_btn": "â Rimuovi elemento",
        "show_hidden": "đ¸ Mostra valore",
        "hide_value": "đ Nascondi valore",
        "builtin": "đ° Built-in",
        "external": "đ¸ Esterni",
        "libraries": "đĻ Librerie",
    }

    strings_de = {
        "choose_core": "âī¸ <b>WÃ¤hle eine Kategorie</b>",
        "configure": "âī¸ <b>WÃ¤hle einen Modul zum Konfigurieren</b>",
        "configure_lib": "đĻ <b>WÃ¤hle eine Bibliothek zum Konfigurieren</b>",
        "configuring_mod": (
            "âī¸ <b>WÃ¤hle eine Option fÃŧr das Modul</b> <code>{}</code>\n\n<b>Aktuelle"
            " Einstellungen:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĻ <b>WÃ¤hle eine Option fÃŧr die Bibliothek</b>"
            " <code>{}</code>\n\n<b>Aktuelle Einstellungen:</b>\n\n{}"
        ),
        "configuring_option": (
            "âī¸ <b>Optionen verwalten</b> <code>{}</code> <b>fÃŧr das Modul"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Standard:"
            " {}</b>\n\n<b>Aktuelle: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĻ <b>Optionen verwalten</b> <code>{}</code> <b>fÃŧr die Bibliothek"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Standard:"
            " {}</b>\n\n<b>Aktuelle: {}</b>\n\n{}"
        ),
        "option_saved": (
            "<emoji document_id=5318933532825888187>âī¸</emoji> <b>Option"
            "</b> <code>{}</code> <b>fÃŧr das Modul</b> <code>{}</code><b>"
            " gespeichert!</b>\n<b>Aktuelle: {}</b>"
        ),
        "option_saved_lib": (
            "<emoji document_id=5431736674147114227>đĻ</emoji> <b>Option"
            "</b> <code>{}</code> <b>fÃŧr die Bibliothek</b> <code>{}</code><b>"
            " gespeichert!</b>\n<b>Aktuelle: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>Option</b> <code>{}</code> <b>fÃŧr das Modul</b> <code>{}</code><b>"
            " auf den Standardwert zurÃŧckgesetzt</b>\n<b>Aktuelle: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>Option</b> <code>{}</code> <b>fÃŧr die Bibliothek</b>"
            " <code>{}</code><b> auf den Standardwert zurÃŧckgesetzt</b>\n<b>Aktuelle:"
            " {}</b>"
        ),
        "args": "đĢ <b>UngÃŧltige Argumente angegeben</b>",
        "no_mod": "đĢ <b>Modul existiert nicht</b>",
        "no_option": "đĢ <b>Das Modul hat keinen solchen Konfigurationswert</b>",
        "validation_error": (
            "đĢ <b>UngÃŧltiger Konfigurationswert eingegeben.\nFehler: {}</b>"
        ),
        "try_again": "đ Versuch es noch einmal",
        "typehint": "đĩī¸ <b>Es sollte {} sein</b>",
        "set": "setzen",
        "set_default_btn": "âģī¸ Standardwert",
        "enter_value_btn": "âī¸ Wert eingeben",
        "enter_value_desc": "âī¸ Gib einen neuen Wert fÃŧr diesen Parameter ein",
        "add_item_desc": "âī¸ Gib das Element ein, das du hinzufÃŧgen mÃļchtest",
        "remove_item_desc": "âī¸ Gib das Element ein, das du entfernen mÃļchtest",
        "back_btn": "đ ZurÃŧck",
        "close_btn": "đģ SchlieÃen",
        "add_item_btn": "â Element hinzufÃŧgen",
        "remove_item_btn": "â Element entfernen",
        "show_hidden": "đ¸ Wert anzeigen",
        "hide_value": "đ Wert verstecken",
        "builtin": "đ° Ingebaut",
        "external": "đ¸ Extern",
        "libraries": "đĻ Bibliotheken",
    }

    strings_uz = {
        "choose_core": "âī¸ <b>Qurilmangizni tanlang</b>",
        "configure": "âī¸ <b>Sozlamalar uchun modulni tanlang</b>",
        "configure_lib": "đĻ <b>Sozlamalar uchun kutubxonani tanlang</b>",
        "configuring_mod": (
            "âī¸ <b>Modul</b> <code>{}</code> <b>sozlamalari</b>\n\n<b>Joriy"
            " sozlamalar:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĻ <b>Kutubxona</b> <code>{}</code> <b>sozlamalari</b>\n\n<b>Joriy"
            " sozlamalar:</b>\n\n{}"
        ),
        "configuring_option": (
            "âī¸ <b>Modul</b> <code>{}</code> <b>parametriga</b> <code>{}</code>\n<i>âšī¸"
            " {}</i>\n\n<b>Standart: {}</b>\n\n<b>Joriy: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĻ <b>Kutubxona</b> <code>{}</code> <b>parametriga</b>"
            " <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Standart: {}</b>\n\n<b>Joriy:"
            " {}</b>\n\n{}"
        ),
        "option_saved": (
            "<emoji document_id=5318933532825888187>âī¸</emoji> <b>Parametr"
            "</b> <code>{}</code> <b>modul</b> <code>{}</code><b>"
            " saqlandi!</b>\n<b>Joriy: {}</b>"
        ),
        "option_saved_lib": (
            "<emoji document_id=5431736674147114227>đĻ</emoji> <b>Parametr"
            "</b> <code>{}</code> <b>kutubxona</b> <code>{}</code><b>"
            " saqlandi!</b>\n<b>Joriy: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>Parametr</b> <code>{}</code> <b>modul</b> <code>{}</code><b>"
            " standart qiymatiga qaytarildi</b>\n<b>Joriy: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>Parametr</b> <code>{}</code> <b>kutubxona</b> <code>{}</code><b>"
            " standart qiymatiga qaytarildi</b>\n<b>Joriy: {}</b>"
        ),
        "_cls_doc": "Hikka konfiguratori interaktiv",
        "args": "đĢ <b>Siz noto'g'ri argumentlarni kiritdingiz</b>",
        "no_mod": "đĢ <b>Ushbu modul mavjud emas</b>",
        "no_option": "đĢ <b>Bunday konfiguratsiya qiymati mavjud emas</b>",
        "validation_error": "đĢ <b>Kiritilgan qiymat noto'g'ri.\nXato: {}</b>",
        "try_again": "đ Qayta urinib ko'ring",
        "typehint": "đĩī¸ <b>{} bo'lishi kerak</b>",
        "set": "sozlash",
        "set_default_btn": "âģī¸ Standart qiymatni o'rnatish",
        "enter_value_btn": "âī¸ Qiymatni kiriting",
        "enter_value_desc": "âī¸ Ushbu parametrdagi yangi qiymatni kiriting",
        "add_item_desc": "âī¸ Qo'shish uchun elementni kiriting",
        "remove_item_desc": "âī¸ O'chirish uchun elementni kiriting",
        "back_btn": "đ Orqaga",
        "close_btn": "đģ Yopish",
        "add_item_btn": "â Element qo'shish",
        "remove_item_btn": "â Elementni o'chirish",
        "show_hidden": "đ¸ Qiymatni ko'rsatish",
        "hide_value": "đ Qiymatni yashirish",
        "builtin": "đ° Tizimli",
        "external": "đ¸ Tashqi",
        "libraries": "đĻ Kutubxonalar",
    }

    strings_tr = {
        "choose_core": "âī¸ <b>ModÃŧl seÃ§</b>",
        "configure": "âī¸ <b>ModÃŧl yapÄąlandÄąr</b>",
        "configure_lib": "đĻ <b>KÃŧtÃŧphaneyi yapÄąlandÄąr</b>",
        "configuring_mod": (
            "âī¸ <b>ModÃŧlÃŧn</b> <code>{}</code> <b>parametresini seÃ§</b>\n\n<b>GeÃ§erli"
            " ayarlar:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĻ <b>KÃŧtÃŧphanenin</b> <code>{}</code> <b>parametresini"
            " seÃ§</b>\n\n<b>GeÃ§erli ayarlar:</b>\n\n{}"
        ),
        "configuring_option": (
            "âī¸ <b>ModÃŧlÃŧn</b> <code>{}</code> <b>parametresi</b> <code>{}</code>"
            " <b>ayarlarÄąnÄą deÄiÅtir</b>\n<i>âšī¸ {}</i>\n\n<b>VarsayÄąlan:"
            " {}</b>\n\n<b>GeÃ§erli: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĻ <b>KÃŧtÃŧphanenin</b> <code>{}</code> <b>parametresi</b> <code>{}</code>"
            " <b>ayarlarÄąnÄą deÄiÅtir</b>\n<i>âšī¸ {}</i>\n\n<b>VarsayÄąlan:"
            " {}</b>\n\n<b>GeÃ§erli: {}</b>\n\n{}"
        ),
        "option_saved": (
            "<emoji document_id=5318933532825888187>âī¸</emoji> <b>Parametre"
            "</b> <code>{}</code> <b>modÃŧlÃŧnÃŧn</b> <code>{}</code><b>"
            " kaydedildi!</b>\n<b>GeÃ§erli: {}</b>"
        ),
        "option_saved_lib": (
            "<emoji document_id=5431736674147114227>đĻ</emoji> <b>Parametre"
            "</b> <code>{}</code> <b>kÃŧtÃŧphanenin</b> <code>{}</code><b>"
            " kaydedildi!</b>\n<b>GeÃ§erli: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>Parametre</b> <code>{}</code> <b>modÃŧlÃŧnÃŧn</b> <code>{}</code><b>"
            " varsayÄąlana sÄąfÄąrlandÄą</b>\n<b>GeÃ§erli: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>Parametre</b> <code>{}</code> <b>kÃŧtÃŧphanenin</b> <code>{}</code><b>"
            " varsayÄąlana sÄąfÄąrlandÄą</b>\n<b>GeÃ§erli: {}</b>"
        ),
        "_cls_doc": "Hikka Interactive Configurater",
        "args": "đĢ <b>Ä°stediÄiniz argumanlarÄą yanlÄąÅ girdiniz</b>",
        "no_mod": "đĢ <b>ModÃŧl mevcut deÄil</b>",
        "no_option": "đĢ <b>ModÃŧlde bÃļyle bir ayar yok</b>",
        "validation_error": "đĢ <b>YanlÄąÅ bir ayar girdiniz.\nHata: {}</b>",
        "try_again": "đ Tekrar deneyin",
        "typehint": "đĩī¸ <b>{} olmalÄą</b>",
        "set": "ayarla",
        "set_default_btn": "âģī¸ VarsayÄąlan ayar",
        "enter_value_btn": "âī¸ DeÄer girin",
        "enter_value_desc": "âī¸ Yeni bu parametrenin deÄerini girin",
        "add_item_desc": "âī¸ Eklemek iÃ§in ÃļÄeyi girin",
        "remove_item_desc": "âī¸ Silinecek ÃļÄeyi girin",
        "back_btn": "đ Geri dÃļn",
        "close_btn": "đģ Kapat",
        "add_item_btn": "â ÃÄe ekle",
        "remove_item_btn": "â ÃÄe sil",
        "show_hidden": "đ¸ DeÄer GÃļster",
        "hide_value": "đ DeÄeri Gizle",
        "builtin": "đ° Dahili",
        "external": "đ¸ DÄąÅ",
        "libraries": "đĻ KitaplÄąklar",
    }

    strings_es = {
        "choose_core": "âī¸ <b>Elige una categorÃ­a</b>",
        "configure": "âī¸ <b>Elige un mÃŗdulo para configurar</b>",
        "configure_lib": "đĻ <b>Elige una librerÃ­a para configurar</b>",
        "configuring_mod": (
            "âī¸ <b>Elige una opciÃŗn para el mÃŗdulo</b>"
            " <code>{}</code>\n\n<b>ConfiguraciÃŗn actual:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĻ <b>Elige una opciÃŗn para la librerÃ­a</b>"
            " <code>{}</code>\n\n<b>ConfiguraciÃŗn actual:</b>\n\n{}"
        ),
        "configuring_option": (
            "âī¸ <b>Administra la opciÃŗn</b> <code>{}</code> <b>del mÃŗdulo"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Predeterminado:"
            " {}</b>\n\n<b>Actual: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĻ <b>Administra la opciÃŗn</b> <code>{}</code> <b>de la librerÃ­a"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>Predeterminado:"
            " {}</b>\n\n<b>Actual: {}</b>\n\n{}"
        ),
        "option_saved": (
            "<emoji document_id=5318933532825888187>âī¸</emoji> <b>La opciÃŗn"
            "</b> <code>{}</code> <b>del mÃŗdulo</b> <code>{}</code><b>"
            " ha sido guardada!</b>\n<b>Actual: {}</b>"
        ),
        "option_saved_lib": (
            "<emoji document_id=5431736674147114227>đĻ</emoji> <b>La opciÃŗn"
            "</b> <code>{}</code> <b>de la librerÃ­a</b> <code>{}</code><b>"
            " ha sido guardada!</b>\n<b>Actual: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>La opciÃŗn</b> <code>{}</code> <b>del mÃŗdulo</b> <code>{}</code><b>"
            " ha sido restablecida al valor predeterminado</b>\n<b>Actual: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>La opciÃŗn</b> <code>{}</code> <b>de la librerÃ­a</b>"
            " <code>{}</code><b> ha sido restablecida al valor"
            " predeterminado</b>\n<b>Actual: {}</b>"
        ),
        "_cls_doc": "Configurador interactivo Hikka",
        "args": "đĢ <b>Has especificado argumentos incorrectos</b>",
        "no_mod": "đĢ <b>El mÃŗdulo no existe</b>",
        "no_option": "đĢ <b>El mÃŗdulo no tiene esta configuraciÃŗn</b>",
        "validation_error": (
            "đĢ <b>Has especificado un valor incorrecto para esta configuraciÃŗn.\nError:"
            " {}</b>"
        ),
        "try_again": "đ Intentar de nuevo",
        "typehint": "đĩī¸ <b>Debe ser {}</b>",
        "set": "establecer",
        "set_default_btn": "âģī¸ Valor predeterminado",
        "enter_value_btn": "âī¸ Ingresar valor",
        "enter_value_desc": "âī¸ Ingresa el nuevo valor de esta configuraciÃŗn",
        "add_item_desc": "âī¸ Ingresa el elemento que deseas agregar",
        "remove_item_desc": "âī¸ Ingresa el elemento que deseas eliminar",
        "back_btn": "đ AtrÃĄs",
        "close_btn": "đģ Cerrar",
        "add_item_btn": "â Agregar elemento",
        "remove_item_btn": "â Eliminar elemento",
        "show_hidden": "đ¸ Mostrar valor",
        "hide_value": "đ Ocultar valor",
        "builtin": "đ° Interno",
        "external": "đ¸ Externo",
        "libraries": "đĻ LibrerÃ­as",
    }

    strings_kk = {
        "choose_core": "âī¸ <b>ĐĸĐ°ŌŅŅŅĐŋŅŅ ŅĐ°ŌŖĐ´Đ°ŌŖŅĐˇ</b>",
        "configure": "âī¸ <b>ĐĐžĐŊŅĐ¸ĐŗŅŅĐ°ŅĐ¸ŅĐģĐ°ĐŊĐ°ŅŅĐŊ ĐŧĐžĐ´ŅĐģŅĐ´Ņ ŅĐ°ŌŖĐ´Đ°ŌŖŅĐˇ</b>",
        "configure_lib": "đĻ <b>ĐĐžĐŊŅĐ¸ĐŗŅŅĐ°ŅĐ¸ŅĐģĐ°ĐŊĐ°ŅŅĐŊ ĐēŅŅĐ°ĐŋŅĐ°ĐŊĐ°ĐŊŅ ŅĐ°ŌŖĐ´Đ°ŌŖŅĐˇ</b>",
        "configuring_mod": (
            "âī¸ <b>ĐĐžĐ´ŅĐģŅ</b> <code>{}</code> <b>Ō¯ŅŅĐŊ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅŅĐŊ"
            " ŅĐ°ŌŖĐ´Đ°ŌŖŅĐˇ</b>\n\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ ĐąĐ°ĐŋŅĐ°ŅĐģĐ°Ņ:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĻ <b>ĐŅŅĐ°ĐŋŅĐ°ĐŊĐ°</b> <code>{}</code> <b>Ō¯ŅŅĐŊ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅŅĐŊ"
            " ŅĐ°ŌŖĐ´Đ°ŌŖŅĐˇ</b>\n\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ ĐąĐ°ĐŋŅĐ°ŅĐģĐ°Ņ:</b>\n\n{}"
        ),
        "configuring_option": (
            "âī¸ <b>ĐĐžĐ´ŅĐģŅ</b> <code>{}</code> <b>Ō¯ŅŅĐŊ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅŅĐŊ</b> <code>{}</code><b>"
            " ĐąĐ°ŅŌĐ°ŅŅŌŖŅĐˇ</b>\n<i>âšī¸ {}</i>\n\n<b>ĶĐ´ĐĩĐŋĐēŅ:"
            " {}</b>\n\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĻ <b>ĐŅŅĐ°ĐŋŅĐ°ĐŊĐ°</b> <code>{}</code> <b>Ō¯ŅŅĐŊ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅŅĐŊ</b>"
            " <code>{}</code><b> ĐąĐ°ŅŌĐ°ŅŅŌŖŅĐˇ</b>\n<i>âšī¸ {}</i>\n\n<b>ĶĐ´ĐĩĐŋĐēŅ:"
            " {}</b>\n\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ: {}</b>\n\n{}"
        ),
        "option_saved": (
            "<emoji document_id=5318933532825888187>âī¸</emoji> <b>ĐĐžĐ´ŅĐģŅ</b>"
            " <code>{}</code><b> ĐŋĐ°ŅĐ°ĐŧĐĩŅŅŅ</b> <code>{}</code><b>"
            " ŅĐ°ŌŅĐ°ĐģĐ´Ņ!</b>\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ: {}</b>"
        ),
        "option_saved_lib": (
            "<emoji document_id=5431736674147114227>đĻ</emoji> <b>ĐŅŅĐ°ĐŋŅĐ°ĐŊĐ°</b>"
            " <code>{}</code><b> ĐŋĐ°ŅĐ°ĐŧĐĩŅŅŅ</b> <code>{}</code><b>"
            " ŅĐ°ŌŅĐ°ĐģĐ´Ņ!</b>\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>ĐĐžĐ´ŅĐģŅ</b> <code>{}</code><b> ĐŋĐ°ŅĐ°ĐŧĐĩŅŅŅ</b> <code>{}</code><b>"
            " ĐąĐ°ŅŅĐ°ĐŋŌŅ ŅĐĩŅŅĐŊĐĩ ŌĐ°ĐšŅĐ°ŅŅĐģĐ´Ņ</b>\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>ĐĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ°</b> <code>{}</code><b> ĐŋĐ°ŅĐ°ĐŧĐĩŅŅŅ</b> <code>{}</code><b>"
            " ĐąĐ°ŅŅĐ°ĐŋŌŅ ŅĐĩŅŅĐŊĐĩ ŌĐ°ĐšŅĐ°ŅŅĐģĐ´Ņ</b>\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ: {}</b>"
        ),
        "_cls_doc": "Hikka Đ¸ĐŊŅĐĩŅĐ°ĐēŅĐ¸Đ˛ŅĐģŅĐē ĐēĐžĐŊŅĐ¸ĐŗŅŅĐ°ŅĐ¸ŅŅŅ",
        "args": "đĢ <b>ĐĄŅĐˇ Đ´ŌąŅŅŅ ĐĩĐŧĐĩŅ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐģĐĩŅĐ´Ņ ĐēĶŠŅŅĐĩŅŅŅŌŖŅĐˇ</b>",
        "no_mod": "đĢ <b>ĐĐžĐ´ŅĐģŅ ĐļĐžŌ</b>",
        "no_option": "đĢ <b>ĐĐžĐ´ŅĐģŅĐ´ŅŌŖ ĐąŌąĐģ ĐēĐžĐŊŅĐ¸ĐŗŅŅĐ°ŅĐ¸Ņ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅŅ ĐļĐžŌ</b>",
        "validation_error": (
            "đĢ <b>ĐŌąŅŅŅ ĐĩĐŧĐĩŅ ĐēĐžĐŊŅĐ¸ĐŗŅŅĐ°ŅĐ¸Ņ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅŅĐŊ ĐĩĐŊĐŗŅĐˇĐ´ŅŌŖŅĐˇ.\nĐĨĐ°ŅĐ°: {}</b>"
        ),
        "try_again": "đ ŌĐ°ĐšŅĐ°ĐģĐ°Đŋ ĐēĶŠŅŅŌŖŅĐˇ",
        "typehint": "đĩī¸ <b>{} ĐąĐžĐģŅŅ ĐēĐĩŅĐĩĐē</b>",
        "set": "ĐŅĐŊĐ°ŅŅ",
        "set_default_btn": "âģī¸ ĐĐ°ŅŅĐ°ĐŋŌŅ ŅĐĩŅ",
        "enter_value_btn": "âī¸ ĐĶĐŊĐ´Ņ ĐĩĐŊĐŗŅĐˇŅ",
        "enter_value_desc": "âī¸ ĐŌąĐģ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐ´ŅŌŖ ĐļĐ°ŌŖĐ° ĐŧĶĐŊŅĐŊ ĐĩĐŊĐŗŅĐˇŅŌŖŅĐˇ",
        "add_item_desc": "âī¸ ŌĐžŅŅĐģŅŅ ĐēĐĩŅĐĩĐē ŅĐģĐĩĐŧĐĩĐŊŅŅŅ ĐĩĐŊĐŗŅĐˇŅŌŖŅĐˇ",
        "remove_item_desc": "âī¸ ĐĐžŅŅ ĐēĐĩŅĐĩĐē ŅĐģĐĩĐŧĐĩĐŊŅŅŅ ĐĩĐŊĐŗŅĐˇŅŌŖŅĐˇ",
        "back_btn": "đ ĐŅŅŌĐ°",
        "close_btn": "đģ ĐĐ°ĐąŅ",
        "add_item_btn": "â Đ­ĐģĐĩĐŧĐĩĐŊŅŅŅ ŌĐžŅŅ",
        "remove_item_btn": "â Đ­ĐģĐĩĐŧĐĩĐŊŅŅŅ ĐļĐžŅ",
        "show_hidden": "đ¸ ĐĶĐŊĐ´Ņ ĐēĶŠŅŅĐĩŅŅ",
        "hide_value": "đ ĐĶĐŊĐ´Ņ ĐļĐ°ŅŅŅŅ",
        "builtin": "đ° ŌŌąŅŅĐģŌŅ",
        "external": "đ¸ ĐĄŅŅŅŌŅ",
        "libraries": "đĻ ĐŅŅĐ°ĐŋŅĐ°ĐŊĐ°ĐģĐ°Ņ",
    }

    strings_tt = {
        "choose_core": "âī¸ <b>ĐĸĐ°ŌŖĐ´Đ° ĐēĐ°ŅĐĩĐŗĐžŅĐ¸Ņ</b>",
        "configure": "âī¸ <b>ĐĸĐ°ŌŖĐ´Đ° ĐŧĐžĐ´ŅĐģŅĐ´Ņ ĐŊĐ°ŅŅŅĐžĐšĐēĐ°</b>",
        "configure_lib": "đĻ <b>ĐĸĐ°ŌŖĐ´Đ° ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ° ĐŊĐ°ŅŅŅĐžĐšĐēĐ°</b>",
        "configuring_mod": (
            "âī¸ <b>ĐĸĐ°ŌŖĐ´Đ° ĐŋĐ°ŅĐ°ĐŧĐĩŅŅ ĐŧĐžĐ´ŅĐģŅ</b> <code>{}</code>\n\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ"
            " ĐŊĐ°ŅŅŅĐžĐšĐēĐ°:</b>\n\n{}"
        ),
        "configuring_lib": (
            "đĻ <b>ĐĸĐ°ŌŖĐ´Đ° ĐŋĐ°ŅĐ°ĐŧĐĩŅŅ ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ°</b> <code>{}</code>\n\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ"
            " ĐŊĐ°ŅŅŅĐžĐšĐēĐ°:</b>\n\n{}"
        ),
        "configuring_option": (
            "âī¸ <b>ĐĐĩŅŅŌ¯ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅ</b> <code>{}</code> <b>ĐŧĐžĐ´ŅĐģŅ"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>ĐĄŅĐ°ĐŊĐ´Đ°ŅŅĐŊŅ:"
            " {}</b>\n\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "đĻ <b>ĐĐĩŅŅŌ¯ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅ</b> <code>{}</code> <b>ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ°"
            "</b> <code>{}</code>\n<i>âšī¸ {}</i>\n\n<b>ĐĄŅĐ°ĐŊĐ´Đ°ŅŅĐŊŅ:"
            " {}</b>\n\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ: {}</b>\n\n{}"
        ),
        "option_saved": (
            "<emoji document_id=5318933532825888187>âī¸</emoji> <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ"
            "</b> <code>{}</code> <b>ĐŧĐžĐ´ŅĐģŅ</b> <code>{}</code><b>"
            " ŅĐ°ŌŅĐ°ĐģĐ´Ņ!</b>\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ: {}</b>"
        ),
        "option_saved_lib": (
            "<emoji document_id=5431736674147114227>đĻ</emoji> <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ"
            "</b> <code>{}</code> <b>ĐąĐ¸ĐąĐģĐ¸ĐžŅĐĩĐēĐ°</b> <code>{}</code><b>"
            " ŅĐ°ŌŅĐ°ĐģĐ´Ņ!</b>\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ: {}</b>"
        ),
        "option_reset": (
            "âģī¸ <b>ĐĐ°ŅĐ°ĐŧĐĩŅŅ</b> <code>{}</code> <b>ĐŧĐžĐ´ŅĐģŅ</b> <code>{}</code><b>"
            " Đ°ĐģŅĐŊŌĐ°ĐŊ ĐēŌ¯ĐšĐ´Đĩ ĐēĐ°ĐšŅĐ°ŅŅĐģĐ´Ņ</b>\n<b>ĐŌŅĐŧĐ´Đ°ŌŅ: {}</b>"
        ),
        "option_reset_lib": (
            "âģī¸ <b>ĐĶŠĐšĐģĶĐŊĐĩŅ</b> <code>{}</code> <b>ĐģĶĐąĐˇĶ</b> <code>{}</code><b>"
            " ĐēĐ°ĐšŅĐ°ŅŅĐģĐ´Ņ</b>\n<b>ĐĐŗŅĐŧĐ´Đ°: {}</b>"
        ),
        "_cls_doc": "Hikka Đ¸ĐŊŅĐĩŅĐ°ĐēŅĐ¸Đ˛ ĐēĐžĐŊŅĐ¸ĐŗŅŅĐ°ŅĐ¸ŅŅĐĩ",
        "args": "đĢ <b>ĐĶŠĐšĐģĶĐŊĐĩŅĐŊĐĩŌŖ Đ´ĶŠŅĐĩŅ ĐąŅĐģĐŧĐ°ĐŗĐ°ĐŊ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐģĐ°ŅŅ ĐąĐ°Ņ</b>",
        "no_mod": "đĢ <b>ĐĐžĐ´ŅĐģŅĐŊĐĩ ŅĐ°ĐąŅĐŋ ĐąŅĐģĐŧĐ°Đ´ŅĐŧ</b>",
        "no_option": (
            "đĢ <b>ĐĶŠĐšĐģĶĐŊĐĩŅĐŊĐĩŌŖ ĐąŅ ĐŧĐžĐ´ŅĐģŅĐ´Đ° ĐŧĶŠĐŧĐēĐ¸ĐŊ ĐąŅĐģĐŧĐ°ĐŗĐ°ĐŊ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐģĐ°ŅŅ ĐąĐ°Ņ</b>"
        ),
        "validation_error": (
            "đĢ <b>ĐĶŠĐšĐģĶĐŊĐĩŅĐŊĐĩŌŖ Đ´ĶŠŅĐĩŅ ĐąŅĐģĐŧĐ°ĐŗĐ°ĐŊ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐģĐ°ŅŅ ĐąĐ°Ņ.\nĐŅĐ¸ĐąĐēĐ°: {}</b>"
        ),
        "try_again": "đ ĐĸĐ°ĐŗŅĐŊ ĐēĐ°ĐąĐ°ŅĐģĐ°Ņ",
        "typehint": "đĩī¸ <b>{} ĐąŅĐģŅŅĐŗĐ° ŅĐ¸ĐĩŅ</b>",
        "set": "ĐēŌ¯ŅŅĶŅĐĩŅĐŗĶ",
        "set_default_btn": "âģī¸ ĐĶŠĐšĐģĶĐŊĐĩŅĐŊĐĩŌŖ ĐēĐ¸ĐģĐĩŅĐĩ ĐēĶŠĐšĐģĶĐŊĐĩŅĐĩ",
        "enter_value_btn": "âī¸ ĐĶŠĐšĐģĶĐŊĐĩŅĐŊĐĩŌŖ ŅŌŖĐ° ĐēĶŠĐšĐģĶĐŊĐĩŅĐĩ",
        "enter_value_desc": "âī¸ ĐĐžĐ´ŅĐģŅĐŊĐĩŌŖ ĐēĶŠĐšĐģĶĐŊĐĩŅĐŊĐĩŌŖ ŅŌŖĐ° ĐēĶŠĐšĐģĶĐŊĐĩŅĐĩ",
        "add_item_desc": "âī¸ ĐĐģĐĩĐŧĐĩĐŊŅĐŊĐĩ ĐēĐĩŅŅĐĩĐŗĐĩĐˇ",
        "remove_item_desc": "âī¸ ĐĐģĐĩĐŧĐĩĐŊŅĐŊĐĩ ĐēĐ°ĐšŅĐ°ŅŅĐŗŅĐˇ",
        "back_btn": "đ ĐŅŅĐēĐ°",
        "close_btn": "đģ Đ¯ĐąŅ",
        "add_item_btn": "â ĐĐģĐĩĐŧĐĩĐŊŅĐŊĐĩ ĐēĐĩŅŅŌ¯",
        "remove_item_btn": "â ĐĐģĐĩĐŧĐĩĐŊŅĐŊĐĩ ĐēĐ°ĐšŅĐ°ŅŅ",
        "show_hidden": "đ¸ ĐĶŠĐšĐģĶĐŊĐĩŅĐŊĐĩ ĐēŌ¯ŅŅĶŅĐĩŅĐŗĶ",
        "hide_value": "đ ĐĶŠĐšĐģĶĐŊĐĩŅĐŊĐĩ ŅŅĐĩŅĐĩŅĐŗĶ",
        "builtin": "đ° Đ¯ŅĐ°ĐģĐŗĐ°ĐŊ",
        "external": "đ¸ ĐĄŅŅŅĐēŅ",
        "libraries": "đĻ ĐĶĐąĐˇĶĐģĶŅ",
    }

    _row_size = 3
    _num_rows = 5

    @staticmethod
    def prep_value(value: typing.Any) -> typing.Any:
        if isinstance(value, str):
            return f"</b><code>{utils.escape_html(value.strip())}</code><b>"

        if isinstance(value, list) and value:
            return (
                "</b><code>[</code>\n    "
                + "\n    ".join(
                    [f"<code>{utils.escape_html(str(item))}</code>" for item in value]
                )
                + "\n<code>]</code><b>"
            )

        return f"</b><code>{utils.escape_html(value)}</code><b>"

    def hide_value(self, value: typing.Any) -> str:
        if isinstance(value, list) and value:
            return self.prep_value(["*" * len(str(i)) for i in value])

        return self.prep_value("*" * len(str(value)))

    def _get_value(self, mod: str, option: str) -> str:
        return (
            self.prep_value(self.lookup(mod).config[option])
            if (
                not self.lookup(mod).config._config[option].validator
                or self.lookup(mod).config._config[option].validator.internal_id
                != "Hidden"
            )
            else self.hide_value(self.lookup(mod).config[option])
        )

    async def inline__set_config(
        self,
        call: InlineCall,
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            self.lookup(mod).config[option] = query
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self._get_value(mod, option),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    async def inline__reset_default(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        mod_instance = self.lookup(mod)
        mod_instance.config[option] = mod_instance.config.getdef(option)

        await call.edit(
            self.strings(
                "option_reset" if isinstance(obj_type, bool) else "option_reset_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self._get_value(mod, option),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
        )

    async def inline__set_bool(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        value: bool,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            self.lookup(mod).config[option] = value
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        validator = self.lookup(mod).config._config[option].validator
        doc = utils.escape_html(
            next(
                (
                    validator.doc[lang]
                    for lang in self._db.get(translations.__name__, "lang", "en").split(
                        " "
                    )
                    if lang in validator.doc
                ),
                validator.doc["en"],
            )
        )

        await call.edit(
            self.strings(
                "configuring_option"
                if isinstance(obj_type, bool)
                else "configuring_option_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                utils.escape_html(self.lookup(mod).config.getdoc(option)),
                self.prep_value(self.lookup(mod).config.getdef(option)),
                (
                    self.prep_value(self.lookup(mod).config[option])
                    if not validator or validator.internal_id != "Hidden"
                    else self.hide_value(self.lookup(mod).config[option])
                ),
                (
                    self.strings("typehint").format(
                        doc,
                        eng_art="n" if doc.lower().startswith(tuple("euioay")) else "",
                    )
                    if doc
                    else ""
                ),
            ),
            reply_markup=self._generate_bool_markup(mod, option, obj_type),
        )

        await call.answer("â")

    def _generate_bool_markup(
        self,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        return [
            [
                *(
                    [
                        {
                            "text": f"â {self.strings('set')} `False`",
                            "callback": self.inline__set_bool,
                            "args": (mod, option, False),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    else [
                        {
                            "text": f"â {self.strings('set')} `True`",
                            "callback": self.inline__set_bool,
                            "args": (mod, option, True),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                )
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    async def inline__add_item(
        self,
        call: InlineCall,
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            with contextlib.suppress(Exception):
                query = ast.literal_eval(query)

            if isinstance(query, (set, tuple)):
                query = list(query)

            if not isinstance(query, list):
                query = [query]

            self.lookup(mod).config[option] = self.lookup(mod).config[option] + query
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self._get_value(mod, option),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    async def inline__remove_item(
        self,
        call: InlineCall,
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            with contextlib.suppress(Exception):
                query = ast.literal_eval(query)

            if isinstance(query, (set, tuple)):
                query = list(query)

            if not isinstance(query, list):
                query = [query]

            query = list(map(str, query))

            old_config_len = len(self.lookup(mod).config[option])

            self.lookup(mod).config[option] = [
                i for i in self.lookup(mod).config[option] if str(i) not in query
            ]

            if old_config_len == len(self.lookup(mod).config[option]):
                raise loader.validators.ValidationError(
                    f"Nothing from passed value ({self.prep_value(query)}) is not in"
                    " target list"
                )
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self._get_value(mod, option),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    def _generate_series_markup(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        return [
            [
                {
                    "text": self.strings("enter_value_btn"),
                    "input": self.strings("enter_value_desc"),
                    "handler": self.inline__set_config,
                    "args": (mod, option, call.inline_message_id),
                    "kwargs": {"obj_type": obj_type},
                }
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("remove_item_btn"),
                            "input": self.strings("remove_item_desc"),
                            "handler": self.inline__remove_item,
                            "args": (mod, option, call.inline_message_id),
                            "kwargs": {"obj_type": obj_type},
                        },
                        {
                            "text": self.strings("add_item_btn"),
                            "input": self.strings("add_item_desc"),
                            "handler": self.inline__add_item,
                            "args": (mod, option, call.inline_message_id),
                            "kwargs": {"obj_type": obj_type},
                        },
                    ]
                    if self.lookup(mod).config[option]
                    else []
                ),
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    async def _choice_set_value(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        value: bool,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            self.lookup(mod).config[option] = value
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self._get_value(mod, option),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
        )

        await call.answer("â")

    async def _multi_choice_set_value(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        value: bool,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            if value in self.lookup(mod).config._config[option].value:
                self.lookup(mod).config._config[option].value.remove(value)
            else:
                self.lookup(mod).config._config[option].value += [value]

            self.lookup(mod).config.reload()
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await self.inline__configure_option(call, mod, option, False, obj_type)
        await call.answer("â")

    def _generate_choice_markup(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        possible_values = list(
            self.lookup(mod)
            .config._config[option]
            .validator.validate.keywords["possible_values"]
        )
        return [
            [
                {
                    "text": self.strings("enter_value_btn"),
                    "input": self.strings("enter_value_desc"),
                    "handler": self.inline__set_config,
                    "args": (mod, option, call.inline_message_id),
                    "kwargs": {"obj_type": obj_type},
                }
            ],
            *utils.chunks(
                [
                    {
                        "text": (
                            f"{'âī¸' if self.lookup(mod).config[option] == value else 'đ'} "
                            f"{value if len(str(value)) < 20 else str(value)[:20]}"
                        ),
                        "callback": self._choice_set_value,
                        "args": (mod, option, value, obj_type),
                    }
                    for value in possible_values
                ],
                2,
            )[
                : (
                    6
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else 7
                )
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    def _generate_multi_choice_markup(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        possible_values = list(
            self.lookup(mod)
            .config._config[option]
            .validator.validate.keywords["possible_values"]
        )
        return [
            [
                {
                    "text": self.strings("enter_value_btn"),
                    "input": self.strings("enter_value_desc"),
                    "handler": self.inline__set_config,
                    "args": (mod, option, call.inline_message_id),
                    "kwargs": {"obj_type": obj_type},
                }
            ],
            *utils.chunks(
                [
                    {
                        "text": (
                            f"{'âī¸' if value in self.lookup(mod).config[option] else 'âģī¸'} "
                            f"{value if len(str(value)) < 20 else str(value)[:20]}"
                        ),
                        "callback": self._multi_choice_set_value,
                        "args": (mod, option, value, obj_type),
                    }
                    for value in possible_values
                ],
                2,
            )[
                : (
                    6
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else 7
                )
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    async def inline__configure_option(
        self,
        call: InlineCall,
        mod: str,
        config_opt: str,
        force_hidden: bool = False,
        obj_type: typing.Union[bool, str] = False,
    ):
        module = self.lookup(mod)
        args = [
            utils.escape_html(config_opt),
            utils.escape_html(mod),
            utils.escape_html(module.config.getdoc(config_opt)),
            self.prep_value(module.config.getdef(config_opt)),
            (
                self.prep_value(module.config[config_opt])
                if not module.config._config[config_opt].validator
                or module.config._config[config_opt].validator.internal_id != "Hidden"
                or force_hidden
                else self.hide_value(module.config[config_opt])
            ),
        ]

        if (
            module.config._config[config_opt].validator
            and module.config._config[config_opt].validator.internal_id == "Hidden"
        ):
            additonal_button_row = (
                [
                    [
                        {
                            "text": self.strings("hide_value"),
                            "callback": self.inline__configure_option,
                            "args": (mod, config_opt, False),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                ]
                if force_hidden
                else [
                    [
                        {
                            "text": self.strings("show_hidden"),
                            "callback": self.inline__configure_option,
                            "args": (mod, config_opt, True),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                ]
            )
        else:
            additonal_button_row = []

        try:
            validator = module.config._config[config_opt].validator
            doc = utils.escape_html(
                next(
                    (
                        validator.doc[lang]
                        for lang in self._db.get(
                            translations.__name__, "lang", "en"
                        ).split(" ")
                        if lang in validator.doc
                    ),
                    validator.doc["en"],
                )
            )
        except Exception:
            doc = None
            validator = None
            args += [""]
        else:
            args += [
                self.strings("typehint").format(
                    doc,
                    eng_art="n" if doc.lower().startswith(tuple("euioay")) else "",
                )
            ]
            if validator.internal_id == "Boolean":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_bool_markup(mod, config_opt, obj_type),
                )
                return

            if validator.internal_id == "Series":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_series_markup(call, mod, config_opt, obj_type),
                )
                return

            if validator.internal_id == "Choice":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_choice_markup(call, mod, config_opt, obj_type),
                )
                return

            if validator.internal_id == "MultiChoice":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_multi_choice_markup(
                        call, mod, config_opt, obj_type
                    ),
                )
                return

        await call.edit(
            self.strings(
                "configuring_option"
                if isinstance(obj_type, bool)
                else "configuring_option_lib"
            ).format(*args),
            reply_markup=additonal_button_row
            + [
                [
                    {
                        "text": self.strings("enter_value_btn"),
                        "input": self.strings("enter_value_desc"),
                        "handler": self.inline__set_config,
                        "args": (mod, config_opt, call.inline_message_id),
                        "kwargs": {"obj_type": obj_type},
                    }
                ],
                [
                    {
                        "text": self.strings("set_default_btn"),
                        "callback": self.inline__reset_default,
                        "args": (mod, config_opt),
                        "kwargs": {"obj_type": obj_type},
                    }
                ],
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ],
            ],
        )

    async def inline__configure(
        self,
        call: InlineCall,
        mod: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        btns = [
            {
                "text": param,
                "callback": self.inline__configure_option,
                "args": (mod, param),
                "kwargs": {"obj_type": obj_type},
            }
            for param in self.lookup(mod).config
        ]

        await call.edit(
            self.strings(
                "configuring_mod" if isinstance(obj_type, bool) else "configuring_lib"
            ).format(
                utils.escape_html(mod),
                "\n".join(
                    [
                        "âĢī¸ <code>{}</code>: <b>{}</b>".format(
                            utils.escape_html(key),
                            self._get_value(mod, key),
                        )
                        for key in self.lookup(mod).config
                    ]
                ),
            ),
            reply_markup=list(utils.chunks(btns, 2))
            + [
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__global_config,
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
        )

    async def inline__choose_category(self, call: typing.Union[Message, InlineCall]):
        await utils.answer(
            call,
            self.strings("choose_core"),
            reply_markup=[
                [
                    {
                        "text": self.strings("builtin"),
                        "callback": self.inline__global_config,
                        "kwargs": {"obj_type": True},
                    },
                    {
                        "text": self.strings("external"),
                        "callback": self.inline__global_config,
                    },
                ],
                *(
                    [
                        [
                            {
                                "text": self.strings("libraries"),
                                "callback": self.inline__global_config,
                                "kwargs": {"obj_type": "library"},
                            }
                        ]
                    ]
                    if self.allmodules.libraries
                    and any(hasattr(lib, "config") for lib in self.allmodules.libraries)
                    else []
                ),
                [{"text": self.strings("close_btn"), "action": "close"}],
            ],
        )

    async def inline__global_config(
        self,
        call: InlineCall,
        page: int = 0,
        obj_type: typing.Union[bool, str] = False,
    ):
        if isinstance(obj_type, bool):
            to_config = [
                mod.strings("name")
                for mod in self.allmodules.modules
                if hasattr(mod, "config")
                and callable(mod.strings)
                and (mod.__origin__.startswith("<core") or not obj_type)
                and (not mod.__origin__.startswith("<core") or obj_type)
            ]
        else:
            to_config = [
                lib.name for lib in self.allmodules.libraries if hasattr(lib, "config")
            ]

        to_config.sort()

        kb = []
        for mod_row in utils.chunks(
            to_config[
                page
                * self._num_rows
                * self._row_size : (page + 1)
                * self._num_rows
                * self._row_size
            ],
            3,
        ):
            row = [
                {
                    "text": btn,
                    "callback": self.inline__configure,
                    "args": (btn,),
                    "kwargs": {"obj_type": obj_type},
                }
                for btn in mod_row
            ]
            kb += [row]

        if len(to_config) > self._num_rows * self._row_size:
            kb += self.inline.build_pagination(
                callback=functools.partial(
                    self.inline__global_config, obj_type=obj_type
                ),
                total_pages=ceil(len(to_config) / (self._num_rows * self._row_size)),
                current_page=page + 1,
            )

        kb += [
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__choose_category,
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ]
        ]

        await call.edit(
            self.strings(
                "configure" if isinstance(obj_type, bool) else "configure_lib"
            ),
            reply_markup=kb,
        )

    @loader.command(
        ru_doc="ĐĐ°ŅŅŅĐžĐ¸ŅŅ ĐŧĐžĐ´ŅĐģĐ¸",
        fr_doc="Configurer les modules",
        it_doc="Configura i moduli",
        de_doc="Konfiguriere Module",
        tr_doc="ModÃŧlleri yapÄąlandÄąr",
        uz_doc="Modullarni sozlash",
        es_doc="Configurar mÃŗdulos",
        kk_doc="ĐĐžĐ´ŅĐģŅĐ´ĐĩŅĐ´Ņ ĐēĐžĐŊŅĐ¸ĐŗŅŅĐ°ŅĐ¸ŅĐģĐ°Ņ",
        alias="cfg",
    )
    async def configcmd(self, message: Message):
        """Configure modules"""
        args = utils.get_args_raw(message)
        if self.lookup(args) and hasattr(self.lookup(args), "config"):
            form = await self.inline.form("đ", message, silent=True)
            mod = self.lookup(args)
            if isinstance(mod, loader.Library):
                type_ = "library"
            else:
                type_ = mod.__origin__.startswith("<core")

            await self.inline__configure(form, args, obj_type=type_)
            return

        await self.inline__choose_category(message)

    @loader.command(
        ru_doc=(
            "<ĐŧĐžĐ´ŅĐģŅ> <ĐŊĐ°ŅŅŅĐžĐšĐēĐ°> <ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ> - ŅŅŅĐ°ĐŊĐžĐ˛Đ¸ŅŅ ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ ĐēĐžĐŊŅĐ¸ĐŗĐ° Đ´ĐģŅ ĐŧĐžĐ´ŅĐģŅ"
        ),
        fr_doc=(
            "<module> <paramÃ¨tre> <valeur> - dÃŠfinir la valeur de configuration pour le"
            " module"
        ),
        it_doc=(
            "<modulo> <impostazione> <valore> - imposta il valore della configurazione"
            " per il modulo"
        ),
        de_doc=(
            "<Modul> <Einstellung> <Wert> - Setze den Wert der Konfiguration fÃŧr das"
            " Modul"
        ),
        tr_doc="<modÃŧl> <ayar> <deÄer> - ModÃŧl iÃ§in yapÄąlandÄąrma deÄerini ayarla",
        uz_doc="<modul> <sozlash> <qiymat> - modul uchun sozlash qiymatini o'rnatish",
        es_doc=(
            "<mÃŗdulo> <configuraciÃŗn> <valor> - Establecer el valor de configuraciÃŗn"
        ),
        kk_doc=(
            "<ĐŧĐžĐ´ŅĐģŅ> <ĐŊĐ°ŅŅŅĐžĐšĐēĐ°> <ĐˇĐŊĐ°ŅĐĩĐŊĐ¸Đĩ> - ĐŧĐžĐ´ŅĐģŅ Ō¯ŅŅĐŊ ĐēĐžĐŊŅĐ¸ĐŗŅŅĐ°ŅĐ¸Ņ ĐŧĶĐŊŅĐŊ ĐžŅĐŊĐ°ŅŅ"
        ),
        alias="setcfg",
    )
    async def fconfig(self, message: Message):
        """<module_name> <property_name> <config_value> - set the config value for the module"""
        args = utils.get_args_raw(message).split(maxsplit=2)

        if len(args) < 3:
            await utils.answer(message, self.strings("args"))
            return

        mod, option, value = args

        instance = self.lookup(mod)
        if not instance:
            await utils.answer(message, self.strings("no_mod"))
            return

        if option not in instance.config:
            await utils.answer(message, self.strings("no_option"))
            return

        instance.config[option] = value
        await utils.answer(
            message,
            self.strings(
                "option_saved"
                if isinstance(instance, loader.Module)
                else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self._get_value(mod, option),
            ),
        )

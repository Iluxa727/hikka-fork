# ÂŠī¸ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# đ https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# đ https://www.gnu.org/licenses/agpl-3.0.html

import git
from hikkatl.tl.types import Message
from hikkatl.utils import get_display_name

from .. import loader, utils, version
from ..inline.types import InlineQuery


@loader.tds
class HikkaInfoMod(loader.Module):
    """Show userbot info"""

    strings = {
        "name": "HikkaInfo",
        "owner": "Owner",
        "version": "Version",
        "build": "Build",
        "prefix": "Prefix",
        "uptime": "Uptime",
        "branch": "Branch",
        "cpu_usage": "CPU usage",
        "ram_usage": "RAM usage",
        "send_info": "Send userbot info",
        "description": "âš This will not compromise any sensitive info",
        "up-to-date": (
            "<emoji document_id=5370699111492229743>đ</emoji> <b>Up-to-date</b>"
        ),
        "update_required": (
            "<emoji document_id=5424728541650494040>đ</emoji> <b>Update required"
            "</b> <code>.update</code>"
        ),
        "setinfo_no_args": (
            "<emoji document_id=5370881342659631698>đĸ</emoji> <b>You need to specify"
            " text to change info to</b>"
        ),
        "setinfo_success": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>Info changed"
            " successfully</b>"
        ),
        "_cfg_cst_msg": (
            "Custom message for info. May contain {me}, {version}, {build}, {prefix},"
            " {platform}, {upd}, {uptime}, {cpu_usage}, {ram_usage}, {branch} keywords"
        ),
        "_cfg_cst_btn": "Custom button for info. Leave empty to remove button",
        "_cfg_banner": "URL to image banner",
        "desc": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Userbot â what is"
            " it?</b>\n\n<emoji document_id=5472238129849048175>đ</emoji> A userbot"
            " refers to a <b>third-party program</b> that interacts with the Telegram"
            " API to perform <b>automated tasks on behalf of a user</b>. These userbots"
            " can be used to automate various tasks such as <b>sending messages,"
            " joining channels, downloading media, and much more</b>.\n\n<emoji"
            " document_id=5474667187258006816>đ</emoji> Userbots are different from"
            " regular Telegram bots as <b>they run on the user's account</b> rather"
            " than a bot account. This means that userbots can access more features and"
            " have greater flexibility in terms of the actions they can"
            " perform.\n\n<emoji document_id=5472267631979405211>đĢ</emoji> However, it"
            " is important to note that <b>userbots are not officially supported by"
            " Telegram</b> and their use may violate the platform's terms of service."
            " As such, <b>users should exercise caution when using userbots</b> and"
            " ensure that they are not being used for malicious purposes.\n\n"
        ),
    }

    strings_ru = {
        "owner": "ĐĐģĐ°Đ´ĐĩĐģĐĩŅ",
        "version": "ĐĐĩŅŅĐ¸Ņ",
        "build": "ĐĄĐąĐžŅĐēĐ°",
        "prefix": "ĐŅĐĩŅĐ¸ĐēŅ",
        "uptime": "ĐĐŋŅĐ°ĐšĐŧ",
        "branch": "ĐĐĩŅĐēĐ°",
        "cpu_usage": "ĐŅĐŋĐžĐģŅĐˇĐžĐ˛Đ°ĐŊĐ¸Đĩ CPU",
        "ram_usage": "ĐŅĐŋĐžĐģŅĐˇĐžĐ˛Đ°ĐŊĐ¸Đĩ RAM",
        "send_info": "ĐŅĐŋŅĐ°Đ˛Đ¸ŅŅ Đ¸ĐŊŅĐžŅĐŧĐ°ŅĐ¸Ņ Đž ŅĐˇĐĩŅĐąĐžŅĐĩ",
        "description": "âš Đ­ŅĐž ĐŊĐĩ ŅĐ°ŅĐēŅĐžĐĩŅ ĐŊĐ¸ĐēĐ°ĐēĐžĐš ĐģĐ¸ŅĐŊĐžĐš Đ¸ĐŊŅĐžŅĐŧĐ°ŅĐ¸Đ¸",
        "_ihandle_doc_info": "ĐŅĐŋŅĐ°Đ˛Đ¸ŅŅ Đ¸ĐŊŅĐžŅĐŧĐ°ŅĐ¸Ņ Đž ŅĐˇĐĩŅĐąĐžŅĐĩ",
        "up-to-date": (
            "<emoji document_id=5370699111492229743>đ</emoji> <b>ĐĐēŅŅĐ°ĐģŅĐŊĐ°Ņ Đ˛ĐĩŅŅĐ¸Ņ</b>"
        ),
        "update_required": (
            "<emoji document_id=5424728541650494040>đ</emoji> <b>ĐĸŅĐĩĐąŅĐĩŅŅŅ ĐžĐąĐŊĐžĐ˛ĐģĐĩĐŊĐ¸Đĩ"
            "</b> <code>.update</code>"
        ),
        "_cfg_cst_msg": (
            "ĐĐ°ŅŅĐžĐŧĐŊŅĐš ŅĐĩĐēŅŅ ŅĐžĐžĐąŅĐĩĐŊĐ¸Ņ Đ˛ info. ĐĐžĐļĐĩŅ ŅĐžĐ´ĐĩŅĐļĐ°ŅŅ ĐēĐģŅŅĐĩĐ˛ŅĐĩ ŅĐģĐžĐ˛Đ° {me},"
            " {version}, {build}, {prefix}, {platform}, {upd}, {uptime}, {cpu_usage},"
            " {ram_usage}, {branch}"
        ),
        "_cfg_cst_btn": (
            "ĐĐ°ŅŅĐžĐŧĐŊĐ°Ņ ĐēĐŊĐžĐŋĐēĐ° Đ˛ ŅĐžĐžĐąŅĐĩĐŊĐ¸Đ¸ Đ˛ info. ĐŅŅĐ°Đ˛Ņ ĐŋŅŅŅŅĐŧ, ŅŅĐžĐąŅ ŅĐąŅĐ°ŅŅ ĐēĐŊĐžĐŋĐēŅ"
        ),
        "_cfg_banner": "ĐĄŅŅĐģĐēĐ° ĐŊĐ° ĐąĐ°ĐŊĐŊĐĩŅ-ĐēĐ°ŅŅĐ¸ĐŊĐēŅ",
        "setinfo_no_args": (
            "<emoji document_id=5370881342659631698>đĸ</emoji> <b>ĐĸĐĩĐąĐĩ ĐŊŅĐļĐŊĐž ŅĐēĐ°ĐˇĐ°ŅŅ"
            " ŅĐĩĐēŅŅ Đ´ĐģŅ ĐēĐ°ŅŅĐžĐŧĐŊĐžĐŗĐž Đ¸ĐŊŅĐž</b>"
        ),
        "setinfo_success": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>ĐĸĐĩĐēŅŅ Đ¸ĐŊŅĐž ŅŅĐŋĐĩŅĐŊĐž"
            " Đ¸ĐˇĐŧĐĩĐŊĐĩĐŊ</b>"
        ),
        "desc": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Đ§ŅĐž ŅĐ°ĐēĐžĐĩ"
            " Userbot?</b>\n\n<emoji document_id=5472238129849048175>đ</emoji> Userbot"
            " - ŅŅĐž <b>ŅŅĐžŅĐžĐŊĐŊŅŅ ĐŋŅĐžĐŗŅĐ°ĐŧĐŧĐ°</b>, ĐēĐžŅĐžŅĐ°Ņ Đ˛ĐˇĐ°Đ¸ĐŧĐžĐ´ĐĩĐšŅŅĐ˛ŅĐĩŅ Ņ Telegram API"
            " Đ´ĐģŅ Đ˛ŅĐŋĐžĐģĐŊĐĩĐŊĐ¸Ņ <b>Đ°Đ˛ŅĐžĐŧĐ°ŅĐ¸ĐˇĐ¸ŅĐžĐ˛Đ°ĐŊĐŊŅŅ ĐˇĐ°Đ´Đ°Ņ ĐžŅ Đ¸ĐŧĐĩĐŊĐ¸ ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ</b>."
            " ĐŽĐˇĐĩŅĐąĐžŅŅ ĐŧĐžĐŗŅŅ Đ¸ŅĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅŅŅŅ Đ´ĐģŅ Đ°Đ˛ŅĐžĐŧĐ°ŅĐ¸ĐˇĐ°ŅĐ¸Đ¸ ŅĐ°ĐˇĐģĐ¸ŅĐŊŅŅ ĐˇĐ°Đ´Đ°Ņ, ŅĐ°ĐēĐ¸Ņ"
            " ĐēĐ°Đē <b>ĐžŅĐŋŅĐ°Đ˛ĐēĐ° ŅĐžĐžĐąŅĐĩĐŊĐ¸Đš, ĐŋŅĐ¸ŅĐžĐĩĐ´Đ¸ĐŊĐĩĐŊĐ¸Đĩ Đē ĐēĐ°ĐŊĐ°ĐģĐ°Đŧ, ĐˇĐ°ĐŗŅŅĐˇĐēĐ° ĐŧĐĩĐ´Đ¸Đ°ŅĐ°ĐšĐģĐžĐ˛"
            " Đ¸ ĐŧĐŊĐžĐŗĐžĐĩ Đ´ŅŅĐŗĐžĐĩ</b>.\n\n<emoji document_id=5474667187258006816>đ</emoji>"
            " ĐŽĐˇĐĩŅĐąĐžŅŅ ĐžŅĐģĐ¸ŅĐ°ŅŅŅŅ ĐžŅ ĐžĐąŅŅĐŊŅŅ ĐąĐžŅĐžĐ˛ Đ˛ Telegram ŅĐĩĐŧ, ŅŅĐž <b>ĐžĐŊĐ¸ ŅĐ°ĐąĐžŅĐ°ŅŅ"
            " ĐŊĐ° Đ°ĐēĐēĐ°ŅĐŊŅĐĩ ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ</b>, Đ° ĐŊĐĩ ĐŊĐ° ĐąĐžŅ-Đ°ĐēĐēĐ°ŅĐŊŅĐĩ. Đ­ŅĐž ĐžĐˇĐŊĐ°ŅĐ°ĐĩŅ, ŅŅĐž ĐžĐŊĐ¸"
            " ĐŧĐžĐŗŅŅ Đ¸ĐŧĐĩŅŅ Đ´ĐžŅŅŅĐŋ Đē ĐąĐžĐģŅŅĐĩĐŧŅ ĐēĐžĐģĐ¸ŅĐĩŅŅĐ˛Ņ ŅŅĐŊĐēŅĐ¸Đš Đ¸ ĐžĐąĐģĐ°Đ´Đ°ŅŅ ĐąĐžĐģŅŅĐĩĐš"
            " ĐŗĐ¸ĐąĐēĐžŅŅŅŅ Đ˛ ĐŋĐģĐ°ĐŊĐĩ Đ˛ŅĐŋĐžĐģĐŊĐĩĐŊĐ¸Ņ Đ´ĐĩĐšŅŅĐ˛Đ¸Đš.\n\n<emoji"
            " document_id=5472267631979405211>đĢ</emoji> ĐĐ´ĐŊĐ°ĐēĐž Đ˛Đ°ĐļĐŊĐž ĐžŅĐŧĐĩŅĐ¸ŅŅ, ŅŅĐž"
            " <b>ŅĐˇĐĩŅĐąĐžŅŅ ĐžŅĐ¸ŅĐ¸Đ°ĐģŅĐŊĐž ĐŊĐĩ ĐŋĐžĐ´Đ´ĐĩŅĐļĐ¸Đ˛Đ°ŅŅŅŅ Telegram</b> Đ¸ Đ¸Ņ Đ¸ŅĐŋĐžĐģŅĐˇĐžĐ˛Đ°ĐŊĐ¸Đĩ"
            " ĐŧĐžĐļĐĩŅ ĐŊĐ°ŅŅŅĐ°ŅŅ ŅŅĐģĐžĐ˛Đ¸Ņ Đ¸ŅĐŋĐžĐģŅĐˇĐžĐ˛Đ°ĐŊĐ¸Ņ ĐŋĐģĐ°ŅŅĐžŅĐŧŅ. ĐĐžŅŅĐžĐŧŅ <b>ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģĐ¸"
            " Đ´ĐžĐģĐļĐŊŅ ĐąŅŅŅ ĐžŅŅĐžŅĐžĐļĐŊŅ ĐŋŅĐ¸ Đ¸Ņ Đ¸ŅĐŋĐžĐģŅĐˇĐžĐ˛Đ°ĐŊĐ¸Đ¸</b> Đ¸ ŅĐąĐĩĐ´Đ¸ŅŅŅŅ, ŅŅĐž ĐŊĐ° Đ¸Ņ"
            " Đ°ĐēĐēĐ°ŅĐŊŅĐĩ ĐŊĐĩ Đ˛ŅĐŋĐžĐģĐŊŅĐĩŅŅŅ Đ˛ŅĐĩĐ´ĐžĐŊĐžŅĐŊŅĐš ĐēĐžĐ´.\n\n"
        ),
    }

    strings_fr = {
        "owner": "PropriÃŠtaire",
        "version": "Version",
        "build": "Construire",
        "prefix": "PrÃŠfixe",
        "uptime": "Uptime",
        "branch": "Branche",
        "cpu_usage": "Utilisation du CPU",
        "ram_usage": "Utilisation de la RAM",
        "send_info": "Envoyer des informations sur l'utilisateurbot",
        "description": "âš Cela ne rÃŠvÃŠlera aucune information personnelle",
        "_ihandle_doc_info": "Envoyer des informations sur l'utilisateurbot",
        "up-to-date": (
            "<emoji document_id=5370699111492229743>đ</emoji> <b>Version Ã  jour</b>"
        ),
        "update_required": (
            "<emoji document_id=5424728541650494040>đ</emoji> <b>Mise Ã  jour"
            " requise</b> <code>.update</code>"
        ),
        "_cfg_cst_msg": (
            "Texte de message personnalisÃŠ dans info. Peut contenir les mots clÃŠs"
            " {me}, {version}, {build}, {prefix}, {platform}, {upd}, {uptime},"
            " {cpu_usage}, {ram_usage}, {branch}"
        ),
        "_cfg_cst_btn": (
            "Bouton personnalisÃŠ dans le message dans info. Laissez vide pour supprimer"
            " le bouton"
        ),
        "_cfg_banner": "Lien vers la banniÃ¨re de l'image",
        "setinfo_no_args": (
            "<emoji document_id=5370881342659631698>đĸ</emoji> <b>Vous devez spÃŠcifier"
            " le texte pour l'info personnalisÃŠe</b>"
        ),
        "setinfo_success": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>L'info personnalisÃŠe"
            " a bien ÃŠtÃŠ modifiÃŠe</b>"
        ),
        "desc": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Qu'est-ce qu'un"
            " Userbot?</b>\n\n<emoji document_id=5472238129849048175>đ</emoji> Userbot"
            " est un <b>programme tiers</b> qui interagit avec l'API Telegram pour"
            " exÃŠcuter des <b>tÃĸches automatisÃŠes au nom de l'utilisateur</b>. Les"
            " userbots peuvent ÃĒtre utilisÃŠs pour automatiser diverses tÃĸches, telles"
            " que <b>l'envoi de messages, l'adhÃŠsion aux canaux, le tÃŠlÃŠchargement de"
            " fichiers multimÃŠdias et bien plus encore</b>.\n\n<emoji"
            " document_id=5474667187258006816>đ</emoji> Les userbots diffÃ¨rent des bots"
            " Telegram classiques dans le sens oÃš <b>ils fonctionnent sur le compte de"
            " l'utilisateur</b> et non sur un compte de bot. Cela signifie qu'ils"
            " peuvent avoir accÃ¨s Ã  plus de fonctions et ÃĒtre plus flexibles dans"
            " l'exÃŠcution de leurs actions.\n\n<emoji"
            " document_id=5472267631979405211>đĢ</emoji> Cependant, il est important de"
            " noter que <b>les userbots ne sont pas officiellement pris en charge par"
            " Telegram</b> et leur utilisation peut enfreindre les conditions"
            " d'utilisation de la plateforme. Par consÃŠquent, <b>les utilisateurs"
            " doivent faire preuve de prudence lors de leur utilisation</b> et"
            " s'assurer que le code malveillant n'est pas exÃŠcutÃŠ sur leur compte.\n\n"
        ),
    }

    strings_it = {
        "owner": "Proprietario",
        "version": "Versione",
        "build": "Build",
        "prefix": "Prefisso",
        "uptime": "Uptime",
        "branch": "Branch",
        "cpu_usage": "Uso CPU",
        "ram_usage": "Uso RAM",
        "send_info": "Invia info del bot",
        "description": "âš Questo non rivelera' alcuna informazione personale",
        "_ihandle_doc_info": "Invia info del bot",
        "up-to-date": (
            "<emoji document_id=5370699111492229743>đ</emoji> <b>Versione"
            " aggiornata</b>"
        ),
        "update_required": (
            "<emoji document_id=5424728541650494040>đ</emoji> <b>Aggiornamento"
            " richiesto</b> <code>.update</code>"
        ),
        "_cfg_cst_msg": (
            "Messaggio personalizzato per info. Puo' contenere {me}, {version},"
            " {build}, {prefix}, {platform}, {upd}, {uptime}, {cpu_usage}, {ram_usage},"
            " {branch} keywords"
        ),
        "_cfg_cst_btn": "Bottone personalizzato per info. Lascia vuoto per rimuovere",
        "_cfg_banner": "URL dell'immagine banner",
        "desc": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Che cos'Ã¨ un"
            " Userbot?</b>\n\n<emoji document_id=5472238129849048175>đ</emoji> Il"
            " Userbot Ã¨ un <b>programma esterno</b> che interagisce con l'API di"
            " Telegram per eseguire <b>compiti automatizzati</b> a nome dell'utente. I"
            " userbot possono essere utilizzati per automatizzare diversi compiti, come"
            " <b>invio di messaggi, iscrizione a canali, caricamento di file"
            " multimediali e molto altro ancora</b>.\n\n<emoji"
            " document_id=5474667187258006816>đ</emoji> I userbot differiscono dai bot"
            " di Telegram nel fatto che <b>funzionano con gli account utente</b> e non"
            " con quelli di bot. CiÃ˛ significa che possono avere accesso a piÃš"
            " funzionalitÃ  e una maggiore flessibilitÃ  nella loro esecuzione.\n\n<emoji"
            " document_id=5472267631979405211>đĢ</emoji> Tuttavia, Ã¨ importante notare"
            " che <b>i userbot non sono supportati ufficialmente da Telegram</b> e"
            " l'utilizzo di quest'ultimi puÃ˛ violare i termini di utilizzo della"
            " piattaforma. Pertanto, <b>gli utenti devono essere cautelosi quando li"
            " utilizzano e assicurarsi che sul loro account non venga eseguito codice"
            " malevolo</b>.\n\n"
        ),
    }

    strings_de = {
        "owner": "Besitzer",
        "version": "Version",
        "build": "Build",
        "prefix": "Prefix",
        "uptime": "Uptime",
        "branch": "Branch",
        "cpu_usage": "CPU Nutzung",
        "ram_usage": "RAM Nutzung",
        "send_info": "Botinfo senden",
        "description": "âš Dies enthÃŧllt keine persÃļnlichen Informationen",
        "_ihandle_doc_info": "Sende Botinfo",
        "up-to-date": "<emoji document_id=5370699111492229743>đ</emoji> <b>Aktuell</b>",
        "update_required": (
            "<emoji document_id=5424728541650494040>đ</emoji> <b>Update benÃļtigt"
            "</b> <code>.update</code>"
        ),
        "_cfg_cst_msg": (
            "Custom message for info. May contain {me}, {version}, {build}, {prefix},"
            " {platform}, {upd}, {uptime}, {cpu_usage}, {ram_usage}, {branch} keywords"
        ),
        "_cfg_cst_btn": "Custom button for info. Leave empty to remove button",
        "_cfg_banner": "URL to image banner",
        "setinfo_no_args": (
            "<emoji document_id=5370881342659631698>đĸ</emoji> <b>Bitte gib einen"
            " Text an, um die Info zu Ã¤ndern</b>"
        ),
        "setinfo_success": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>Info geÃ¤ndert</b>"
        ),
        "desc": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Was ist ein"
            " Userbot?</b>\n\n<emoji document_id=5472238129849048175>đ</emoji> Userbot"
            " ist ein <b>externe Programm</b>, welches mit der Telegram API"
            " kommuniziert, um <b>automatisierte Aufgaben</b> fÃŧr den Benutzer"
            " auszufÃŧhren. Userbots kÃļnnen benutzt werden, um verschiedene Aufgaben zu"
            " automatisieren, wie zum Beispiel <b>Nachrichten senden, KanÃ¤le beitreten,"
            " Medien hochladen und vieles mehr</b>.\n\n<emoji"
            " document_id=5474667187258006816>đ</emoji> Userbots unterscheiden sich von"
            " normalen Telegram Bots darin, dass <b>sie auf einem Benutzerkonto"
            " laufen</b> und nicht auf einem Botkonto. Das bedeutet, dass sie mehr"
            " Funktionen haben und mehr FlexibilitÃ¤t bei der AusfÃŧhrung von Aktionen"
            " haben.\n\n<emoji document_id=5472267631979405211>đĢ</emoji> Es ist jedoch"
            " wichtig zu beachten, dass <b>Userbots nicht offiziell von Telegram"
            " unterstÃŧtzt werden</b> und ihre Verwendung gegen die Nutzungsbedingungen"
            " von Telegram verstoÃen kann. Deshalb <b>mÃŧssen Benutzer vorsichtig sein,"
            " wenn sie Userbots benutzen</b> und sicherstellen, dass auf ihrem Konto"
            " kein schÃ¤dlicher Code ausgefÃŧhrt wird.\n\n"
        ),
    }

    strings_uz = {
        "owner": "Egasi",
        "version": "Versiya",
        "build": "Build",
        "prefix": "Prefix",
        "uptime": "Ishlash vaqti",
        "branch": "Vetkasi",
        "cpu_usage": "CPU foydalanish",
        "ram_usage": "RAM foydalanish",
        "send_info": "Bot haqida ma'lumot",
        "description": "âš Bu shaxsiy ma'lumot emas",
        "_ihandle_doc_info": "Bot haqida ma'lumot",
        "up-to-date": (
            "<emoji document_id=5370699111492229743>đ</emoji> <b>So'ngi versia</b>"
        ),
        "update_required": (
            "<emoji document_id=5424728541650494040>đ</emoji> <b>Yangilash"
            " kerak</b> <code>.update</code>"
        ),
        "_cfg_cst_msg": (
            "Xabar uchun shaxsiy xabar. {me}, {version}, {build}, {prefix}, {platform},"
            " {upd}, {uptime}, {cpu_usage}, {ram_usage}, {branch} kalit so'zlarni"
            " ishlatishingiz mumkin"
        ),
        "_cfg_cst_btn": (
            "Xabar uchun shaxsiy tugma. Tugmani o'chirish uchun bo'sh qoldiring"
        ),
        "_cfg_banner": "URL uchun rasmi",
        "setinfo_no_args": (
            "<emoji document_id=5370881342659631698>đĸ</emoji> <b>Ma'lumotni"
            " o'zgartirish uchun matn kiriting</b>"
        ),
        "setinfo_success": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>Ma'lumotlar"
            " o'zgartirildi</b>"
        ),
        "desc": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Userbot"
            " nima?</b>\n\n<emoji document_id=5472238129849048175>đ</emoji> Userbot -"
            " bu <b>tashqi dastur</b>, <b>foydalanuvchi tomonidan</b> ishlaydigan"
            " Telegram API bilan aloqa qilish uchun ishlatiladi. Userbotlarni"
            " <b>avtomatlashtirilgan vazifalarni bajarish</b> uchun ishlatish mumkin."
            " Userbotlar <b>habarlarni yuborish, kanallarga ulanish, media fayllarni"
            " yuklash va boshqa biror vazifa bajarish</b> uchun ishlatilishi"
            " mumkin.\n\n<emoji document_id=5474667187258006816>đ</emoji> Userbotlar"
            " Telegramda obyektiv bo'lgan botlardan farqli. Userbotlar"
            " <b>bot-hisobotlaridan</b> ishlaydi, <b>foydalanuvchi hisobotidan</b>"
            " ishlaydi. Bu shuni anglatadiki, userbotlar <b>Telegram platformasida"
            " ishlash</b> uchun kerakli funksiyalarga ega va ular <b>qanday vazifalarni"
            " bajarishni</b> xohlayotgan bo'lishi mumkin.\n\n<emoji"
            " document_id=5472267631979405211>đĢ</emoji> Lekin shuni unutmangki,"
            " <b>userbotlar Telegram tomonidan rasmiylashtirilmagan</b> va ularni"
            " ishlatish <b>Telegram shartlari bilan</b> bir-biriga mos kelmaydi."
            " Shuning uchun <b>foydalanuvchilar userbotlarni ishlatishda</b> qattiq"
            " bo'lishi lozim va <b>ularning hisobotlari</b> bo'lmaguncha biror zararli"
            " kod yuklamasini tekshirish kerak.\n\n"
        ),
    }

    strings_tr = {
        "owner": "Sahip",
        "version": "SÃŧrÃŧm",
        "build": "Derleme",
        "prefix": "Ãnek",
        "uptime": "Aktif SÃŧre",
        "branch": "Dal",
        "cpu_usage": "CPU KullanÄąmÄą",
        "ram_usage": "RAM KullanÄąmÄą",
        "send_info": "Bot hakkÄąnda bilgi",
        "description": "âšī¸ KiÅisel bilgileri tehlikeye atmaz",
        "_ihandle_doc_info": "Bot hakkÄąnda bilgi",
        "up-to-date": "<emoji document_id=5370699111492229743>đ</emoji> <b>GÃŧncel</b>",
        "update_required": (
            "<emoji document_id=5424728541650494040>đ</emoji> <b>GÃŧncelleme"
            " gerekli</b> <code>.update</code>"
        ),
        "_cfg_cst_msg": (
            "KiÅisel mesaj iÃ§in bilgi. {me}, {version}, {build}, {prefix}, {platform},"
            " {upd}, {uptime}, {cpu_usage}, {ram_usage}, {branch} anahtar kelimeleri"
            " kullanÄąlabilir"
        ),
        "_cfg_cst_btn": "KiÅisel tuÅ iÃ§in bilgi. TuÅu kaldÄąrmak iÃ§in boÅ bÄąrakÄąn",
        "_cfg_banner": "Resim iÃ§in URL",
        "setinfo_no_args": (
            "<emoji document_id=5370881342659631698>đĸ</emoji> <b>Bilgiyi deÄiÅtirmek"
            " iÃ§in herhangi bir metin girin</b>"
        ),
        "setinfo_success": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>Bilgiler"
            " deÄiÅtirildi</b>"
        ),
        "desc": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Neden"
            " Userbot?</b>\n\n<emoji document_id=5472238129849048175>đ</emoji> Userbot"
            " - <b>Telegram API ile</b> <b>KullanÄącÄą adÄąna</b> <b>otomatikleÅtirilmiÅ"
            " iÅlemleri</b> yÃŧrÃŧten bir <b>ÃŧÃ§ÃŧncÃŧ taraf programÄądÄąr</b>. Userbotlar,"
            " <b>mesaj gÃļnderme, kanallara katÄąlma, medya yÃŧkleme ve diÄer iÅlemleri"
            " otomatize etmek iÃ§in kullanÄąlabilecek</b> birÃ§ok iÅi otomatize etmenizi"
            " saÄlar.\n\n<emoji document_id=5474667187258006816>đ</emoji> Userbotlar,"
            " <b>normal Telegram botlarÄąndan farklÄą olarak</b>, <b>KullanÄącÄą hesabÄąnda"
            " Ã§alÄąÅÄąrlar</b>. Bu, <b>daha fazla iÅ yapmalarÄąna</b> ve <b>daha esnek"
            " olmalarÄąna</b> olanak verir.\n\n<emoji"
            " document_id=5472267631979405211>đĢ</emoji> Bununla birlikte, <b>Userbotlar"
            " Telegram tarafÄąndan resmi olarak desteklenmez</b> ve bunlarÄąn kullanÄąmÄą"
            " platformun kullanÄąm koÅullarÄąnÄą ihlal edebilir. KullanÄącÄąlar <b>bu"
            " nedenle UserbotlarÄąn kullanÄąmÄąnÄą dikkatli bir Åekilde yapmalÄądÄąr</b> ve"
            " kullanÄącÄą hesaplarÄąnda kÃļtÃŧ niyetli kodun Ã§alÄąÅtÄąrÄąlmadÄąÄÄąndan emin"
            " olmalÄądÄąrlar.\n\n"
        ),
    }

    strings_es = {
        "owner": "Propietario",
        "version": "VersiÃŗn",
        "build": "Construir",
        "prefix": "Prefijo",
        "uptime": "Tiempo de actividad",
        "branch": "Rama",
        "cpu_usage": "Uso de CPU",
        "ram_usage": "Uso de RAM",
        "send_info": "Enviar informaciÃŗn del bot",
        "description": "âšī¸ No exponga su informaciÃŗn personal",
        "_ihandle_doc_info": "InformaciÃŗn del bot",
        "up-to-date": (
            "<emoji document_id=5370699111492229743>đ</emoji> <b>Actualizado</b>"
        ),
        "update_required": (
            "<emoji document_id=5424728541650494040>đ</emoji> <b>ActualizaciÃŗn"
            " necesaria</b> <code>.update</code>"
        ),
        "_cfg_cst_msg": (
            "InformaciÃŗn del mensaje personalizado. Puede usar las palabras clave {me},"
            " {version}, {build}, {prefix}, {platform}, {upd}, {uptime}, {cpu_usage},"
            " {ram_usage}, {branch}"
        ),
        "_cfg_cst_btn": (
            "InformaciÃŗn del botÃŗn personalizado. Eliminar el botÃŗn deje en blanco"
        ),
        "_cfg_banner": "URL de la imagen",
        "setinfo_no_args": (
            "<emoji document_id=5370881342659631698>đĸ</emoji> <b>Para cambiar la"
            " informaciÃŗn, ingrese algÃēn texto</b>"
        ),
        "setinfo_success": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>InformaciÃŗn cambiada"
            " con ÃŠxito</b>"
        ),
        "desc": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>ÂŋQuÃŠ es un"
            " Userbot?</b>\n\n<emoji document_id=5472238129849048175>đ</emoji> Un"
            " Userbot es un <b>programa externo</b> que interactÃēa con la API de"
            " Telegram para realizar <b>tareas automatizadas en nombre del usuario</b>."
            " Los userbots pueden utilizarse para automatizar diversas tareas, como"
            " <b>envÃ­o de mensajes, unirse a canales, subir archivos multimedia y mucho"
            " mÃĄs</b>.\n\n<emoji document_id=5474667187258006816>đ</emoji> Los userbots"
            " se diferencian de los bots normales de Telegram en que <b>trabajan en la"
            " cuenta del usuario</b> en lugar de en una cuenta de bot. Esto significa"
            " que tienen acceso a mÃĄs funciones y son mÃĄs flexibles a la hora de"
            " realizar acciones.\n\n<emoji document_id=5472267631979405211>đĢ</emoji>"
            " Sin embargo, es importante seÃąalar que <b>los userbots no son oficiales y"
            " no son compatibles con Telegram</b> y su uso puede violar los tÃŠrminos de"
            " servicio de la plataforma. Por lo tanto, <b>los usuarios deben tener"
            " cuidado al usarlos</b> y asegurarse de que en su cuenta no se ejecute"
            " cÃŗdigo malicioso.\n\n"
        ),
    }

    strings_kk = {
        "owner": "ĶĐēŅĐŧŅŅ",
        "version": "ĐŌąŅŌĐ°ŅŅ",
        "build": "ŌŌąŅŅĐģŌĐ°ĐŊ",
        "prefix": "ĐĐ°ŅŅĐ°ŅŅŅ",
        "uptime": "ŌĐžŅŅĐģŌĐ°ĐŊ ĐēĐĩĐˇĐĩŌŖ",
        "branch": "ĐĶŠĐģŅĐŧŅ",
        "cpu_usage": "CPU ŌĐžĐģĐ´Đ°ĐŊŅĐŧŅ",
        "ram_usage": "RAM ŌĐžĐģĐ´Đ°ĐŊŅĐŧŅ",
        "send_info": "ĐĐžŅ ŅŅŅĐ°ĐģŅ Đ°ŌĐŋĐ°ŅĐ°Ņ",
        "description": "âšī¸ ĐĐĩĐēĐĩ ĐŧĶĐģŅĐŧĐĩŅŅĐĩŅŅŌŖŅĐˇĐ´Ņ ŌĐžŅŌĐ°Ņ",
        "_ihandle_doc_info": "ĐĐžŅ ŅŅŅĐ°ĐģŅ Đ°ŌĐŋĐ°ŅĐ°Ņ",
        "up-to-date": (
            "<emoji document_id=5370699111492229743>đ</emoji> <b>ĐĐ°ŌŖĐ°ŅŅŅĐģŌĐ°ĐŊ</b>"
        ),
        "update_required": (
            "<emoji document_id=5424728541650494040>đ</emoji> <b>ĐĐ°ŌŖĐ°ŅŅŅ"
            " ŅĐ°ĐģĐ°Đŋ ĐĩŅŅĐģĐĩĐ´Ņ</b> <code>.update</code>"
        ),
        "_cfg_cst_msg": (
            "ĐĐĩĐēĐĩ ŅĐ°ĐąĐ°ŅĐģĐ°ĐŧĐ° Ō¯ŅŅĐŊ Đ°ŌĐŋĐ°ŅĐ°Ņ. {me}, {version}, {build}, {prefix},"
            " {platform}, {upd}, {uptime}, {cpu_usage}, {ram_usage}, {branch} ĐēŅĐģŅ"
            " ŅĶŠĐˇĐ´ĐĩŅĐ´Ņ ŌĐžĐģĐ´Đ°ĐŊĐ° Đ°ĐģĐ°ŅŅĐˇ"
        ),
        "_cfg_cst_btn": "ĐĐĩĐēĐĩ ŅŌ¯ĐšĐŧĐĩ Ō¯ŅŅĐŊ Đ°ŌĐŋĐ°ŅĐ°Ņ. ĐĸŌ¯ĐšĐŧĐĩŅŅĐŊ ĐļĐžŅ Ō¯ŅŅĐŊ ĐąĐžŅ ŌĐ°ĐģĐ´ŅŅŅŌŖŅĐˇ",
        "_cfg_banner": "ĐĄŅŅĐĩŅ Ō¯ŅŅĐŊ URL",
        "setinfo_no_args": (
            "<emoji document_id=5370881342659631698>đĸ</emoji> <b>ĐŌĐŋĐ°ŅĐ°ŅŅŅ ĶŠĐˇĐŗĐĩŅŅŅ Ō¯ŅŅĐŊ"
            " ĐĩŅŅĐĩŌŖĐĩ ĐĩĐŊĐŗŅĐˇĐąĐĩŌŖŅĐˇ</b>"
        ),
        "setinfo_success": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>ĐŌĐŋĐ°ŅĐ°Ņ ŅĶŅŅŅ"
            " ĶŠĐˇĐŗĐĩŅŅŅĐģĐ´Ņ</b>"
        ),
        "desc": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>ĐĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅ ĐąĐžŅŅĐ°ŅĐ´Ņ"
            " ŌĐ°ĐŊĐ´Đ°Đš ĐąĐžĐģĐ°Đ´Ņ?</b>\n\n<emoji document_id=5472238129849048175>đ</emoji>"
            " ĐĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅ ĐąĐžŅŅĐ°Ņ - <b>ŅĐĩŅĐĩĐģ ĐŋŅĐžĐŗŅĐ°ĐŧĐŧĐ°</b>, ĐžĐģ Telegram API ĐŧĐĩĐŊ"
            " ŌĐžĐģĐ´Đ°ĐŊŅŅŅĐŊŅŌŖ Đ°ŅŅĐŧĐĩĐŊ ĐąĐ°ĐšĐģĐ°ĐŊŅŅĐ°Đ´Ņ ĐļĶĐŊĐĩ <b>Đ°Đ˛ŅĐžĐŧĐ°ŅŅĐ°ĐŊĐ´ŅŅŅĐģŌĐ°ĐŊ ĐļŌąĐŧŅŅŅĐ°ŅĐ´Ņ"
            " ĶŠŅĐēŅĐˇĐĩĐ´Ņ</b>. ĐĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅ ĐąĐžŅŅĐ°Ņ <b>ŅĐ°ĐąĐ°ŅĐģĐ°ĐŧĐ°ĐģĐ°ŅĐ´Ņ ĐļŅĐąĐĩŅŅ, ĐēĐ°ĐŊĐ°ĐģŌĐ°"
            " ŌĐžŅŅĐģŅ, ĐŧĐĩĐ´Đ¸Đ° ŅĐ°ĐšĐģĐ´Đ°ŅĐ´Ņ ĐļŌ¯ĐēŅĐĩŅ ĐļĶĐŊĐĩ ĐąĐ°ŅŌĐ° ŌĐ°ŅĐ°ŅŅŅŅŅĐģĐŧĐ°ŌĐ°ĐŊ ĐļŌąĐŧŅŅŅĐ°ŅĐ´Ņ"
            " ĐļĐ°ŅĐ°Ņ</b> Ō¯ŅŅĐŊ ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅĐģĐ°Đ´Ņ.\n\n<emoji"
            " document_id=5474667187258006816>đ</emoji> ĐĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅ ĐąĐžŅŅĐ°Ņ Telegram"
            " ĐąĐžŅŅĐ°ŅŅĐŊĐ°ĐŊ Đ°ĐšŅŅĐŧĐ°ĐģŅ, ŅĐĩĐąĐĩĐąŅ ĐžĐģĐ°Ņ <b>ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅĐŊŅŌŖ Đ°ĐēĐēĐ°ŅĐŊŅŅĐŧĐĩĐŊ ĐļŌąĐŧŅŅ"
            " ŅŅŅĐĩĐšĐ´Ņ</b>, ĐąĐžŅ-Đ°ĐēĐēĐ°ŅĐŊŅĐŋĐĩĐŊ ĐļŌąĐŧŅŅ ŅŅŅĐĩŅĐŗĐĩ ĐąĐĩŅŅĐģĐŧĐĩĐšĐ´Ņ. ĐŌąĐģ ĐžĐģĐ°ŅŌĐ°"
            " <b>ŌĐ°ŅŅŅŅŌĐ° ĐąĐžĐģĐ°ŅŅĐŊ ĐēĶŠĐŋ ĐēĶŠŅŅĐĩŅĐēŅŅŅĐĩŅĐŗĐĩ ĐļĶĐŊĐĩ ĐļŌąĐŧŅŅ ŅŅŅĐĩŅĐŗĐĩ ĐēĶŠĐŋ"
            " ŌŌąŅĐ°ĐģĐ´Đ°ŅŌĐ°</b> ĐąĐžĐģĐ°ŅŅĐŊ ĐļĐ°ŌŅŅ ŌŌąŅĐ°ĐģĐ´Đ°ŅĐ´Ņ ĐąĐĩŅĐĩĐ´Ņ.\n\n<emoji"
            " document_id=5472267631979405211>đĢ</emoji> ĐĐ´Đ°ĐŊ ŌĐžŅŅĐŧŅĐ°, <b>ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅ"
            " ĐąĐžŅŅĐ°ŅĐ´ŅŌŖ Telegram Ō¯ŅŅĐŊ ĐžŅĐ¸ŅĐ¸Đ°ĐģĐ´Ņ ŌĐžĐģĐ´Đ°Ņ ĐēĶŠŅŅĐĩŅŅŅ ĐļĐžŌ</b> ĐļĶĐŊĐĩ ĐžĐģĐ°ŅĐ´Ņ"
            " ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅ ĐžŅŅĐ°ĐģŅŌŅĐŊŅŌŖ ŌĐžĐģĐ´Đ°ĐŊŅ ŅĐ°ŅŅŅĐ°ŅŅĐŊ ĐąŌ¯ĐŗŅĐŊĐŗĐĩ Đ´ĐĩĐšŅĐŊ ĐąŌąĐˇŅŅ ĐŧŌ¯ĐŧĐēŅĐŊ."
            " ĐĐģĐ°ŅĐ´Ņ ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅ <b>ŌĐžĐģĐ´Đ°ĐŊŅŅŅĐģĐ°ŅŌĐ° ŌĐ°ŅŅŅĐ°ŅŅĐŊ ĐŊĶŅĐ¸ĐļĐĩĐģĐĩŅĐ´ŅŌŖ ĐąĐ°ŅĐģŅŌŅĐŊ"
            " ŌĐ°ŅĐ°ŅŌĐ°</b> ĐŧŌ¯ĐŧĐēŅĐŊĐ´ŅĐē ĐąĐĩŅĐĩĐ´Ņ.\n\n"
        ),
    }

    strings_tt = {
        "owner": "ĐĐ´Đ°ŅĶŅĐĩ",
        "version": "ĐĐĩŅŅĐ¸Ņ",
        "build": "ĐĐ¸ĐģĐ´",
        "prefix": "ĐŅĐĩŅĐ¸ĐēŅ",
        "uptime": "ĐĸĶŅŅĐ¸ĐąĐ¸ Đ˛Đ°ĐēŅŅŅ",
        "branch": "ĐĐ¸ŅĐĩĐģĐĩĐē",
        "cpu_usage": "CPU ŌŅĐĩĐģĐŧĐ°ŅŅ",
        "ram_usage": "RAM ŌŅĐĩĐģĐŧĐ°ŅŅ",
        "send_info": "ĐĐžŅ ŅŅŅŅĐŊĐ´Đ° ĐŧĶĐŗŅĐģŌ¯ĐŧĐ°ŅĐŊŅ ŌĐ¸ĐąĶŅŌ¯",
        "description": "âšī¸ Đ¨ĶŅŅĐ¸ ĐŧĶĐŗŅĐģŌ¯ĐŧĐ°ŅŅŌŖŅĐˇĐŊŅ ŅŅŅŅ",
        "_ihandle_doc_info": "ĐĐžŅ ŅŅŅŅĐŊĐ´Đ° ĐŧĶĐŗŅĐģŌ¯ĐŧĐ°Ņ",
        "up-to-date": (
            "<emoji document_id=5370699111492229743>đ</emoji> <b>Đ¯ŌŖĐ°ŅŅŅĐģĐŗĐ°ĐŊ</b>"
        ),
        "update_required": (
            "<emoji document_id=5424728541650494040>đ</emoji> <b>Đ¯ŌŖĐ°ŅŅŅĐģŅ"
            " ŅĐ°ĐģĶĐŋ Đ¸ŅĐĩĐģĶ</b><code>.update</code>"
        ),
        "_cfg_cst_msg": (
            "Đ¨ĶŅŅĐ¸ ŅĶĐąĶŅ ĐŧĶĐŗŅĐģŌ¯ĐŧĐ°ŅŅ. {me}, {version}, {build}, {prefix}, {platform},"
            " {upd}, {uptime}, {cpu_usage}, {ram_usage}, {branch} ĐēŌ¯ŅĐĩŅĐŧĶĐģĶŅĐĩĐŊ ŌĐ¸ĐąĶŅŌ¯"
            " ĐŧĶŠĐŧĐēĐ¸ĐŊ"
        ),
        "_cfg_cst_btn": "Đ¨ĶŅŅĐ¸ ŅĶŠĐšĐŧĶ ĐŧĶĐŗŅĐģŌ¯ĐŧĐ°ŅŅ. ĐĸĶŠĐšĐŧĶĐŊĐĩ ŅĐšĐŧĐ°ĐŗŅŅ, ĐąŅŅ ŌĐ¸ĐąĶŅŌ¯",
        "_cfg_banner": "ĐĄŌ¯ŅĶŅ URL-Ņ",
        "setinfo_no_args": (
            "<emoji document_id=5370881342659631698>đĸ</emoji> <b>ĐĶĐŗŅĐģŌ¯ĐŧĐ°ŅĐŊŅ"
            " Ō¯ĐˇĐŗĶŅŅŌ¯ ĶŠŅĐĩĐŊ, ĐŧĶĐŗŅĐģŌ¯ĐŧĐ°ŅĐŊŅ ĐēĐĩŅŅĐĩĐŗĐĩĐˇ</b>"
        ),
        "setinfo_success": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>ĐĶĐŗŅĐģŌ¯ĐŧĐ°Ņ"
            " ĐŧĶŠĐŧĐēĐ¸ĐŊ ĐąŅĐģĐ´Ņ</b>"
        ),
        "desc": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>ĐĐ°ŅŅĐ°"
            " Userbot?</b>\n\n<emoji document_id=5472238129849048175>đ</emoji> Userbot"
            " - ĐąŅ <b>ŅĐ°ĐšĐģĐ°ĐŧĐ° ĐŋŅĐžĐŗŅĐ°ĐŧĐŧĐ°</b>, ĐēĐ°ĐģĐ°ĐŊ <b>Telegram API</b> Đ¸ŅĐģĶĐŋ <b>ŅĐ¸ŅĐ°Đŋ"
            " ŅĐˇĐŧĐ°ŅŅ Đ¸ŅĐĩĐŧĐĩ</b> ĐąĐĩĐģĶĐŊ <b>Đ°Đ˛ŅĐžĐŧĐ°ŅĐ¸Đē ĶŠŅĶŅĐŗĶ</b> ĐŧĶŠĐŧĐēĐ¸ĐŊ. ĐŽĐˇĐĩŅĐąĐžŅĐģĐ°Ņ <b>ŅĐ°Ņ"
            " ŌĐ¸ĐąĶŅŌ¯, ĐēĐ°ĐŊĐ°ĐģĐŗĐ° ŌĐ¸ĐąĶŅŌ¯, ĐŧĐĩĐ´Đ¸Đ° ŅĐ°ĐšĐģĐģĐ°ŅĐŊŅ ŅĐēĐģĶŌ¯ Đ˛Ķ ĐēŌ¯ĐąŅĶĐē ĐąĐ°ŅĐēĐ°"
            " ĐŧĶĐŗŅĐģŌ¯ĐŧĐ°ŅĐģĐ°Ņ</b> ĐŊŅ Đ°Đ˛ŅĐžĐŧĐ°ŅĐ¸Đē ĶŠŅĶŅĐŗĶ ĐŧĶŠĐŧĐēĐ¸ĐŊ.\n\n<emoji"
            " document_id=5474667187258006816>đ</emoji> ĐŽĐˇĐĩŅĐąĐžŅĐģĐ°Ņ <b>ŅĐ¸ŅĐ°Đŋ ŅĐˇĐŧĐ°ŅŅ"
            " Đ¸ŅĐĩĐŧĐĩ</b> ĐąĐĩĐģĶĐŊ ĐąĐĩŅĐŗĶĐŊĐ´Ķ, <b>ĐąĐžŅ Đ¸ŅĐĩĐŧĐĩ</b> ĐąĐĩĐģĶĐŊ ĐąĐĩŅĐŧĶĐŗĶĐŊĐ´ĶĐŊ ŅŌŖĐ°"
            " Đ¸ŅĐĩĐŧĐģĐĩĐēŅĶ ĐąŅĐģŅŅ.\n\n<emoji document_id=5472267631979405211>đĢ</emoji>"
            " <b>ĐŽĐˇĐĩŅĐąĐžŅĐģĐ°Ņ Telegram</b> ŅĐ°ŅĐ°ŅŅĐŊĐŊĐ°ĐŊ <b>Đ´ĶŠŅĐĩŅ ŅŅĐ´ĶĐŧĐĩĐŊĐ´ĶŅ</b> ĐąŅĐģĐŗĐ°ĐŊŅĐŊĐ´Đ°"
            " ŅŅĐ°ĐģĐŗĐ°ĐŊ. <b>ĐŽĐˇĐĩŅĐąĐžŅĐģĐ°Ņ</b> <b>ŅĐ¸ŅĐ°Đŋ ŅĐˇĐŧĐ°ŅŅ Đ¸ŅĐĩĐŧĐĩ</b> ĐąĐĩĐģĶĐŊ ĐąĐĩŅĐŗĶĐŊĐ´Ķ,"
            " <b>ĐąĐžŅ Đ¸ŅĐĩĐŧĐĩ</b> ĐąĐĩĐģĶĐŊ ĐąĐĩŅĐŧĶĐŗĶĐŊĐ´ĶĐŊ ŅŌŖĐ° Đ¸ŅĐĩĐŧĐģĐĩĐēŅĶ ĐąŅĐģŅŅ. <b>ĐŽĐˇĐĩŅĐąĐžŅĐģĐ°Ņ</b>"
            " <b>ŅĐ¸ŅĐ°Đŋ ŅĐˇĐŧĐ°ŅŅ Đ¸ŅĐĩĐŧĐĩ</b> ĐąĐĩĐģĶĐŊ ĐąĐĩŅĐŗĶĐŊĐ´Ķ, <b>ĐąĐžŅ Đ¸ŅĐĩĐŧĐĩ</b> ĐąĐĩĐģĶĐŊ"
            " ĐąĐĩŅĐŧĶĐŗĶĐŊĐ´ĶĐŊ ŅŌŖĐ° Đ¸ŅĐĩĐŧĐģĐĩĐēŅĶ ĐąŅĐģŅŅ.\n\n"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_message",
                doc=lambda: self.strings("_cfg_cst_msg"),
            ),
            loader.ConfigValue(
                "custom_button",
                ["đ Support chat", "https://t.me/hikka_talks"],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Union(
                    loader.validators.Series(fixed_len=2),
                    loader.validators.NoneType(),
                ),
            ),
            loader.ConfigValue(
                "banner_url",
                "https://github.com/hikariatama/assets/raw/master/hikka_banner.mp4",
                lambda: self.strings("_cfg_banner"),
                validator=loader.validators.Link(),
            ),
        )

    def _render_info(self, inline: bool) -> str:
        try:
            repo = git.Repo(search_parent_directories=True)
            diff = repo.git.log([f"HEAD..origin/{version.branch}", "--oneline"])
            upd = (
                self.strings("update_required") if diff else self.strings("up-to-date")
            )
        except Exception:
            upd = ""

        me = '<b><a href="tg://user?id={}">{}</a></b>'.format(
            self._client.hikka_me.id,
            utils.escape_html(get_display_name(self._client.hikka_me)),
        )
        build = utils.get_commit_url()
        _version = f'<i>{".".join(list(map(str, list(version.__version__))))}</i>'
        prefix = f"ÂĢ<code>{utils.escape_html(self.get_prefix())}</code>Âģ"

        platform = utils.get_named_platform()

        for emoji, icon in {
            "đ": "<emoji document_id=5449599833973203438>đ§Ą</emoji>",
            "đ": "<emoji document_id=5449468596952507859>đ</emoji>",
            "â": "<emoji document_id=5407025283456835913>đą</emoji>",
            "đ": "<emoji document_id=6332120630099445554>đ</emoji>",
            "đĻž": "<emoji document_id=5386766919154016047>đĻž</emoji>",
            "đ": "<emoji document_id=5359595190807962128>đ</emoji>",
            "đŗ": "<emoji document_id=5431815452437257407>đŗ</emoji>",
            "đļ": "<emoji document_id=5407025283456835913>đą</emoji>",
            "đââŦ": "<emoji document_id=6334750507294262724>đââŦ</emoji>",
            "âī¸": "<emoji document_id=5469986291380657759>âī¸</emoji>",
            "đģ": "<emoji document_id=5471952986970267163>đ</emoji>",
            "đ": "<emoji document_id=5370610867094166617>đ</emoji>",
        }.items():
            platform = platform.replace(emoji, icon)

        return (
            (
                "<b>đ Hikka</b>\n"
                if "hikka" not in self.config["custom_message"].lower()
                else ""
            )
            + self.config["custom_message"].format(
                me=me,
                version=_version,
                build=build,
                prefix=prefix,
                platform=platform,
                upd=upd,
                uptime=utils.formatted_uptime(),
                cpu_usage=utils.get_cpu_usage(),
                ram_usage=f"{utils.get_ram_usage()} MB",
                branch=version.branch,
            )
            if self.config["custom_message"]
            else (
                f'<b>{{}}</b>\n\n<b>{{}} {self.strings("owner")}:</b> {me}\n\n<b>{{}}'
                f' {self.strings("version")}:</b> {_version} {build}\n<b>{{}}'
                f' {self.strings("branch")}:'
                f"</b> <code>{version.branch}</code>\n{upd}\n\n<b>{{}}"
                f' {self.strings("prefix")}:</b> {prefix}\n<b>{{}}'
                f' {self.strings("uptime")}:'
                f"</b> {utils.formatted_uptime()}\n\n<b>{{}}"
                f' {self.strings("cpu_usage")}:'
                f"</b> <i>~{utils.get_cpu_usage()} %</i>\n<b>{{}}"
                f' {self.strings("ram_usage")}:'
                f"</b> <i>~{utils.get_ram_usage()} MB</i>\n<b>{{}}</b>"
            ).format(
                *map(
                    lambda x: utils.remove_html(x) if inline else x,
                    (
                        (
                            utils.get_platform_emoji()
                            if self._client.hikka_me.premium and not inline
                            else "đ Hikka"
                        ),
                        "<emoji document_id=5373141891321699086>đ</emoji>",
                        "<emoji document_id=5469741319330996757>đĢ</emoji>",
                        "<emoji document_id=5449918202718985124>đŗ</emoji>",
                        "<emoji document_id=5472111548572900003>â¨ī¸</emoji>",
                        "<emoji document_id=5451646226975955576>âī¸</emoji>",
                        "<emoji document_id=5431449001532594346>âĄī¸</emoji>",
                        "<emoji document_id=5359785904535774578>đŧ</emoji>",
                        platform,
                    ),
                )
            )
        )

    def _get_mark(self):
        return (
            {
                "text": self.config["custom_button"][0],
                "url": self.config["custom_button"][1],
            }
            if self.config["custom_button"]
            else None
        )

    @loader.inline_handler(
        thumb_url="https://img.icons8.com/external-others-inmotus-design/344/external-Moon-round-icons-others-inmotus-design-2.png"
    )
    @loader.inline_everyone
    async def info(self, _: InlineQuery) -> dict:
        """Send userbot info"""

        return {
            "title": self.strings("send_info"),
            "description": self.strings("description"),
            **(
                {"photo": self.config["banner_url"], "caption": self._render_info(True)}
                if self.config["banner_url"]
                else {"message": self._render_info(True)}
            ),
            "thumb": (
                "https://github.com/hikariatama/Hikka/raw/master/assets/hikka_pfp.png"
            ),
            "reply_markup": self._get_mark(),
        }

    @loader.command(
        ru_doc="ĐŅĐŋŅĐ°Đ˛ĐģŅĐĩŅ Đ¸ĐŊŅĐžŅĐŧĐ°ŅĐ¸Ņ Đž ĐąĐžŅĐĩ",
        fr_doc="Envoie des informations sur le bot",
        it_doc="Invia informazioni sul bot",
        de_doc="Sendet Informationen Ãŧber den Bot",
        tr_doc="Bot hakkÄąnda bilgi gÃļnderir",
        uz_doc="Bot haqida ma'lumot yuboradi",
        es_doc="EnvÃ­a informaciÃŗn sobre el bot",
        kk_doc="ĐĐžŅ ŅŅŅĐ°ĐģŅ Đ°ŌĐŋĐ°ŅĐ°Ņ ĐļŅĐąĐĩŅĐĩĐ´Ņ",
    )
    @loader.unrestricted
    async def infocmd(self, message: Message):
        """Send userbot info"""

        if self.config["custom_button"]:
            await self.inline.form(
                message=message,
                text=self._render_info(True),
                reply_markup=self._get_mark(),
                **(
                    {"photo": self.config["banner_url"]}
                    if self.config["banner_url"]
                    else {}
                ),
            )
        else:
            await utils.answer_file(
                message,
                self.config["banner_url"],
                self._render_info(False),
            )

    @loader.unrestricted
    @loader.command(
        ru_doc="ĐŅĐŋŅĐ°Đ˛Đ¸ŅŅ Đ¸ĐŊŅĐžŅĐŧĐ°ŅĐ¸Ņ ĐŋĐž ŅĐ¸ĐŋŅ 'Đ§ŅĐž ŅĐ°ĐēĐžĐĩ ĐĨĐ¸ĐēĐēĐ°?'",
        fr_doc="Envoyer des informations du type 'Qu'est-ce que Hikka?'",
        it_doc="Invia informazioni del tipo 'Cosa Ã¨ Hikka?'",
        de_doc="Sende Informationen Ãŧber den Bot",
        tr_doc="Bot hakkÄąnda bilgi gÃļnderir",
        uz_doc="Bot haqida ma'lumot yuborish",
        es_doc="Enviar informaciÃŗn sobre el bot",
        kk_doc="ĐĐžŅ ŅŅŅĐ°ĐģŅ Đ°ŌĐŋĐ°ŅĐ°Ņ ĐļŅĐąĐĩŅŅ",
    )
    async def hikkainfo(self, message: Message):
        """Send info aka 'What is Hikka?'"""
        await utils.answer(message, self.strings("desc"))

    @loader.command(
        ru_doc="<ŅĐĩĐēŅŅ> - ĐĐˇĐŧĐĩĐŊĐ¸ŅŅ ŅĐĩĐēŅŅ Đ˛ .info",
        fr_doc="<texte> - Changer le texte dans .info",
        it_doc="<testo> - Cambia il testo in .info",
        de_doc="<text> - Ãndere den Text in .info",
        tr_doc="<metin> - .info'da metni deÄiÅtir",
        uz_doc="<matn> - .info'dagi matnni o'zgartirish",
        es_doc="<texto> - Cambiar el texto en .info",
        kk_doc="<ĐŧĶŅŅĐŊ> - .info ĐŧĶŅŅĐŊŅĐŊ ĶŠĐˇĐŗĐĩŅŅŅ",
    )
    async def setinfo(self, message: Message):
        """<text> - Change text in .info"""
        args = utils.get_args_html(message)
        if not args:
            return await utils.answer(message, self.strings("setinfo_no_args"))

        self.config["custom_message"] = args
        await utils.answer(message, self.strings("setinfo_success"))

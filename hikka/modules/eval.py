# ÂŠī¸ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# đ https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# đ https://www.gnu.org/licenses/agpl-3.0.html

import contextlib
import itertools
import os
import subprocess
import sys
import tempfile
import typing
from types import ModuleType

import hikkatl
from hikkatl.errors.rpcerrorlist import MessageIdInvalidError
from hikkatl.sessions import StringSession
from hikkatl.tl.types import Message
from meval import meval

from .. import loader, main, utils
from ..log import HikkaException


class Brainfuck:
    def __init__(self, memory_size: int = 30000):
        if memory_size < 0:
            raise ValueError("memory size cannot be negative")

        self._data = [0] * memory_size
        self.out = ""
        self.error = None

    @property
    def data(self):
        return self._data

    def run(self, code: str) -> str:
        self.out = ""
        had_error = self._eval(code)

        if had_error:
            return

        self._interpret(code)
        return self.out

    def _report_error(
        self,
        message: str,
        line: typing.Optional[int] = None,
        column: typing.Optional[int] = None,
    ):
        self.error = (
            message + f" at line {line}, column {column}"
            if line is not None and column is not None
            else ""
        )

    def _eval(self, source: str):
        line = col = 0

        stk = []

        loop_open = False

        for c in source:
            if c == "[":
                if loop_open:
                    self._report_error("unexpected token '['", line, col)
                    return True

                loop_open = True
                stk.append("[")
            elif c == "]":
                loop_open = False
                if len(stk) == 0:
                    self._report_error("unexpected token ']'", line, col)
                    return True

                stk.pop()
            elif c == "\n":
                line += 1
                col = -1

            col += 1

        if len(stk) != 0:
            self._report_error("unmatched brackets")
            return True

        return False

    def _interpret(self, source: str):
        line = col = ptr = current = 0

        while current < len(source):
            if source[current] == ">":
                if ptr == (len(self.data) - 1):
                    self._report_error("pointer out of range", line, col)
                    return True

                ptr += 1
            elif source[current] == "<":
                if ptr == 0:
                    self._report_error("pointer out of range", line, col)
                    return True

                ptr -= 1
            elif source[current] == "+":
                if self.data[ptr] >= 2**32:
                    self._report_error("cell overflow")
                    return True

                self.data[ptr] += 1

            elif source[current] == "-":
                if self.data[ptr] == 0:
                    self._report_error("cell underflow")
                    return True

                self.data[ptr] -= 1
            elif source[current] == ".":
                self.out += chr(self.data[ptr])
            elif source[current] == ",":
                value = input()
                if not value.isdigit():
                    self._report_error("invalid input")

                self.data[ptr] = value
            elif source[current] == "[":
                if self.data[ptr] == 0:
                    while source[current] != "]":
                        current += 1
            elif source[current] == "]":
                if self.data[ptr] != 0:
                    while source[current] != "[":
                        current -= 1
            elif source[current] == "\n":
                line += 1
                col = -1

            col += 1
            current += 1

        return False


@loader.tds
class Evaluator(loader.Module):
    """Evaluates code in various languages"""

    strings = {
        "name": "Evaluator",
        "eval": (
            "<emoji document_id={}>đģ</emoji><b>"
            " Code:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5197688912457245639>â</emoji><b>"
            " Result:</b>\n<code>{}</code>"
        ),
        "err": (
            "<emoji document_id={}>đģ</emoji><b>"
            " Code:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5312526098750252863>đĢ</emoji> <b>Error:</b>\n{}"
        ),
        "compiling": (
            "<emoji document_id=5325787248363314644>đĢĨ</emoji> <b>Compiling code...</b>"
        ),
        "no_compiler": (
            "<emoji document_id={}>đģ</emoji> <b>{} compiler is not installed on the"
            " system.</b>"
        ),
    }

    strings_ru = {
        "eval": (
            "<emoji document_id={}>đģ</emoji><b>"
            " ĐĐžĐ´:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5197688912457245639>â</emoji><b>"
            " Đ ĐĩĐˇŅĐģŅŅĐ°Ņ:</b>\n<code>{}</code>"
        ),
        "err": (
            "<emoji document_id={}>đģ</emoji><b>"
            " ĐĐžĐ´:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5312526098750252863>đĢ</emoji> <b>ĐŅĐ¸ĐąĐēĐ°:</b>\n{}"
        ),
        "_cls_doc": "ĐŅĐŋĐžĐģĐŊŅĐĩŅ ĐēĐžĐ´ ĐŊĐ° ŅĐ°ĐˇĐģĐ¸ŅĐŊŅŅ ŅĐˇŅĐēĐ°Ņ ĐŋŅĐžĐŗŅĐ°ĐŧĐŧĐ¸ŅĐžĐ˛Đ°ĐŊĐ¸Ņ",
        "compiling": (
            "<emoji document_id=5325787248363314644>đĢĨ</emoji> <b>ĐĐžĐŧĐŋĐ¸ĐģŅŅĐ¸Ņ ĐēĐžĐ´Đ°...</b>"
        ),
        "no_compiler": (
            "<emoji document_id={}>đģ</emoji> <b>ĐĐžĐŧĐŋĐ¸ĐģŅŅĐžŅ {} ĐŊĐĩ ŅŅŅĐ°ĐŊĐžĐ˛ĐģĐĩĐŊ ĐŊĐ°"
            " ŅĐ¸ŅŅĐĩĐŧĐĩ.</b>"
        ),
    }

    strings_fr = {
        "eval": (
            "<emoji document_id={}>đģ</emoji><b>"
            " Code:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5197688912457245639>â</emoji><b>"
            " Resultat:</b>\n<code>{}</code>"
        ),
        "err": (
            "<emoji document_id={}>đģ</emoji><b>"
            " Code:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5312526098750252863>đĢ</emoji> <b>Erreur:</b>\n{}"
        ),
        "_cls_doc": "ExÃŠcute du code sur diffÃŠrents langages de programmation",
        "compiling": (
            "<emoji document_id=5325787248363314644>đĢĨ</emoji> <b>Compilation du"
            " code...</b>"
        ),
        "no_compiler": (
            "<emoji document_id={}>đģ</emoji> <b>Le compilateur {} n'est pas installÃŠ"
            " sur le systÃ¨me.</b>"
        ),
    }

    strings_it = {
        "eval": (
            "<emoji document_id={}>đģ</emoji><b>"
            " Codice:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5197688912457245639>â</emoji><b>"
            " Risultato:</b>\n<code>{}</code>"
        ),
        "err": (
            "<emoji document_id={}>đģ</emoji><b>"
            " Codice:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5312526098750252863>đĢ</emoji> <b>Errore:</b>\n{}"
        ),
        "_cls_doc": "Esegue il codice su diversi linguaggi di programmazione",
        "compiling": (
            "<emoji document_id=5325787248363314644>đĢĨ</emoji> <b>Compilazione del"
            " codice...</b>"
        ),
        "no_compiler": (
            "<emoji document_id={}>đģ</emoji> <b>Il compilatore {} non Ã¨ installato sul"
            " sistema.</b>"
        ),
    }

    strings_de = {
        "eval": (
            "<emoji document_id={}>đģ</emoji><b>"
            " Code:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5197688912457245639>â</emoji><b>"
            " Resultat:</b>\n<code>{}</code>"
        ),
        "err": (
            "<emoji document_id={}>đģ</emoji><b>"
            " Code:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5312526098750252863>đĢ</emoji> <b>Fehler:</b>\n{}"
        ),
        "_cls_doc": "FÃŧhrt Code auf verschiedenen Programmiersprachen aus",
        "compiling": (
            "<emoji document_id=5325787248363314644>đĢĨ</emoji> <b>Kompilieren des"
            " Codes...</b>"
        ),
        "no_compiler": (
            "<emoji document_id={}>đģ</emoji> <b>Der Compiler {} ist nicht auf dem"
            " System installiert.</b>"
        ),
    }

    strings_tr = {
        "eval": (
            "<emoji document_id={}>đģ</emoji><b>"
            " Kod:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5197688912457245639>â</emoji><b>"
            " SonuÃ§:</b>\n<code>{}</code>"
        ),
        "err": (
            "<emoji document_id={}>đģ</emoji><b>"
            " Kod:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5312526098750252863>đĢ</emoji> <b>Hata:</b>\n{}"
        ),
        "_cls_doc": "ÃeÅitli programlama dillerinde kodu Ã§alÄąÅtÄąrÄąr",
        "compiling": (
            "<emoji document_id=5325787248363314644>đĢĨ</emoji> <b>Kod derleniyor...</b>"
        ),
        "no_compiler": (
            "<emoji document_id={}>đģ</emoji> <b>Sistemde {} derleyicisi yÃŧklÃŧ"
            " deÄil.</b>"
        ),
    }

    strings_uz = {
        "eval": (
            "<emoji document_id={}>đģ</emoji><b>"
            " Kod:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5197688912457245639>â</emoji><b>"
            " Natija:</b>\n<code>{}</code>"
        ),
        "err": (
            "<emoji document_id={}>đģ</emoji><b>"
            " Kod:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5312526098750252863>đĢ</emoji> <b>Xato:</b>\n{}"
        ),
        "_cls_doc": "Dasturlash tillarida kodni bajaradi",
        "compiling": (
            "<emoji document_id=5325787248363314644>đĢĨ</emoji> <b>Kod derleniyor...</b>"
        ),
        "no_compiler": (
            "<emoji document_id={}>đģ</emoji> <b>Tizimda {} derleyicisi yo'q.</b>"
        ),
    }

    strings_es = {
        "eval": (
            "<emoji document_id={}>đģ</emoji><b>"
            " CÃŗdigo:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5197688912457245639>â</emoji><b>"
            " Resultado:</b>\n<code>{}</code>"
        ),
        "err": (
            "<emoji document_id={}>đģ</emoji><b>"
            " CÃŗdigo:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5312526098750252863>đĢ</emoji> <b>Error:</b>\n{}"
        ),
        "_cls_doc": "Ejecuta cÃŗdigo en diferentes lenguajes de programaciÃŗn",
        "compiling": (
            "<emoji document_id=5325787248363314644>đĢĨ</emoji> <b>Compilando"
            " cÃŗdigo...</b>"
        ),
        "no_compiler": (
            "<emoji document_id={}>đģ</emoji> <b>El compilador {} no estÃĄ instalado en"
            " el sistema.</b>"
        ),
    }

    strings_kk = {
        "eval": (
            "<emoji document_id={}>đģ</emoji><b>"
            " ĐĐžĐ´:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5197688912457245639>â</emoji><b>"
            " ĐĶŅĐ¸ĐļĐĩ:</b>\n<code>{}</code>"
        ),
        "err": (
            "<emoji document_id={}>đģ</emoji><b>"
            " ĐĐžĐ´:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5312526098750252863>đĢ</emoji> <b>ŌĐ°ŅĐĩ:</b>\n{}"
        ),
        "_cls_doc": "ĐĐ°ŅŌĐ° ŅŅĐģĐ´ĐĩŅĐ´Đĩ ĐēĐžĐ´ŅŅ ĐžŅŅĐŊĐ´Đ°ĐšĐ´Ņ",
        "compiling": (
            "<emoji document_id=5325787248363314644>đĢĨ</emoji> <b>ĐĐžĐ´"
            " ĐēĐžĐŧĐŋĐ¸ĐģŅŅĐ¸ŅŅŅ...</b>"
        ),
        "no_compiler": (
            "<emoji document_id={}>đģ</emoji> <b>ĐĄĐ¸ŅŅĐĩĐŧĐ°Đ´Đ° {} ĐēĐžĐŧĐŋĐ¸ĐģŅŅĐžŅŅ"
            " ĐļŌ¯ĐēŅĐĩĐģĐŧĐĩĐŗĐĩĐŊ.</b>"
        ),
    }

    strings_tt = {
        "eval": (
            "<emoji document_id={}>đģ</emoji><b>"
            " ĐĐžĐ´:</b>\n<code>{}</code>\n<emoji"
            " document_id=5197688912457245639>â</emoji><b>"
            " ĐĶŅĐ¸ŌĶ:</b>\n<code>{}</code>"
        ),
        "err": (
            "<emoji document_id={}>đģ</emoji><b>"
            " ĐĐžĐ´:</b>\n<code>{}</code>\n\n<emoji"
            " document_id=5312526098750252863>đĢ</emoji> <b>ĐĨĐ°ŅĐ°:</b>\n{}"
        ),
        "_cls_doc": "ĐĐ°ŅĐēĐ° ŅĐ¸ĐģĐģĶŅĐ´Ķ ĐēĐžĐ´ŅŅ Ō¯ĐˇĐŗĶŅŅĶ Đ°ĐģĐŧŅĐš",
        "compiling": (
            "<emoji document_id=5325787248363314644>đĢĨ</emoji> <b>ĐĐžĐ´"
            " ĐēĐžĐŧĐŋĐ¸ĐģŅŅĐ¸ŅŅŅ...</b>"
        ),
        "no_compiler": (
            "<emoji document_id={}>đģ</emoji> <b>ĐĄĐ¸ŅŅĐĩĐŧĐ°Đ´Đ° {} ĐēĐžĐŧĐŋĐ¸ĐģŅŅĐžŅŅ"
            " ĐļŌ¯ĐēŅĐĩĐģĐŧĶĐŗĶĐŊ.</b>"
        ),
    }

    @loader.owner
    @loader.command(
        ru_doc="ĐŅĐŋĐžĐģĐŊŅĐĩŅ Python ĐēĐžĐ´",
        fr_doc="Ãvalue du code Python",
        it_doc="Esegue codice Python",
        de_doc="FÃŧhrt Python Code aus",
        tr_doc="Python kodu Ã§alÄąÅtÄąrÄąr",
        uz_doc="Python kodini ishga tushiradi",
        es_doc="Ejecuta cÃŗdigo Python",
        kk_doc="Python ĐēĐžĐ´ŅĐŊ ĐžŅŅĐŊĐ´Đ°Ņ",
        alias="eval",
    )
    async def e(self, message: Message):
        """Evaluates python code"""
        try:
            result = await meval(
                utils.get_args_raw(message),
                globals(),
                **await self.getattrs(message),
            )
        except Exception:
            item = HikkaException.from_exc_info(*sys.exc_info())

            await utils.answer(
                message,
                self.strings("err").format(
                    "4985626654563894116",
                    utils.escape_html(utils.get_args_raw(message)),
                    self.censor(
                        (
                            "\n".join(item.full_stack.splitlines()[:-1])
                            + "\n\n"
                            + "đĢ "
                            + item.full_stack.splitlines()[-1]
                        )
                    ),
                ),
            )

            return

        if callable(getattr(result, "stringify", None)):
            with contextlib.suppress(Exception):
                result = str(result.stringify())

        with contextlib.suppress(MessageIdInvalidError):
            await utils.answer(
                message,
                self.strings("eval").format(
                    "4985626654563894116",
                    utils.escape_html(utils.get_args_raw(message)),
                    utils.escape_html(self.censor(str(result))),
                ),
            )

    @loader.command(
        ru_doc="ĐŅĐŋĐžĐģĐŊŅĐĩŅ C++ ĐēĐžĐ´",
        fr_doc="Ãvalue du code C++",
        it_doc="Esegue codice C++",
        de_doc="FÃŧhrt C++ Code aus",
        tr_doc="C++ kodu Ã§alÄąÅtÄąrÄąr",
        uz_doc="C++ kodini ishga tushiradi",
        es_doc="Ejecuta cÃŗdigo C++",
        kk_doc="C++ ĐēĐžĐ´ŅĐŊ ĐžŅŅĐŊĐ´Đ°Ņ",
    )
    async def ecpp(self, message: Message, c: bool = False):
        """Evaluates C++ code"""
        try:
            subprocess.check_output(
                ["gcc" if c else "g++", "--version"],
                stderr=subprocess.STDOUT,
            )
        except Exception:
            await utils.answer(
                message,
                self.strings("no_compiler").format(
                    "4986046904228905931" if c else "4985844035743646190",
                    "C (gcc)" if c else "C++ (g++)",
                ),
            )
            return

        code = utils.get_args_raw(message)
        message = await utils.answer(message, self.strings("compiling"))
        error = False
        with tempfile.TemporaryDirectory() as tmpdir:
            file = os.path.join(tmpdir, "code.cpp")
            with open(file, "w") as f:
                f.write(code)

            try:
                result = subprocess.check_output(
                    ["gcc" if c else "g++", "-o", "code", "code.cpp"],
                    cwd=tmpdir,
                    stderr=subprocess.STDOUT,
                ).decode()
            except subprocess.CalledProcessError as e:
                result = e.output.decode()
                error = True

            if not result:
                try:
                    result = subprocess.check_output(
                        ["./code"],
                        cwd=tmpdir,
                        stderr=subprocess.STDOUT,
                    ).decode()
                except subprocess.CalledProcessError as e:
                    result = e.output.decode()
                    error = True

        with contextlib.suppress(MessageIdInvalidError):
            await utils.answer(
                message,
                self.strings("err" if error else "eval").format(
                    "4986046904228905931" if c else "4985844035743646190",
                    utils.escape_html(code),
                    f"<code>{utils.escape_html(result)}</code>",
                ),
            )

    @loader.command(
        ru_doc="ĐŅĐŋĐžĐģĐŊŅĐĩŅ C ĐēĐžĐ´",
        fr_doc="Ãvalue du code C",
        it_doc="Esegue codice C",
        de_doc="FÃŧhrt C Code aus",
        tr_doc="C kodu Ã§alÄąÅtÄąrÄąr",
        uz_doc="C kodini ishga tushiradi",
        es_doc="Ejecuta cÃŗdigo C",
        kk_doc="C ĐēĐžĐ´ŅĐŊ ĐžŅŅĐŊĐ´Đ°Ņ",
    )
    async def ec(self, message: Message):
        """Evaluates C code"""
        await self.ecpp(message, c=True)

    @loader.command(
        ru_doc="ĐŅĐŋĐžĐģĐŊŅĐĩŅ Node.js ĐēĐžĐ´",
        fr_doc="Ãvalue du code Node.js",
        it_doc="Esegue codice Node.js",
        de_doc="FÃŧhrt Node.js Code aus",
        tr_doc="Node.js kodu Ã§alÄąÅtÄąrÄąr",
        uz_doc="Node.js kodini ishga tushiradi",
        es_doc="Ejecuta cÃŗdigo Node.js",
        kk_doc="Node.js ĐēĐžĐ´ŅĐŊ ĐžŅŅĐŊĐ´Đ°Ņ",
    )
    async def enode(self, message: Message):
        """Evaluates Node.js code"""
        try:
            subprocess.check_output(
                ["node", "--version"],
                stderr=subprocess.STDOUT,
            )
        except Exception:
            await utils.answer(
                message,
                self.strings("no_compiler").format(
                    "4985643941807260310",
                    "Node.js",
                ),
            )
            return

        code = utils.get_args_raw(message)
        error = False
        with tempfile.TemporaryDirectory() as tmpdir:
            file = os.path.join(tmpdir, "code.js")
            with open(file, "w") as f:
                f.write(code)

            try:
                result = subprocess.check_output(
                    ["node", "code.js"],
                    cwd=tmpdir,
                    stderr=subprocess.STDOUT,
                ).decode()
            except subprocess.CalledProcessError as e:
                result = e.output.decode()
                error = True

        with contextlib.suppress(MessageIdInvalidError):
            await utils.answer(
                message,
                self.strings("err" if error else "eval").format(
                    "4985643941807260310",
                    utils.escape_html(code),
                    f"<code>{utils.escape_html(result)}</code>",
                ),
            )

    @loader.command(
        ru_doc="ĐŅĐŋĐžĐģĐŊŅĐĩŅ PHP ĐēĐžĐ´",
        fr_doc="Ãvalue du code PHP",
        it_doc="Esegue codice PHP",
        de_doc="FÃŧhrt PHP Code aus",
        tr_doc="PHP kodu Ã§alÄąÅtÄąrÄąr",
        uz_doc="PHP kodini ishga tushiradi",
        es_doc="Ejecuta cÃŗdigo PHP",
        kk_doc="PHP ĐēĐžĐ´ŅĐŊ ĐžŅŅĐŊĐ´Đ°Ņ",
    )
    async def ephp(self, message: Message):
        """Evaluates PHP code"""
        try:
            subprocess.check_output(
                ["php", "--version"],
                stderr=subprocess.STDOUT,
            )
        except Exception:
            await utils.answer(
                message,
                self.strings("no_compiler").format(
                    "4985815079074136919",
                    "PHP",
                ),
            )
            return

        code = utils.get_args_raw(message)
        error = False
        with tempfile.TemporaryDirectory() as tmpdir:
            file = os.path.join(tmpdir, "code.php")
            with open(file, "w") as f:
                f.write(f"<?php {code} ?>")

            try:
                result = subprocess.check_output(
                    ["php", "code.php"],
                    cwd=tmpdir,
                    stderr=subprocess.STDOUT,
                ).decode()
            except subprocess.CalledProcessError as e:
                result = e.output.decode()
                error = True

        with contextlib.suppress(MessageIdInvalidError):
            await utils.answer(
                message,
                self.strings("err" if error else "eval").format(
                    "4985815079074136919",
                    utils.escape_html(code),
                    f"<code>{utils.escape_html(result)}</code>",
                ),
            )

    @loader.command(
        ru_doc="ĐŅĐŋĐžĐģĐŊŅĐĩŅ Ruby ĐēĐžĐ´",
        fr_doc="Ãvalue du code Ruby",
        it_doc="Esegue codice Ruby",
        de_doc="FÃŧhrt Ruby Code aus",
        tr_doc="Ruby kodu Ã§alÄąÅtÄąrÄąr",
        uz_doc="Ruby kodini ishga tushiradi",
        es_doc="Ejecuta cÃŗdigo Ruby",
        kk_doc="Ruby ĐēĐžĐ´ŅĐŊ ĐžŅŅĐŊĐ´Đ°Ņ",
    )
    async def eruby(self, message: Message):
        """Evaluates Ruby code"""
        try:
            subprocess.check_output(
                ["ruby", "--version"],
                stderr=subprocess.STDOUT,
            )
        except Exception:
            await utils.answer(
                message,
                self.strings("no_compiler").format(
                    "4985760855112024628",
                    "Ruby",
                ),
            )
            return

        code = utils.get_args_raw(message)
        error = False
        with tempfile.TemporaryDirectory() as tmpdir:
            file = os.path.join(tmpdir, "code.rb")
            with open(file, "w") as f:
                f.write(code)

            try:
                result = subprocess.check_output(
                    ["ruby", "code.rb"],
                    cwd=tmpdir,
                    stderr=subprocess.STDOUT,
                ).decode()
            except subprocess.CalledProcessError as e:
                result = e.output.decode()
                error = True

        with contextlib.suppress(MessageIdInvalidError):
            await utils.answer(
                message,
                self.strings("err" if error else "eval").format(
                    "4985760855112024628",
                    utils.escape_html(code),
                    f"<code>{utils.escape_html(result)}</code>",
                ),
            )

    @loader.command(
        ru_doc="ĐŅĐŋĐžĐģĐŊŅĐĩŅ Brainf*ck ĐēĐžĐ´",
        fr_doc="Ãvalue du code Brainf*ck",
        it_doc="Esegue codice Brainf*ck",
        de_doc="FÃŧhrt Brainf*ck Code aus",
        tr_doc="Brainf*ck kodu Ã§alÄąÅtÄąrÄąr",
        uz_doc="Brainf*ck kodini ishga tushiradi",
        es_doc="Ejecuta cÃŗdigo Brainf*ck",
        kk_doc="Brainf*ck ĐēĐžĐ´ŅĐŊ ĐžŅŅĐŊĐ´Đ°Ņ",
    )
    async def ebf(self, message: Message):
        """Evaluates Brainf*ck code"""
        code = utils.get_args_raw(message)
        if "-debug" in code:
            code = code.replace("-debug", "")
            code = code.replace(" ", "")
            debug = True
        else:
            debug = False

        error = False

        bf = Brainfuck()
        result = bf.run(code)
        if bf.error:
            result = bf.error
            error = True

        if not result:
            result = "<empty>"

        if debug:
            result += "\n\n" + " | ".join(map(str, filter(lambda x: x, bf.data)))

        with contextlib.suppress(MessageIdInvalidError):
            await utils.answer(
                message,
                self.strings("err" if error else "eval").format(
                    "5474256197542486673",
                    utils.escape_html(code),
                    f"<code>{utils.escape_html(result)}</code>",
                ),
            )

    def censor(self, ret: str) -> str:
        ret = ret.replace(str(self._client.hikka_me.phone), "&lt;phone&gt;")

        if redis := os.environ.get("REDIS_URL") or main.get_config_key("redis_uri"):
            ret = ret.replace(redis, f'redis://{"*" * 26}')

        if db := os.environ.get("DATABASE_URL") or main.get_config_key("db_uri"):
            ret = ret.replace(db, f'postgresql://{"*" * 26}')

        if btoken := self._db.get("hikka.inline", "bot_token", False):
            ret = ret.replace(
                btoken,
                f'{btoken.split(":")[0]}:{"*" * 26}',
            )

        if htoken := self.lookup("loader").get("token", False):
            ret = ret.replace(htoken, f'eugeo_{"*" * 26}')

        ret = ret.replace(
            StringSession.save(self._client.session),
            "StringSession(**************************)",
        )

        return ret

    async def getattrs(self, message: Message) -> dict:
        reply = await message.get_reply_message()
        return {
            **{
                "message": message,
                "client": self._client,
                "reply": reply,
                "r": reply,
                **self.get_sub(hikkatl.tl.types),
                **self.get_sub(hikkatl.tl.functions),
                "event": message,
                "chat": message.to_id,
                "hikkatl": hikkatl,
                "telethon": hikkatl,
                "utils": utils,
                "main": main,
                "loader": loader,
                "f": hikkatl.tl.functions,
                "c": self._client,
                "m": message,
                "lookup": self.lookup,
                "self": self,
                "db": self.db,
            },
        }

    def get_sub(self, obj: typing.Any, _depth: int = 1) -> dict:
        """Get all callable capitalised objects in an object recursively, ignoring _*"""
        return {
            **dict(
                filter(
                    lambda x: x[0][0] != "_"
                    and x[0][0].upper() == x[0][0]
                    and callable(x[1]),
                    obj.__dict__.items(),
                )
            ),
            **dict(
                itertools.chain.from_iterable(
                    [
                        self.get_sub(y[1], _depth + 1).items()
                        for y in filter(
                            lambda x: x[0][0] != "_"
                            and isinstance(x[1], ModuleType)
                            and x[1] != obj
                            and x[1].__package__.rsplit(".", _depth)[0] == "hikkatl.tl",
                            obj.__dict__.items(),
                        )
                    ]
                )
            ),
        }

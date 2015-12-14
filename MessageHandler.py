# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 14:29:29 2015

@author: jborwey
"""
from NumericStringParsing import NumericStringParser
import pprint
import time

from functionClasses import AbstractHandler
from functionClasses.MagicTheGathering import MagicHandler
from functionClasses.Math import MathHandler
from functionClasses.ImageSearch import ImageSearch
from functionClasses.Wikipedia import WikipediaHandler

COMMAND_CHAR = '!'
class MessageHandler:

    def __init__(self, bot):
        self.math_parser = NumericStringParser()
        self.pprinter = pprint.PrettyPrinter(indent=4)
        self.bot = bot
        self.enable_bot = False
        self.last_msg = long(str(time.time()).split('.')[0])

        self.command_dict = dict()
        self.command_admin_permission = dict()
        self.command_enable_permission = dict()

        # add commands as needed
        self.register_command('enable', self.enable_bot_cmd, admin_only=True, enable_independent=True)
        self.register_command('disable', self.disable_bot_cmd, admin_only=True)
        self.register_command('join', self.join_cmd, admin_only=True)

        self.register_command('math', MathHandler.MathHandler(self.bot, self.math_parser).handle)
        self.register_command('image', ImageSearch.ImageSearch(self.bot).handle)
        self.register_command('mtg', MagicHandler.MagicTheGatheringHandler(self.bot).handle)
        self.register_command('wiki', WikipediaHandler.WikipediaHandler(self.bot).handle)

    def register_command(self, command_string, message_handler, admin_only=False, enable_independent=False):
        self.command_dict[command_string] = message_handler

        if admin_only:
            self.command_admin_permission[command_string] = admin_only
        else:
            self.command_admin_permission[command_string] = False

        if enable_independent:
            self.command_enable_permission[command_string] = enable_independent
        else:
            self.command_enable_permission[command_string] = False

    def handle(self, msg):
        time_stamp_str = msg.xml.attrib['ts'].split('.')[0]
        time_stamp = long(time_stamp_str)

        if time_stamp < self.last_msg:
            return None
        elif msg['type'] == 'groupchat':
            self.last_msg = time_stamp

            message_body = msg['body']
            from_name_full = msg['mucnick']
            split_str = message_body.split(' ')

            if len(split_str[0]) <= len(COMMAND_CHAR) or not split_str[0].startswith(COMMAND_CHAR):
                return None

            command = split_str[0].replace(COMMAND_CHAR, "", 1)

            handler = self.command_dict[command]
            admin_permission = self.command_admin_permission[command]
            enable_independent_permission = self.command_enable_permission[command]

            if handler is None or \
                    (admin_permission and not from_name_full == self.bot.user_nickname) or \
                    (not enable_independent_permission and not self.enable_bot):
                return None

            reply_msg = handler(split_str, from_name_full)

            print("command %s by %s" % (command, from_name_full))

            if reply_msg is not None:
                self.bot.reply_room(msg, reply_msg)

    def enable_bot_cmd(self, message, from_name_full):
        self.enable_bot = True
        return "Functions Enabled"

    def disable_bot_cmd(self, message, from_name_full):
        self.enable_bot = False
        return "Functions Disabled"

    def join_cmd(self, message, from_name_full):
        room_name = ' '.join(message[1:])
        if self.bot.join_room_by_name(room_name):
            self.bot.reply_room(msg, "Joining room '%s'" % room_name)
        else:
            self.bot.reply_room(msg, "Could not find room")
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 14:29:29 2015

@author: jborwey
"""
from NumericStringParsing import NumericStringParser
import pprint
import time
from Scheduler import Scheduler
from functionClasses.MagicTheGathering import MagicHandler
from functionClasses.Math import MathHandler
from functionClasses.ImageSearch import ImageSearch
from functionClasses.Netrunner import NetrunnerHandler
from functionClasses.RemindMeHandler import RemindMeHandler
from functionClasses.Roll import RollHandler
from functionClasses.Translate import TranslateHandler
from functionClasses.Wikipedia import WikipediaHandler
from functionClasses.LastFM import SimilarArtist
from functionClasses.Lenny import LennyFaceHandler

COMMAND_CHAR = '!'


class MessageHandler:

    def __init__(self, bot):
        self.math_parser = NumericStringParser()
        self.pprinter = pprint.PrettyPrinter(indent=4)
        self.bot = bot
        self.enable_bot = False
        self.last_msg = long(str(time.time()).split('.')[0])
        self.scheduler = Scheduler()
        self.scheduler.start()

        self.command_dict = dict()
        self.help_dict = dict()
        self.command_admin_permission = dict()
        self.command_enable_permission = dict()

        # add commands as needed
        self.register_command('enable', self.enable_bot_cmd, admin_only=True, enable_independent=True)
        self.register_command('disable', self.disable_bot_cmd, admin_only=True)
        self.register_command('join', self.join_cmd, admin_only=True)
        self.register_command('help', self.help_cmd, help='Display this message')

        self.register_command('math', MathHandler.MathHandler(self.bot, self.math_parser).handle,
                                help='Executes basic mathematics statements')
        self.register_command('image', ImageSearch.ImageSearch(self.bot).handle,
                                help='Finds and displays the requested image from the internet.')
        self.register_command('mtg', MagicHandler.MagicTheGatheringHandler(self.bot).handle,
                                help='Finds and displays the requested Magic: The Gathering card.')
        self.register_command('wiki', WikipediaHandler.WikipediaHandler(self.bot).handle,
                                help='Finds and displays the requested wikipedia article, if it exists.')
        self.register_command('netrunner', NetrunnerHandler.NetrunnerHandler(self.bot).handle,
                                help='Finds and displays the requested Android: Netrunner card.')
        self.register_command('remind', self.remindme_cmd,
                                help='Reminds the user after the requested time period.')
        self.register_command('similarartist', SimilarArtist.SimilarArtist(self.bot).handle,
                                help='Displays a similar artist to the listed one.')
        self.register_command('lenny', LennyFaceHandler.LennyFaceHandler(self.bot).handle,
                                help='Finds and displays a random Lenny Face.')
        self.register_command('roll', RollHandler.RollHandler(self.bot).handle,
                                help='Rolls Y X-sided dice with the phrasing !roll YdX')
        self.register_command('translate', TranslateHandler.TranslateHandler(self.bot).handle,
                                help='Translates a phrase from one language to another. \nUse   '
                                     ' phrase|from_language|to_language \n'
                                     'OR phrase|to_language to translate to another language and trust in language auto-detection\n'
                                     'OR just phrase if you want to translate to English and still trust auto-detection. \n')
        print('Bot started')

    def register_command(self, command_string, message_handler, help=None,
                                admin_only=False, enable_independent=False):
        self.command_dict[command_string] = message_handler

        if not admin_only:
            self.help_dict[command_string] = help

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

            reply_msg = handler(split_str, from_name_full, msg)

            print("command %s by %s" % (command, from_name_full))

            if reply_msg is not None:
                self.bot.reply_room(msg, reply_msg)

    def enable_bot_cmd(self, message, from_name_full, msg_obj):
        self.enable_bot = True
        return "Functions Enabled"

    def disable_bot_cmd(self, message, from_name_full, msg_obj):
        self.enable_bot = False
        return "Functions Disabled"

    def join_cmd(self, message, from_name_full, msg_obj):
        room_name = ' '.join(message[1:])
        if self.bot.join_room_by_name(room_name):
            self.bot.reply_room(msg_obj, "Joining room '%s'" % room_name)
        else:
            self.bot.reply_room(msg_obj, "Could not find room")

    def help_cmd(self, message, from_name_full, msg_obj):
        returned_message = ""
        for help_message in self.help_dict.items():
            returned_message = returned_message + help_message[0] + ' : ' + help_message[1] + '\n'
        return returned_message

    def remindme_cmd(self, message, from_name_full, msg_obj):
        remind_date_text = ' '.join(message[1:])
        self.scheduler.schedule_job(remind_date_text,
                                    RemindMeHandler.RemindMeHandler(self.bot, from_name_full, msg_obj).job)

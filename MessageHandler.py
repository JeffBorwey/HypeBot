# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 14:29:29 2015

@author: jborwey
"""
from NumericStringParsing import NumericStringParser
import pprint
import re
from hypchat import HypChat
import time

class MessageHandler:
    
    
    def __init__(self, bot, enable_seed):
        self.math_parser = NumericStringParser()
        self.pprinter = pprint.PrettyPrinter(indent=4)
        self.bot = bot
        self.enable_bot = False
        self.enable_seed = enable_seed
        self.last_msg = long(str(time.time()).split('.')[0])
        self.hc = HypChat("gRtEMnmibuedVa4iHnBSylYI2pJ8TPKwpBqjTtgP")
        print('Random start seed:' + enable_seed)
        
    
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

            #admin commands can only be invoked by the user
            if from_name_full == self.bot.nickname:
                if message_body == '!enable ' + self.enable_seed:
                    print('Enabling Bot')
                    self.enable_bot = True
                    self.bot.reply_room(msg, 'Functions now enabled')
                elif message_body == '!disable' + self.enable_seed:
                    print('Disabling Bot')
                    self.enable_bot = False
                    self.bot.reply_room(msg, 'Functions now disabled')
                
                if self.enable_bot == True:
                    if split_str[0] == '!join':
                        room_name = ' '.join(split_str[1:])
                        room_to_join = self.hc.get_room(room_name)
                        if room_to_join == None:
                            self.bot.reply_room(msg, "Could not find room")
                        else:
                            xmpp_jid = room_to_join['xmpp_jid']
                            self.bot.reply_room(msg, "Joining room '%s'" % room_to_join['name'])
                            self.bot.join_room(xmpp_jid)
                
            if self.enable_bot == False:
                return None

            #Normal commands
            #should break this out into another function
            if self.enable_bot == True and message_body[0] == '!':
                if split_str[0] == '!math':
                    args = ' '.join(split_str[1:])
                    self.handle_math(from_name_full,args,msg)

              
    def handle_math(self, name, math_str, msg):
        answer = self.math_parser.eval(math_str)
        self.bot.reply_room(msg, '%s, the answer is %f' % (name, answer))
        
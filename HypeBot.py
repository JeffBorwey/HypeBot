#Requires SleekXMPP, dnspython, pyasn1-modules, hypchat

import logging
import codecs
import time
from MessageHandler import MessageHandler
from threading import Thread
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
import uuid

#https://nisc.hipchat.com/account/xmpp
USER_ROOM_NICKNAME = 'First Last'
#Jabber ID
USER_JID = '123456_1234567@chat.hipchat.com'
#Login password
USER_PWD = 'password'

class HypeBot(ClientXMPP):

    def __init__(self, jid, password, nickname):
        ClientXMPP.__init__(self, jid, password)

        self.nickname = nickname

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0045') # MUC
        self.register_plugin('xep_0060') # PubSub
        
        self.msg_handler = MessageHandler(self, str(uuid.uuid1()))


    def session_start(self, event):
        self.get_roster()
        self.send_presence()

    #Join a hipchat room
    def join_room(self, room_jid):
        self.plugin['xep_0045'].joinMUC(room_jid, self.nickname, wait=True)


    def reply_room(self, msg, body):
            self.send_message(mto = msg['from'].bare, mbody = body, mtype = 'groupchat')


    def message(self, msg):
        self.msg_handler.handle(msg)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

    xmpp = HypeBot(USER_JID, USER_PWD, USER_ROOM_NICKNAME)
    xmpp.connect()
    xmpp.process(block=False)
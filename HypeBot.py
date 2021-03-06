# Requires SleekXMPP, dnspython, pyasn1-modules, hypchat

from MessageHandler import MessageHandler
from hypchat import HypChat
from sleekxmpp import ClientXMPP
import ConfigParser

CONFIG_FILE = 'hypebot.conf'

CONFIG_AUTH = 'Authentication'
CONFIG_GENERAL = 'General'


class HypeBot(ClientXMPP):
    def __init__(self, config_file):
        # setup configuration
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)

        self.user_nickname = self.config.get(CONFIG_AUTH, 'user_nickname')
        self.user_jid = self.config.get(CONFIG_AUTH, 'user_jid')
        self.user_pwd = self.config.get(CONFIG_AUTH, 'user_pwd')
        self.user_api_token = self.config.get(CONFIG_AUTH, 'user_api_token')

        # setup xmpp client
        ClientXMPP.__init__(self, self.user_jid, self.user_pwd)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

        # register plugins for additional functionality
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0004')  # Data Forms
        self.register_plugin('xep_0045')  # MUC
        self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0199')  # Ping

        # Setup message handler
        self.msg_handler = MessageHandler(self)

        # Setup HypChat api client
        self.hc = HypChat(self.user_api_token)

        # get jid to room map
        self.jid_to_room = dict()

        # Join rooms on startup
        startup_rooms = self.config.get(CONFIG_GENERAL, 'startup_rooms_to_join').split(',')
        for room in startup_rooms:
            self.join_room_by_name(room)

        print('Bot initialized')

    def session_start(self, event):
        self.get_roster()
        self.send_presence(ppriority=0)

        # enable keepalive, times are in seconds
        self.plugin['xep_0199'].enable_keepalive(interval=30, timeout=30)

    def populate_jid_to_room(self, room_name):
        room = self.hc.get_room(room_name)
        self.jid_to_room[room['xmpp_jid']] = room
        return room
        # rooms = self.hc.rooms()
        # room_list = list(rooms.contents())
        # for room in room_list:
        #     room_self = room.self()
        #     self.jid_to_room[room_self['xmpp_jid']] = room

    # Join a hipchat room
    def join_room(self, room_jid):
        self.plugin['xep_0045'].joinMUC(room_jid, self.user_nickname, maxhistory=None, wait=True)

    def join_room_by_name(self, room_name):
        # Populate a map from jid to room
        # and return the room at the same time
        # this should help with rate-limiting on api calls
        print("Joining room: " + room_name)
        room_to_join = self.populate_jid_to_room(room_name)
        if room_to_join is None:
            return False

        self.join_room(room_to_join['xmpp_jid'])
        return True

    def reply_room_name(self, room_name, body):
        room_to_reply = self.hc.get_room(room_name)
        if room_to_reply is None:
            return False
        self.send_message(mto=room_name, mbody=body, mtype='groupchat')
        return True

    def reply_room(self, msg, body):
        print(msg['from'].bare)
        self.send_message(mto=msg['from'].bare, mbody=body, mtype='groupchat')

    def message(self, msg):
        self.msg_handler.handle(msg)

    def notify_room_html(self, text, jid):
        self.jid_to_room[jid].notification(text, format='html')

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(levelname)-8s %(message)s')

    xmpp = HypeBot(CONFIG_FILE)
    xmpp.connect()
    xmpp.process(block=False)

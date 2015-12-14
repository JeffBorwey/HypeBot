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

        # Join rooms on startup
        startup_rooms=self.config.get(CONFIG_GENERAL,'startup_rooms_to_join').split(',')
        for room in startup_rooms:
            self.join_room_by_name(room)

    def session_start(self, event):
        self.get_roster()
        self.send_presence()

        # enable keepalive, times are in seconds
        self.plugin['xep_0199'].enable_keepalive(interval=30, timeout=60)

    # Join a hipchat room
    def join_room(self, room_jid):
        self.plugin['xep_0045'].joinMUC(room_jid, self.user_nickname, wait=True)

    def join_room_by_name(self, room_name):
        room_to_join = self.hc.get_room(room_name)
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

    def notify_room_html(self, text):
        self.hc.get_room('Hypebot').notification(text, format='html')

    def notify_room(self, text, format):
        self.hc.get_room('Hypebot').notification(text, format=format)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(levelname)-8s %(message)s')

    xmpp = HypeBot(CONFIG_FILE)
    xmpp.connect()
    xmpp.process(block=False)

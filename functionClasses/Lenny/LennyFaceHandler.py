# Generate a lenny face

import urllib2
from functionClasses import AbstractHandler
from lxml import html
import random

LENNY_SEARCH_URL = 'http://textsmili.es/?cr=1'
LENNY_SEARCH_2 = 'https://textfac.es'


class LennyFaceHandler(AbstractHandler.AbstractHandler):

    def __init__(self, input_bot):
        AbstractHandler.AbstractHandler.__init__(self)
        self.bot = input_bot
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    def handle(self, message, from_name_full, msg_obj):
        # message should be sanitised
        html_str = self.opener.open(LENNY_SEARCH_2).read()

        tree = html.fromstring(html_str)
        buttons = tree.xpath("//button[@class = 'facebtn center-block btn-material btn-material-default ']")
        rand_index = random.randint(0, len(buttons)-1)
        face = buttons[rand_index].attrib['data-clipboard-text']
        return face

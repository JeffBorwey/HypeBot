# Generate a lenny face

import urllib2
from functionClasses import AbstractHandler
from lxml import html

LENNY_SEARCH_URL = 'http://textsmili.es/?cr=1'


class LennyFaceHandler(AbstractHandler.AbstractHandler):

    def __init__(self, input_bot):
        AbstractHandler.AbstractHandler.__init__(self)
        self.bot = input_bot
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    def handle(self, message, from_name_full, msg_obj):
        # message should be sanitised
        html_str = self.opener.open(LENNY_SEARCH_URL).read()

        tree = html.fromstring(html_str)
        button = tree.xpath("//button[@class = 'btn btn-default unicomp-do-copy']")
        print(vars(button))
        print(vars(button.attrib))
        face = button.attrib['data-clipboard-text']
        return face

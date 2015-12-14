import urllib2
import random
from functionClasses import AbstractHandler
from lxml import html
from utils.UrlUtils import convertRawStringToURL

ARTIST_SEARCH_URL = 'http://www.last.fm/music/{query}/+similar'


class SimilarArtist(AbstractHandler.AbstractHandler):

    def __init__(self, input_bot):
        AbstractHandler.AbstractHandler.__init__(self)
        self.bot = input_bot
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    def handle(self, message, from_name_full, msg_obj):
        args = ' '.join(message[1:])

        # message should be sanitised
        search_url = ARTIST_SEARCH_URL.replace("{query}", args.replace(' ', '+'))

        html_str = self.opener.open(search_url).read()

        if '404 - Page Not Found' in html_str:
            return "Could not find Artist '%s'" % args

        tree = html.fromstring(html_str)
        isrmc = tree.xpath("//p[@class = 'grid-items-item-main-text']")
        rand_index = random.randint(0, len(isrmc)-1)
        artist = "".join(isrmc[rand_index].itertext()).strip()
        return 'Similar artist: ' + artist

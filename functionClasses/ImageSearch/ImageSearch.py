import urllib2
import random
from functionClasses import AbstractHandler
from lxml import html
from utils.UrlUtils import convertRawStringToURL

GOOGLE_IMAGE_SEARCH_URL = 'https://www.google.com/search?q={query}&tbm=isch'


class ImageSearch(AbstractHandler.AbstractHandler):

    def __init__(self, input_bot):
        AbstractHandler.AbstractHandler.__init__(self)
        self.bot = input_bot
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    def handle(self, message, from_name_full, msg_obj):
        args = ' '.join(message[1:])

        # message should be sanitised
        search_url = GOOGLE_IMAGE_SEARCH_URL.replace("{query}", convertRawStringToURL(args))

        html_str = self.opener.open(search_url).read()

        tree = html.fromstring(html_str)
        isrmc = tree.xpath("//table[@class = 'images_table']//tr//td//a//img")

        rand_index = random.randint(0, len(isrmc)-1)
        for links in isrmc:
            print(links.attrib['src'])

        url = isrmc[rand_index].attrib['src']
        self.bot.notify_room_html("<img src='" + url + "' />")

        return "Image: %s" % url

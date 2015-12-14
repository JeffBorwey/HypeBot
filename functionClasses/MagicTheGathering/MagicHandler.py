from functionClasses import AbstractHandler
from utils import UrlUtils
from utils.WebserviceTools import WebserviceTools


class MagicTheGatheringHandler(AbstractHandler.AbstractHandler):

    def __init__(self, bot):
        AbstractHandler.AbstractHandler.__init__(self)
        self.bot = bot

    def handle(self, message, from_name_full):
        card_name =' '.join(message[1:])
        soup = self.create_url(card_name)
        return self.find_card(soup, from_name_full, card_name)

    def create_url(self, card_name):
        modified_name = UrlUtils.convertRawStringToURL(card_name)
        url = 'http://sales.starcitygames.com/cardsearch.php?singlesearch=%s' % modified_name
        soupUtils = WebserviceTools()
        soupForCard = soupUtils.getPageAsBeautifulSoup(url)
        return soupForCard

    def find_card(self, soup, name, card_name):
        # if len(soup.findAll(text='zero results')) == 0:
        #     return '%s, could not find any card named %s' % (name, card_name)
        # else:
        fixed_name = card_name.replace("'", "\\")
        div = soup.findAll('img', {'alt' : fixed_name})
        if len(div) == 0:
            return '%s, could not find any card named %s' % (name, card_name)
        else:
            possibleImage = div[0]['src']
            if possibleImage != None:
                return 'Hey %s, I found %s: %s' % (name, card_name, possibleImage)


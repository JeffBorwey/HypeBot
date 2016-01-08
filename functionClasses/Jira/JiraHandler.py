from functionClasses import AbstractHandler
from utils import UrlUtils
from utils.WebserviceTools import WebserviceTools


class JiraHandler(AbstractHandler.AbstractHandler):

    def __init__(self, bot):
        AbstractHandler.AbstractHandler.__init__(self)
        self.bot = bot

    def handle(self, message, from_name_full):
        jira_issue =' '.join(message[1:])



        soup = self.create_url(card_name)
        return self.find_card(soup, from_name_full, card_name)


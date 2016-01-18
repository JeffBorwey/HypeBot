from functionClasses import AbstractHandler
from utils.WebserviceTools import WebserviceTools


class WikipediaHandler(AbstractHandler.AbstractHandler):

    def __init__(self, input_bot):
        AbstractHandler.AbstractHandler.__init__(self)

    def handle(self, message, from_name_full, msg_obj):
        response = self.get_extract_response(message)
        pages = response['query']['pages']
        if '-1' in pages.keys():
            return "%s, The page %s doesn't seem to exist..." % (from_name_full, ' '.join(message[1:]))
        else:
            query = ' '.join(message[1:])
            query = query.replace(' ', '_')
            response = 'https://en.wikipedia.org/wiki/%s' % query
            return '%s, I found the article you requested: %s' % (from_name_full, response)

    # Pulls from the Wikimedia API.  See https://www.mediawiki.org/wiki/API:Main_page for documentation.
    def get_extract_response(self, message):
        args = ' '.join(message[1:])
        url = 'https://en.wikipedia.org/w/api.php?'
        params = {'format': 'json', 'action':'query', 'prop':'extracts', 'titles': args}
        utils = WebserviceTools()
        response = utils.getJsonResponse(url, params)

        return response
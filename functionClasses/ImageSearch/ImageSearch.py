import random
from functionClasses import AbstractHandler
from googleapiclient.discovery import build


class ImageSearch(AbstractHandler.AbstractHandler):

    def __init__(self, input_bot, dev_key, engine_id):
        AbstractHandler.AbstractHandler.__init__(self)
        self.bot = input_bot
        self.dev_key = dev_key
        self.engine_id = engine_id
        self.service = build("customsearch", "v1", developerKey=self.dev_key)

    def handle(self, message, from_name_full, msg_obj):
        args = ' '.join(message[1:])

        res = self.service.cse().list(q=args, cx=self.engine_id,).execute()
        res_items = res['items']
        rand_idx = random.randint(0, len(res_items)-1)
        img_url = res_items[rand_idx]['pagemap']['cse_image'][0]

        return 'Here is your image: ' + img_url['src']
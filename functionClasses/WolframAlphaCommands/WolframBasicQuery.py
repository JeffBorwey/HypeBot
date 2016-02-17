from functionClasses import AbstractHandler
import urllib
import uuid
from utils import ImageUtils
import os

MAX_IMG_HEIGHT = 1000


class WolframAlphaBasicQueryHandler(AbstractHandler.AbstractHandler):

    def __init__(self, input_bot, input_client):
        AbstractHandler.AbstractHandler.__init__(self)
        self.bot = input_bot
        self.client = input_client

    def handle(self, message, from_name_full, msg_obj):
        args = ' '.join(message[1:])
        res = self.client.get_query(args)

        for pod in res.pods:
            print(pod.id)

        notify_message = "%s, This is what I found for you:" % from_name_full

        for pod in res.pods:
            if pod.img is not None:
                img_url = pod.img
                pod_id = pod.id
                # download the image to see its size
                img_file_name = str(uuid.uuid1()) + '.gif'
                urllib.urlretrieve(img_url, img_file_name)
                (width, height) = ImageUtils.get_image_size(img_file_name)
                print "Width: %d Height: %d" % (width, height)
                if width is not None and height is not None and height < MAX_IMG_HEIGHT:
                    notify_message += "<br><strong>%s</strong><br><img src='%s'/>" % (pod_id, img_url)
                os.remove(img_file_name)

        self.bot.notify_room_html(notify_message, msg_obj['from'].bare)
        return
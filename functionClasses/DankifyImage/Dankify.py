import urllib
import uuid
from PIL import Image
import cv2
import numpy as np
from pgmagick import Image as PGImage, ImageList
import os
from functionClasses import AbstractHandler
from gifextract import process_image


def save_files(png_list, save_name):
    print("Saving files to gif:%s" % save_name)
    imgs = ImageList()
    for file_name in png_list:
        im = PGImage(file_name)
        imgs.animationDelayImages(5)
        imgs.append(im)

    imgs.writeImages(save_name)


def colorizer_with_transparency(f_name, offset):
    image_rgba = cv2.imread(f_name, cv2.IMREAD_UNCHANGED)
    height,width, depth = image_rgba.shape
    print("Colorize image (%d,%d,%d)" % (height, width, depth))
    if depth == 3:
        image_rgb = image_rgba
    elif depth == 4:
        image_rgb = cv2.cvtColor(image_rgba, cv2.COLOR_BGRA2RGB)
    image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
    image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    image_hsv[:,:,0] = image_gray
    image_hsv[:,:,0] = image_hsv[:,:,0] * (180.0/256.0)
    image_hsv[:,:,0] = np.mod(image_hsv[:,:,0] + offset + 180, 180)
    image_hsv[:,:,1] = 255
    image_hsv[:,:,2] = 255

    image_rgb = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2RGB)
    image_rgba[:,:,0] = image_rgb[:,:,0]
    image_rgba[:,:,1] = image_rgb[:,:,1]
    image_rgba[:,:,2] = image_rgb[:,:,2]
    return image_rgba


def colorize_file(input_file_name, _input_file_type, max_frames=10):
    # ToDo: split animated images up into different frames and colorize individually
    # ToDo: resize images to some maximum size (to prevent really large images)
    gif_frame_names = list()
    input_file = input_file_name
    input_file_type = _input_file_type
    for x in range(0, max_frames):
        i = int((180.0/max_frames)*x)

        save_name = '%s_%d.%s'%(input_file, i, input_file_type)
        img = colorizer_with_transparency('%s.%s' % (input_file, input_file_type), i)
        abc = Image.fromarray(np.uint8(img)).save(save_name)
        gif_frame_names.append(save_name)

    save_files(gif_frame_names, '%s_dank.gif' % input_file)
    for file_name in gif_frame_names:
        os.remove(file_name)
    return '%s_dank.gif' % input_file


class Dankify(AbstractHandler.AbstractHandler):

    def __init__(self, input_bot, imgur_client):
        AbstractHandler.AbstractHandler.__init__(self)
        self.bot = input_bot
        self.imgur_client = imgur_client

    def handle(self, message, from_name_full, msg_obj):
        url = message[1]

        # download the image
        split = url.split('.')
        extension = split[-1]
        file_name = str(uuid.uuid4())
        file_name_with_extension = file_name + '.' + extension
        if extension != 'png' and extension != 'gif' and extension != 'jpg':
            return 'Invalid image type'

        urllib.urlretrieve(url, file_name_with_extension)
        dank_image_path = colorize_file(file_name, extension)
        uploaded_link = self.imgur_client.upload_file(dank_image_path)

        os.remove(file_name_with_extension)
        os.remove(dank_image_path)

        return 'Here is your image: ' + uploaded_link

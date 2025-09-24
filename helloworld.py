import os
import time

from lib.waveshare_epd import epd7in5_V2

from PIL import Image, ImageDraw, ImageFont

pic_dir = 'pic' # Points to pic directory

display = epd7in5_V2.EPD()
display.init()
display.Clear()

body = ImageFont.truetype(os.path.join(pic_dir, 'Roboto-Regular.ttf'), 18)

image = Image.new(mode='1', size=(800,480), color=255)
draw = ImageDraw.Draw(image)
draw.text((0, 0), 'Quoth the Raven',
          font=body, fill=0, align='left')

display.display(display.getbuffer(image))

#blackbird = Image.open('pic/IMG_5758.JPG')
#image.paste(blackbird, (0, 0))

#display.display(display.getbuffer(image))

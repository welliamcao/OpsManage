#!/usr/bin/env python
#coding:utf8
# fork from https://github.com/phodal-archive/text2logo
import os, random
from PIL import Image, ImageDraw, ImageFont

class Avatar(object):
    def __init__(self):
        super(Avatar, self).__init__()  
        self.width = 128
        self.height = 128
        self.font_size = 24
        self.en_text_length = 13
        self.zh_text_length = 22
        self.zh_text_size = 3
        self.offset = 8  
        self.font = ImageFont.truetype(os.getcwd() + '/static/font-awesome/fonts/NotoSansCJKsc-Regular.otf', self.font_size)      
    
    def randomColor(self):
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
        
    def circle_avatar(self,im, rad):
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        image = ImageDraw.Draw(circle)
        image.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im


    def cal_text_length(self,text):
#         if chardet.detect(text).get('encoding') == 'utf-8':
#         w = self.zh_text_length * text.__len__() / self.zh_text_size + self.offset
#         else:
        w = self.en_text_length * text.__len__()
        return w
    
    
    def generate_image(self,text, filePath, background_color=(105,139,105), fill_color=(255,255,255)):
        img = Image.new('RGB', (self.width, self.height), background_color)
        draw = ImageDraw.Draw(img)
        text_to_draw = text.encode('utf-8').decode('unicode_escape')  
        w = self.cal_text_length(text)
        draw.text(((self.width - w) / 2, (self.height - self.font_size) / 2), text_to_draw, font=self.font, fill=fill_color)
        del draw
        img = self.circle_avatar(img, 20)
        if os.path.isdir(os.path.dirname(filePath)) is not True:os.makedirs(os.path.dirname(filePath))
        img.save(filePath)

AVATAR =  Avatar()

if __name__ == '__main__':   
    AVATAR.generate_image('中','./ops.png',(72,118,255),'white')
from PIL import Image
import uuid
from os.path import join
import os
import glob

def resize_images(table):
    new_images = []
    for row in table:
        path = row[1]
        basewidth = 150
        filename = str(uuid.uuid4())
        img = Image.open(path)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        filepath = "static/temp/{}.bmp".format(filename)
        new_images.append(filepath)
        img.save(join("tool/", filepath))
    return new_images


def remove_images(imgs):
    print("Deletando arquivos!!!")
    for img in imgs:
        print(os.getcwd()+'/tool/'+img)
        if os.path.exists(os.getcwd()+'/tool/'+img):
            os.remove(os.getcwd()+'/tool/'+img)

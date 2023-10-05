from PIL import Image
from random import randint
import os


def save_picture(picture , name , folder):

    _, f_ext = os.path.splitext(picture)
    picture_fn = name +str(randint) + f_ext
    print(picture_fn)
    path = 'static/assets/img/' + folder
    picture_path = os.path.join(app.root_path,path,picture_fn)
    i = Image.open(picture)
    i.save(picture_path)

    return picture_fn
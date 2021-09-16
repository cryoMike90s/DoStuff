import os
import secrets
from PIL import Image
from DoStuff import current_app


def save_image(form_picture):
    """Function which takes the picture path from account post form, changes it name to avoid repetition, changes
        it size into 125x125px to lighten server usage and then save it"""

    random_name = secrets.token_hex(8)
    _, picture_extension = os.path.splitext(form_picture.filename)
    new_picture_name = random_name + picture_extension
    path_name = os.path.join(current_app.root_path, 'static/images/', new_picture_name)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(path_name)
    return new_picture_name

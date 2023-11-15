import functools
from PIL import Image


def to_pil(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        img_array = func(*args, **kwargs)

        pil = Image.fromarray(img_array)

        return pil

    return wrapper

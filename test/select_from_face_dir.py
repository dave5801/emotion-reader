"""Reusable File Directory contents."""

import os
from os import listdir
from os.path import isfile, join


def select_from_face_dir(filepath):
    if not os.path.isdir(filepath):
        return "Invalid File Path"

    return [f for f in listdir(filepath) if isfile(join(filepath, f))]


if __name__ == '__main__':
    directory = "nicholas_cage"
    image_contents = select_from_face_dir(directory)
    print(image_contents)

    
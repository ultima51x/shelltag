# Copyright 2010 David Hwang
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#

"""
These are some helper functions for tests.
"""

import shutil
import os
import os.path

front = "../test/data/original/front.jpg"
back = "../test/data/original/back.jpg"
pathlist = [
        "../test/data/2010 - The Noise",
        "../test/data/test.mp3",
        "../test/data/front.jpg",
        "../test/data/back.jpg"
]

def copymp3(filename):
    """
    Copies a test mp3 to a testfile called test.mp3. Valid inputs include:
    "empty.mp3"
    "id3v1.mp3"
    "id3v23.mp3"
    "id3v24art.mp3"
    "id3v24noart.mp3"
    "id3v123.mp3"
    "id3v124.mp3"
    """
    shutil.copyfile(
        "../test/data/original/" + filename,
        "../test/data/test.mp3")

def copyfolder():
    shutil.copytree("../test/data/original/2010 - The Noise",
            "../test/data/2010 - The Noise")

def clear():
    """
    Deletes all files which exist under pathlist
    """
    for path in pathlist:
        if os.path.exists(path):
            if os.path.isdir(path): shutil.rmtree(path)
            else: os.remove(path)


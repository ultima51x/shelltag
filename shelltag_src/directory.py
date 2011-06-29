# Copyright 2010 David Hwang
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#

"""
This module contains functions pertaining to directories and paths.
"""

import os
import os.path
import sys

def getlist(path, reversal = False):
    """
    Returns a list of filenames of mp3s of absolute path of given directory
    path.

    Attributes:
    path - string of pathname in absolute or relative
    reversal - True = reverse order, False = do not reverse
    """
    rootdir = os.getcwd()   #TODO getcwdu - unicode version
    os.chdir(path)
    filelist = os.listdir(path)
    
    if reversal == True:
        filelist.reverse()
    absfilelist = []
    for file in filelist:
        if file[-4:] == ".mp3": absfilelist.append(os.path.abspath(file))

    os.chdir(rootdir)
    return absfilelist

def getlistwithsubdirectory(path, reversal = False):
    """
    Returns a list of filenames of mp3s of absolute path of a given
    directory, including subdirectories.

    Attributes:
    path - string of pathname in absolute or relative
    reversal - True = reverse order, False = do not reverse
    """
    filelist = []
    for root, dirs, files in os.walk(os.path.abspath(path)):
        for name in files:
            if name[-4:] == ".mp3":
                filelist.append(os.path.join(root,name))
                print os.path.join(root,name)
    if reversal == True: filelist.reverse()
    return filelist
            

# Copyright 2010 David Hwang
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#

"""
This is a script/program for the shelltag command-line tagging program.
"""

from optparse import OptionParser
import sys
import os
import os.path
import time
import sys

import shelltag_src.id3tag as id3tag
import shelltag_src.directory as directory

def processfile(options, filename='', value=None):
    try: filetag = id3tag.ID3Tag(filename)
    except: return
    
    #--delete
    if options.deletetag == True:
        filetag.removetag()
    #--create
    if options.createtag == True:
        filetag = tag.ID3v24(filename)
    #--remove
    if options.removefield != None:
        filetag.removefield(options.removefield)   
    #--removeart
    if options.removeart == True:
        filetag.removefield("PICTURE")
    #--removepriv
    if options.removepriv == True:
        filetag.removefield("PRIVATE")
    #--add
    if options.addfield != None:
        if value == None:
            raise Exception, "No value given."
        filetag.addfield(options.addfield,value)
    #--save
    if options.save == True:
        filetag.savetag()
    #--delay
    if options.delay != None:
        time.sleep(int(options.delay))
    #--info
    if options.info == True:
        filetag.printtag()

def main():
    usage = "Usage: %prog [options] FILENAME VALUE\n\t%prog [options] DIRECTORY VALUE"
    parser = OptionParser(usage=usage)
    #--ORDER OF OPERATIONS
    parser.add_option("-d","--delete", action='store_true', dest="deletetag",
            help="deletes tag from FILENAME")
    parser.add_option("-c","--create", action='store_true', dest="createtag",
            help="creates blank tag in FILENAME")
    parser.add_option("-r","--remove", dest="removefield",
            help="removes FIELDNAME from tag", metavar="FIELDNAME")
    #TODO add option for removing id3v1 only
    parser.add_option("-a","--add", dest="addfield",
            help="adds VALUE onto tag under FIELDNAME", metavar="FIELDNAME")
    parser.add_option("-i","--info", action='store_true', dest="info",
            help="displays information about file's, directory's tag")   
    #--SPECIALITY FEATURES
    parser.add_option("--removeart", action='store_true', dest="removeart",
            help="removes artwork from tag")
    parser.add_option("--removepriv", action='store_true', dest="removepriv",
            help="removes private fields from tag")
    parser.add_option("--save", action='store_true', dest="save",
            help="rewrites tag so that date last modified is updated")
    parser.add_option("--delay", dest="delay",
            help="delays number of seconds after each action", metavar="NUM_OF_SECONDS")
    
    #--DIRECTORY FEATURES
    parser.add_option("-s","--include_subdirectories", action='store_true', dest="subdirectory",
            help="include subdirectories")
    parser.add_option("--reverse_directory", action='store_true', dest="reversedirectory",
            help="reverse directory order")
    
    #--CONVENIENCE FEATURES 
    parser.add_option("-l","--hold", action='store_true', dest="hold",
            help="at end of execution, user has to press enter to exit")
    parser.add_option("-q","--quiet", action='store_true', dest="quiet",
            help="no output")
    (options, args) = parser.parse_args()
   
    #--quiet is enabled -> write to null
    if options.quiet == True:
        sys.stdout = open(os.devnull,'w')

    #--reversedirectory is enabled -> reverse directory reading order
    if options.reversedirectory: reverse = True
    else: reverse = False
    
    try: path = args[0] #file/directory
    except IndexError:
        parser.print_usage()
        return
    try: value = args[1] #value
    except IndexError: value = None
    
    if os.path.isdir(path): #Directory processing
        if options.subdirectory == True:
            pathlist = directory.getlistwithsubdirectory(path, reverse)
        else:
            pathlist = directory.getlist(path, reverse)
        for eachfile in pathlist:
            processfile(options,eachfile,value)
    elif os.path.isfile(path) and path[-4:] == ".mp3":  #File processing
        processfile(options,path,value)
    else:
        raise Exception, "Invalid path given."

    #--hold is enabled -> Press any key to exit.
    if options.hold == True:
        raw_input("Press any key to exit.")

if __name__ == "__main__":
    main()


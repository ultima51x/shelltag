# Copyright 2010 David Hwang
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#

"""
This module holds a ID3Tag class which takes a file and constructs an object
representing the tag.
"""

import os
import sys
import frame as Frame

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError, ID3TimeStamp, TPE1

from compatid3 import CompatID3

class ID3TagInvalidFrame(Exception):
    pass

class ID3TagNoHeaderError(ID3NoHeaderError):
    pass

class ID3Tag(object):
    """
    Tag represents the tag and filename of a mp3 file.

    Attributes:
    filename - name of file the tag's from
    tag - ID3 object defined by the mutagen library
    version - tuple representing id3 version, ex. (2,3,0)->2.3

    Exceptions:
    IOError - invalid or dne filename
    """
    def __init__(self, filename=""):
        """
        Constructs object representing tag of filename given.
        """
        try:
            self.filename = filename
            self.tag = CompatID3(filename)
        except IOError:
            #bad filename error
            raise IOError
        except ID3NoHeaderError:
            #no header error -> report that there's no header, but store None in self.tag
            self.tag = None
            print >> sys.stderr, "shelltag: " + self.filename + ": ID3 tag does not exist. Please create tag first."
            return

    def removetag(self,versions=0):
        """
        Removes ID3 tags.
        
        Attributes:
        versions
            0 removes all tags
            1 removes ID3v1
            2 removes ID3v2
        
        Exceptions:
        ID3TagNoHeaderError - if no id3 tag exists
        """
        if self.tag == None: raise ID3TagNoHeaderError #check for header
        output = ["[DELETE]"]
        
        if versions == 0:   #remove all tags
            self.tag.delete(delete_v1=True,delete_v2=True)
            self.tag = None
            output.append(self.filename + ": all ID3 tag(s) removed.")
        elif versions == 1: #remove v1 only
            self.tag.delete(delete_v1=True,delete_v2=False)
            output.append(self.filename + ": ID3v1 tag removed.")
        elif versions == 2: #remove v2 only
            self.tag.delete(delete_v1=False,delete_v2=True)
            output.append(self.filename + ": ID3v2 tag removed.")
        print ''.join(output)


    #TODO output
    def createtag(self,v1=False,v2=4):
        """
        Creates a "blank" tag onto a file.
        The blank tag consists of TITLE = one blank space.
        
        Attributes:
        v1
            False id3v1 tag removed
            True id3v1 will be added and updated
        v2
            0 id3v2 will be skipped
            3 id3v2.3
            4 id3v2.4        
        """
        #if tag is not empty, delete it
        if self.tag != None: self.tag.delete()

        #tag creation
        self.tag = MP3(self.filename)
        self.tag.add_tags()
        self.tag['TPE1'] = TPE1(encoding=3,text=' ') #adding blank artist
        self.tag.save()

        self.tag = CompatID3(self.filename) #reconstructing
        
        #v1 conditions
        if v1 == True: self.tag.save(v1=2)
        else: self.tag.save(v1=0)

        #v2 conditions
        if v2 == 0: #delete v_2
            self.tag.delete(delete_v1=False,delete_v2=True)
        elif v2 == 3: #convert to v2.3
            self.tag.update_to_v23()
            self.tag.save(v2=3)
            self.tag = CompatID3(self.filename)    #reload tag


    def savetag(self):
        """
        Saves tag onto file.
        Exceptions:
        Exception - undefined errors
        """
        if self.tag == None: raise ID3TagNoHeaderError #no header
        
        if self.tag.version[0] == 1: #by default, 2.4 is added, so remove 2.4
            self.tag.save()
            self.tag.delete(delete_v1=False,delete_v2=True)
        elif self.tag.version[0] == 2 and self.tag.version[1] < 4: #below 2.4
            self.tag.update_to_v23()
            self.tag.save(v2=3)
            self.tag = CompatID3(self.filename) #reload tag
        elif self.tag.version[0] == 2 and self.tag.version[1] == 4:   #2.4
            self.tag.save()
        else:   #undefined
            raise Exception

    def addfield(self,field,string):
        """
        Adds field.
        
        Attributes:
        field - string representing field you wish to addto (example='ARTIST')
        string - string of value to insert

        Exceptions:
        ID3TagInvalidFrame - if field is invalid
        """
        if self.tag == None: raise ID3TagNoHeaderError
        field = field.upper()    #capitalize

        #if v1, reject invalid frames
        if self.tag.version[0] == 1:
            if field not in Frame.v1frames:
                raise ID3TagInvalidFrame
        
        #check for different type of frames
        #note: items delimited by '\\' are divided into muliple-line fields

        output = ["[ADD]"]
        if field in Frame.timeframes.keys():
            listofstrings = unicode(string).split('\\')
            ts = []
            for onestring in listofstrings: #must use ID3TimeStamp in mutagen
                ts.append(ID3TimeStamp(onestring))
            frame = Frame.timeframes[field][Frame.constructor]
            frame.encoding = 0
            frame.text = ts
            self.tag.add(frame)
            output.append(self.filename + ": " + field + "=" + string)
            self.savetag()
        elif field in Frame.urlframes.keys():   #note: mutagen can't support multiline for url
            frame = Frame.urlframes[field][Frame.constructor]
            frame.url = unicode(string)
            self.tag.add(frame)
            output.append(self.filename + ": " + field + "=" + string)
            self.savetag()
        elif field in Frame.textframes.keys():
            frame = Frame.textframes[field][Frame.constructor]
            if frame.encoding != 0: frame.encoding = 3
            frame.text = unicode(string).split('\\')
            self.tag.add(frame)
            output.append(self.filename + ": " + field + "=" + string)
            self.savetag()
        else: #custom frames
            frame = Frame.custom[Frame.constructor]
            frame.encoding = 3
            frame.desc = unicode(field)
            frame.text = unicode(string).split('\\')
            self.tag.add(frame)
            output.append(self.filename + ": " + field + "=" + string)
            self.savetag()
        print ''.join(output)
    
    def getfield(self,field):
        """
        Returns unicode string.

        Attributes:
        field - string representing field you wish to retrieve (example="ARTIST")

        Exceptions:
        KeyError: field does not exist in tag
        ID3TagInvalidFrame: invalid frame
        """
        if self.tag == None: raise ID3TagNoHeaderError
        field = field.upper()    #capitalize

        #urlframes - multiline support does not exist
        if field in Frame.urlframes.keys():
            return self.tag[Frame.urlframes[field][Frame.frame]].url
        #timeframes
        elif field in Frame.timeframes.keys():
            index = Frame.timeframes[field][Frame.frame]
            try:
                returnstring = ''
                id3timestamplist = self.tag[index].text
            except KeyError: raise KeyError
            else:
                if len(id3timestamplist) == 0: return u''
                else:
                    for id3timestamp in id3timestamplist:
                        returnstring = returnstring + id3timestamp.text + '\\'
                    return returnstring[:-1]
        #textframes
        elif field in Frame.textframes.keys():
            index = Frame.textframes[field][Frame.frame]
            try: textlist = self.tag[index].text
            except KeyError: raise KeyError
            else:
                if len(textlist) == 0: return u''
                else: return '\\'.join(textlist)
        #customframes
        elif self.tag.getall('TXXX:' + field) != []:
            try: textlist = self.tag['TXXX:' + field].text
            except KeyError: raise KeyError
            else:
                if len(textlist) == 0: return u''
                else: return '\\'.join(textlist)
        else:   #error
            raise ID3TagInvalidFrame
        
    def clearfield(self,field):
        """
        Sets a field to an empty string.

        Attributes:
        field - field you want set to be ''
        field - string representing field you wish to clear (example="ARTIST")
        """
        if self.tag == None: raise ID3TagNoHeaderError
        field = field.upper()

        self.addfield(field,u'')
        self.savetag()

    def removefield(self,field):
        """
        Removes a field from tag.

        Attributes:
        field - string representing field you wish to remove (example="ARTIST")

        Exceptions:
        KeyError - invalid key
        """
        output = ["[REMOVE]"]

        if self.tag == None: raise ID3TagNoHeaderError
        field = field.upper()

        if field in Frame.urlframes.keys(): #url
            self.tag.delall(Frame.urlframes[field][Frame.frame])
        elif field in Frame.timeframes.keys(): #time
            self.tag.delall(Frame.timeframes[field][Frame.frame])
        elif field in Frame.textframes.keys(): #text
            self.tag.delall(Frame.textframes[field][Frame.frame])
        elif self.tag.getall('TXXX:' + field) != []: #custom
            self.tag.delall('TXXX:' + field)
        else:
            print >> sys.stderr, "shelltag: " + self.filename + ": " + field + "does not exist"
            return
         
        self.savetag()
        output.append(self.filename + ": " + field + " removed.")
        print ''.join(output)

    def printtag(self):
        """
        Prints contents of a tag
        """
        output = []
        output.append(u"[INFO]")
        #filename
        output.append(u" FILENAME=")
        output.append(unicode(self.filename,errors='ignore'))   #TODO hackish
        output.append(u"; ")
        #version
        if self.tag != None:
            output.append(u"VERSION=" + unicode(str(self.tag.version)) + u" ")
        #textframes
        for field in Frame.textframes.keys():
            try: text = self.getfield(field)
            except KeyError: pass
            else: output.append(unicode(field) + u"=" + unicode(text) + u"; ")
        #urlframes
        for field in Frame.urlframes.keys():
            try: url = self.getfield(field)
            except KeyError: pass
            else: output.append(unicode(field) + u"=" + unicode(url) + u"; ")
        #timeframes
        for field in Frame.timeframes.keys():
            try: time = self.getfield(field)
            except KeyError: pass
            else: output.append(unicode(field) + u"=" + unicode(time) + u"; ")
        #customframes
        if len(self.tag.getall('TXXX')) > 0:
            for custom in self.tag.getall('TXXX'): 
                output.append(unicode(custom.pprint()) + u" ")
        #private frames
        if len(self.tag.getall('PRIV')) > 0:
            for private in self.tag.getall('PRIV'): 
                output.append(unicode(private.pprint()) + u" ")
        #picture frames
        if len(self.tag.getall('APIC')) > 0:
            for picture in self.tag.getall('APIC'): 
                output.append(unicode(picture.pprint()) + u" ")
        print (''.join(output)).encode('UTF-8')

if __name__ == "__main__":
    pass


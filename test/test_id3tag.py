# Copyright 2010 David Hwang
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#

"""
This is a unit test module for shelltag_src/id3tag.py.
"""
import sys
import unittest
import shutil
import os

import functions
sys.path.append("../shelltag_src/")
import id3tag
from id3tag import ID3Tag

test = "data/test.mp3"

class ID3TagFileLoading(unittest.TestCase):

    def test_filedoesntexist(self):
        self.assertRaises(IOError,ID3Tag,"blah.mp3")

    def test_filehasnotag(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        self.assertEquals(a.tag,None)

    def test_readtag(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        self.assertEquals(a.tag.version,(1,1))

    def tearDown(self):
        functions.clear()

class ID3RemoveTag(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_removeemptytag(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        self.assertRaises(id3tag.ID3TagNoHeaderError,a.removetag,0)

    def test_removealltags(self):
        functions.copymp3("id3v123.mp3")
        a = ID3Tag(test)
        a.removetag()
        self.assertEquals(a.tag, None)

    def test_removev1only(self):
        functions.copymp3("id3v123.mp3")
        a = ID3Tag(test)
        a.removetag(1)
        self.assertEquals(a.tag.version,(2,3,0))

    def test_removev2only(self):
        functions.copymp3("id3v124.mp3")
        a = ID3Tag(test)
        a.removetag(2)
        b = ID3Tag(test)
        self.assertEquals(b.tag.version,(1,1))

    def tearDown(self):
        functions.clear()

class ID3CreateTag(unittest.TestCase):

    def setup(self):
        pass

    def test_recreate(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.createtag(v1=False)
        b = ID3Tag(test)
        self.assertEquals(b.tag.version,(2,4,0))

    def test_createv1tag(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        a.createtag(v1=True,v2=0)
        b = ID3Tag(test)
        self.assertEquals(b.tag.version,(1,1))

    def test_createv1v23tag(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        a.createtag(v1=True,v2=3)
        b = ID3Tag(test)
        b.removetag(2)
        c = ID3Tag(test)
        self.assertEquals(c.tag.version,(1,1))

    def test_createv1v24tag(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        a.createtag(v1=True,v2=4)
        b = ID3Tag(test)
        b.removetag(2)
        c = ID3Tag(test)
        self.assertEquals(c.tag.version,(1,1))

    def test_createv23tag(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        a.createtag(v1=False,v2=3)
        b = ID3Tag(test)
        self.assertEquals(b.tag.version,(2,3,0))

    def test_createv24tag(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        a.createtag(v1=False,v2=4)
        b = ID3Tag(test)
        self.assertEquals(b.tag.version,(2,4,0))

    def tearDown(self):
        functions.clear()

class ID3SaveTag(unittest.TestCase):

    def setup(self):
        pass

    def test_saveemptytag(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        self.assertRaises(id3tag.ID3TagNoHeaderError,a.savetag)

    def test_savev1tag(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        a.savetag()
        b = ID3Tag(test)
        self.assertEquals(b.tag.version,(1,1))

    def test_savev23tag(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.savetag()
        b = ID3Tag(test)
        self.assertEquals(b.tag.version,(2,3,0))

    def test_savev24tag(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.savetag()
        b = ID3Tag(test)
        self.assertEquals(b.tag.version,(2,4,0))

    def tearDown(self):
        functions.clear()

class ID3AddField(unittest.TestCase):

    def setup(self):
        pass

    def test_emptyadd(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        self.assertRaises(id3tag.ID3TagNoHeaderError,a.addfield,"WWWCOPYRIGHT","blah")

    def test_v1addurl(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        self.assertRaises(id3tag.ID3TagInvalidFrame,a.addfield,"WWWCOPYRIGHT","blah")

    def test_v1adddate(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        a.addfield("YEAR","1992")
        b = ID3Tag(test)
        self.assertEquals("1992",b.tag['TDRC'])

    def test_v1addtext(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        a.addfield("TITLE","Prowler")
        b = ID3Tag(test)
        self.assertEquals("Prowler",b.tag['TIT2'])

    def test_v1addcustom(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        self.assertRaises(id3tag.ID3TagInvalidFrame,a.addfield,"DAVIDISAWESOME","awesome")

    def test_v23addurl(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("WWWCOPYRIGHT","blah")
        self.assertEquals("blah",a.tag.getall('WCOP')[0])

    def test_v23adddate(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("YEAR","1992")
        self.assertEquals("1992",a.tag['TDRC'])

    def test_v23addtext(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("TITLE","Prowler")
        self.assertEquals("Prowler",a.tag['TIT2'])

    def test_v23addcustom(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","Hwang")
        self.assertEquals("Hwang",a.tag['TXXX:DAVID'])

    def test_v24addurl(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("WWWCOPYRIGHT","blah")
        self.assertEquals("blah",a.tag.getall('WCOP')[0])

    def test_v24adddate(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("YEAR","1992")
        self.assertEquals("1992",a.tag['TDRC'])

    def test_v24addtext(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("TITLE","Prowler")
        self.assertEquals("Prowler",a.tag['TIT2'])

    def test_v24addcustom(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","Hwang")
        self.assertEquals("Hwang",a.tag[u'TXXX:DAVID'])

    #url doesn't support multiline
    
    #in this case, the 2nd year seems to disappear
    def test_multiv23adddate(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("YEAR","1992\\2000")
        self.assertEquals("1992",a.tag['TDRC'])

    def test_multiv23addtext(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("TITLE","Prowler\\Yo")
        self.assertEquals("Prowler/Yo",a.tag['TIT2'])

    def test_multiv23addcustom(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","Hwang\\Miles")
        self.assertEquals("Hwang/Miles",a.tag['TXXX:DAVID'])

    def test_multiv24adddate(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("YEAR","1992\\2000")
        from mutagen.id3 import TDRC
        self.assertEquals(TDRC(encoding=0,text=[u'1992',u'2000']),a.tag['TDRC'])

    def test_multiv24addtext(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("TITLE","Prowler\\No Surprises")
        self.assertEquals(["Prowler","No Surprises"],a.tag['TIT2'])

    def test_multiv24addcustom(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","Hwang\\Hello")
        self.assertEquals(["Hwang","Hello"],a.tag[u'TXXX:DAVID'])

    def tearDown(self):
        functions.clear()

class ID3GetField(unittest.TestCase):
    def setup(self):
        pass

    def test_emptygetfield(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        self.assertRaises(id3tag.ID3TagNoHeaderError,a.getfield,'ARTIST')

    def test_v1getdate(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        self.assertEquals("2010",a.getfield('YEAR'))

    def test_v1gettext(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        self.assertEquals("Unknown",a.getfield('ARTIST'))

    def test_v23geturl(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("WWWCOPYRIGHT","blah")
        self.assertEquals("blah",a.getfield('WWWCOPYRIGHT'))

    def test_v23getdate(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        self.assertEquals("2010",a.getfield('YEAR'))

    def test_v23gettext(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        self.assertEquals("Sound 3",a.getfield("TITLE"))

    def test_v24custom(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","HWANG")
        from mutagen.id3 import TXXX
        self.assertEquals(TXXX(desc=u'DAVID',encoding=0,text=[u'HWANG']),a.tag.getall('TXXX:DAVID')[0])

    def test_v24geturl(self):
        functions.copymp3("id3v24noart.mp3")
        a = ID3Tag(test)
        a.addfield("WWWCOPYRIGHT","blah")
        self.assertEquals("blah",a.getfield('WWWCOPYRIGHT'))

    def test_v24getdate(self):
        functions.copymp3("id3v24noart.mp3")
        a = ID3Tag(test)
        self.assertEquals("2010",a.getfield('YEAR'))

    def test_v24gettext(self):
        functions.copymp3("id3v24noart.mp3")
        a = ID3Tag(test)
        self.assertEquals("Avantgarde",a.getfield("GENRE"))

    def test_v24multilinegetdate(self):
        functions.copymp3("id3v24noart.mp3")
        a = ID3Tag(test)
        a.addfield("YEAR","2010\\1999")
        from mutagen.id3 import TDRC
        self.assertEquals(TDRC(encoding=0,text=[u'2010',u'1999']),a.tag['TDRC'])

    def test_v24multilinegettext(self):
        functions.copymp3("id3v24noart.mp3")
        a = ID3Tag(test)
        self.assertEquals("Sound 5\\The Interlude",a.getfield("TITLE"))

    def test_v24custom(self):
        functions.copymp3("id3v24noart.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","HWANG")
        from mutagen.id3 import TXXX
        self.assertEquals(TXXX(desc=u'DAVID',encoding=0,text=[u'HWANG']),a.tag.getall('TXXX:DAVID')[0])

    def tearDown(self):
        functions.clear()

#No tests for clear field...all based on addfield and savetag

class ID3TagRemoveField(unittest.TestCase):

    def test_emptyremovefield(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        self.assertRaises(id3tag.ID3TagNoHeaderError,a.removefield,'ARTIST')
    
    def test_v1removesomethingnotthere(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        a.removefield("WWWCOPYRIGHT")
        self.assertEquals([], a.tag.getall('WCOP'))

    def test_v23removesomethingnotthere(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.removefield("PERFORMER")
        self.assertEquals([], a.tag.getall('PERFORMER'))
    
    def test_v23removeurl(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("WWWCOPYRIGHT","blah")
        a.removefield("WWWCOPYRIGHT")
        self.assertEquals([], a.tag.getall('WCOP'))

    def test_v23removetime(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.removefield("YEAR")
        self.assertEquals([],a.tag.getall('TDRC'))
    
    def test_v23removetext(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.removefield("TITLE")
        self.assertEquals([],a.tag.getall('TIT2'))
    
    def test_v23removecustom(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","HWANG")
        a.removefield("DAVID")
        self.assertEquals([],a.tag.getall('TXXX:DAVID'))
    
    def test_v24removeurl(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("WWWCOPYRIGHT","blah")
        a.removefield("WWWCOPYRIGHT")
        self.assertEquals([], a.tag.getall('WCOP'))

    def test_v24removetime(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.removefield("YEAR")
        self.assertEquals([],a.tag.getall('TDRC'))
    
    def test_v24removetext(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.removefield("TITLE")
        self.assertEquals([],a.tag.getall('TIT2'))
    
    def test_v24removecustom(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","HWANG")
        a.removefield("DAVID")
        self.assertEquals([],a.tag.getall('TXXX:DAVID'))
    
    def test_v24removecover(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.removefield("PICTURE")
        self.assertEquals([],a.tag.getall('APIC'))

    def tearDown(self):
        functions.clear()

if __name__ == '__main__':
    unittest.main()

    def tearDown(self):
        functions.clear()

class ID3SaveTag(unittest.TestCase):

    def setup(self):
        pass

    def test_saveemptytag(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        self.assertRaises(id3tag.ID3TagNoHeaderError,a.savetag)

    def test_savev1tag(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        a.savetag()
        b = ID3Tag(test)
        self.assertEquals(b.tag.version,(1,1))

    def test_savev23tag(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.savetag()
        b = ID3Tag(test)
        self.assertEquals(b.tag.version,(2,3,0))

    def test_savev24tag(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.savetag()
        b = ID3Tag(test)
        self.assertEquals(b.tag.version,(2,4,0))

    def tearDown(self):
        functions.clear()

class ID3AddField(unittest.TestCase):

    def setup(self):
        pass

    def test_emptyadd(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        self.assertRaises(id3tag.ID3TagNoHeaderError,a.addfield,"WWWCOPYRIGHT","blah")

    def test_v1addurl(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        self.assertRaises(id3tag.ID3TagInvalidFrame,a.addfield,"WWWCOPYRIGHT","blah")

    def test_v1adddate(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        a.addfield("YEAR","1992")
        b = ID3Tag(test)
        self.assertEquals("1992",b.tag['TDRC'])

    def test_v1addtext(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        a.addfield("TITLE","Prowler")
        b = ID3Tag(test)
        self.assertEquals("Prowler",b.tag['TIT2'])

    def test_v1addcustom(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        self.assertRaises(id3tag.ID3TagInvalidFrame,a.addfield,"DAVIDISAWESOME","awesome")

    def test_v23addurl(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("WWWCOPYRIGHT","blah")
        self.assertEquals("blah",a.tag.getall('WCOP')[0])

    def test_v23adddate(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("YEAR","1992")
        self.assertEquals("1992",a.tag['TDRC'])

    def test_v23addtext(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("TITLE","Prowler")
        self.assertEquals("Prowler",a.tag['TIT2'])

    def test_v23addcustom(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","Hwang")
        self.assertEquals("Hwang",a.tag['TXXX:DAVID'])

    def test_v24addurl(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("WWWCOPYRIGHT","blah")
        self.assertEquals("blah",a.tag.getall('WCOP')[0])

    def test_v24adddate(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("YEAR","1992")
        self.assertEquals("1992",a.tag['TDRC'])

    def test_v24addtext(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("TITLE","Prowler")
        self.assertEquals("Prowler",a.tag['TIT2'])

    def test_v24addcustom(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","Hwang")
        self.assertEquals("Hwang",a.tag[u'TXXX:DAVID'])

    #url doesn't support multiline
    
    #in this case, the 2nd year seems to disappear
    def test_multiv23adddate(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("YEAR","1992\\2000")
        self.assertEquals("1992",a.tag['TDRC'])

    def test_multiv23addtext(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("TITLE","Prowler\\Yo")
        self.assertEquals("Prowler/Yo",a.tag['TIT2'])

    def test_multiv23addcustom(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","Hwang\\Miles")
        self.assertEquals("Hwang/Miles",a.tag['TXXX:DAVID'])

    def test_multiv24adddate(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("YEAR","1992\\2000")
        from mutagen.id3 import TDRC
        self.assertEquals(TDRC(encoding=0,text=[u'1992',u'2000']),a.tag['TDRC'])

    def test_multiv24addtext(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("TITLE","Prowler\\No Surprises")
        self.assertEquals(["Prowler","No Surprises"],a.tag['TIT2'])

    def test_multiv24addcustom(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","Hwang\\Hello")
        self.assertEquals(["Hwang","Hello"],a.tag[u'TXXX:DAVID'])

    def tearDown(self):
        functions.clear()

class ID3GetField(unittest.TestCase):
    def setup(self):
        pass

    def test_emptygetfield(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        self.assertRaises(id3tag.ID3TagNoHeaderError,a.getfield,'ARTIST')

    def test_v1getdate(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        self.assertEquals("2010",a.getfield('YEAR'))

    def test_v1gettext(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        self.assertEquals("Unknown",a.getfield('ARTIST'))

    def test_v23geturl(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("WWWCOPYRIGHT","blah")
        self.assertEquals("blah",a.getfield('WWWCOPYRIGHT'))

    def test_v23getdate(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        self.assertEquals("2010",a.getfield('YEAR'))

    def test_v23gettext(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        self.assertEquals("Sound 3",a.getfield("TITLE"))

    def test_v24custom(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","HWANG")
        from mutagen.id3 import TXXX
        self.assertEquals(TXXX(desc=u'DAVID',encoding=0,text=[u'HWANG']),a.tag.getall('TXXX:DAVID')[0])

    def test_v24geturl(self):
        functions.copymp3("id3v24noart.mp3")
        a = ID3Tag(test)
        a.addfield("WWWCOPYRIGHT","blah")
        self.assertEquals("blah",a.getfield('WWWCOPYRIGHT'))

    def test_v24getdate(self):
        functions.copymp3("id3v24noart.mp3")
        a = ID3Tag(test)
        self.assertEquals("2010",a.getfield('YEAR'))

    def test_v24gettext(self):
        functions.copymp3("id3v24noart.mp3")
        a = ID3Tag(test)
        self.assertEquals("Avantgarde",a.getfield("GENRE"))

    def test_v24multilinegetdate(self):
        functions.copymp3("id3v24noart.mp3")
        a = ID3Tag(test)
        a.addfield("YEAR","2010\\1999")
        from mutagen.id3 import TDRC
        self.assertEquals(TDRC(encoding=0,text=[u'2010',u'1999']),a.tag['TDRC'])

    def test_v24multilinegettext(self):
        functions.copymp3("id3v24noart.mp3")
        a = ID3Tag(test)
        self.assertEquals("Sound 5\\The Interlude",a.getfield("TITLE"))

    def test_v24custom(self):
        functions.copymp3("id3v24noart.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","HWANG")
        from mutagen.id3 import TXXX
        self.assertEquals(TXXX(desc=u'DAVID',encoding=0,text=[u'HWANG']),a.tag.getall('TXXX:DAVID')[0])

    def tearDown(self):
        functions.clear()

#No tests for clear field...all based on addfield and savetag

class ID3TagRemoveField(unittest.TestCase):

    def test_emptyremovefield(self):
        functions.copymp3("empty.mp3")
        a = ID3Tag(test)
        self.assertRaises(id3tag.ID3TagNoHeaderError,a.removefield,'ARTIST')
    
    def test_v1removesomethingnotthere(self):
        functions.copymp3("id3v1.mp3")
        a = ID3Tag(test)
        a.removefield("WWWCOPYRIGHT")
        self.assertEquals([], a.tag.getall('WCOP'))

    def test_v23removesomethingnotthere(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.removefield("PERFORMER")
        self.assertEquals([], a.tag.getall('PERFORMER'))
    
    def test_v23removeurl(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("WWWCOPYRIGHT","blah")
        a.removefield("WWWCOPYRIGHT")
        self.assertEquals([], a.tag.getall('WCOP'))

    def test_v23removetime(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.removefield("YEAR")
        self.assertEquals([],a.tag.getall('TDRC'))
    
    def test_v23removetext(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.removefield("TITLE")
        self.assertEquals([],a.tag.getall('TIT2'))
    
    def test_v23removecustom(self):
        functions.copymp3("id3v23.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","HWANG")
        a.removefield("DAVID")
        self.assertEquals([],a.tag.getall('TXXX:DAVID'))
    
    def test_v24removeurl(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("WWWCOPYRIGHT","blah")
        a.removefield("WWWCOPYRIGHT")
        self.assertEquals([], a.tag.getall('WCOP'))

    def test_v24removetime(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.removefield("YEAR")
        self.assertEquals([],a.tag.getall('TDRC'))
    
    def test_v24removetext(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.removefield("TITLE")
        self.assertEquals([],a.tag.getall('TIT2'))
    
    def test_v24removecustom(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.addfield("DAVID","HWANG")
        a.removefield("DAVID")
        self.assertEquals([],a.tag.getall('TXXX:DAVID'))
    
    def test_v24removecover(self):
        functions.copymp3("id3v24art.mp3")
        a = ID3Tag(test)
        a.removefield("PICTURE")
        self.assertEquals([],a.tag.getall('APIC'))

    def tearDown(self):
        functions.clear()

if __name__ == '__main__':
    unittest.main()


# Copyright 2010 David Hwang
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#

"""
This module holds dictionaries which can translate common "field" names to its
proper "frame" name.

A frame can consist of the following...

encoding (int): ISO-8859 -> 0, UTF-16 -> 1, UTF-16BE -> 2, UTF-8 -> 3
mime (unicode)): u'image/jpeg' u'image/png'
type (int): other -> 0, front cover -> 2, back cover -> 3
desc (unicode): u'28 Days Later'
data (binary): 'binary data'
text (list of unicode): [u'28 Days Later Soundtrack']
url (text of unicode): u'blah'
"""

from mutagen.id3 import TALB,TBPM,TCMP,TCOM,TCON,TCOP,TDEN,TDLY,TDOR,TDRC,TDRL,TDTG,TENC
from mutagen.id3 import TEXT,TFLT,TIPL,TIT1,TIT2,TIT3,TKEY,TLAN,TLEN,TMCL,TMED,TMOO,TOAL
from mutagen.id3 import TOFN,TOLY,TOPE,TOWN,TPE1,TPE2,TPE3,TPE4,TPOS,TPRO,TPUB,TRCK,TRSN
from mutagen.id3 import TRSO,TSO2,TSOA,TSOC,TSOP,TSOT,TSRC,TSSE,TSST,TXXX

from mutagen.id3 import WCOM,WCOP,WOAF,WOAR,WOAS,WORS,WPAY,WPUB,WXXX

from mutagen.id3 import APIC,COMM,PRIV

frame,constructor = range(0,2)

v1frames = (
    'TITLE',
    'ARTIST',
    'ALBUM',
    'YEAR',
    'COMMENT',
    'TRACK',
    'GENRE'
)

timeframes = {
    #encoding = 0, text = list of ID3TimeStamp
    'ENCODINGTIME': ['TDEN',TDEN()],
    'ORIGYEAR':     ['TDOR',TDOR()],
    'YEAR':         ['TDRC',TDRC()],
    'RELEASETIME':  ['TDRL',TDRL()],
    'TAGGINGTIME':  ['TDTG',TDTG()]
}

urlframes = {
    #url
    'WWWCOMMERCIALINFO':['WCOM',WCOM()],
    'WWWCOPYRIGHT':     ['WCOP',WCOP()],
    'WWWAUDIOFILE':     ['WOAF',WOAF()],
    'WWWARTIST':        ['WOAR',WOAR()],
    'WWWAUDIOSOURCE':   ['WOAS',WOAS()],
    'WWWRADIOPAGE':     ['WORS',WORS()],
    'WWWPAYMENT':       ['WPAY',WPAY()],
    'WWWPUBLISHER':     ['WPUB',WPUB()]
}

textframes = {
    #encoding = 3 or 0, text
    'ALBUM':        ['TALB',TALB()],
    'BPM':          ['TBPM',TBPM(encoding=0)],
    #'TCMP':         ['TCMP',TCMP(encoding=0)],  #not in standard
    'COMPOSER':     ['TCOM',TCOM()],
    'GENRE':        ['TCON',TCON()],
    'COPYRIGHT':    ['TCOP',TCOP()],
    #'TDLY':         ['TDLY',TDLY()],    #TDLY playlist delay
    'ENCODEDBY':    ['TENC',TENC()],
    'LYRICIST':     ['TEXT',TEXT()],
    'FILETYPE':     ['TFLT',TFLT()],
    'INVOLVEDPEOPLE':   ['TIPL',TIPL(people=[])],
    'CONTENTGROUP': ['TIT1',TIT1()],
    'TITLE':        ['TIT2',TIT2()],
    'SUBTITLE':     ['TIT3',TIT3()],
    'INITIALKEY':   ['TKEY',TKEY()],
    'LANGUAGE':     ['TLAN',TLAN()],
    'LENGTH':       ['TLEN',TLEN(encoding=0)],
    'MUSICIANCREDITS':      ['TMCL',TMCL(people=[])],
    'MEDIATYPE':    ['TMED',TMED()],
    'MOOD':         ['TMOO',TMOO()],
    'ORIGALBUM':    ['TOAL',TOAL()],
    'ORIGFILENAME': ['TOFN',TOFN()],
    'ORIGLYRICIST': ['TOLY',TOLY()],
    'ORIGARTIST':   ['TOPE',TOPE()],
    'FILEOWNER':    ['TOWN',TOWN()],
    'ARTIST':       ['TPE1',TPE1()],
    'BAND':         ['TPE2',TPE2()],
    'CONDUCTOR':    ['TPE3',TPE3()],
    'MIXARTIST':    ['TPE4',TPE4()],
    'DISCNUMBER':   ['TPOS',TPOS(encoding=0)],
    #'TPRO':         ['TPRO',TPRO()],        #TPRO Produced notice
    'PUBLISHER':    ['TPUB',TPUB()],
    'TRACK':        ['TRCK',TRCK(encoding=0)],
    'NETRADIOSTATION':  ['TRSN',TRSN()],
    'NETRADIOOWNER':    ['TRSO',TRSO()],
    'BANDSORTORDER':    ['TSO2',TSO2()],
    'ALBUMSORTORDER':   ['TSOA',TSOA()],
    'COMPOSERSORTORDER':['TSOC',TSOC()],
    'ARTISTSORTORDER':   ['TSOP',TSOP()],
    'TITLESORTORDER':   ['TSOT',TSOT()],
    'ISRC':         ['TSRC',TSRC()],
    'ENCODERSETTINGS':  ['TSSE',TSSE()],
    'SETSUBTITLE':  ['TSST',TSST()],
    #encoding, desc, text
    'ALBUM ARTIST': [u'TXXX:ALBUM ARTIST',TXXX(desc=u'ALBUM ARTIST')],
    'PERFORMER': [u'TXXX:PERFORMER',TXXX(desc=u'PERFORMER')],
    'REPLAYGAIN_ALBUM_GAIN': [u'TXXX:replaygain_album_gain',TXXX(desc=u'replaygain_album_gain')],
    'REPLAYGAIN_ALBUM_PEAK': [u'TXXX:replaygain_album_peak',TXXX(desc=u'replaygain_album_peak')],
    'REPLAYGAIN_TRACK_GAIN': [u'TXXX:replaygain_track_gain',TXXX(desc=u'replaygain_track_gain')],
    'REPLAYGAIN_TRACK_PEAK': [u'TXXX:replaygain_track_peak',TXXX(desc=u'replaygain_track_peak')],
    #encoding, lang, desc, text
    'COMMENT': ['COMM',COMM(lang=u'eng', desc=u'')],
    #encoding, mime, type, desc, data
    'CUSTOM':   ['TXXX',TXXX()],
    'PICTURE':  ['APIC',APIC()],
    'PRIVATE':  ['PRIV',PRIV()]
}

#encoding, desc, text
custom = ['TXXX',TXXX()]
#encoding, mime, type, desc, data
private = ['PRIV',PRIV()]
picture = ['APIC',APIC()]

#TODO add support for new TXXX and WXXX frames


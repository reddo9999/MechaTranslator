"""
PyAtlasTranslator

This code is distributed to the Public Domain, with the only requirement on
redistribion that this notice is reproduced in source code form, or that an
acknowledgement to the author given if reproduced in binary form (or other
compiled forms, given that this is Python)

(C) Habisain 2012

Documentation:

Provides the AtlasTranslator class, which provides a nice Pythonic interface
to the Atlas translation program by Fujitsu.
"""

import winreg as winreg
from winreg import HKEY_CURRENT_USER, KEY_READ
import ctypes
from ctypes import c_int, c_char_p, POINTER, byref
import os.path
import win32api
LOAD_WITH_ALTERED_SEATCH_PATH = 0x8 # A constant from microsofts API - has correct effect here

__all__ = ['AtlasTranslator', 'MissingAtlasException', 'AtlasInitErrorException']

atlaskey = r"Software\Fujitsu\ATLAS\V%i.0\EJ"
vkeys = dict([(x, atlaskey.replace('%i', str(x))) for x in range(13, 15)])
intarrayType = (c_int * 2000)

createEngineType = ctypes.CFUNCTYPE(c_int, c_int, c_int, c_int, c_char_p)
destroyEngineType = ctypes.CFUNCTYPE(c_int)
translatePairType = ctypes.CFUNCTYPE(c_int, c_char_p, POINTER(c_char_p), POINTER(c_int), POINTER(c_int))
atlInitEngineDataType = ctypes.CFUNCTYPE(c_int, c_int, c_int, POINTER(intarrayType), c_int, POINTER(intarrayType))
freeAtlasDataType = ctypes.CFUNCTYPE(c_int, c_char_p, c_int, c_int, c_int)

class MissingAtlasException(Exception):
    """Raised if Atlas cannot be found"""

class AtlasInitErrorException(Exception):
    """Raised if Atlas doesn't give expected return values during init"""

def findAtlasPath():
    """Attempt to extract Atlas path from registry"""
    for v in vkeys:
        try:
            key = winreg.OpenKey(HKEY_CURRENT_USER, vkeys[v], 0, KEY_READ)
            val = winreg.QueryValueEx(key, r"TRENV EJ")
            atlasPath = val[0].rpartition('\\')[0]
            return atlasPath
        except:
            pass
    raise MissingAtlasException()


class AtlasTranslator(object):
    """Provides nice methods to translate cp932 strings, as well as unicode strings"""
    def __init__(self, atlasPath = None, direction=2):
        """Intialise the Atlas translation engine
        Args: atlasPath: a path to atlas; will try and figure it out from registry if not given
              direction: 1 = JP to ENG, 2 = ENG to JP
        """
        if atlasPath is None:
            try:
                atlasPath = findAtlasPath()
            except MissingAtlasException:
                print("Could not find ATLAS Translator")

        atlecont  = win32api.LoadLibraryEx(os.path.join(atlasPath, "AtleCont.dll"), 0,  LOAD_WITH_ALTERED_SEATCH_PATH)

        self.createEngine = createEngineType(win32api.GetProcAddress(atlecont, "CreateEngine"))
        self.destroyEngine = destroyEngineType(win32api.GetProcAddress(atlecont, "DestroyEngine"))
        self.translatePair = translatePairType(win32api.GetProcAddress(atlecont, "TranslatePair"))
        self.atlInitEngineData = atlInitEngineDataType(win32api.GetProcAddress(atlecont, "AtlInitEngineData"))
        self.freeAtlasData = freeAtlasDataType(win32api.GetProcAddress(atlecont, "FreeAtlasData"))

        intarray1 = intarrayType()
        intarray2 = intarrayType()
        genString = b'General'
        ret = self.atlInitEngineData(c_int(0), c_int(2), byref(intarray1), c_int(0), byref(intarray2))
        if ret != 0: raise AtlasInitErrorException()
        ret2 = self.createEngine(c_int(1), c_int(direction), c_int(0), c_char_p(genString))
        if ret2 != 1: raise AtlasInitErrorException()

    def __del__(self):
        """Tidy up the Atlas translation engine"""
        self.destroyEngine()

    def raw_translate(self, string):
        """Translate the given cp932 encoded byte string - returns a cp932 encoded byte string"""
        cinput = c_char_p(string)
        unknown1 = c_int(0)
        unknown2 = c_int(0)
        output = c_char_p()
        self.translatePair(cinput, byref(output), byref(unknown1), byref(unknown2))
        pyoutput = output.value.partition(b'\x00')[0]
        self.freeAtlasData(output, c_int(0), c_int(0), c_int(0))
        return pyoutput

    def translate(self, unicodeString):
        """Translate the given string - returns a string"""
        encoded = unicodeString.encode('cp932', errors='ignore')
        encodedRet = self.raw_translate(encoded)
        return encodedRet.decode('cp932', errors='ignore')

if __name__ == '__main__':
    x = AtlasTranslator(direction = 2)
    print(x.translate("A test to see if it still works"))

from . import habisainAtlas
from ..mtranslate import translate as mtranslate
from time import sleep
from .. import kataKatcher

class TranslationEngine (object):
    # TranslationEngine simply holds an ATLASTranslator object and interacts with a TranslationDictionary before actually translating
    def __init__(self, dictionary):
        self.atlas = habisainAtlas.AtlasTranslator(direction = 1)
        self.dictionary = dictionary

    def translate (self, text, block = None):
        # Translates text through ATLAS
        if block != None and block.isGoogleTranslated() and kataKatcher.searchAnyJapanese(text):
            trans = mtranslate(text, "en", "ja")
            print (trans)
            sleep(2)
        else:
            trans = self.atlas.translate(text)
        return trans

    def hasTranslation (self, text, block):
        # Returns boolean regarding "text" being in the dictionary
        bestContext = block.getBestContext()
        return self.dictionary.hasTranslation(bestContext, text)

    def getTranslation (self, text, block):
        # Returns dictionary translation for text
        bestContext = block.getBestContext()
        return self.dictionary.getTranslation(bestContext, text)

    def addToDictionary (self, originalString, translatedString, block):
        # Adds translatedString in the dictionary for originalString
        bestContext = block.getBestContext()
        self.dictionary.addMachineTranslation(bestContext, originalString, translatedString)
from . import habisainAtlas

class TranslationEngine (object):
    def __init__(self, dictionary):
        self.atlas = habisainAtlas.AtlasTranslator(direction = 1)
        self.dictionary = dictionary

    def translate (self, text, block):
        trans = self.atlas.translate(text)
        return trans

    def hasTranslation (self, text, block):
        bestContext = block.getBestContext()
        return self.dictionary.hasTranslation(bestContext, text)

    def getTranslation (self, text, block):
        bestContext = block.getBestContext()
        return self.dictionary.getTranslation(bestContext, text)

    def addToDictionary (self, originalString, translatedString, block):
        bestContext = block.getBestContext()
        self.dictionary.addMachineTranslation(bestContext, originalString, translatedString)
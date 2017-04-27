from .version import version

_CONTEXT_HIGH_PRIORITY = "0Level"
_CONTEXT_INLINESCRIPT = "InlineScript"
_CONTEXT_VOCABULARY = "Vocabulary"
_CONTEXT_NAMES = "Names"
_CONTEXT_CHOICE = "Choice"
_CONTEXT_DIALOGUE = "Dialogue"
_CONTEXT_DESCRIPTION = "Description"
_CONTEXT_SYSTEM = "System"
_CONTEXT_MV = "MV"
_CONTEXT_V2 = "RPGMakerV2"
_CONTEXT_GAME_TITLE = "GameTitle"
_CONTEXT_NOT_FOUND = "OtherText"

contextNames = [_CONTEXT_HIGH_PRIORITY, _CONTEXT_NOT_FOUND, _CONTEXT_GAME_TITLE, _CONTEXT_V2, _CONTEXT_MV, _CONTEXT_SYSTEM,
                _CONTEXT_DESCRIPTION, _CONTEXT_DIALOGUE, _CONTEXT_CHOICE, _CONTEXT_NAMES, _CONTEXT_VOCABULARY, _CONTEXT_INLINESCRIPT]

class TranslationDictionary (object):
    def __init__(self, dictDict):
        self.dicts = dictDict

    def addMachineTranslation (self, context, originalSentence, translatedSentence):
        contextedDict = self.dicts[context]
        contextedDict[originalSentence] = translatedSentence + machineTranslatorTag()

    def addGoogleTranslation (self, context, originalSentence, translatedSentence):
        contextedDict = self.dicts[context]
        contextedDict[originalSentence] = translatedSentence

    def hasTranslation (self, context, originalSentence):
        # Checks context dictionary for originalSentence, returns boolean regarding it being found
        if originalSentence in self.dicts['0Level']:
            trans = self.dicts['0Level'][originalSentence]
            if not isMachineTranslation(trans) or isCurrentMachineTranslation(trans):
                return True
        if originalSentence in self.dicts[context]:
            trans = self.dicts[context][originalSentence]
            if not isMachineTranslation(trans) or isCurrentMachineTranslation(trans):
                return True
        return False

    def getTranslation (self, context, originalSentence):
        # Returns dictionary translation for originalSentence in context
        if originalSentence in self.dicts['0Level']:
            trans = self.dicts['0Level'][originalSentence]
        else:
            trans = self.dicts[context][originalSentence]
        if not isMachineTranslation(trans):
            return trans
        if isCurrentMachineTranslation(trans):
            index = trans.find(machineTranslatorTag())
            return trans[:index]

def machineTranslatorTag ():
    # Returns a full tag to be added to machine translated dictionary entries
    return "*MechaTranslator V" + version + "*"

def isMachineTranslation (text):
    # Returns boolean regarding text being an machine translated entry
    return text.find("*MechaTranslator V") != -1

def isCurrentMachineTranslation (text):
    # Returns boolean regarding text being an up to date machine translated entry
    return text.find(machineTranslatorTag()) != -1
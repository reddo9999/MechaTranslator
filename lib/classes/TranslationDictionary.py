from .version import version

contextNames = ["0Level", "RPGMakerV2", "InlineScript", "Vocabulary", "GameTitle", "Names", "Choice", "Dialogue", "Description", "System", "OtherText", "MV"]

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

class TranslationDictionary (object):
    def __init__(self, dictDict):
        self.dicts = dictDict

    def addMachineTranslation (self, context, originalSentence, translatedSentence):
        contextedDict = self.dicts[context]
        contextedDict[originalSentence] = translatedSentence + machineTranslatorTag()

    def hasTranslation (self, context, originalSentence):
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
        trans = self.dicts[context][originalSentence]
        if not isMachineTranslation(trans):
            return trans
        if isCurrentMachineTranslation(trans):
            index = trans.find(machineTranslatorTag())
            return trans[:index]

    # def getBestContext (self, translationBlock):
    #     if translationBlock.isV2():
    #         return "RPGMakerV2"
    #     if translationBlock.isMV():
    #         return translationBlock.getCurrentContext()
    #     if translationBlock.isDescription():
    #         return "Description"
    #     if translationBlock.isInlineScript():
    #         return "InlineScript"
    #     if translationBlock.isVocabulary():
    #         return "Vocabulary"
    #     if translationBlock.isGameTitle():
    #         return "GameTitle"
    #     if translationBlock.isNames():
    #         return "Names"
    #     if translationBlock.isSystem():
    #         return "System"
    #     if translationBlock.isChoice():
    #         return "Choice"
    #     if translationBlock.isDialogue():
    #         return "Dialogue"
    #     print ("Unrecognized context: " + str(translationBlock.contexts))
    #     return "OtherText"

def machineTranslatorTag ():
    return "*MechaTranslator V" + version + "*"

def isMachineTranslation (text):
    return text.find("*MechaTranslator V") != -1

def isCurrentMachineTranslation (text):
    return text.find(machineTranslatorTag()) != -1
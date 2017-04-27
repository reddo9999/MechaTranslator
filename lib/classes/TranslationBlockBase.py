from . import TranslationDictionary as td

class TranslationBlockBase (object):
    def __init__(self):
        self.contexts = []
        self.originalStrings = []
        self.contextNotFound = False

    def translate (self, x):
        pass

    def isInlineScript (self):
        return False

    def isVocabulary (self):
        return False

    def isGameTitle (self):
        return False

    def isNames (self):
        return False

    def isChoice (self):
        return False

    def isDialogue (self):
        return False

    def isDescription (self):
        return False

    def isSystem (self):
        return False

    def isMV (self):
        return False

    def isV2(self):
        return False

    def getCurrentContext (self):
        return td._CONTEXT_NOT_FOUND

    def considerUnknownContext (self):
        pass;

    def getBestContext (self):
        if self.isV2():
            return td._CONTEXT_V2
        if self.isMV():
            return self.getCurrentContext()
        if self.isDescription():
            return td._CONTEXT_DESCRIPTION
        if self.isInlineScript():
            return td._CONTEXT_INLINESCRIPT
        if self.isVocabulary():
            return td._CONTEXT_VOCABULARY
        if self.isGameTitle():
            return td._CONTEXT_GAME_TITLE
        if self.isNames():
            return td._CONTEXT_NAMES
        if self.isSystem():
            return td._CONTEXT_SYSTEM
        if self.isChoice():
            return td._CONTEXT_CHOICE
        if self.isDialogue():
            return td._CONTEXT_DIALOGUE
        #print ("Unrecognized context: " + str(self.contexts))
        self.contextNotFound = True
        return td._CONTEXT_NOT_FOUND

    def isGoogleTranslated (self):
        return False

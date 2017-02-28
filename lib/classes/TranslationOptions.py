_RPGMAKERTRANS = 0
_WOLFTRANS = 1
_RPGMAKERMV = 2
_RPGMAKERV2 = 3

class TranslationOptions(object):
    def __init__ (self):
        self.RPGMAKERTRANS = 0
        self.WOLFTRANS = 1
        self.RPGMAKERMV = 2
        self.RPGMAKERV2 = 3
        self.maxLength = 42
        self.translateScripts = True
        self.translateActors = True
        self.translateInlineScripts = False
        self.maxLengthItems = 42
        self.keepEmptyLines = True
        self.angryContexts = True
        self.type = self.RPGMAKERTRANS
        self.mvAddWrapPlugin = True

    def updateTo (self, d):
        a = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self,a))]
        for c in a:
            d[c] = self.__getattribute__(c)

    def askOptions (self):
        if input("Use default settings? (Y/N): ").lower() != "n":
            return
        if self.isRPGMakerMV():
            self.mvAddWrapPlugin = input("Add Word Wrap plugin automatically? (Y/N): ").lower() != "n"
            return
        print("MechaTranslator can restrict itself to translating only known contexts (to avoid errors).")
        self.angryContexts = input("Translate unknown/unhandled contexts? (Y/N): ").lower() == "y"
        self.keepEmptyLines = input("Maintain empty lines on translations? (Y/N): ").lower() != "n"
        if self.isRPGMakerTrans():
            self.translateScripts = input("Translate Scripts.txt? (Y/N): ").lower() != "n"
            self.translateActors = input("Translate Actors.txt? (Y/N): ").lower() != "n"
            self.translateInlineScripts = input("Translate InlineScripts? (Y/N): ").lower() != "n"
            print(".")
            print("RPG Maker is usually able to show 52 characters if not showing a face or 42 otherwise.")
            print("This can change if the game uses a different font or resolution.")
        elif self.isWolf():
            print("Wolf RPG can usually show up to 62 characters without faces.")
        try:
            self.maxLength = int(input("Amount of characters per line: "))
        except:
            self.maxLength = 42

        try:
            self.maxLengthItems = int(input("Amount of characters per item description line: "))
        except:
            self.maxLengthItems = 52

    def setWolf (self):
        self.type = self.WOLFTRANS

    def setRPGMakerTrans (self):
        self.type = self.RPGMAKERTRANS

    def setRPGMakerMV (self):
        self.type = self.RPGMAKERMV

    def isRPGMakerV2 (self):
        return self.type == self.RPGMAKERV2

    def setRPGMakerV2 (self):
        self.type = self.RPGMAKERV2

    def isWolf (self):
        return self.type == self.WOLFTRANS

    def isRPGMakerTrans (self):
        return self.type == self.RPGMAKERTRANS

    def isRPGMakerMV (self):
        return self.type == self.RPGMAKERMV
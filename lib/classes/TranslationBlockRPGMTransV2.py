from .TranslationString import TranslationString
from .TranslationBlockRPGMTrans import TranslationBlockRPGMTrans

# V2 as in "RPG Maker Trans V2", used in RPG Maker 2000 and 2003 Games
# The current version is Version 3, which gets handled by TranslationBlockRPGMTrans
class TranslationBlockRPGMTransV2 (TranslationBlockRPGMTrans):
    # A TranslationBlock represents an RPGMakerTrans/WolfTrans multi-line string Block
    def __init__(self, options, isScripts, position):
        TranslationBlockRPGMTrans.__init__(self, options, isScripts, position)
        self.options['maxLength'] = 9999 #RPG Maker Trans V2 can't handle extra lines. :(
        self.translationSeparator = "# TRANSLATION"
        self.originalLines = []
        self.grabbingTranslations = 0
        self.oldTranslation = []

    def isV2(self):
        return True

    def addLine (self, line):
        if line.find("# CONTEXT") == 0:
            self.contexts.append(line)
        if self.grabbingTranslations == 0:
            if len(line) > 0 and line[0] != "#":
                self.grabbingTranslations = 1
            else:
                self.initialLines.append(line)
        if self.grabbingTranslations == 1:
            if len(line) > 0 and line[0] == "#":
                self.grabbingTranslations = 2
            else:
                if line.strip() != "" or self.options["keepEmptyLines"]:
                    self.strings.append(TranslationString(line, self))
                self.originalLines.append(line)
        if self.grabbingTranslations == 2:
            if line == "# END STRING":
                self.finalLines.append(line)
                self.finished = 1
            else:
                self.oldTranslation.append(line)
        return self.finished

    def translate (self, x):
        # Generates translatedLines for later picking.
        self.setUpValues()
        self.translatedLines.extend(self.initialLines)
        self.translatedLines.extend(self.originalLines)
        self.translatedLines.append(self.translationSeparator)
        translatedStrings = []
        for s in self.strings:
            s.setCarefully(self.carefully)
            s.setSkip(self.skipLine)
            translatedStrings.append(s.translate(x, self))
        for s in translatedStrings:
            self.translatedLines.extend(self.cleanUpString(s))
        self.translatedLines.extend(self.finalLines)
        self.translatedLines.append("")
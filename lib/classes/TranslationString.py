from .TranslationSymbol import TranslationSymbol

class TranslationString (object):
    # A translation string is a line from a message.
    # This class takes care of the original string and spits it into multiple symbols for more accurate translations.
    def __init__(self, text, block):
        self.carefully = 0
        self.parent = block
        self.text = text
        self.translated = text
        self.skip = 0
        self.translations = []
        self.code = "abcdefghijklmnopqrstuvxzwyABCDEFGHIJKLMNOPQRSTUVXZWY(){}[]"
        self.symbols = "\\…〚〘〖【《〈｛［〔（『[{(「〛〙〗】》〉｝］〕）』]})」><'\""
        self.validSlashers = "0123456789[]{}()\\abcdefghijklmnopqrstuvxzwyABCDEFGHIJKLMNOPQRSTUVXZWY!"
        self.sentenceFinishers = ".!?！？。,、"

    def setSkip (self, skip):
        # Defines whether this string is translatable.
        self.skip = skip == 1

    def setCarefully (self, carefully):
        # Defines whether this string can be code and should be translated carefully (avoiding any code symbols).
        self.carefully = carefully == 1

    def translate (self, x, block):
        # Returns this string translated.
        if self.carefully and not self.skip:
            lower = self.text.lower()
            if lower.find(".png") != -1 or lower.find(".jpg") != -1 or lower.find(".jpeg") != -1 or lower.find(".gif") != -1 or lower.find(".bmp") != -1 \
                    or lower.find(".ogg") != -1or lower.find(".mp3") != -1 or lower.find(".m4a") != -1 or lower.find(".mid") != -1 or lower.find(".midi") != -1:
                self.skip = 1
        if self.skip:
            return self.text

        if x.hasTranslation(self.text, block):
            self.translated =  x.getTranslation(self.text, block)
            return self.translated

        self.createSymbols()
        translated = ""
        for s in self.translations:
            translated += s.translate(x, self.parent)
        x.addToDictionary(self.text, translated, block)
        self.translated = translated
        return translated

    def createSymbols (self):
        # Turns this string into multiple TranslationSymbol
        open = 0
        index = 0
        start = -1
        self.line = self.text
        while index < len(self.line):
            # Are we dealing with a slash command?
            if start == -1:
                # We are not dealing with a slash command
                try:
                    # Attempts to encode at cp932 - this is the encoding used by ATLAS, so any symbols unencodable need to be removed now
                    self.line[index].encode('cp932')

                    if (self.line[index] in self.sentenceFinishers):
                        # Split string into TranslationSymbol as sentences end
                        self.translations.append(TranslationSymbol(self.line[:(index)], 1))
                        self.translations.append(TranslationSymbol(self.line[index], 0))
                        self.line = self.line[index + 1:]
                        index = -1
                    elif self.line[index] in self.symbols:
                        # Split string into TranslationSymbol when a symbol appears
                        self.translations.append(TranslationSymbol(self.line[:index], 1))
                        self.translations.append(TranslationSymbol(self.line[index], 0))
                        self.line = self.line[index + 1:]
                        index = -1
                    elif (self.line[index] == "\\" and (self.line[index + 1] == '\\' or self.line[index+1] == '>')):
                        # Start looking for a slash command
                        start = index
                        index+= 1
                    elif self.line[index] == "%" and (index + 1) < len(self.line) and self.line[index + 1] in "s0123456789":
                        # In RPG Maker XP/VX/VX Ace, "%s" is used to be replaced in strings
                        # In RPG Maker MV, %0-%9 are also used.
                        self.translations.append(TranslationSymbol(self.line[:index], 1))
                        self.translations.append(TranslationSymbol(" %" + self.line[index + 1] + " ", 0))
                        self.line = self.line[index + 2:]
                        index = -1
                except Exception as e:
                    # Unencodable character found, turn it into an untranslatable symbol
                    self.translations.append(TranslationSymbol(self.line[:index], 1))
                    self.translations.append(TranslationSymbol(self.line[index], 0))
                    self.line = self.line[index + 1:]
                    index = -1
            else:
                # We are dealing with a slash command
                # See if it's opening a bracket
                if (self.line[index] in "[{("):
                    open = 1
                elif (self.line[index] in "]})"):
                    open = 0
                # Are we seeing a character that is NOT valid slash command?
                # Does our slash command still have an open bracket?
                if (self.line[index] not in self.validSlashers) and open == 0:
                    self.translations.append(TranslationSymbol(self.line[:start], 1))
                    self.translations.append(TranslationSymbol(self.line[start:index], 0))
                    self.line = self.line[index:]
                    start = -1
                    index = -1
            index += 1
        # We have reached the end of self.line

        # Do we have a slash command open?
        if start != -1:
            self.translations.append(TranslationSymbol(self.line, 0))
        elif len(self.line) > 0:
            self.translations.append(TranslationSymbol(self.line, 1))
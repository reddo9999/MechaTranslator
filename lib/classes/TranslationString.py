import re

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
            # for c in self.text:
            #     if c in self.code:
            #         self.skip = 1
            #         break
            lower = self.text.lower()
            if lower.find(".png") != -1 or lower.find(".jpg") != -1 or lower.find(".jpeg") != -1 or lower.find(".gif") != -1 or lower.find(".bmp") != -1:
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

    def createSymbols(self):
        open = 0
        index = 0
        start = -1
        self.line = self.text
        while index < len(self.line):
            if start == -1:
                try:
                    self.line[index].encode('cp932')
                    if (self.line[index] in self.sentenceFinishers):
                        self.translations.append(TranslationSymbol(self.line[:(index)], 1))
                        self.translations.append(TranslationSymbol(self.line[index], 0))
                        self.line = self.line[index + 1:]
                        index = -1
                    elif self.line[index] in self.symbols:
                        if self.line[index] == "\\" and self.line[index + 1] == '\\':
                            funMatch = re.search(r"[a-z\d]+\[[\S]+\]", self.line)
                            if funMatch:
                                self.translations.append(TranslationSymbol(self.line[:funMatch.end()], 0))

                                self.line = self.line[funMatch.end():]

                                index = -1
                        else:
                            self.translations.append(TranslationSymbol(self.line[:index], 1))
                            self.translations.append(TranslationSymbol(self.line[index], 0))
                            self.line = self.line[index + 1:]
                            index = -1
                    elif (self.line[index] == "\\" and (self.line[index + 1] == '\\' or self.line[index+1] == '>')):
                        start = index
                        index+= 1
                    elif self.line[index] in "%@" and (index + 1) < len(self.line):
                        varMatch = re.search(r"[%@][\ds]+", self.line)
                        if varMatch:
                            self.translations.append(TranslationSymbol(self.line[:varMatch.end()], 0))

                            self.line = self.line[varMatch.end():]

                            index = -1
                except Exception as e:
                    self.translations.append(TranslationSymbol(self.line[:index], 1))
                    self.translations.append(TranslationSymbol(self.line[index], 0))
                    self.line = self.line[index + 1:]
                    index = -1
            else:
                try:
                    if (self.line[index] in "[{("):
                        open = 1
                    elif (self.line[index] in "]})"):
                        open = 0
                    if (self.line[index] not in self.validSlashers) and open == 0:
                        self.translations.append(TranslationSymbol(self.line[:start], 1))
                        self.translations.append(TranslationSymbol(self.line[start:index], 0))
                        self.line = self.line[index:]
                        start = -1
                        index = -1
                except:
                    pass
            index += 1
        if start != -1:
            self.translations.append(TranslationSymbol(self.line, 0))
        elif len(self.line) > 0:
            self.translations.append(TranslationSymbol(self.line, 1))

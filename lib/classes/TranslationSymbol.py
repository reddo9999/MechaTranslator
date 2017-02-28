import re

class TranslationSymbol (object):
    # A translation Symbol is a small part of a string that will be translated.
    # It can be a single character (in case it's really just a symbol which we don't want to translate at all)
    # Or it can be multiple words which will be translated as a single thing (a "symbol").
    def __init__(self, text, translatable):
        self.text = text
        self.translatable = translatable
        self.carefully = 0
        self.symbols = r"[\.!?！？。\\…〚〘〖【《〈｛［〔（『\[\{\(「〛〙〗】》〉｝］〕）』\]\}\)」'\"]"
        self.atlasSymbols = r"[\.!?\[\]]"

    def translate(self, x, block):
        # Returns a string with the translated/original symbol, as applicable.
        if self.translatable:
            trimmed = self.text.strip()
            translation = x.translate(trimmed, block)
            #[Wo] = Without object
            translation = translation.replace("[wo]", "it")
            translation = translation.replace("[Wo]", "It")
            translation = translation.replace("[WO]", "IT")
            translation = translation.replace("\"", "") # These symbols are being put manually, impede ATLAS from ruining it!
            translation = translation.replace("'", "")
            # TODO: Add other ATLAS translations. [O*], for instance, would appear if someone has a badly configured ATLAS
            # TODO: ([O*] is ATLAS way of saying "Object in sentence should be here but isn't")

            translation = re.sub(self.atlasSymbols, "", translation)
            translation = translation.strip()
            return translation
        else:
            return self.text
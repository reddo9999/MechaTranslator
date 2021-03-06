from .TranslationString import TranslationString
from .TranslationBlockBase import TranslationBlockBase
from . import TranslationDictionary as td

class TranslationBlockRPGMTrans (TranslationBlockBase):
    # A TranslationBlock represents an RPGMakerTrans/WolfTrans multi-line string Block
    def __init__(self, options, isScripts, position):
        TranslationBlockBase.__init__(self)
        self.options = options
        self.initialLines = []
        self.contexts = []
        self.strings = []
        self.finalLines = []
        self.translatedLines = []
        self.grabbingTranslations = 0
        self.isScripts = isScripts
        self.carefully = 0
        self.skipLine = isScripts
        self.position = position
        self.finished = 0

    def setUpValues (self):
        # Decides if this is translatable and/or if care has to be put when translating it
        self.skipLine = self.isScripts
        if self.isVocabulary() and self.options['translateScripts']:
            self.skipLine = 0

        if self.isInlineScript():
            if self.options['translateInlineScripts']:
                self.skipLine = 0
                self.carefully = 1
            else:
                self.skipLine = 1

        if self.isGameTitle() or self.isSystem():
            self.carefully = 1

        if self.isUntranslatable():
            self.skipLine = 1
        elif self.isDangerous():
            self.carefully = 1
        elif self.getBestContext() == td._CONTEXT_NOT_FOUND:
            self.contextNotFound = True;
            if self.options['angryContexts']:
                self.skipLine = 1

    def translate (self, x):
        # Generates translatedLines for later picking.
        self.setUpValues()
        self.translatedLines.extend(self.initialLines)
        for c in self.contexts:
            #self.translatedLines.extend(self.contexts)
            idx = c.find(" < UNTRANSLATED")
            if idx == -1:
                self.translatedLines.append(c)
            else:
                self.translatedLines.append(c[:(idx)])
        translatedStrings = []
        for s in self.strings:
            s.setCarefully(self.carefully)
            s.setSkip(self.skipLine)
            translatedStrings.append(s.translate(x, self))
        for s in translatedStrings:
            self.translatedLines.extend(self.cleanUpString(s))
        self.translatedLines.extend(self.finalLines)
        self.translatedLines.append("")
        self.translatedLines.append("")

    def cleanUpString (self, translated):
        # Cleans up a translated string so that it'll:
        # - Fit in a message box length
        # - Have english symbols rather than Japanese ones where appropriate
        # - Never be empty
        # Always returns an array of strings
        final = []

        if self.isItemDescription():
            maxLength = self.options['maxLengthItems']
        else:
            maxLength = self.options['maxLength']

        if self.carefully or self.isItemName() or self.isActorName():
            maxLength = len(translated) + 100 #no splitting

        japSymbols = "。！？［］（）｛｝"
        asciiSymbols = ".!?[](){}"
        i = 0

        while i < len(japSymbols):
            translated = translated.replace(japSymbols[i], asciiSymbols[i])
            i+=1

        translated = translated.replace("、", ", ")

        while len(translated) > maxLength:
            index = translated.rfind(" ", 0, maxLength)
            if index < 0:
                final.append(translated)
                translated = ""
                break
            else:
                final.append(translated[:index])
                if len(translated) > index + 1:
                    translated = translated[(index+1):]
                else:
                    translated = ""

        if translated != "":
            final.append(translated)

        if (len(final) < 1):
            final = [""]
        else:
            i = 0
            while i < len(final):
                if len(final[i]) > 0 and final[i][0] == ">":
                    final[i] = "\\" + final[i]
                i+= 1

        return final

    def getTranslatedLines (self):
        # This returns an array of strings with the translated block.
        return self.translatedLines

    def considerUnknownContext (self):
        if self.contextNotFound:
            print("Unknown context: %s" % ( str(self.contexts) ) );

    def addLine (self, line):
        # Adds a line to the block. It'll interpret it on it's own. This only works if following RPGMakerTrans syntax
        if self.grabbingTranslations:
            if len(line) > 0 and line[0] == ">":
                self.grabbingTranslations = 0
            else:
                if line.strip() != "" or self.options["keepEmptyLines"]:
                    self.strings.append(TranslationString(line, self))
                    self.originalStrings.append(line)
                self.initialLines.append(line)
        if not self.grabbingTranslations:
            if line == "> BEGIN STRING":
                self.initialLines.append(line)
                self.grabbingTranslations = 1
            elif line == "> END STRING":
                self.finalLines.append(line)
                self.finished = 1
            elif len(self.strings) > 0 and (len(line) < 1 or line[0] != ">"):
                pass
            else:
                if line.find("> CONTEXT") == 0:
                    self.contexts.append(line)
                elif len(self.initialLines) < 1 and len(line) > 0 and line[0] == ">":
                    # This must be the tag for the file, such as "> RPGMAKER TRANS PATCH FILE VERSION 3.2"
                    self.initialLines.append(line)
        return self.finished

    def isNames (self):
        return self.isActorName() or self.isActorNickname() or self.isItemName() \
               or self.isClassName() or self.isSkillName() or self.isDisplayName() \
               or self.isEnemyName() or self.isTroopsName() or self.isStatesName()

    def isActors (self):
        for c in self.contexts:
            if c.find("> CONTEXT: Actors") == 0:
                return True
        return False

    def isSystem (self):
        for c in self.contexts:
            if c.find("> CONTEXT: System/") == 0:
                return True
        return False

    def isActorName (self):
        for c in self.contexts:
            if c.find("> CONTEXT: Actors") == 0 and c.find("/name/") != -1:
                return True
            #WOLF, Hero Name, Hero Title
            if (c.find("主人公ステータス/") != -1 and c.find("キャラ名") != -1) or \
                    (c.find("主人公ステータス/") != -1 and c.find("肩書き") != -1):
                return True
        return False

    def isEnemyName (self):
        for c in self.contexts:
            if c.find("> CONTEXT: Enemies") == 0 and c.find("/name/") != -1:
                return True
            if c.find("敵ｷｬﾗ個体ﾃﾞｰﾀ/") != -1 and c.find("敵キャラ名") != -1: #WOLF
                return True
        return False

    def isActorNickname (self):
        for c in self.contexts:
            if c.find("> CONTEXT: Actors") == 0 and c.find("/nickname/") != -1:
                return True
        return False

    def isClassName (self):
        for c in self.contexts:
            if c.find("> CONTEXT: Classes") == 0 and c.find("/name/") != -1:
                return True
        return False

    def isDisplayName (self):
        for c in self.contexts:
            if c.find("/display_name/") != -1:
                return True
        return False

    def isSkillName (self):
        for c in self.contexts:
            if c.find("> CONTEXT: Skills/") != -1 and c.find("/name/") != -1:
                return True
            # WOLF
            if c.find("技能/") != -1 and c.find("技能の名前") != -1:
                return True
        return False

    def isTroopsName (self):
        for c in self.contexts:
            if c.find("> CONTEXT: Troops/") != -1 and c.find("/name/") != -1:
                return True
        return False

    def isStatesName (self):
        for c in self.contexts:
            if c.find("> CONTEXT: States/") != -1 and c.find("/name/") != -1:
                return True
            if (c.find("状態設定/") != -1 and c.find("状態名") != -1) or \
                    (c.find("属性名の設定/") != -1 and c.find("属性名'") != -1) : #WOLF
                return True
        return False

    def isActorDescription (self):
        for c in self.contexts:
            if c.find("> CONTEXT: Actors") == 0 and c.find("/description/") != -1:
                return True
        return False

    def isSkillDescription (self):
        for c in self.contexts:
            if c.find("> CONTEXT: Skills") == 0 and c.find("/description/") != -1:
                return True
            if c.find("技能/") != -1 and c.find("説明") != -1: #WOLF
                return True
        return False

    def isSkillMessage (self):
        for c in self.contexts:
            if c.find("> CONTEXT: Skills") == 0 and c.find("/message") != -1:
                return True
            if (c.find("技能/") != -1 and (c.find("使用時文章[戦闘](人名~") != -1 or c.find("失敗時文章[(対象)～") != -1)) or \
                (c.find("状態設定/") != -1 and c.find("ｶｳﾝﾀｰ発動文[対象～") != -1): #WOLF
                return True
        return False

    def isStatesMessage (self):
        for c in self.contexts:
            if c.find("> CONTEXT: States") == 0 and c.find("/message") != -1:
                return True
            if (c.find("状態設定/") != -1 and c.find("回復時の文章[(人名)～]") != -1) or \
                    (c.find("状態設定/") != -1 and c.find("発生時の文章[(人名)～]") != -1) or \
                    (c.find("状態設定/") != -1 and c.find("行動制限時文章(空欄:ﾅｼ") != -1): #WOLF
                return True
        return False

    def isItemName (self):
        for c in self.contexts:
            if (c.find("> CONTEXT: Armors") == 0 and c.find("/name/") != -1)\
                or (c.find("> CONTEXT: Items") == 0 and c.find("/name/") != -1)\
                    or (c.find("> CONTEXT: Weapons") == 0 and c.find("/name/") != -1):
                return True
            # WOLF
            if (c.find("アイテム/") != -1 and c.find("アイテム名") != -1) or \
                    (c.find("防具/") != -1 and c.find("防具の名前") != -1) or \
                    (c.find("武器/") != -1 and c.find("武器の名前") != -1) or \
                    (c.find("鍛冶師用DB/") != -1 and c.find("作る装備") != -1) or \
                    (c.find("属性名の設定/") != -1 and c.find("属性名") != -1) or \
                    (c.find("装備タイプ/") != -1 and c.find("装備タイプ名(剣･鎧など）") != -1):
                return True
        return False

    def isItemDescription (self):
        for c in self.contexts:
            if (c.find("> CONTEXT: Armors") == 0 and c.find("/description/") != -1)\
                        or (c.find("> CONTEXT: Items") == 0 and c.find("/description/") != -1)\
                        or (c.find("> CONTEXT: Weapons") == 0 and c.find("/description/") != -1):
                return True
            if (c.find("アイテム/") != -1 and c.find("説明文[2行まで可]") != -1) or \
                    (c.find("防具/") != -1 and c.find("防具の説明[2行まで可]") != -1) or \
                    (c.find("武器/") != -1 and c.find("武器の説明[2行まで可]") != -1): #WOLF
                return True
        return False

    def isDialogue (self):
        for c in self.contexts:
            if c.find("/Dialogue") != -1 or c.find("/Message") != -1:
                return True
        return False

    def isChoice (self):
        for c in self.contexts:
            if c.find("/Choice") != -1:
                return True
        return False

    def isInlineScript (self):
        for c in self.contexts:
            if c.find("InlineScript") != -1 or c.find("> CONTEXT: Scripts/Window_nxt/") == 0 \
                    or c.find("> CONTEXT: Scripts/Window_MenuCommand/") == 0 or c.find("> CONTEXT: Scripts/Window_Base/") == 0:
                return True
            # Knights of the Phantasm
            if c.find("Scripts/Window_Status★") != -1 or c.find("Scripts/Window_MenuStatus★") != -1:
                return True
            # XVI - Achievement Medals, Volume change screen
            if c.find("Scripts/RGSS3_実績メダルEX") != -1 or c.find("Scripts/音量変更スクリプトさん") != -1:
                return True
            #RJ194683
            if c.find("Scripts/設定項目") != -1 or c.find("Scripts/ショップ在庫数設定") != -1 or c.find("Scripts/オプション") != -1 or c.find("Scripts/Window_HinminOption") != -1 or c.find("Scripts/Game_Hinmin") != -1:
                return True
            #Vera
            if c.find("Scripts/冒険メモ") != -1:
                return True
            #Crotch new game
            # Villager's Tweets, Status Screen
            if c.find("Scripts/村人のつぶやき") != -1 or c.find("Scripts/オシブ様ステータス画面変更/") != -1:
                return True
        return False

    def isVocabulary (self):
        for c in self.contexts:
            if c.find("> CONTEXT: Scripts/Vocab/") == 0:
                return True
            # WOLF
            if (c.find("戦闘コマンド/") != -1 and c.find("コマンド名'") != -1) or \
                    (c.find("戦闘コマンド/") != -1 and c.find("コマンドの説明文") != -1) or \
                    (c.find("戦闘コマンド/") != -1 and c.find("コマンド名") != -1) or \
                    (c.find("用語設定/") != -1 and c.find("用語基本設定/") != -1) or \
                    (c.find("基本ｼｽﾃﾑ用変数/") != -1 and c.find("文字列") != -1) or \
                    (c.find("システム設定/") != -1 and c.find("特殊メニューA名称") != -1) or \
                    (c.find("システム設定/") != -1 and c.find("[戦闘]敵逃走文 [対象～") != -1) or \
                    (c.find("合成基本設定/") != -1):
                return True
        if self.isSkillDescription() or self.isSkillMessage() or self.isStatesMessage():
            return True
        return False

    def isGameTitle (self):
        for c in self.contexts:
            if c.find("> CONTEXT: GameINI/Title") == 0:
                return True
        return False

    def isSound (self):
        for c in self.contexts:
            if c.find("/bgm/name/") != -1 or c.find("/bgs/name/") != -1 or \
                    c.find("_se/name/") != -1 or c.find("_bgm/name/") != -1 or \
                    c.find("_me/name/") != -1:
                return True
        return False

    def isUntranslatable (self):
        if self.isSound():
            return True
        for c in self.contexts:
            if (c.find("> CONTEXT") != -1 and c.find("/Picture") != -1) or \
                    (c.find("> CONTEXT") != -1 and c.find("/SetString") != -1) or \
                    (c.find("> CONTEXT") != -1 and c.find("/Database") != -1) or \
                    (c.find("> CONTEXT") != -1 and c.find("/StringCondition") != -1) or \
                    (c.find("Scripts/Cache") != -1) or (c.find("Scripts/Window_NameInput") != -1):
                return True
        return False

    def isDangerous (self):
        return False

    def isDescription(self):
        return self.isActorDescription() or self.isItemDescription() or self.isSkillDescription()

    def isGoogleTranslated (self):
        if self.options['googleNames'] or self.options['googleAll']:
            if self.isNames() or self.options['googleAll']:
                return True
        return False
from .TranslationBlockBase import TranslationBlockBase
from .TranslationString import TranslationString
from ..MVPlugin import mechaWrapBreak, mechaWrapCommand

from . import TranslationDictionary as td

class TranslationBlockRPGMV (TranslationBlockBase):
    def __init__(self, dict, options, position):
        TranslationBlockBase.__init__(self)
        self.findType(dict)
        self.translationStrings = {}
        self.paramTranslationStrings = []
        self.position = position
        self.findStrings(dict)
        self.context = td._CONTEXT_MV

    def getCurrentContext(self):
        return self.context

    ######
    ## Creates TranslationString based on self.type
    ######
    def findStrings (self, dict):
        if self.type == _MV_CHARACTER_TYPE:
            self.translationStrings['name'] = TranslationString(dict['name'], self)
            self.translationStrings['nickname'] = TranslationString(dict['nickname'], self)
            self.translationStrings['profile'] = TranslationString(dict['profile'], self)
        elif self.type == _MV_ARMOR_TYPE:
            self.translationStrings['name'] = TranslationString(dict['name'], self)
            self.translationStrings['description'] = TranslationString(dict['description'], self)
        elif self.type == _MV_WEAPON_TYPE:
            self.translationStrings['name'] = TranslationString(dict['name'], self)
            self.translationStrings['description'] = TranslationString(dict['description'], self)
        elif self.type == _MV_CLASS_TYPE:
            self.translationStrings['name'] = TranslationString(dict['name'], self)
        elif self.type == _MV_ENEMY_TYPE:
            self.translationStrings['name'] = TranslationString(dict['name'], self)
        elif self.type == _MV_ITEM_TYPE:
            self.translationStrings['name'] = TranslationString(dict['name'], self)
            self.translationStrings['description'] = TranslationString(dict['description'], self)
        elif self.type == _MV_MAP_TYPE:
            self.translationStrings['name'] = TranslationString(dict['name'], self)
        elif self.type == _MV_SKILL_TYPE:
            self.translationStrings['name'] = TranslationString(dict['name'], self)
            self.translationStrings['description'] = TranslationString(dict['description'], self)
            self.translationStrings['message1'] = TranslationString(dict['message1'], self)
            self.translationStrings['message2'] = TranslationString(dict['message2'], self)
        elif self.type == _MV_STATE_TYPE:
            self.translationStrings['name'] = TranslationString(dict['name'], self)
            self.translationStrings['message1'] = TranslationString(dict['message1'], self)
            self.translationStrings['message2'] = TranslationString(dict['message2'], self)
            self.translationStrings['message3'] = TranslationString(dict['message3'], self)
            self.translationStrings['message4'] = TranslationString(dict['message4'], self)
        elif self.type == _MV_SYSTEM_TYPE:
            self.translationStrings['terms'] = {}
            terms = _MV_SYSTEM_TERMS
            for i in terms:
                self.translationStrings['terms'][i] = []
                for k in dict['terms'][i]:
                    if k == None:
                        self.translationStrings['terms'][i].append(None)
                    else:
                        self.translationStrings['terms'][i].append(TranslationString(k, self))
            self.translationStrings['messages'] = {}
            for idx, value in dict['terms']['messages'].items():
                self.translationStrings['messages'][idx] = TranslationString(value, self)
            for i in _MV_SYSTEM_NAMES:
                self.translationStrings[i] = []
                for k in dict[i]:
                    self.translationStrings[i].append(TranslationString(k, self))
            self.translationStrings[_MV_SYSTEM_TITLE] = TranslationString(dict[_MV_SYSTEM_TITLE], self)
            self.translationStrings[_MV_SYSTEM_CURRENCY] = TranslationString(dict[_MV_SYSTEM_CURRENCY], self)
        elif self.type == _MV_DIALOGUE_TYPE:
            self.translationStrings['parameters'] = []
            for v in dict['parameters']:
                self.translationStrings['parameters'].append(TranslationString(v, self))
        elif self.type == _MV_CHOICE_TYPE:
            self.translationStrings['parameters'] = []
            for v in dict['parameters'][0]:
                self.translationStrings['parameters'].append(TranslationString(v, self))

    ###########
    #### Actually Translates stored TranslationStrings
    ###########
    def translate (self, translationEngine):
        if self.type == _MV_CHARACTER_TYPE:
            self.context = td._CONTEXT_NAMES
            self.translationStrings['name'].translate(translationEngine, self)
            self.translationStrings['nickname'].translate(translationEngine, self)
            self.context = td._CONTEXT_DESCRIPTION
            self.translationStrings['profile'].translate(translationEngine, self)
        elif self.type == _MV_ARMOR_TYPE:
            self.context = td._CONTEXT_NAMES
            self.translationStrings['name'].translate(translationEngine, self)
            self.context = td._CONTEXT_DESCRIPTION
            self.translationStrings['description'].translate(translationEngine, self)
        elif self.type == _MV_WEAPON_TYPE:
            self.context = td._CONTEXT_NAMES
            self.translationStrings['name'].translate(translationEngine, self)
            self.context = td._CONTEXT_DESCRIPTION
            self.translationStrings['description'].translate(translationEngine, self)
        elif self.type == _MV_ITEM_TYPE:
            self.context = td._CONTEXT_NAMES
            self.translationStrings['name'].translate(translationEngine, self)
            self.context = td._CONTEXT_DESCRIPTION
            self.translationStrings['description'].translate(translationEngine, self)
        elif self.type == _MV_CLASS_TYPE:
            self.context = td._CONTEXT_NAMES
            self.translationStrings['name'].translate(translationEngine, self)
        elif self.type == _MV_ENEMY_TYPE:
            self.context = td._CONTEXT_NAMES
            self.translationStrings['name'].translate(translationEngine, self)
        elif self.type == _MV_MAP_TYPE:
            self.context = td._CONTEXT_NAMES
            self.translationStrings['name'].translate(translationEngine, self)
        elif self.type == _MV_SKILL_TYPE:
            self.context = td._CONTEXT_NAMES
            self.translationStrings['name'].translate(translationEngine, self)
            self.context = td._CONTEXT_DESCRIPTION
            self.translationStrings['description'].translate(translationEngine, self)
            self.context = td._CONTEXT_VOCABULARY
            self.translationStrings['message1'].translate(translationEngine, self)
            self.translationStrings['message2'].translate(translationEngine, self)
        elif self.type == _MV_STATE_TYPE:
            self.context = td._CONTEXT_NAMES
            self.translationStrings['name'].translate(translationEngine, self)
            self.context = td._CONTEXT_VOCABULARY
            self.translationStrings['message1'].translate(translationEngine, self)
            self.translationStrings['message2'].translate(translationEngine, self)
            self.translationStrings['message3'].translate(translationEngine, self)
            self.translationStrings['message4'].translate(translationEngine, self)
        elif self.type == _MV_DIALOGUE_TYPE:
            self.context = td._CONTEXT_DIALOGUE
            for k in self.translationStrings['parameters']:
                k.translate(translationEngine, self)
        elif self.type == _MV_CHOICE_TYPE:
            self.context = td._CONTEXT_CHOICE
            for k in self.translationStrings['parameters']:
                #for v in dict['parameters'][0]:
                k.translate(translationEngine, self)
        elif self.type == _MV_SYSTEM_TYPE:
            self.context = td._CONTEXT_MV
            for i in _MV_SYSTEM_TERMS:
                for k in self.translationStrings['terms'][i]:
                    if k != None:
                        k.translate(translationEngine, self)
            for idx, value in self.translationStrings['messages'].items():
                value.translate(translationEngine, self)
            for i in _MV_SYSTEM_NAMES:
                for k in self.translationStrings[i]:
                    k.translate(translationEngine, self)
            self.translationStrings[_MV_SYSTEM_CURRENCY].translate(translationEngine, self)
            self.context = td._CONTEXT_GAME_TITLE
            self.translationStrings[_MV_SYSTEM_TITLE].translate(translationEngine, self)

    ####################
    #### Applies Stored translation to dictionary in the list
    ####################
    def apply (self, list):
        dict = list[self.position]
        if self.type == _MV_CHARACTER_TYPE:
            dict['name'] = self.cleanUpString([self.translationStrings['name']], False)
            dict['nickname'] = self.cleanUpString([self.translationStrings['name']], False)
            dict['profile'] = self.cleanUpString([self.translationStrings['name']], True)
        elif self.type == _MV_DIALOGUE_TYPE:
            dict['parameters'] = [(self.cleanUpString(self.translationStrings['parameters'], True))]
        elif self.type == _MV_CHOICE_TYPE:
            i = 0
            while i < len(self.translationStrings['parameters']):
                dict['parameters'][0][i] = self.cleanUpString([self.translationStrings['parameters'][i]], False)
                i+= 1
        elif self.type == _MV_ARMOR_TYPE or self.type == _MV_WEAPON_TYPE or self.type == _MV_ITEM_TYPE:
            dict['name'] = self.cleanUpString([self.translationStrings['name']], False)
            dict['description'] = self.cleanUpString([self.translationStrings['description']], True)
        elif self.type == _MV_CLASS_TYPE or self.type == _MV_ENEMY_TYPE or self.type == _MV_MAP_TYPE:
            dict['name'] = self.cleanUpString([self.translationStrings['name']], False)
        elif self.type == _MV_SKILL_TYPE or self.type == _MV_STATE_TYPE:
            dict['name'] = self.cleanUpString([self.translationStrings['name']], False)
            dict['message1'] = self.cleanUpString([self.translationStrings['message1']], False)
            dict['message2'] = self.cleanUpString([self.translationStrings['message2']], False)
            if self.type == _MV_SKILL_TYPE:
                dict['description'] = self.cleanUpString([self.translationStrings['description']], True)
            else:
                dict['message3'] = self.cleanUpString([self.translationStrings['message3']], False)
                dict['message4'] = self.cleanUpString([self.translationStrings['message4']], False)
        elif self.type == _MV_SYSTEM_TYPE:
            for i in _MV_SYSTEM_TERMS:
                k = 0
                while k < len(self.translationStrings['terms'][i]):
                    if (self.translationStrings['terms'][i][k] != None):
                        dict['terms'][i][k] = self.cleanUpString([self.translationStrings['terms'][i][k]], False)
                    k+=1
            for idx, value in self.translationStrings['messages'].items():
                dict['terms']['messages'][idx] = self.cleanUpString([value], False)
            for i in _MV_SYSTEM_NAMES:
                k = 0
                while k < len(self.translationStrings[i]):
                    dict[i][k] = self.cleanUpString([self.translationStrings[i][k]], False)
                    k+= 1
            dict[_MV_SYSTEM_TITLE] = self.cleanUpString([self.translationStrings[_MV_SYSTEM_TITLE]], False)
            dict[_MV_SYSTEM_CURRENCY] = self.cleanUpString([self.translationStrings[_MV_SYSTEM_CURRENCY]], False)

    def cleanUpString (self, strings, isMessage):
        if isMessage:
            newText = mechaWrapCommand + " "
        else:
            newText = ""
        i = 0
        while i < len(strings):
            newText += strings[i].translated
            i+= 1
        if isMessage:
            newText += mechaWrapBreak

        japSymbols = "。！？［］（）｛｝"
        asciiSymbols = ".!?[](){}"
        i = 0
        while i < len(japSymbols):
            newText = newText.replace(japSymbols[i], asciiSymbols[i])
            i+=1
        newText = newText.replace("、", ", ")
        return newText


    ## Sets self.type
    def findType (self, d):
        self.type = _MVfindType(d)

    def isMV (self):
        return True

######
## Reads a json dictionary entry to see what kind of thing it is
######
def _MVfindType (d):
    if "id" in d and "battlerName" in d and "characterIndex" in d and "characterName" in d and "classId" in d and "equips" in d and "faceIndex" in d and "faceName" in d and "traits" in d and "initialLevel" in d and "maxLevel" in d and "name" in d and "nickname" in d and "note" in d and "profile" in d:
        return _MV_CHARACTER_TYPE
    elif "id" in d and "atypeId" in d and "description" in d and "etypeId" in d and "traits" in d and "iconIndex" in d and "name" in d and "note" in d and "params" in d and "price" in d:
        return _MV_ARMOR_TYPE
    elif "id" in d and "expParams" in d and "traits" in d and "learnings" in d and "name" in d and "note" in d and "params" in d:
        return _MV_CLASS_TYPE
    elif "id" in d and "actions" in d and "battlerHue" in d and "battlerName" in d and "dropItems" in d and "exp" in d and "traits" in d and "gold" in d and "name" in d and "note" in d and "params" in d:
        return _MV_ENEMY_TYPE
    elif "id" in d and "animationId" in d and "consumable" in d and "damage" in d and "description" in d and "effects" in d and "hitType" in d and "iconIndex" in d and "itypeId" in d and "name" in d and "note" in d and "occasion" in d and "price" in d and "repeats" in d and "scope" in d and "speed" in d and "successRate" in d and "tpGain" in d:
        return _MV_ITEM_TYPE
    elif "id" in d and "expanded" in d and "name" in d and "order" in d and "parentId" in d and "scrollX" in d and "scrollY" in d:
        return _MV_MAP_TYPE
    elif "id" in d and "animationId" in d and "damage" in d and "description" in d and "effects" in d and "hitType" in d and "iconIndex" in d and "message1" in d and "message2" in d and "mpCost" in d and "name" in d and "note" in d and "occasion" in d and "repeats" in d and "requiredWtypeId1" in d and "requiredWtypeId2" in d and "scope" in d and "speed" in d and "stypeId" in d and "successRate" in d and "tpCost" in d and "tpGain" in d:
        return _MV_SKILL_TYPE
    elif "id" in d and "autoRemovalTiming" in d and "chanceByDamage" in d and "iconIndex" in d and "maxTurns" in d and "message1" in d and "message2" in d and "message3" in d and "message4" in d and "minTurns" in d and "motion" in d and "name" in d and "note" in d and "overlay" in d and "priority" in d and "releaseByDamage" in d and "removeAtBattleEnd" in d and "removeByDamage" in d and "removeByRestriction" in d and "removeByWalking" in d and "restriction" in d and "stepsToRemove" in d and "traits" in d:
        return _MV_STATE_TYPE
    elif "airship" in d and "armorTypes" in d and "attackMotions" in d and "battleBgm" in d and "battleback1Name" in d and "battleback2Name" in d and "battlerHue" in d and "battlerName" in d and "boat" in d and "currencyUnit" in d and "defeatMe" in d and "editMapId" in d and "elements" in d and "equipTypes" in d and "gameTitle" in d and "gameoverMe" in d and "locale" in d and "magicSkills" in d and "menuCommands" in d and "optDisplayTp" in d and "optDrawTitle" in d and "optExtraExp" in d and "optFloorDeath" in d and "optFollowers" in d and "optSideView" in d and "optSlipDeath" in d and "optTransparent" in d and "partyMembers" in d and "ship" in d and "skillTypes" in d and "sounds" in d and "startMapId" in d and "startX" in d and "startY" in d and "switches" in d and "terms" in d and "testBattlers" in d and "testTroopId" in d and "title1Name" in d and "title2Name" in d and "titleBgm" in d and "variables" in d and "versionId" in d and "victoryMe" in d and "weaponTypes" in d and "windowTone" in d:
        return _MV_SYSTEM_TYPE
    elif "id" in d and "animationId" in d and "description" in d and "etypeId" in d and "traits" in d and "iconIndex" in d and "name" in d and "note" in d and "params" in d and "price" in d and "wtypeId" in d:
        return _MV_WEAPON_TYPE
    elif "code" in d:
        if d['code'] == 401 and "parameters" in d:
            return _MV_DIALOGUE_TYPE
        elif d['code'] == 102 and "parameters" in d:
            return _MV_CHOICE_TYPE
    else:
        return _MV_UNKNOWN_TYPE

_MV_CHARACTER_TYPE = 0
_MV_ARMOR_TYPE = 1
_MV_CLASS_TYPE = 2
_MV_ENEMY_TYPE = 3
_MV_ITEM_TYPE = 4
_MV_MAP_TYPE = 5
_MV_SKILL_TYPE = 6
_MV_STATE_TYPE = 7
_MV_SYSTEM_TYPE = 8
_MV_WEAPON_TYPE = 9
_MV_DIALOGUE_TYPE = 10
_MV_CHOICE_TYPE = 11
_MV_UNKNOWN_TYPE = 12
_MV_SYSTEM_TERMS = ["basic", "commands", "params"]
_MV_SYSTEM_NAMES = ['armorTypes', 'elements', 'equipTypes', 'skillTypes', 'weaponTypes']
_MV_SYSTEM_TITLE = "gameTitle"
_MV_SYSTEM_CURRENCY = "currencyUnit"
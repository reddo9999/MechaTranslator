from os import path, makedirs
from io import open
from json import load, dump
from .classes import TranslationDictionary
from multiprocessing.managers import BaseManager

dicFolder = "translations"

def getDictionaries (manager):
    mainDict = {}
    for c in TranslationDictionary.contextNames:
        dictionary = getDic(c)
        sharedDictionary = manager.dict()
        sharedDictionary.update(dictionary)
        mainDict[c] = sharedDictionary
    return mainDict

def saveDictionaries (mainDict):
    for key in TranslationDictionary.contextNames:
        simplerInsideDic = {}
        simplerInsideDic.update(mainDict[key])
        saveDic(simplerInsideDic, key)

def getDic (filename):
    dic = {}
    try:
        if filename != "0Level":
            if path.isfile(path.join(dicFolder, (filename + "Machine.json"))):
                try:
                    with open(path.join(dicFolder, (filename + "Machine.json")), "r", encoding="utf-8") as f:
                        dic.update(load(f, encoding="utf-8"))
                except Exception as e:
                    with open(path.join(dicFolder, (filename + "Machine.json")), "r", encoding="utf-8-sig") as f:
                        dic.update(load(f, encoding="utf-8-sig"))
            if path.isfile(path.join(dicFolder, (filename + "Human.json"))):
                try:
                    with open(path.join(dicFolder, (filename + "Human.json")), "r", encoding="utf-8") as f:
                        dic.update(load(f, encoding="utf-8"))
                except Exception as e:
                    with open(path.join(dicFolder, (filename + "Human.json")), "r", encoding="utf-8-sig") as f:
                        dic.update(load(f, encoding="utf-8-sig"))
        else:
            if path.isfile(path.join(dicFolder, (filename + ".json"))):
                try:
                    with open(path.join(dicFolder, (filename + ".json")), "r", encoding="utf-8") as f:
                        dic.update(load(f, encoding="utf-8"))
                except Exception as e:
                    with open(path.join(dicFolder, (filename + ".json")), "r", encoding="utf-8-sig") as f:
                        dic.update(load(f, encoding="utf-8-sig"))
        return dic
    except Exception as e:
        print(str(e) + ": Error loading old translations. Will create new file. Stop now if that's not wanted.")
    return {}

def saveDic (dic, filename):
    if not path.exists(dicFolder):
        makedirs(dicFolder)
    machine = {}
    personal = {}
    for key in dic:
        if key != "open":
            if not TranslationDictionary.isMachineTranslation(dic[key]):
                personal[key] = dic[key]
            elif TranslationDictionary.isCurrentMachineTranslation(dic[key]):
                machine[key] = dic[key]
    if filename != "0Level":
        with open(path.join(dicFolder, (filename + "Machine.json")), "w", encoding="utf-8") as f:
            dump(machine, f, indent=4, sort_keys=True, ensure_ascii=False)
        with open(path.join(dicFolder, (filename + "Human.json")), "w", encoding="utf-8") as f:
            dump(personal, f, indent=4, sort_keys=True, ensure_ascii=False)
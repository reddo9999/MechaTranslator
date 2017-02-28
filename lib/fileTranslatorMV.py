from os.path import basename
from .classes import TranslationBlockRPGMV
import codecs
import json

backupExt = ".mekkabakkapu"

def translateFile (filename, options, input, output, inputSemaphore, outputSemaphore, progress, total):
    if filename.find(".mekkabakkapu") != -1:
        return
    print ("Translating " + basename(filename) + " (" + str(progress) + "/" + str(total) + ")")

    global relevantDicts
    relevantDicts = []
    try:
        try:
            with codecs.open(filename + backupExt, "r", encoding="utf-8") as fo:
                oregano = json.load(fo, encoding="utf-8")
                fo.close()
            with codecs.open(filename + backupExt, "r", encoding="utf-8") as fo:
                file = json.load(fo, encoding="utf-8")
                fo.close()
        except:
            with codecs.open(filename, "r", encoding="utf-8") as f:
                oregano = json.load(f, encoding="utf-8")
                f.close()
            with codecs.open(filename, "r", encoding="utf-8") as f:
                file = json.load(f, encoding="utf-8")
                f.close()
    except Exception as e:
        print("Failed to open JSON: " + str(e))
        return

    walk(file)

    i = 0
    while i < len(relevantDicts):
        block = TranslationBlockRPGMV.TranslationBlockRPGMV(relevantDicts[i], options, i)
        input.append(block)
        inputSemaphore.release()
        i+= 1

    while i > 0:
        outputSemaphore.acquire()
        block = output.pop()
        block.apply(relevantDicts)
        i-=1

    try:
        with codecs.open(filename, "w", encoding="utf-8") as f:
            json.dump(file, f, sort_keys=False, ensure_ascii=False)
            f.close()
        with codecs.open(filename + backupExt, "w", encoding="utf-8") as f:
            json.dump(oregano, f, sort_keys=False, ensure_ascii=False)
            f.close()
    except Exception as e:
        print("Failed to save JSON: " + str(e))
        return

relevantDicts = []

def listWalk(d):
    for k, v in enumerate(d):
        if isinstance(v, dict):
            walk(v)
        elif isinstance(v, list):
            listWalk(v)

def walk(d):
    global relevantDicts
    if isinstance(d, dict) and TranslationBlockRPGMV._MVfindType(d) != TranslationBlockRPGMV._MV_UNKNOWN_TYPE:
        relevantDicts.append(d)
    elif isinstance(d, dict):
        for k,v in d.items():
            if isinstance(v, dict):
                walk(v)
            elif isinstance(v, list):
                listWalk(v)
    elif isinstance(d, list):
        listWalk(d)
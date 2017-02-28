from os.path import basename
from codecs import open
from .classes.TranslationBlockRPGMTrans import TranslationBlockRPGMTrans
from .classes.TranslationBlockRPGMTransV2 import TranslationBlockRPGMTransV2
from .classes import TranslationOptions
from time import sleep

def translateFile (filename, options, input, output, inputSemaphore, outputSemaphore, progress, total):
    isScripts = basename(filename).find("Scripts") != -1
    isActors = basename(filename).find("Actors") != -1
    if isScripts and not options['translateScripts']:
        print("Skipping Scripts.txt due to user choice.")
        return
    if isActors and not options['translateActors']:
        print("Skipping Actors.txt due to user choice.")
        return

    count = 0
    try:
        with open(filename, "r", "utf-8") as file:
            print ("Translating " + basename(filename) + " (" + str(progress) + "/" + str(total) + ")")
            lines = file.read().splitlines()
            count = 0
            if options['type'] == TranslationOptions._RPGMAKERV2:
                translationBlock = TranslationBlockRPGMTransV2(options, isScripts, count)
            else:
                translationBlock = TranslationBlockRPGMTrans(options, isScripts, count)
            for line in lines:
                if translationBlock.addLine(line) == 1:
                    try:
                        input.append(translationBlock)
                        inputSemaphore.release()
                    except Exception as e:
                        print ("Unable to feed queue for " + basename(filename) + ": " + str(e))
                    count+=1
                    if options['type'] == TranslationOptions._RPGMAKERV2:
                        translationBlock = TranslationBlockRPGMTransV2(options, isScripts, count)
                    else:
                        translationBlock = TranslationBlockRPGMTrans(options, isScripts, count)
            file.close()
    except Exception as e:
        print ("Unable to open " + basename(filename) + ": " + str(e))

    while count > 0:
        outputSemaphore.acquire()
        count -= 1

    ordered = sorted(output, key = lambda TranslationString : TranslationString.position)

    allLines = []
    for block in ordered:
        allLines.extend(block.getTranslatedLines())

    with open(filename, "w", "utf-8") as file:
        file.write("\r\n".join(allLines))
        file.close()

    del output[:]
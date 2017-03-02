# from lib.classes.TestClass import *
#
# a = TestClass()
# a.hi()
from tkinter import Tk
from multiprocessing import Process, Manager, cpu_count, freeze_support
from lib.classes.TranslationOptions import TranslationOptions
from lib import dictionaryLoader, fileLoader
from lib.classes.TranslationEngine import TranslationEngine
from lib.classes.TranslationDictionary import TranslationDictionary
from os.path import basename
from lib import fileTranslator
from lib import fileTranslatorMV
from lib import MVPlugin
from time import sleep, time
import sys

def translationThread (threadNum, dictionary, inputList, outputList, inputSemaphore, outputSemaphore):
    dic = TranslationDictionary(dictionary)
    translationEngine = TranslationEngine(dic)
    while True:
        inputSemaphore.acquire()
        myBlock = inputList.pop()
        try:
            myBlock.translate(translationEngine)
        except Exception as e:
            print("Thread " + str(threadNum) + " failed to translate: " + str(e))
        outputList.append(myBlock)
        outputSemaphore.release()

if __name__ == '__main__':
    freeze_support()
    Tk().withdraw()


    manager = Manager()
    dic = dictionaryLoader.getDictionaries(manager)
    a = 1
    threads = cpu_count() * 5
    procs = []
    inputList = manager.list()
    output = manager.list()
    inputSemaphore = manager.Semaphore(0)
    outputSemaphore = manager.Semaphore(0)

    try:
        while a <= threads:
            p = Process(target=translationThread, args = (a, dic, inputList, output, inputSemaphore, outputSemaphore))
            p.start()
            procs.append(p)
            a+=1
    except Exception as e:
        print("Unable to start thread " + str(a) + ":" + str(e))

    file = fileLoader.getFile()
    options = TranslationOptions()
    options.askOptions()

    if basename(file) == "RPGMKTRANSPATCH":
        options.setRPGMakerTrans()
    elif basename(file) == "GameDat.txt":
        options.setWolf()
    elif basename(file) == "package.json":
        options.setRPGMakerMV()

    files = fileLoader.getFiles(file, options)

    optionsDict = manager.dict()
    options.updateTo(optionsDict)

    totalFiles = len(files)
    print ("Translating " + str(totalFiles) + " files.")
    start_time = time()
    unknownContexts = []
    if options.isWolf() or options.isRPGMakerTrans() or options.isRPGMakerV2():
        current = 1
        for f in files:
            fileTranslator.translateFile(f, optionsDict, inputList, output, inputSemaphore, outputSemaphore, current, totalFiles, unknownContexts)
            current += 1
    elif options.isRPGMakerMV():
        current = 1
        for f in files:
            fileTranslatorMV.translateFile(f, optionsDict, inputList, output, inputSemaphore, outputSemaphore, current, totalFiles)
            current +=1
        if options.mvAddWrapPlugin:
            print("Adding Word Wrap plugin by Dr.Yami.")
            MVPlugin.addPlugin(file)

    try:
        dictionaryLoader.saveDictionaries(dic)
    except Exception as e:
        print("Was unable to save old translations.")

    for p in procs:
        p.terminate()

    if len(unknownContexts) > 0:
        print ("Printing contexts which were not found:")
    for block in unknownContexts:
        string = str(block.originalStrings) + " from " + str(block.contexts)
        try:
            print (string)
        except:
            print ("Original String not available from " + str(block.contexts))

    input("Finished in " + (str(time() - start_time)) + " seconds. Press Enter to exit.")
    exit()
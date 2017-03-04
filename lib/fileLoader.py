from .fileTranslatorMV import backupExt
from tkinter import filedialog
from os import path, listdir

def getFile ():
    return filedialog.askopenfilename(initialdir='.', filetypes=[('RPG Maker/Wolf Trans Patch', 'RPGMKTRANSPATCH;GameDat.txt;package.json')])

def getFiles (file, options):
    folder = path.abspath(path.dirname(file))
    folders = []
    if path.basename(file) == "RPGMKTRANSPATCH":
        if not path.exists(path.join(folder, "patch")):
            options.setRPGMakerV2()
        else:
            folders = ['patch']
    elif path.basename(file) == "GameDat.txt":
        folders = ['common', path.join('db', 'CDataBase'), path.join('db', 'DataBase'), 'mps']
    elif path.basename(file) == "package.json":
        folders = [path.join("www", "data")]
    else:
        print("Unknown patch type.")
        exit()
    allFiles = []
    for f in folders:
        if (options.isRPGMakerV2()):
            newFiles = listdir(folder)
        else:
            newFiles = (listdir(path.join(folder, f)))
        newFilesCorrected = []
        i = 0
        while i < len(newFiles):
            if newFiles[i].find(backupExt) == -1 and newFiles[i].find("RPGMKTRANSPATCH") == -1 and newFiles[i].find("UnknownContexts") != -1:
                if (options.isRPGMakerV2()):
                    newFilesCorrected.append(path.join(folder, newFiles[i]))
                else:
                    newFilesCorrected.append(path.join(folder, f, newFiles[i]))
            i+=1
        allFiles.extend(newFilesCorrected)
    allFiles.sort(key = path.getsize, reverse=True)
    return allFiles
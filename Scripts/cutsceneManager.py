import os, importlib.util

def findNextAvailableID(List):
    KeyList = List.keys()
    for i in range(len(List) + 1):
        if not i in KeyList:
            return i
                
cutsceneActive = True
cutsceneID = 0
cutsceneList = {}

def init():
    for i in os.listdir(os.getcwd()+r"\Cutscenes"):
        if i in {
            "templateCutscene.py",
            "__pycache__",
        }:
            continue
        module = importlib.util.spec_from_file_location("platformingInitializeCutscene", "Cutscenes\platformingInitializeCutscene.py")
        moduleProper = importlib.util.module_from_spec(module)
        module.loader.exec_module(moduleProper)
        cutsceneList[findNextAvailableID(cutsceneList)] = moduleProper    


if __name__ == "__main__":
    init()
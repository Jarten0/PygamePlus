import character, cameramanager, boards, platforms, os, sys, importlib.util
#from timer import Timer

def findNextAvailableID(List):
    KeyList = List.keys()
    for i in range(len(List) + 1):
        if not i in KeyList:
            return i
                
cutsceneActive = False
cutsceneID = 0
cutsceneList = {
}

def main():
    for i in os.listdir(os.getcwd()+r"\Cutscenes"):
        module = importlib.util.spec_from_file_location("platformingInitializeCutscene", "Cutscenes\platformingInitializeCutscene.py")
        moduleProper = importlib.util.module_from_spec(module)
        module.loader.exec_module(moduleProper)
        cutsceneList[findNextAvailableID(cutsceneList)] = moduleProper    

    for i in cutsceneList:
        cutsceneList[i].start()


if __name__ == "__main__":
    main()
import os, importlib.util

def findNextAvailableID(List):
    KeyList = List.keys()
    for i in range(len(List) + 1):
        if not i in KeyList:
            return i
                
componentList = {}

def init():
    for i in os.listdir(os.getcwd()+'\Scripts\Components'):
        if i in {"templateCutscene.py", "__pycache__"}:
            continue
        moduleSpec = importlib.util.spec_from_file_location(i, 'Scripts\Components\ ' - '' + i)
        module = importlib.util.module_from_spec(moduleSpec)
        moduleSpec.loader.exec_module(module)
        componentList[i] = module    


if __name__ == "__main__":
    init()
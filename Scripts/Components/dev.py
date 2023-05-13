# pyright: reportGeneralTypeIssues=false

from main import newPrefab, newComponent
from random import randint as r
from os import getcwd

@newComponent
class Button:
    def Start(self, mode):
        pass


@newPrefab
class devInterface(): 
    def Start(self): 
        self.newComponent(devScript)


@newComponent
class devScript:
    def Start(self): 
        self.fileInterface = ""
        self.modes = {
            "idle": idle,
            "component": createComponentMode,            
            "prefab": createPrefabMode,
            "inspect": inspect
        }
        with open(getcwd()+"\\DevInterface.py", "w") as wf: pass
        
        @fileDec
        def runFileInterface(readfile, writefile):
            file.write()

    def fileDec(func):
        with open(getcwd()+"\\DevInterface.py") as rf:
            with open(getcwd()+"\\DevInterface.py", "w") as wf:
                func(rf, wf)

    def updateMode(self):
        self.mode = self.newComponent()
    
    def Update(self):
        @fileDec
        def updateFileInterface(readfile, writefile):
            if 'exit' in readfile.readline():
                self.mode = self.newComponent(idle)
            self.modes[self.mode]()

@newComponent
class idle:
    def Start(self):
        pass
    def Update(self):
        @devScript.fileDec
        def _(rf, wf):
            wf.writefile(
"""Welcome to dev interface

Type in a mode in the line below:
>
And type in done below to confirm:
>
""")        
            if not 'done' in rf.readline(5).lower: return

            if rf.readline(3).removeprefix(">").lower() in self.parent.modes:
                self.parent.mode = self.parent.newComponent(self.parent.modes[rf.readline(3).removeprefix(">").lower()])
@newComponent
class createComponentMode: pass
def createPrefabMode():
    file = readfile.read()

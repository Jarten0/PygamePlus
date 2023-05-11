# pyright: reportGeneralTypeIssues=false

from main import newPrefab, newComponent
from random import randint as r
@newPrefab
class ButtonObj:
    def Start(self, 
        x=0, y=0,
        xl=50, yl=50,
        color = (r(0, 255), r(0, 255), r(0, 255)),
        ):

        self.newComponent("components\\Transform", x, y)
        self.newComponent("Renderer\\Renderer", xl,yl,)
        self.newComponent("Collider\\Collider", 50, 50)


@newComponent
class Button:
    def Start(self):
        self.Renderer = self.parent.Renderer

@newPrefab
class devInterface(): 
    def Start(self): 
        self.newComponent(devScript)


@newComponent
class devScript:
    def Start(self): pass
    def Update(self): pass

# pyright: reportGeneralTypeIssues=false

from main import Component, newPrefab, newComponent
from random import randint as r
@newPrefab
class ButtonObj: # type: ignore
    def init(self, 
        x=0, y=0,
        xl=50, yl=50,
        color = (r(0, 255), r(0, 255), r(0, 255)),

        ):
        Transform = self.newComponent("components\\Renderer",
            x, y)
        Renderer = self.newComponent("Renderer\\Renderer",
            Transform,
            xl,yl,
            )
        Collider = self.newComponent("Collider\\Collider",
            Transform,
            50, 50                         
        )

        return {
            "Transform": Transform,
            "Renderer": Renderer,
            "Collider": Collider
        }

@newComponent
class Button:
    def init(self, components):
        self.Renderer = components['Renderer']

@newPrefab
class devInterface(): 
    def init(self): 
        devScript = self.newComponent()

@newComponent
class devScript:
    def init(self): pass
    def update(self): pass

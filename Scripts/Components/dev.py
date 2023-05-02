from main import Component, newPrefab, newComponent
from random import randint as r
@newPrefab
class ButtonObj: # type: ignore
    def init(self, 
        x=0, y=0,
        xl=50, yl=50,
        color = (r(0, 255), r(0, 255), r(0, 255)),

        ):
        Transform = Component.new("components\\Renderer",
            x, y)
        Renderer = Component.new("Renderer\\Renderer",
            Transform,
            xl,yl,
            )
        Collider = Component.new("Collider\\Collider",
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
class devInterface(): pass

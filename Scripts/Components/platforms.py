import Scripts.Components.Collider
import Scripts.Components.Renderer
import Scripts.Components.components as MainComponent
from Scripts.componentManager import *
Main = __import__("__main__")



@newComponent
class Platform:

    class InteractFunc:
        def __init__(self, func):
            self.func = func

    @InteractFunc
    def hehe(self, object):
        print("Hehe")


    InteractFunc(hehe)

    interactionFunctions = {}

    requiredDependencies={
        "Transform" : MainComponent.Transform ,
        "Collider"  : Scripts.Components.Collider.Collider ,
        "Renderer"  : Scripts.Components.Renderer.Renderer ,
    }

    def Start(self, Scene, parent, xLength:int=0, yLength:int=0, platformType:int=0) -> None: # type: ignore
        self.Transform = parent.Transform
        self.Collider = parent.Collider
        self.Renderer = parent.Renderer 

        self.xLength = xLength
        self.yLength = yLength
        self.type  = platformType

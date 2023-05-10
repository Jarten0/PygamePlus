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
    }

    def init(self, Transform:MainComponent.Transform, Collider:Scripts.Components.Collider.Collider, 
    xLength:int=0, yLength:int=0, platformType:int=0, Renderer:Scripts.Components.Renderer.Renderer|None = None, **kwargs) -> None: # type: ignore
        self.Transform = Transform
        self.Collider = Collider
        self.Renderer = Renderer 

        self.xLength = xLength
        self.yLength = yLength
        self.type  = platformType

    def update__(self) -> None:
        pass
import Scripts.Components.components as MainComponent
from Scripts.componentManager import *
Main = __import__("__main__")



@newComponent
class Platform():
    requiredDependencies={
        "Transform" : MainComponent.Transform ,
        "Collider"  : MainComponent.Collider ,
    }
    
    
    placeprop = {
    0: {
        "#HasPlaceReq": False,
        "#object": False,},
    1: {
        "#HasPlaceReq": False,
        "#object": False,},
    2: {
        "#HasPlaceReq": True,
        "xl": False,
        "yl": 7,
        "#object": False,},
    3: {
        "#HasPlaceReq": True,
        "xl": False,
        "yl": False,
        "#object": False,},
    4: {
        "#HasPlaceReq": True,
        "xl": 30,
        "yl": 10,
        "#object": True},
    }

    @classmethod
    def create(cls,
        Transform:MainComponent.Transform=MainComponent.Transform,
        Collider :MainComponent.Collider|None = None, # type: ignore
        ) -> object:
        
        return "New Platform", cls, {
            'Transform': Transform,
            'Collider': Collider
        }

    def init(self, Transform:MainComponent.Transform, Collider:MainComponent.Collider, 
    xLength:int=0, yLength:int=0, platformType:int=0, Renderer:MainComponent.Renderer|None = None, **kwargs) -> None: # type: ignore
        self.Transform = Transform
        self.Collider = Collider
        self.Renderer = Renderer 

        self.xLength = xLength
        self.yLength = yLength
        self.type  = platformType

    def update__(self) -> None:
        pass
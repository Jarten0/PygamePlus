import Scripts.Components.Collider
import Scripts.Components.Renderer
import Scripts.Components.components as MainComponent
from Scripts.componentManager import *
Main = __import__("__main__")



@newComponent
class Platform():
    requiredDependencies={
        "Transform" : MainComponent.Transform ,
        "Collider"  : Scripts.Components.Collider.Collider ,
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
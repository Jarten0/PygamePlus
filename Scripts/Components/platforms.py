import pygame as pyg
import Scripts.Components.components as MainComponent
import Scripts.timer  as Timer
import Scripts.boards as Boards
from Scripts.inputMapper import Input
from Scripts.componentManager import *
Main = __import__("__main__")


#wrappa
@dependencyWrapper_
class Platform():
    requiredDependencies={
        "Transform" : MainComponent.Transform ,
        "Renderer"  : False ,
        "ConfigData": False ,
        "Collider"  : MainComponent.Collider ,
        "RigidBody" : False ,
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

    def create__(
        Transform:MainComponent.Transform=MainComponent.Transform,
        Renderer :MainComponent.Renderer =MainComponent.Transform,
        ):
        Transform = Transform
        Renderer  = Renderer

    @initializationWrapper_
    def initialize__(self, Transform:MainComponent.Transform, Collider:MainComponent.Collider, 
    xLength:int, yLength:int, platformType:int, Renderer:MainComponent.Renderer|None = None) -> None:
        self.Transform = Transform
        self.Collider = C
        self.Renderer = Renderer 

        self.xLength = xLength
        self.yLength = yLength
        self.type  = platformType

    def update__(self) -> None:
        pass
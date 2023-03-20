import pygame as pyg
import Scripts.Components.components as MainComponent
import Scripts.timer  as Timer
import Scripts.boards as Boards
from Scripts.inputMapper import Input
from Scripts.componentManager import *
Main = __import__("__main__")

def NextID(platformList) -> int:
    keylist = platformList.keys()
    #print(keylist, platformList)
    for i in range(len(platformList)):
        if not i in keylist:
            name = i
            return name
    return len(platformList)

#This is responsible for all of the actions a Character can do
#Mostly used for the player character
@dependencyWrapper_
class Platform():
    requiredDependencies={
        "Transform" : MainComponent.Transform ,
        "Renderer"  : MainComponent.Renderer  ,
        "ConfigData": False ,
        "Collider"  : False ,
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
    @initializationWrapper_
    def initialize__(self, Transform: MainComponent.Transform, Renderer: MainComponent.Renderer,
    xLength:int, yLength:int, platformType:int) -> None:
        self.Transform = Transform
        self.xLength = xLength
        self.yLength = yLength
        self.type  = platformType

    def update__(self) -> None:
        pass
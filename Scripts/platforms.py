import pygame as pyg
import Scripts.Components.components as MainComponent
import Scripts.timer  as Timer
import Scripts.boards as Boards
import Scripts.input  as Input
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
@dependencyWrapper_(requiredDependencies={
    "Transform" : MainComponent.Transform ,
    "Renderer"  : MainComponent.Renderer  ,
    "ConfigData": False ,
    "Collider"  : False ,
    "RigidBody" : False ,
}) # type: ignore
class Platform():
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
    @initializeWrapper_
    def initialize__(self, Transform: MainComponent.Transform, Renderer: MainComponent.Renderer,
    xLength:int, yLength:int, platformType:int) -> None:
        self.Transform = Transform
        self.xLength = xLength
        self.yLength = yLength
        self.type  = platformType
        self.color = platcolors[self.platformType]

    class types():
        def wall(self, prop, character) -> None:
            pTBC = prop["platformToBeChecked"]
            if wallcheck[1]:       
                char.gr = True
                char.y = pTBC.y - char.yl  
                char.yv = 0
                Timer.set("CoyoteTime", 0, True)
            
            if wallcheck[2] or wallcheck[4]:
                    char.wj = True
                    char.w = [wallcheck[2], wallcheck[4]]
        
        def passthrough(self, prop) -> None:
            wallcheck = prop["wallcheck"]
            char = prop["char"]
            pTBC = prop["platformToBeChecked"]
            if wallcheck[1]:
                if char.yv >= 0 and not Boards.getFromPerm("down"):           
                    char.gr = True
                    char.y = pTBC.y - char.yl  
                    char.yv = 0
                    #Timer.set("dashcool", True)
                    Timer.set("CoyoteTime", 0, True)

        def lava(self, prop) -> None:
            if prop["wallcheck"][0]:
                prop["char"].die()
        
        def bounce(self, prop) -> None:
            char = prop["char"]
            if prop["wallcheck"][0]:
                char.resetDash()
                char.yv = -22
                if char.xv > char.speed:
                    char.xv = char.speed
                elif char.xv < -char.speed:
                    char.xv = -char.speed     
                
        functionList = {
            1: wall,
            2: passthrough,
            3: lava,
            4: bounce,
        }
                    
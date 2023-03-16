import pygame as pyg
import Scripts.Components.components as MainComponent
import Scripts.Components.character as CharacterComponent
import Scripts.timer  as Timer
import Scripts.boards as Boards
import Scripts.input  as Input
from Scripts.componentDependencyDecorators import *
Main = __import__("__main__")


@dependencyWrapper(requiredDependencies={
    'Controller': MainComponent.Controller,
    'Character' : CharacterComponent.Character,
}) # type: ignore
class Camera():
    @initializationWrapper
    def initialize(self, 
    Character:  CharacterComponent.Character, 
    Controller: MainComponent.Controller,
    dependencies:dict, *args) -> None:
        self.Character = Character
        self.Controller = Controller
    
        self.xPosition = 0
        self.yPosition = 0
    

    def update(cam):
        if Controller.currentInpu("LEFT"):
            cam.xOffset -= 10
        elif Boards.getP("RIGHT"):
            cam.xOffset += 10
        if Boards.getP("UP"):
            cam.yOffset -= 10
        elif Boards.getP("DOWN"):
            cam.yOffset += 10

        if Boards.getP("up") or Boards.getP("down") or Boards.getP("left") or Boards.getP("right"):
            cam.xOffset = 0
            cam.yOffset = 0

        if char.x + 1 >= p.screen_width / 2 and char.x < level.length - p.screen_width / 2:
            cam.xdefault = char.x - p.screen_width / 2    
        else:
            if char.x <= p.screen_width / 2:
                cam.xdefault = 0
            else:
                cam.xdefault = level.length - p.screen_width

        if char.y +1 >= p.screen_height / 2 and char.y < level.height - p.screen_height / 2:
            cam.ydefault = char.y - p.screen_height / 2    
        else:
            if char.y < p.screen_height / 2:
                cam.ydefault = 0
            else:
                cam.ydefault = level.height - p.screen_height   
                
        cam.xpos = cam.xdefault + cam.xOffset
        cam.ypos = cam.ydefault + cam.yOffset
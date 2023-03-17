import pygame as pyg
from   Scripts.componentManager import *
import Scripts.Components.components as MainComponent
import Scripts.Components.character as CharacterComponent
import Scripts.timer  as Timer
import Scripts.boards as Boards
import Scripts.input  as Input
Main = __import__("__main__")


@dependencyWrapper_(requiredDependencies={
    'Transform' : MainComponent.Transform,
    'Controller': MainComponent.Controller,
    'Character' : CharacterComponent.Character,
}) # type: ignore
class Camera():
    @initalizeOnStartWrapper_
    def create__(Character) -> MainComponent.DependenciesTemplate:
        Camera = Main.createObject()
        Camera.Transform = MainComponent.Transform()
        Camera.Controller = MainComponent.Controller()
        Camera.Character = Character
        Camera = Main.createComplexObject(
            Transform= Camera.Transform,
            Controller=Camera.Controller,
            Character=Camera.Character
        )
        
        return Camera

    @initializationWrapper_
    def initialize__(self, 
    Transform:  MainComponent.Transform,
    Character:  CharacterComponent.Character, 
    Controller: MainComponent.Controller,
    dependencies:dict, *args) -> None:
        self.Transform = Transform
        self.Character = Character
        self.Controller = Controller

    def update__(self):
        char = self.Character
        p, level = Main.Settings, Main.level
        if MainComponent.Controller.currentInputs["LEFT"]:
            self.xOffset -= 10
        elif MainComponent.Controller.currentInputs["RIGHT"]:
            self.xOffset += 10
        if MainComponent.Controller.currentInputs["UP"]:
            self.yOffset -= 10
        elif MainComponent.Controller.currentInputs["DOWN"]:
            self.yOffset += 10

        if MainComponent.Controller.currentInputs["up"] or MainComponent.Controller.currentInputs["down"] or MainComponent.Controller.currentInputs["left"] or MainComponent.Controller.currentInputs["right"]:
            self.xOffset = 0
            self.yOffset = 0

        if char.Transform.xPosition + 1 >= p.screen_width / 2 and char.Transform.xPosition < level.length - p.screen_width / 2:
            self.xdefault = char.Transform.xPosition - p.screen_width / 2    
        else:
            if char.Transform.xPosition <= p.screen_width / 2:
                self.xdefault = 0
            else:
                self.xdefault = level.length - p.screen_width

        if char.Transform.yPosition +1 >= p.screen_height / 2 and char.Transform.yPosition < level.height - p.screen_height / 2:
            self.ydefault = char.Transform.yPosition - p.screen_height / 2    
        else:
            if char.Transform.yPosition < p.screen_height / 2:
                self.ydefault = 0
            else:
                self.ydefault = level.height - p.screen_height   
                
        self.xpos = self.xdefault + self.xOffset
        self.ypos = self.ydefault + self.yOffset
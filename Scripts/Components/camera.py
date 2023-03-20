import pygame as pyg
from   Scripts.componentManager import *
import Scripts.Components.components as MainComponent
import Scripts.Components.character as CharacterComponent
import Scripts.timer  as Timer
import Scripts.boards as Boards
from Scripts.inputMapper  import Input
Main = __import__("__main__")


@dependencyWrapper_
class Camera():
    requiredDependencies={
    'Transform' : MainComponent.Transform,
}
    @initializeOnStartWrapper_
    def create__() -> MainComponent.DependenciesTemplate:
        camera = Main.createComplexObject(
            name = 'Camera', class_=Camera,
            Transform=  MainComponent.Transform(),
        )
        
        return camera

    @initializationWrapper_
    def initialize__(self, 
        Transform:  MainComponent.Transform, 
        dependencies:dict, *args, **kwargs) -> None:
        
        self.Transform = Transform

    def update__(self) -> None:
        if 'Character' in Main.Objects:
            Character = Main.Objects['Character']
        else:
            self.xpos = 0
            self.ypos = 0
            return
    
        if Character.direction == 'left':
            focusPointx = Character.Transform.xPosition - 20

        p, level = Main.Settings, Main.level
        if Input.getHeld("LEFT"):
            self.xOffset -= 10
        elif Input.getHeld("RIGHT"):
            self.xOffset += 10
        if Input.getHeld("UP"):
            self.yOffset -= 10
        elif Input.getHeld("DOWN"):
            self.yOffset += 10

        if Input.getHeld("up") or Input.getHeld("down") or Input.getHeld("left") or Input.getHeld("right"):
            self.xOffset = 0
            self.yOffset = 0

        if Character.Transform.xPosition + 1 >= p.screen_width / 2 and Character.Transform.xPosition < level.length - p.screen_width / 2:
            self.xdefault = Character.Transform.xPosition - p.screen_width / 2    
        else:
            if Character.Transform.xPosition <= p.screen_width / 2:
                self.xdefault = 0
            else:
                self.xdefault = level.length - p.screen_width

        if Character.Transform.yPosition +1 >= p.screen_height / 2 and Character.Transform.yPosition < level.height - p.screen_height / 2:
            self.ydefault = Character.Transform.yPosition - p.screen_height / 2    
        else:
            if Character.Transform.yPosition < p.screen_height / 2:
                self.ydefault = 0
            else:
                self.ydefault = level.height - p.screen_height   
                
        self.xpos = self.xdefault + self.xOffset
        self.ypos = self.ydefault + self.yOffset
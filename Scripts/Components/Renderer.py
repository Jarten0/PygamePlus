# pyright: reportGeneralTypeIssues=false

from Scripts.Components.components import Transform
from Scripts.componentManager import newComponent


import pygame as pyg


from os import getcwd
from sys import exit


@newComponent
class Renderer():
    """Draws an image, sprite from spritesheet, or rectangle to the screen. Has quite a few arguments.
    Required:
    path: str # example = '\\Assets\\Images\\[image name], pull from root of framework, ie where main.py is located
    tier: int # used for increased render ordering capabilities. Refer to the renderer tier txt
    Optional:
    xOffset:float=0 # Offsets are used for rendering offsetted from the Transform point 
    yOffset:float=0
    <These next ones are used for selecting what part of the image is going to be used.
    Still functional with spritesheets, but you must keep these in mind>
    xStart :float=0 # Used to pick from where in an image the render point starts. Anything before that is cropped out
    yStart :float=0
    xLength:float=0 # Used to pick how much of an image is used. Anything outside of that is cropped out
    yLength:float=0
    surfaceRows: int = 1 # This is important if you want to use images from a spritesheet. This is how many horizontal sprites are in the image.
    surfaceColumns: int = 1 # Same as rows, but vertically.
    <the rest of these are a bit more advanced, change if you so wish>
    surface: Pygame Surface, if you want to handle loading of images yourself
    alpha = int, 0-100, if you want to change the opacity of the object 
    autoCulling: bool=True, optimization that stops from rendering if the object is off screen
    """

    requiredDependencies={
    "Transform": Transform
    }
    arguments = {
        "path        ": "''",
        "tier        ": 3,
        "xOffset     ":0.0,
        "yOffset     ":0.0,
        "xLength     ":0.0,
        "yLength     ":0.0,
        "color       ":(30, 30, 30),
        "surface     ": pyg.image.load(getcwd()+"\\Assets\\Images\\MissingImage.png"),
        "alpha       ": 0.0,
        "surfaceRows ": 1,
        "surfaceColumns": 1,
        "autoCulling ": True
    }
    optionalArguments = {
        "xOffset     ",
        "yOffset     ",
    }

    colors = {
    "red":   (255, 0,   0  ),
    "green": (0,   255, 0  ),
    "blue":  (0,   0,   255),
    "gray":  (30,  30,  30 ),
    }
    
    def init(self,
        Transform,
        path: str|None = None,
        tier: int = 3,
        xOffset:float=0, yOffset:float=0,
        xLength:float=0, yLength:float=0,
        color:tuple[int, int, int]=colors["gray"],
        surface:pyg.Surface|None = None,
        alpha: int = 0,
        surfaceRows:int = 1, surfaceColumns:int = 1,
        autoCulling:bool = True,
        **kwargs) -> None:

        if path == None:
            self.path = "\\Assets\\Images\\MissingImage.png"
            self.surface = pyg.image.load(getcwd()+self.path)
        elif isinstance(path, str):
            self.surface = pyg.image.load(getcwd()+path)
        else:
            if surface == None:
                exit("No available path or surface"+ str(path))
            self.surface = surface

        self.mode = 'rect'
        self.area    = ()
        self.Transform = Transform
        self.tier    = tier
        self.xOffset, self.yOffset, self.xLength, self.yLength = \
            xOffset, yOffset, xLength, yLength
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.xLength = xLength
        self.yLength = yLength
        self.color   = color
        self.alpha   = alpha
        self.autoCull = autoCulling

        self.flags = {
        "flipHorizontal": False,
        "flipVertical"  : False,
        }

    def update(self):
        print("Am updating")

    def render(self, Screen: pyg.Surface, Camera, **kwargs):
        if self.mode == 'rect':            
            pyg.draw.rect(Screen, self.color, 
               (int(self.Transform.xPos + self.xOffset,) - int(Camera.xPosition), int(self.Transform.yPos + self.yOffset,) - 
                int(Camera.yPos), int(self.xLength), int(self.yLength))
            )


            return
        
        Screen.blit(
            source = self.surface,
            dest = (int(self.Transform.xPos) - int(self.xOffset) - Camera.xPos,
                    int(self.Transform.yPos) - int(self.yOffset) - Camera.yPos))

    def flip(self, flipVertically: bool = False, value: str | bool = "invert"):
        try:
            direction = 'flipHorizontal'
            if flipVertically == True: direction = 'flipVertical'
            if isinstance(value, str): value = 'invert'
            if value == 'invert': value = not self.flags[direction]
            self.flags[direction] = value

        except KeyError as ke: return ke
"""Contains a group of basic components for fundamental level design. Includes essential components like Transform and ConfigData, among a few other useful ones."""

from sys import exit
if __name__ == "__main__": print(r"Cannot run components script as main :/"); exit()
import pygame         as pyg
from Scripts.componentManager import newComponent
from Scripts import Board

from os         import getcwd
from typing import Any
from main import Object, Component

@newComponent
class Transform():
    """Handles all positioning aspects of an object in world space
    Units are in pixels, 1 unit = 1 pixel
    X: - <> + = left <> right
    Y: - <> + = up   <> down
    Z: - <> + = back <> front
 
    Rotation: 0 - 360, clockwise
    """
    
    requiredDependencies={}
    arguments = {
        "xPosition":0.0, 
        "yPosition":0.0, 
        "zPosition":0,
        "xVelocity":0.0, 
        "yVelocity":0.0, 
        "rotation": 0.0
    }
    optionalArguments = {
        "xPosition", 
        "yPosition", 
        "zPosition",
        "xVelocity", 
        "yVelocity", 
        "rotation"
    }
    
    class Vector:
        def __init__(self, x, y) -> None:
            self.xPosition = self.xPos = self.x = x
            self.yPosition = self.yPos = self.y = y
    

    def init(self,
            xPosition:float=0, yPosition:float=0, zPosition:int=0, 
            xVelocity:float=0, yVelocity:float=0, rotation:float = 0, 
            *args, **kwargs) -> None:
        self.xPosition = self.xPos = self.x = xPosition
        self.yPosition = self.yPos = self.y = yPosition
        self.zPosition = self.zPos = self.z = zPosition
        self.xVelocity = self.xv = xVelocity
        self.yVelocity = self.yv = yVelocity
        self.rotation  = self.r = rotation
    
    def update(self) -> None:
        self.xPosition += self.xVelocity
        self.yPosition += self.yVelocity

    def set(self, vector:Vector):
        self.xPosition

@newComponent
class DependenciesTemplate():
    requiredDependencies={}
 
    def init(self, *args, **kwargs) -> None: 
        pass

@newComponent
class Collider():
    """Used to check as to whether the selected item is colliding with the object
    This will NOT handle collisions, incase it should be used as a collisionless trigger that has an
    activation area. If you want to add collisions, use this in tangent with RigidBody
    
    collideList = list[isColliding, colTop, colBottom, colLeft, colRight]"""

    from main import Object

    requiredDependencies={
    "Transform": Transform 
    }

 
    def init(self, 
            Transform,
            xLength:int=50, yLength:int=50, **kwargs) -> None:
        self.Transform = Transform
        self.xLength = xLength
        self.yLength = yLength
        self.Objects = Object.getAll()
        self.collideList: list[tuple[object, list[bool]]] = []

    def update(self) -> None:
        for i in self.Objects:
            checkList = self.check(i)
            if checkList[0]:
                self.collideList.append((self.Objects[i], checkList))

    def check(self, item) -> list[bool]:
        lis = [False, False, False, False, False]
    #S and I are shorthands for self and item to drastically simplify this function and reduce characters
        s = self.Transform
        i = item.Transform
        #Colliding
        if i.yPosition + item.Collider.yLength >= s.yPosition and i.yPosition <= s.yPosition + self.yLength and i.xPosition + item.Collider.xLength >= s.xPosition and i.xPosition <= s.xPosition + self.xLength:
            return lis
        
        lis[0] = True
        #Top side
        if s.yPosition + (self.yLength / 2) < i.yPosition + (item.Collider.yLength / 2) \
        and s.xPosition > i.xPosition \
        and s.xPosition + self.xLength < i.xPosition + i.Collider.xLength \
        and s.xVelocity > self.xLength and s.xVelocity < -self.xLength:
            lis[1] = True
        
        #Bottom side
        if s.yPosition + (self.yLength / 2) > i.yPosition + (item.Collider.yLength / 2) \
        and s.xPosition > i.xPosition \
        and s.xPosition + self.xLength < i.xPosition + i.Collider.xLength \
        and s.xVelocity > self.xLength and s.xVelocity < -self.xLength:
            lis[2] = True
        
        #Left side
        if s.xPosition + (self.yLength / 2) < i.xPosition + (item.Collider.xLength / 2) \
        and s.yPosition + self.yLength > item.yPosition:
            lis[3] = True
        
        #Right side
        if s.xPosition + (self.yLength / 2) > i.xPosition + (item.Collider.xLength / 2) \
        and s.yPosition + self.yLength > item.yPosition:
            lis[4] = True
        
        return lis

@newComponent
class RigidBody():
    """Used to handle collisions, gravity and other physical forces
    Use with a Collider to properly collide with other objects that have Colliders 
    
    mass = weight of object

    grounded = is touching ground and is unaffected by gravity until leaving ground again. 
    """
    requiredDependencies={
    "Transform": Transform, "Collider": Collider
    }

 
    def init(self,  
            Transform,
            Collider,
            mass:int=0,
            
            **kwargs) -> None:
        self.Transform = Transform
        self.Collider = Collider
        self.mass = mass
        self.grounded = True

    def update(self) -> None:
        if not self.grounded:
            if self.Transform.yVelocity < self.mass: 
                self.Transform.yVelocity += self.mass / 100
                if self.Transform.yVelocity > self.mass:
                    self.Transform.yVelocity = self.mass
        
        self.grounded = False
        for i in self.Collider.collideList:
            item, lis = i
            if lis[1]:
                self.grounded = True
                self.Transform.yVelocity = 0
                self.Transform.yPosition = item.yPosition - self.Collider.yLength
            if lis[2]:
                self.Transform.yVelocity = 0 
                self.Transform.yPosition = item.yPosition + item.Collider.yLength
            if lis[3]:
                self.Transform.xVelocity = 0
                self.Transform.xPosition = item.xPosition + self.Collider.xLength
            if lis[4]:
                self.Transform.xVelocity = 0
                self.Transform.xPosition = item.yPosition - item.Collider.yLength

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
    
    from main import Object, programPath, RenderQueue

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

    Camera = Object.get('Camera')
    Level = Object.get('Level')
    
    @classmethod
    def create(cls, name:str='New Renderer') -> Any:
        return name, cls, {
            'Transform': Component.new(
                Transform, 
                xPosition=0, yPosition=0
            )
        }
 
    def init(self, Transform:Transform,
        path: str|None = None, tier: int = 3, xOffset:float=0, yOffset:float=0, xLength:float=0, yLength:float=0, 
        color:tuple[int]=colors["gray"], surface:pyg.Surface|None = None,  alpha: int = 0, 
        surfaceRows:int = 1, surfaceColumns:int = 1, autoCulling:bool = True, **kwargs) -> None:
        if path == None:    
            self.path = "\\Assets\\Images\\MissingImage.png"
            self.surface = pyg.image.load(getcwd()+self.path)
        elif isinstance(path, str):
            self.surface = pyg.image.load(getcwd()+path)
        else:
            if surface == None:
                exit("No available path or surface"+ str(path))
            self.surface = surface

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

    def render(self, Screen: pyg.Surface, Camera, **kwargs):
        Screen.blit(
    source=self.surface, 
    dest=(int(self.Transform.xPosition) - int(self.xOffset) - Camera.xPosition,  # type: ignore
          int(self.Transform.yPosition) - int(self.yOffset) - Camera.yPosition) # type: ignore
          )


    def flip(self, flipVertically: bool = False, value: str | bool = "invert"):
        try:
            direction = 'flipHorizontal'
            if flipVertically == True:
                direction = 'flipVertical'
            if isinstance(value, str):
                value = 'invert'
            if value == 'invert':
                value = not self.flags[direction]
            self.flags[direction] = value
        
        except KeyError as ke:
            return ke
        
@newComponent
class ConfigData():
    """     Grabs data from a toml or other type config file. It checks for files located in the ConfigFiles directory,
so input dirFileName as the name with a backslash before it. If it is located in a folder, input the path from
    \\ConfigFiles to locate the file you wish to load. Also, omit the .toml from the file name.
    \nExample: 

    ConfigFile = Component.new(Component.get('ConfigData')(dirFileName = '\\settings'))
    
    dirFileName: str, the name of the config file you wish to pull from.
    fileType; str = "toml", the file extension of the file you wish to pull from,
    """
    from tomllib    import load
 
    def init(self, dirFileName: str = "settings", fileType: str = "toml", *args, **kwargs) -> None:
        try:
            if not list(dirFileName)[0] == "\\": dirFileName = "\\" + dirFileName
            self.fileName = dirFileName
            self.fileType = fileType
            if self.fileType == "toml":
                with open(getcwd()+"\\ConfigFiles" + self.fileName + '.toml', "rb" ) as f:
                    self.configFile = ConfigData.load(f) # type: ignore

        except FileNotFoundError as fnfe:
            print(f"{dirFileName}: Invalid Config File. Make sure that the file is located in '\\ConfigFiles' and is typed as the name without the file extension. \nExample: 'assetData.toml'")
            raise fnfe

        except:
            print("\n"*10, dirFileName, fileType, args, kwargs)
            raise

@newComponent
class Mouse():

    requiredDependencies={}
 
    def init(self) -> None:
        from main import Object, settings
        from Scripts import Camera
        self.Object, self._Settings, self.Camera = Object, settings, Camera
        self.placestage = 0
        self.select = 1
        self.tempx = 0
        self.tempy = 0 
        self.down = False
        self.pos = pyg.mouse.get_pos()
        self.pos = (self.pos[0], self.pos[1])
        self.posx = round((self.pos[0]), 0)
        self.posy = round((self.pos[1]), 0)
        self.list = pyg.mouse.get_pressed(num_buttons=5)

    def update(self):
        self.pos =  pyg.mouse.get_pos()
        cameraXOffset, cameraYOffset = self.Camera.get()
        self.pos = (self.pos[0] + cameraXOffset, self.pos[1] + cameraYOffset)
        self.posx = round((self.pos[0]/self._Settings['Screen']['grid']), 0)*self._Settings['Screen']['grid']
        self.posy = round((self.pos[1]/self._Settings['Screen']['grid']), 0)*self._Settings['Screen']['grid']
        self.list = pyg.mouse.get_pressed(num_buttons=5)
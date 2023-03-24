from sys import exit
if __name__ == "__main__":
    print(r"Cannot run components script as main :/")
    exit()
import pygame         as pyg
from Scripts.componentManager import ComponentTools as comTools
from Scripts.timer  import Timer
from Scripts.boards import Boards
from Scripts.inputMapper import Input
from os         import getcwd
from tomllib    import load       
from typing import Any
Main = __import__("__main__")

@comTools.newClass
class Transform():
    """Handles all positioning aspects of an object in world space
    Units are in pixels, 1 unit = 1 pixel
    X: - -> + = left -> right
    Y: - -> + = up   -> down
    Z: - -> + = back -> front
 
    Rotation: 0 - 360, clockwise
    """
    requiredDependencies={}
    @comTools.init
    def initialize__(self,
    xPosition:float=0, yPosition:float=0, zPosition:int=0, \
    xVelocity:float=0, yVelocity:float=0, rotation:float = 0, **kwargs) -> None:
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.zPosition = zPosition
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.rotation  = rotation
    
    def update__(self) -> None:
        self.xPosition += self.xVelocity
        self.yPosition += self.yVelocity

@comTools.newClass
class DependenciesTemplate():
    requiredDependencies={}
    @comTools.init
    def initialize__(self, dependencies, *args, **kwargs) -> None: 
        pass

@comTools.newClass
class PlatformSceneData():
    """ Is responsible for containing all of a room's data
    """
    requiredDependencies={}
    @comTools.init
    def initialize__(self, dependencies, name, plat: dict, length: int = 20000, height: int = 20000):
        self.name = name
        self.plat = plat
        self.length = length
        self.height = height

@comTools.newClass
class Collider():
    """Used to check as to whether the selected item is colliding with the object
    This will NOT handle collisions, incase it should be used as a collisionless trigger that has an
    activation area. If you want to add collisions, use this in tangent with RigidBody
    
    collideList = list[isColliding, colTop, colBottom, colLeft, colRight]"""

    requiredDependencies={
    "Transform": Transform 
    }

    @comTools.init
    def initialize__(self, dependencies:dict,
    xLength:int=50, yLength:int=50, **kwargs) -> None:
        self.Transform = dependencies["Transform"]
        self.xLength = xLength
        self.yLength = yLength
        self.Objects = Object.getAll()
        self.collideList: list[bool, bool, bool, bool, bool] = []

    def update__(self):
        for i in self.Objects:
            checkList = self.check(i)
            if checkList[0]:
                self.collideList.append((i, checkList))

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

@comTools.newClass
class RigidBody():
    """Used to handle collisions, gravity and other physical forces
    Use with a Collider to properly collide with other objects that have Colliders 
    
    mass = weight of object

    grounded = is touching ground and is unaffected by gravity until leaving ground again. 
    """
    requiredDependencies={
    "Transform": Transform, "Collider": Collider
    }

    @comTools.init
    def initialize__(self, dependencies: dict, mass:int=0, **kwargs) -> None:
        self.Transform = dependencies["Transform"]
        self.Collider = dependencies["Collider"]
        self.mass = mass
        self.grounded = True

    def update__(self) -> None:
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

@comTools.newClass
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

    colors = {
    "red":   (255, 0,   0  ),
    "green": (0,   255, 0  ),
    "blue":  (0,   0,   255),
    "gray":  (30,  30,  30 ),
    }

    @comTools.create
    def create__(self, name:str='New Renderer', 
        xPosition:float=0,
        yPosition:float=0,
        zPosition:int  =0,
        xVelocity:float=0,
        yVelocity:float=0,
        *args, **kwargs
        ) -> Any:

        transform = Transform(xPosition=xPosition, 
            yPosition=yPosition, zPosition=zPosition, 
            xVelocity=xVelocity, yVelocity=yVelocity)
        
        Renderer_ = Main.createComplexObject(
            name, class_=Renderer,
            Transform=transform,

            *args, **kwargs
            )

        return Renderer_

    @comTools.init
    def initialize__(self, dependencies: dict={},
        path: str = '', tier: int = 3, xOffset:float=0, yOffset:float=0, xLength:float=0, yLength:float=0, 
        color=colors["gray"], surface:pyg.Surface|None = None,  alpha: int = 0, 
        surfaceRows:int = 1, surfaceColumns:int = 1, autoCulling:bool = True, **kwargs) -> None:
            
        if path == '':    
            self.path = "\\Assets\\Images\\MissingImage.png"
            if Main.LogInConsole: print(f"{self.__repr__()}/Renderer: No path argument found! Add 'path=None' or 'path=<path name>' to the initializer")
        if surface == None:
            self.surface = pyg.image.load(Main.programPath+"\\Assets\\Images\\SkyBox.png")
        else:
            self.surface = surface

        self.area    = ()

        self.Transform = dependencies["Transform"]
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

    Camera = Object.get('Camera')
    Level = Object.get('Level')

    def update__(self):
        if self.autoCull: 
            if self.Transform.xPosition + xLength < 0 \
            or self.Transform.yPosition > 0:
                return

        Main.renderQueue[self] = (self, self.tier, self.Transform.zPosition)
    
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
        
@comTools.newClass
class ConfigData():
    """     Grabs data from a toml or other type config file. It checks for files located in the ConfigFiles directory,
so input dirFileName as the name with a backslash before it. If it is located in a folder, input the path from
    \\ConfigFiles to locate the file you wish to load. Also, omit the .toml from the file name.
    \nExample: 

    ConfigFile = Component.new(Component.get('ConfigData')(dirFileName = '\\settings'))
    
    dirFileName: str, the name of the config file you wish to pull from.
    fileType; str = "toml", the file extension of the file you wish to pull from,
    """
    requiredDependencies={}
    @comTools.init
    def initialize__(self, dependencies, dirFileName: str = "", fileType: str = "toml", *args, **kwargs) -> None:
        try:
            if not list(dirFileName)[0] == "\\": dirFileName = "\\" + dirFileName
            self.fileName = dirFileName
            self.fileType = fileType
            if self.fileType == "toml":
                with open(getcwd()+"\\ConfigFiles" + self.fileName + '.toml', "rb" ) as f:
                    self.configFile = load(f)

        except FileNotFoundError as fnfe:
            print(f"{dirFileName}: Invalid Config File. Make sure that the file is located in '\\ConfigFiles' and is typed as the name without the file extension. \nExample: 'assetData.toml'")
            raise fnfe

        except:
            print("\n"*10, dependencies, dirFileName, fileType, args, kwargs)
            raise

@comTools.newClass
class Mouse():
    requiredDependencies={}
    @comTools.init
    def initialize__(self, dependencies) -> None:
        print("A?")
        print("Objects", Main.Objects)
        self.Camera = Main.Objects['Camera']
        print("B!")
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
        print("Done")

    def update__(self):
        self.pos =  pyg.mouse.get_pos()
        self.pos = (self.pos[0] + self.Camera.xpos, self.pos[1] + self.Camera.ypos)
        self.posx = round((self.pos[0]/Main.Settings.grid), 0)*Main.Settings.grid
        self.posy = round((self.pos[1]/Main.Settings.grid), 0)*Main.Settings.grid
        self.list = pyg.mouse.get_pressed(num_buttons=5)
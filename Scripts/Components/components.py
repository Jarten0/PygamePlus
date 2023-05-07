"""Contains a group of basic components for fundamental level design. Includes essential components like Transform and ConfigData, among a few other useful ones."""

from sys import exit

if __name__ == "__main__": print(r"Cannot run components script as main :/"); exit()
import pygame         as pyg #type: ignore
from Scripts.componentManager import newComponent, newPrefab
from Scripts import Board

from os         import getcwd
from typing import Any
from main import gameObject, Component

@newPrefab
class BasicObject:
    def init(self, *args, **kwargs):
        pass

@newPrefab
class Scene:
    def init(self, *args, **kwargs):
        self.SceneTags:dict[str, dict[str, object]] = {}
        self.delta = 0
        self.settings = ConfigData.load(getcwd()+"\\ConfigFiles\\debugSettings.toml")

@newPrefab
class Tag:
    def init(self, name, *args, **kwargs):
        self.NAME = name
        

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
        "xPos":0.0, 
        "yPos":0.0, 
        "zPosition":0,
        "xVel":0.0, 
        "yVel":0.0, 
        "rotation": 0.0
    }
    optionalArguments = {
        "xPos", 
        "yPos", 
        "zPosition",
        "xVel", 
        "yVel", 
        "rotation"
    }
    
    class Vector:
        def __init__(self, x, y) -> None:
            self.x = x
            self.y = y

        def __add__(self, other):
            if isinstance(other, type(self)):
                return Vector(self.x + other.x, self.y + other.y) #type: ignore 
            elif isinstance(other, float):
                return Vector(self.x + other, self.y + other) #type: ignore 
            raise TypeError(f"Unsupported operation between 'Vector' and '{type(other)}'")
    
        def __iadd__(self, other):
            if isinstance(other, type(self)):
                self.x += other.x 
                self.y += other.y 
            elif isinstance(other, float):
                self.x += other 
                self.y += other 
            raise TypeError(f"Unsupported operation between 'Vector' and '{type(other)}'")

        def __mul__(self, other):
            if isinstance(other, type(self)):
                return Vector(self.x * other.x, self.y * other.y) #type: ignore 
            elif isinstance(other, float):
                return Vector(self.x * other, self.y * other) #type: ignore 
            raise TypeError(f"Unsupported operation between 'Vector' and '{type(other)}'")

        def __imul__(self, other):
            if isinstance(other, type(self)):
                self.x *= other.x 
                self.y *= other.y 
            elif isinstance(other, float):
                self.x *= other 
                self.y *= other 
            raise TypeError(f"Unsupported operation between 'Vector' and '{type(other)}'")
                    

    def init(self,
            xPos:float=0, yPos:float=0, zPosition:int=0, 
            xVel:float=0, yVel:float=0, rotation:float = 0, 
            *args, **kwargs) -> None:
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPosition
        self.xVel = xVel
        self.yVel = yVel
        self.Rotation = rotation
    
    def update(self) -> None:
        self.xPos += self.xVel
        self.yPos += self.yVel

    def set(self, vector:Vector):
        self.xPos = vector.x
        self.yPos = vector.y

@newComponent
class DependenciesTemplate():
    requiredDependencies={} 
    def init(self, *args, **kwargs) -> None: pass

@newComponent
class ConfigData():
    """     Grabs data from a toml or other type config file. It checks for files located in the ConfigFiles directory,
so input dirFileName as the name with a backslash before it. If it is located in a folder, input the path from
    \\ConfigFiles to locate the file you wish to load. Also, omit the .toml from the file name.
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

@newPrefab
class MousePrefab:
    def init(self):
        self.newComponent(Mouse)

@newComponent
class Mouse():
    requiredDependencies={}
    def init(self) -> None:
        from Scripts import Camera
        self.Camera = Camera
        self.placestage = 0
        self.select = 1
        self.tempx = 0
        self.tempy = 0 
        self.down = False
        self.pos = pyg.mouse.get_pos()
        self.pos = (self.pos[0], self.pos[1])
        self.xPos = round((self.pos[0]), 0)
        self.yPos = round((self.pos[1]), 0)
        self.list = pyg.mouse.get_pressed(num_buttons=5)

    def update(self):
        self.pos =  pyg.mouse.get_pos()
        cameraXOffset, cameraYOffset = self.Camera.getObject()
        self.pos = (self.pos[0] + cameraXOffset, self.pos[1] + cameraYOffset)
        self.xPos = round((self.pos[0]/self._Settings['Screen']['grid']), 0)*self._Settings['Screen']['grid']
        self.yPos = round((self.pos[1]/self._Settings['Screen']['grid']), 0)*self._Settings['Screen']['grid']
        self.list = pyg.mouse.get_pressed(num_buttons = 5)
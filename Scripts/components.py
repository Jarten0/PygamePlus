# self. = kwargs[""]
from Scripts.timer import Timer
import Scripts.boards as Boards

#Handles all positioning aspects of an object in world space
class Transform():
    def __init__(self, **kwargs) -> None:
        self.xPosition = kwargs["xPosition"]
        self.yPosition = kwargs["yPosition"]
        self.zPosition = kwargs["zPosition"]
        self.xVelocity = kwargs["xVelocity"]
        self.yVelocity = kwargs["yVelocity"]
        self.zVelocity = kwargs["zVelocity"]


#Used to check as to whether the selected item is colliding with the object
#This will NOT handle collisions, incase it should be used as a collisionless trigger that has an
#activation area. If you want to add collisions, use this in tangent with RigidBody
class Collider():

    componentDependencies = {
        "Transform": None,
    }

    def __init__(self, dependencies = componentDependencies, **kwargs) -> None:
        
        for i in dependencies.keys(): 
            if dependencies[i] == None:
                print(f"Missing {dependencies[i]} in {self.__str__}!")
        
        self.Transform = dependencies["Transform"]


        self.xLength = kwargs["xLength"]
        self.yLength = kwargs["yLength"]

    def check(self, item) -> list[bool]:
        lis = [False, False, False, False, False]
        if item.Transform.yPosition + item.yLength >= self.Transform.yPosition and item.Transform.yPosition <= self.Transform.yPosition + self.yLength and item.Transform.xPosition + item.xLength >= self.Transform.xPosition and item.Transform.xPosition <= self.Transform.xPosition + self.xLength:
            return lis
        lis[0] = True
        if item.Transform.yPosition + item.yLength   < self.Transform.yPosition + 10 and item.Transform.xPosition + item.xLength     > self.Transform.xPosition and item.Transform.xPosition < self.Transform.xPosition + self.xLength:
            lis[1] = True
        if item.Transform.xPosition + item.xLength   < self.Transform.xPosition + 20 and item.Transform.yPosition + item.yLength - 5 > self.Transform.yPosition and item.Transform.yPosition < self.Transform.yPosition + self.yLength:
            lis[2] = True
        if item.Transform.yPosition > self.Transform.yPosition + self.yLength - 10   and item.Transform.xPosition + item.xLength     > self.Transform.xPosition and item.Transform.xPosition < self.Transform.xPosition + self.xLength:
            lis[3] = True
        if item.Transform.xPosition > self.Transform.xPosition + self.xLength - 20   and item.Transform.yPosition + item.yLength - 5 > self.Transform.yPosition and item.Transform.yPosition < self.Transform.yPosition + self.yLength:
            lis[4] = True         
        
        return lis


#Used to handle collisions and other physical forces
#Use with a Collider to properly collide with other objects that have Colliders 
class RigidBody():
    dependancies = {
        "Transform",
        "Collider",
    }
    def __init__(self, **kwargs) -> None:
        self.mass = kwargs["mass"]
        

#Renders an object either via image or rectangle
class Renderer():

    dependencies = {
        "Transform",
    }

    colors = {
    "red":   (255, 0,   0  ),
    "green": (0,   255, 0  ),
    "blue":  (0,   0,   255),
    "gray":  (30,  30,  30 ),
    }

    def __init__(self, **kwargs) -> None:
        try:
            self.path = kwargs["path"]    
        except KeyError as ke:
            raise Exception(f"{self.__repr__()}/Renderer: No path argument found! Add 'path=None' or 'path=<path name>' to the initializer")

        try:
            self.xOffset = kwargs["xOffset"]
            self.yOffset = kwargs["yOffset"]
            self.xLength = kwargs["xLength"]
            self.yLength = kwargs["yLength"]
        except KeyError as ke:
            print(f"Warning: {self.__repr__()}/Renderer: Invalid arguments, some are missing.")

    def renderUpdate(self, transform):
        if self.path == None:
            return {
            "xPosition": transform.xVelocity,
            "yPosition": transform.yVelocity,
            "path": None,
            "xLength": self.xLength,
            "yLength": self.yLength,
            "xSpeed": transform.xVelocity,
            "ySpeed": transform.yVelocity,    
            }
        return {
            "xPosition": transform.xVelocity,
            "yPosition": transform.yVelocity,
            "path": self.path,
            "xSpeed": transform.xVelocity,
            "ySpeed": transform.yVelocity,
        }

class Controller():
    def __init__(self) -> None:
        pass




class ConfigData():
    def __init__(self, filename) -> None:
        from os import getcwd
        from tomllib import load
        
        with open(getcwd()+r"\ConfigFiles" + fr"\{filename}" + r'.toml', "rb" ) as f:
            self.configFile = load(f)
            






class CharacterManager():
    componentDependencies = {
        "Transform": None,
        "Renderer": None,
        "ConfigData": None,
    }

    def __init__(self, dependencies = componentDependencies, **kwargs) -> None:
        
        for i in dependencies.keys(): 
            if dependencies[i] == None:
                print(f"Missing {dependencies[i]} in {self}!")
        
        self.Transform = dependencies["Transform"]
        self.Renderer = dependencies["Renderer"]
        self.configData = dependencies["ConfigData"]
        
        
        configFile = self.configData.configFile
        self.allowControl = True
        self.gr = False
        self.st = False
        self.wj = False
        self.w = None
        self.dead = False
        self.speed = configFile['run']['runSpeed']
        self.acc = configFile['run']['runAcceleration']
        self.decel = configFile['run']['runDeceleration']
        self.dyndecel = 1
        self.jumppower = configFile['jump']['jumpPower']
        self.gravity = configFile['jump']['gravityStrength']
        self.dashes = configFile['dash']['dashCount']
        self.dashstate = False
        self.dashleave = True
        self.dashlength = configFile['dash']['dashLength']
        self.dashcooldown = configFile['dash']['dashCooldownLength']
        self.dashspeed = configFile['dash']['dashSpeed']
        self.dashlist = [False, False, False, False]
        self.dashslow = configFile['dash']['dashDeceleration']
        self.color = self.Renderer.colors["red"]
        self.DCsuper = 0
        self.DChyper = 0

    def die(self):
        self.Transform.xPosition = 500        
        self.Transform.yPosition = 0
        self.Transform.xVelocity = 0
        self.Transform.yVelocity = 1
        self.dead = True

    def jump(self, transform):
        self.Transform.yVelocity = self.jumppower
        self.gr = False
        self.dashslow = 1
        self.Transform.xVelocity *= 2
        self.dashslow = 1
        if self.dashleave or self.dashstate:
            print("Dash Cancel")
            if not self.xv == 0:
                self.xv = abs(self.Transform.xVelocity)/ self.xv * 24
                if self.dashlist[3] == True:
                    print("Hyper")
                    self.yv = -13
                    self.xv *= 3

    def walljump(self, wallcheck):
        if wallcheck[0] and wallcheck[1]:
            self.yv = self.jumppower
        elif wallcheck[0]:
            self.xv = -7
            self.yv = self.jumppower
        elif wallcheck[1]:
            self.xv = 7
            self.yv = self.jumppower

        if self.dashleave or self.dashstate:
            if self.dashlist[0]:
                print("Dash Cancel")
                self.yv *= 1.2
                self.xv *= 1.5
                
#Run on the first frame of a check
    def dash(self):
        input = ["up", "left", "right", "down", "jump", "dash"]
        self.dashes -= 1
        self.dashslow = 2
        for i in range(4):
            if Boards.getP(input[i]):
                self.dashlist[i] = True
        if self.dashlist == [False, False, False, False]:
            self.dashlist[2] = True

#Run every frame, to run checks and blocks of code for all dash related stuff
    def dashManager(self):
        if not Timer.get("dash") and self.dashstate:
            self.color = self.Renderer.colors["green"]
            if self.dashlist[0]:
                if self.yv > -self.dashspeed:
                    self.yv = -self.dashspeed
            if self.dashlist[1]:
                if self.xv > -self.dashspeed:
                    self.xv = -self.dashspeed
            if self.dashlist[2]:
                if self.xv < self.dashspeed:
                    self.xv = self.dashspeed
            if self.dashlist[3]:
                if self.yv < self.dashspeed:
                    self.yv = self.dashspeed
            if self.dashlist[3]:
                if self.dashlist[0]:
                    self.yv = 0
#                    self.xv *= 1.2
        elif self.dashstate:
            self.dashstate = False
            self.dashleave = True
            self.color = (200, 200, 200)
            Timer.set("dashleave", self.dashcooldown)
        if Timer.get("dashleave") == False:
            if self.gr:
                self.dashes = 1   

        if Timer.get("dashleave") == True:
            self.dashlist = [False, False, False, False]
            self.dashleave = False
            self.color = self.Renderer.colors["blue"]

        if self.dashes > 0:
            self.color = self.Renderer.colors["red"]
        
        if self.dashslow > 1:
            self.dashslow /= 1.066
        if self.dashslow < 1:
            self.dashslow = 1
        #print(self.dashlist, Timer.get("dash"))

    def resetDash(self):
        self.dashes = 1
        self.dashstate = False
        self.dashleave = False
        Timer.set("dashleave", True)
        Timer.set("dash", True)
        Timer.set("dashcool", True)

# self. = kwargs[""]

#Handles all positioning aspects of an object in world space
class Transform():
    def __init__(self, **kwargs) -> None:
        self.xPosition = kwargs["x"]
        self.yPosition    = kwargs["y"]
        self.z = kwargs["z"]
        self.xVelocity = kwargs["xVelocity"]
        self.yVelocity = kwargs["yVelocity"]
        self.zVelocity = kwargs["zVelocity"]


#Used to check as to whether the selected item is colliding with the object
#This will NOT handle collisions, incase it should be used as a collisionless trigger that has an
#activation area. If you want to add collisions, use this in tangent with RigidBody
class Collider():
    def __init__(self, **kwargs) -> None:
        self.xLength = kwargs["xLength"]
        self.yLength = kwargs["yLength"]

    def check(self, item) -> list[bool, bool, bool, bool, bool]:
        lis = [False, False, False, False, False]
        if not item.yPosition    + item.yLength >= self.yPosition and item.yPosition <= self.yPosition + self.yLength and item.xPosition + item.xLength >= self.xPosition and item.xPosition <= self.xPosition + self.xl:
            return lis
        
        lis[0] = True
        #
        if item.yPosition + item.yLength   < self.yPosition + 10 and item.xPosition + item.xLength     > self.xPosition and item.xPosition < self.xPosition + self.xl:
            lis[1] = True
        #
        if item.xPosition + item.xLength   < self.xPosition + 20 and item.yPosition + item.yLength - 5 > self.yPosition and item.yPosition < self.yPosition + self.yl:
            lis[2] = True
        #
        if item.yPosition > self.yPosition + self.yLength - 10   and item.xPosition + item.xLength     > self.xPosition and item.xPosition < self.xPosition + self.xl:
            lis[3] = True
        #
        if item.xPosition > self.xPosition + self.xLength - 20   and item.yPosition + item.yLength - 5 > self.yPosition and item.yPosition < self.yPosition + self.yl:
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
        
    
    def check(self, item) -> list[bool, bool, bool, bool, bool]:
        lis = [False, False, False, False, False]
        if not item.yPosition    + item.yLength >= self.yPosition and item.yPosition <= self.yPosition + self.yLength and item.xPosition + item.xLength >= self.xPosition and item.xPosition <= self.xPosition + self.xl:
            return lis
        
        lis[0] = True
        #
        if item.yPosition + item.yLength   < self.yPosition + 10 and item.xPosition + item.xLength     > self.xPosition and item.xPosition < self.xPosition + self.xl:
            lis[1] = True
        #
        if item.xPosition + item.xLength   < self.xPosition + 20 and item.yPosition + item.yLength - 5 > self.yPosition and item.yPosition < self.yPosition + self.yl:
            lis[2] = True
        #
        if item.yPosition > self.yPosition + self.yLength - 10   and item.xPosition + item.xLength     > self.xPosition and item.xPosition < self.xPosition + self.xl:
            lis[3] = True
        #
        if item.xPosition > self.xPosition + self.xLength - 20   and item.yPosition + item.yLength - 5 > self.yPosition and item.yPosition < self.yPosition + self.yl:
            lis[4] = True         
        
        return lis
        

#Renders an object either via image or rectangle
class Renderer():
    dependencies = {
        "Transform",
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








def initDependencyWrapper(componentFunction):
    def wrapper():
        for i in [Transform, Renderer]: 
            if i == None:
                print(f"Missing {i} in {self.__str__}!")
        componentFunction()
    return wrapper


class CharacterActions():
    componentDependencies = {
        "Transform": None,
        "Renderer": None,
    }

    def __init__(self, dependencies = componentDependencies, **kwargs) -> None:
        for i in [Transform, Renderer]: 
            if i == None:
                print(f"Missing {i} in {self.__str__}!")

        
        self.Transform = Transform
        self.Renderer = Renderer

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
        self.color = colors["red"]
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
        self.Transform.xVelocity * 2
        self.dashslow = 1
        if self.dashleave or self.dashstate:
            print("Dash Cancel")
            if not self.xv == 0:
                self.xv = abs(self.xv)/ self.xv * 24
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
    def dashManager(char):
        if not Timer.get("dash") and char.dashstate:
            char.color = colors["green"]
            if char.dashlist[0]:
                if char.yv > -char.dashspeed:
                    char.yv = -char.dashspeed
            if char.dashlist[1]:
                if char.xv > -char.dashspeed:
                    char.xv = -char.dashspeed
            if char.dashlist[2]:
                if char.xv < char.dashspeed:
                    char.xv = char.dashspeed
            if char.dashlist[3]:
                if char.yv < char.dashspeed:
                    char.yv = char.dashspeed
            if char.dashlist[3]:
                if char.dashlist[0]:
                    char.yv = 0
#                    char.xv *= 1.2
        elif char.dashstate:
            char.dashstate = False
            char.dashleave = True
            char.color = (200, 200, 200)
            Timer.set("dashleave", char.dashcooldown)
        if Timer.get("dashleave") == False:
            if char.gr:
                char.dashes = 1   

        if Timer.get("dashleave") == True:
            char.dashlist = [False, False, False, False]
            char.dashleave = False
            char.color = colors["blue"]

        if char.dashes > 0:
            char.color = colors["red"]
        
        if char.dashslow > 1:
            char.dashslow / 1.066
        if char.dashslow < 1:
            char.dashslow = 1
        #print(char.dashlist, Timer.get("dash"))

    def resetDash(self):
        self.dashes = 1
        self.dashstate = False
        self.dashleave = False
        Timer.set("dashleave", True)
        Timer.set("dash", True)
        Timer.set("dashcool", True)

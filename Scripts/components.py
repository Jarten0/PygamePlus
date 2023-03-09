# self. = kwargs[""]
if not __name__ == "__main__":
    import Scripts.timer as Timer
    import Scripts.boards as Boards
from componentDependencyDecorators import *






#Handles all positioning aspects of an object in world space
@dependencyWrapper(requiredDependencies={}) # type: ignore
class Transform():
    @initializationWrapper
    def initalize(self, **kwargs) -> None:
        self.xPosition = kwargs["xPosition"]
        self.yPosition = kwargs["yPosition"]
        self.zPosition = kwargs["zPosition"]
        self.xVelocity = kwargs["xVelocity"]
        self.yVelocity = kwargs["yVelocity"]
        self.zVelocity = kwargs["zVelocity"]

@dependencyWrapper(requiredDependencies={}) # type: ignore
class Camera():
    @initializationWrapper
    def initalize(self, dependencies) -> None:
        self.xPosition = 0
        self.yPosition = 0
#Used to check as to whether the selected item is colliding with the object
#This will NOT handle collisions, incase it should be used as a collisionless trigger that has an
#activation area. If you want to add collisions, use this in tangent with RigidBody
@dependencyWrapper(requiredDependencies=
{ "Transform": Transform }
)# type: ignore
class Collider():
    @initializationWrapper
    def initilization(self, dependencies, **kwargs):
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
@dependencyWrapper(requiredDependencies={
    "Transform": Transform, "Collider": False
    })# type: ignore
class RigidBody():
    @initializationWrapper
    def initialization(self, dependencies, **kwargs) -> None:

                
        self.Transform = dependencies["Transform"]
        self.Collider = dependencies["Collider"]

        self.mass = kwargs["mass"]
        

#Renders an object either via image or rectangle
@dependencyWrapper(requiredDependencies={
    "Transform": Transform
    })# type: ignore
class Renderer():
    colors = {
    "red":   (255, 0,   0  ),
    "green": (0,   255, 0  ),
    "blue":  (0,   0,   255),
    "gray":  (30,  30,  30 ),
    }
    def initalize(self, dependencies, **kwargs) -> None:
        try:
            self.path = kwargs["path"]    
        except KeyError as ke:
            self.path = r'\Assets\Images\MissingImage.png'
            print(f"{self.__repr__()}/Renderer: No path argument found! Add 'path=None' or 'path=<path name>' to the initializer")

        try:
            self.xOffset = kwargs["xOffset"]
            self.yOffset = kwargs["yOffset"]
            self.xLength = kwargs["xLength"]
            self.yLength = kwargs["yLength"]
        except KeyError as ke:
            print(f"Warning: {self.__repr__()}/Renderer: Invalid arguments, some are missing.")
        


#Allows one to get inputs to be used by a scripting component
@dependencyWrapper(requiredDependencies={
    "Transform": Transform
    })# type: ignore
class Controller():
    @initializationWrapper
    def initalize(self) -> None:
        pass

    



#Grabs data from a config file for use
@dependencyWrapper(requiredDependencies={})# type: ignore
class ConfigData():
    @initializationWrapper
    def initalize(self, filename, fileType="toml") -> None:
        from os import getcwd
        from tomllib import load
        if fileType == "toml":
            with open(getcwd()+r"\ConfigFiles" + fr"\{filename}" + r'.toml', "rb" ) as f:
                self.configFile = load(f)
            








#This is responsible for all of the actions a Character can do
#Mostly used for the player character
@dependencyWrapper(requiredDependencies={
    "Transform" : Transform,
    "Renderer"  : Renderer,
    "Controller": Controller,
    "ConfigData": ConfigData,
}) # type: ignore
class CharacterManager():
    @initializationWrapper
    def initalize(self, dependencies, **kwargs) -> None:
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


#Movement/Collisions =========================================================================================================
#Ideally the best course of action is to have all of the movements before
# the collisions so that the player's momentum doesn't push the character
# into the ground after the collision checks have already taken place
# leaving the character in the ground as the frame ends 

#Movement
    def update(self):
        if Timer.get('dashcool') == True and self.gr and self.dashstate == False and self.dashleave == False:
            self.dashes = 1            
            self.color = self.Renderer.colors["red"]

        if Boards.getP('left') and not Boards.getP('right'):
            if self.Transform.xv > -self.speed:
                self.Transform.xv -= self.acc
            else:
                self.Transform.xv += self.decel
        elif Boards.getP('right') and not Boards.getP('left'):
            if self.xv < self.speed:
                self.xv += self.acc
            else:
                self.xv -= self.decel
        else:
            if   self.xv <=-self.decel:
                 self.xv += self.decel * self.dashslow
            elif self.xv >= self.decel:
                 self.xv -= self.decel * self.dashslow
            else:
                self.xv = 0

        

#Gravity
        if Boards.getP("down"):
            self.gravity = 14
        else:
            self.gravity = 7

        if self.yv < self.gravity and self.gr == False:
            self.yv += 1 /(p.fps * delta)
        elif self.gr == False and self.yv > self.gravity + 1:
            self.yv -= 1

#Actions
        if Boards.getP("jump") and self.gr or Boards.getP("jump") and Timer.get("CoyoteTime", True) < p.coyoteTime:
            print("Jump!")
            Timer.set("CoyoteTime", p.coyoteTime, True)
            self.jump()

        elif Boards.getP("jump") and self.wj:
            print("Walljump!")
            self.walljump(self.w)

        if Boards.getP("dash") and self.dashes > 0 and Timer.get("dashcool"):
            Timer.set("dashcool", self.dashcooldown * renderframeavg)
            Timer.set("dash", self.dashlength * renderframeavg)
            self.dashstate = True
            fREEZEFRAMES += 2
            self.dash()            
        self.dashManager()

#Momentum to actual movement
        self.x += self.xv /( p.fps * delta)
        self.y += self.yv /( p.fps * delta)
        self.gr = False
        self.wj = False
        
#Death from void        
        if self.y > level.height:
            self.die()

        if self.x < 0:
            self.x = 0
        elif self.x > p.screen_width + level.length:
            self.x = 0


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
    
def mainfunc():
    character = Renderer()

if __name__ == "main":
    mainfunc()
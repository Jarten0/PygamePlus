from sys import exit
if __name__ == "__main__":
    print(r"Cannot run components script as main :/")
    exit()
import pygame as pyg
import Scripts.timer  as Timer
import Scripts.boards as Boards
import Scripts.input  as Input
from Scripts.componentDependencyDecorators import *
Main = __import__("__main__")



#Standard naming conventions: camelCaseForRegularVariables, AlwaysUppercaseForComponents
#To create a component, copy and study the template below. You can also study any of the built in components aswell
#To create a component that uses dependencies, check out the template below the Transform component
# (DependenciesTemplate) to see how it's done
class Template(): 
#The decoraters used in DependenciesTemplate are not required at all if you do not wish to import
#any dependencies from any other objects. The component itself can still be used for dependencies
#with or without the decorater. ! Note the difference in function names, however ! 'def __init__(self)' is fine
#to use if you are not using the decoraters, though if you are it must be replaced with 'def initialize(self, dependencies)'
#else the decoraters will fail to function. Keep that in mind as you add new components.
    def __init__(self, *whateverArgumetsYouWant, **kwargs): #**kwargs to catch any loose keyword arguments if you wish

#Once you have defined an initialize function, __init__ or initialize, now you can add whatever scripting
#components and methods you wish to be used by other components.
        #self.variable = "whatever"
    #def method(self):
        #print(self.variable) 
        pass

#Handles all positioning aspects of an object in world space
@dependencyWrapper(requiredDependencies={}) # type: ignore
class Transform():
    @initializationWrapper
    def initialize(self,
    xPosition:int=0, yPosition:int=0, zPosition:int=0, xVelocity:int=0, yVelocity:int=0, **kwargs) -> None:
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.zPosition = zPosition #Z position is used for rendering order purposes, the lower the higher priority
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
    
    def update(self):
        self.xPosition += self.xVelocity
        self.yPosition += self.yVelocity

#How these dependency wrappers work (the @ function) is where it takes in a set amount of dependencies, 
# and will add in missing depenndences if a required one is missing, at set default values. 
@dependencyWrapper(requiredDependencies={
    "Transform": Transform
})     # type: ignore  (The use of this is to ignore vscode warnings, there is an error when inputting dependencies into decoraters.)
    #"Transform": Transform,  #To input a required dependency, input the name of the class as a string in the key.
# Then add the class name into the value DO NOT USE PARENTHESIS. It will call a default init function and somewhat break the system.
    #"Transform2": False,     #To input an optional dependency, input the name into the key and False into the value.
    #"Transform3": Transform })    #You can have multiple clones of components, just make sure they have different keys. 
class DependenciesTemplate():   #Best practices are to not use inheritance. Keep it procedural here.
    #You can also throw any general class variables here incase you so wish
    #accessibleValue = 5

    @initializationWrapper      #This should be right under an 'initialize' function.
    def initialize(self, dependencies, keywordArgument, *args, **kwargs): #IT IS REQUIRED to have this named 'initialize' 
    #if you use the @dependencyWrapper, else it will pull up an error

        #You can now initialize whatevver variables you wish
        #DependenciesTemplate.accessibleValue += 3
        #self.valueFromKeyword = keywordArgument
        #self.Transform = dependencies["Transform"]
        #self.OtherTransform = dependencies["Transform3"]

        pass #Feel free to study the other components given

@dependencyWrapper(requiredDependencies={
}) # type: ignore
class Camera():
    @initializationWrapper
    def initialize(self, dependencies:dict, *args) -> None:
        self.xPosition = 0
        self.yPosition = 0

#Used to check as to whether the selected item is colliding with the object
#This will NOT handle collisions, incase it should be used as a collisionless trigger that has an
#activation area. If you want to add collisions, use this in tangent with RigidBody
@dependencyWrapper(requiredDependencies={
    "Transform": Transform 
    }
)# type: ignore
class Collider():
    @initializationWrapper
    def initialize(self, dependencies:dict, Objects:dict={}, xLength:int=50, yLength:int=50, **kwargs):
        self.Transform = dependencies["Transform"]
        self.xLength = xLength
        self.yLength = yLength
        self.Objects = Objects #Used as a pointer
        self.collideList = []

    def update(self):
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

#Used to handle collisions and other physical forces
#Use with a Collider to properly collide with other objects that have Colliders 
@dependencyWrapper(requiredDependencies={
    "Transform": Transform, "Collider": Collider
    })# type: ignore
class RigidBody():

    @initializationWrapper
    def initialize(self, dependencies: dict, mass:int=0, **kwargs) -> None:
        self.Transform = dependencies["Transform"]
        self.Collider = dependencies["Collider"]
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

#Renders an object either via image or rectangle
@dependencyWrapper(requiredDependencies={
    "Transform": Transform
    }) # type: ignore
class Renderer():
    
    colors = {
    "red":   (255, 0,   0  ),
    "green": (0,   255, 0  ),
    "blue":  (0,   0,   255),
    "gray":  (30,  30,  30 ),
    }

    @initializationWrapper
    def initialize(self, dependencies: dict,
        path: str = "", tier: int = 3, xOffset:int=0, yOffset:int=0, xLength:int=0, yLength:int=0, color=colors["gray"], **kwargs) -> None:
        
        self.path = path    
        if path == "":    
            self.path = r'\Assets\Images\MissingImage.png'
            print(f"{self.__repr__()}/Renderer: No path argument found! Add 'path=None' or 'path=<path name>' to the initializer")

        self.Transform = dependencies["Transform"]
        self.tier    = tier
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.xLength = xLength
        self.yLength = yLength
        self.color   = color

    def update(self):
        Main.renderQueue[self] = (self, self.tier, self.Transform.zPosition)
        
#Allows one to get inputs to be used by a scripting component
@dependencyWrapper(requiredDependencies={})# type: ignore
class Controller():
    defaultInputs = {
        "up":    False, 
        "left":  False, 
        "down":  False,
        "right": False,
        "jump":  False,
        "dash":  False, 
        "UP":    False, 
        "LEFT":  False,
        "DOWN":  False,
        "RIGHT": False,
        }
    currentInputs = defaultInputs
   
    @initializationWrapper
    def initialize(self, dependencies: dict, **kwargs) -> None:
        pass


    def update(self):
        pass

    def classUpdate(self):
        eventsGet = pyg.event.get()
        eventsGetHeld = pyg.key.get_pressed()
        for actionToCheck in Input.defaultInputKeys:
            for keyToCheck in range(len(Main.input[actionToCheck])):
                if self.getKeyHeld(Main.input[actionToCheck][keyToCheck], eventsGetHeld):
                    Boards.appendToPerm(True, actionToCheck)
                    self.currentInputs[actionToCheck] = True
                    break
                else:
                    Boards.appendToPerm(False, actionToCheck)

    def getKeyDown(self, input, events) -> bool:
        for event in events:
            if not event.type == pyg.KEYDOWN:
                return False
            if not event.key == Input.keyBindList[input]:
                return False
            return True
        return False

    def getKeyHeld(self, input, events) -> bool:
        if not events[Input.keyBindList[input]]:
            return False
        return True

#Grabs data from a config file for use
@dependencyWrapper(requiredDependencies={})# type: ignore
class ConfigData():
    @initializationWrapper
    def initialize(self, dirFileName: str = "", fileType: str = "toml", *args, **kwargs) -> None:
        self.fileName = dirFileName
        self.fileType = fileType
        if self.fileType == "toml":
            from os import getcwd
            from tomllib import load       
            with open(getcwd()+'\ConfigFiles\\' + f'{self.fileName}' + '.toml', "rb" ) as f:
                self.configFile = load(f)
        
#This is responsible for all of the actions a Character can do
#Mostly used for the player character
@dependencyWrapper(requiredDependencies={
    "Transform" : Transform ,
    "Renderer"  : Renderer  ,
    "Controller": Controller,
    "ConfigData": ConfigData,
    "Collider"  : Collider  ,
    "RigidBody" : RigidBody ,
}) # type: ignore
class Character():
    @initializationWrapper
    def initialize(self, dependencies, **kwargs) -> None:
        self.Transform = dependencies["Transform"]
        self.Renderer = dependencies["Renderer"]
        self.ConfigData = dependencies["ConfigData"]
        self.Controller = dependencies["Controller"]
        self.Collider = dependencies["Collider"]
        self.RigidBody = dependencies["RigidBody"]
        
        print(self.ConfigData)
        configFile = self.ConfigData.configFile
        
        self.allowControl = True
        self.st = False
        self.canWalljump = False
        self.w = None
        self.dead = False
        self.speed = configFile['run']['runSpeed']
        self.acc = configFile['run']['runAcceleration']
        self.decel = configFile['run']['runDeceleration']
        self.dyndecel = 1
        self.jumppower = configFile['jump']['jumpPower']
        self.gravity = configFile['jump']['gravityStrength']
        self.dashes = configFile['dash']['dashCount']
        self.dashState = False
        self.dashLeave = True
        self.dashLength = configFile['dash']['dashLength']
        self.dashCooldown = configFile['dash']['dashCooldownLength']
        self.dashSpeed = configFile['dash']['dashSpeed']
        self.dashList = [False, False, False, False]
        self.dashSlow = configFile['dash']['dashDeceleration']
        self.color = self.Renderer.colors["red"]
        self.DCsuper = 0
        self.DChyper = 0

    def update(self):
        if Timer.get('dashcool') == True and self.RigidBody.grounded and self.dashState == False and self.dashLeave == False:
            self.dashes = 1            
            self.color = self.Renderer.colors["red"]

        if self.Controller.getKeyHeld('left') and not self.Controller.getKeyHeld('right'):
            if self.Transform.xVelocity > -self.speed:
                self.Transform.xVelocity -= self.acc
            else:
                self.Transform.xVelocity += self.decel
        elif self.Controller.getKeyHeld('right') and not self.Controller.getKeyHeld('left'):
            if self.Transform.xVelocity < self.speed:
                self.Transform.xVelocity += self.acc
            else:
                self.Transform.xVelocity -= self.decel
        else:
            if   self.Transform.xVelocity <=-self.decel:
                 self.Transform.xVelocity += self.decel * self.dashSlow
            elif self.Transform.xVelocity >= self.decel:
                 self.Transform.xVelocity -= self.decel * self.dashSlow
            else:
                self.Transform.xVelocity = 0

        

#Gravity
        if self.Controller.getKeyHeld("down"):
            self.RigidBody.mass = 14
        else:
            self.RigidBody.mass = 7
#Actions
        if self.Controller.getKeyHeld("jump") and self.RigidBody.grounded or self.Controller.getKeyHeld("jump") and Timer.get("CoyoteTime", True) < Main.p.coyoteTime:
            print("Jump!")
            Timer.set("CoyoteTime", Main.p.coyoteTime, True)
            self.jump()

        elif self.Controller.getKeyHeld("jump") and self.canWalljump:
            print("Walljump!")
            self.walljump(self.w)

        if self.Controller.getKeyHeld("dash") and self.dashes > 0 and Timer.get("dashcool"):
            Timer.set("dashcool", self.dashCooldown )
            Timer.set("dash", self.dashLength )
            self.dashState = True
            Main.fREEZEFRAMES += 2
            self.dash()            
        self.dashManager()

#Momentum to actual movement
        self.canWalljump = False
        
#Death from void        
        if self.Transform.yPosition > Main.level.height:
            self.die()

        if self.Transform.xPosition < 0:
            self.Transform.xPosition = 0
        elif self.Transform.xPosition > Main.p.screen_width + Main.level.length:
            self.Transform.xPosition = 0

    def die(self):
        self.Transform.xPosition = 500        
        self.Transform.yPosition = 0
        self.Transform.xVelocity = 0
        self.Transform.yVelocity = 1
        self.dead = True

    def jump(self):
        self.Transform.yVelocity = self.jumppower
        self.RigidBody.grounded = False
        self.dashSlow = 1
        self.Transform.xVelocity *= 2
        if self.dashLeave or self.dashState:
            print("Dash Cancel")
            if not self.Transform.xVelocity == 0:
                self.Transform.xVelocity = abs(self.Transform.xVelocity)/ self.Transform.xVelocity * 24
                if self.dashList[3] == True:
                    print("Hyper")
                    self.Transform.yVelocity = -13
                    self.Transform.xVelocity *= 3

    def walljump(self, wallcheck):
        if wallcheck[0] and wallcheck[1]:
            self.Transform.yVelocity = self.jumppower
        elif wallcheck[0]:
            self.Transform.xVelocity = -7
            self.Transform.yVelocity = self.jumppower
        elif wallcheck[1]:
            self.Transform.xVelocity = 7
            self.Transform.yVelocity = self.jumppower

        if self.dashLeave or self.dashState:
            if self.dashList[0]:
                print("Dash Cancel")
                self.Transform.yVelocity *= 1.2
                self.Transform.xVelocity *= 1.5
                
    def dash(self):
        input = ["up", "left", "right", "down", "jump", "dash"]
        self.dashes -= 1
        self.dashSlow = 2
        for i in range(4):
            if self.Controller.getKeyHeld(input[i]):
                self.dashList[i] = True
        if self.dashList == [False, False, False, False]:
            self.dashList[2] = True

    def dashManager(self):
        if not Timer.get("dash") and self.dashState:
            self.color = self.Renderer.colors["green"]
            if self.dashList[0]:
                if self.Transform.yVelocity > -self.dashSpeed:
                    self.Transform.yVelocity = -self.dashSpeed
            if self.dashList[1]:
                if self.Transform.xVelocity > -self.dashSpeed:
                    self.Transform.xVelocity = -self.dashSpeed
            if self.dashList[2]:
                if self.Transform.xVelocity < self.dashSpeed:
                    self.Transform.xVelocity = self.dashSpeed
            if self.dashList[3]:
                if self.Transform.yVelocity < self.dashSpeed:
                    self.Transform.yVelocity = self.dashSpeed
            if self.dashList[3]:
                if self.dashList[0]:
                    self.Transform.yVelocity = 0
#                    self.Transform.xVelocity *= 1.2
        elif self.dashState:
            self.dashState = False
            self.dashLeave = True
            self.color = (200, 200, 200)
            Timer.set("dashLeave", self.dashCooldown)
        if Timer.get("dashLeave") == False:
            if self.RigidBody.grounded:
                self.dashes = 1   

        if Timer.get("dashLeave") == True:
            self.dashList = [False, False, False, False]
            self.dashLeave = False
            self.color = self.Renderer.colors["blue"]

        if self.dashes > 0:
            self.color = self.Renderer.colors["red"]
        
        if self.dashSlow > 1:
            self.dashSlow /= 1.066
        if self.dashSlow < 1:
            self.dashSlow = 1
        #print(self.dashList, Timer.get("dash"))

    def resetDash(self):
        self.dashes = 1
        self.dashState = False
        self.dashLeave = False
        Timer.set("dashLeave", True)
        Timer.set("dash", True)
        Timer.set("dashcool", True)

import pygame as pyg
import Scripts.Components.components as MainComponent
import Scripts.timer  as Timer
import Scripts.boards as Boards
import Scripts.input  as Input
from Scripts.componentDependencyDecorators import *
Main = __import__("__main__")


#This is responsible for all of the actions a Character can do
#Mostly used for the player character
@dependencyWrapper(requiredDependencies={
    "Transform" : MainComponent.Transform ,
    "Renderer"  : MainComponent.Renderer  ,
    "Controller": MainComponent.Controller,
    "ConfigData": MainComponent.ConfigData,
    "Collider"  : MainComponent.Collider  ,
    "RigidBody" : MainComponent.RigidBody ,
}) # type: ignore
class Character():
    init_ = {
        'OnStart': True

    }
    @initOnCreate
    def __create() -> MainComponent.DependenciesTemplate:
        Character = Main.createObject("Character")
        Character.ConfigData = MainComponent.ConfigData(     # type: ignore
            dirFileName = 'CharacterProperties',
            fileType = "toml"
            )
        Character.Transform = MainComponent.Transform(     # type: ignore
            xPosition=Character.ConfigData.configFile["body"]["xpos"],     # type: ignore
            yPosition=Character.ConfigData.configFile["body"]["ypos"],     # type: ignore
            zPosition=Character.ConfigData.configFile["body"]["zpos"],     # type: ignore
            )
        Character.Renderer = MainComponent.Renderer(     # type: ignore
            Transform = Character.Transform,     # type: ignore
            xOffset=0,
            yOffset=0,
            xLength=20,
            yLength=20,
            path='Assets\Images\hehe.png',
            tier=5,
            )
        Character.Controller = MainComponent.Controller()     # type: ignore
        Character.Collider = MainComponent.Collider(     # type: ignore
            Transform = Character.Transform,     # type: ignore
            xLength = 20,
            yLength = 20,
            Objects = Objects,
            )
        Character.RigidBody = MainComponent.RigidBody(     # type: ignore
            Transform = Character.Transform,     # type: ignore
            Collider = Character.Collider,     # type: ignore
            mass = 5,
            )
        Character.Character=Character(     # type: ignore
            ConfigData = Character.ConfigData,     # type: ignore
            Transform = Character.Transform,     # type: ignore
            Renderer = Character.Renderer,     # type: ignore
            Controller = Character.Controller,     # type: ignore
            Collider = Character.Collider,     # type: ignore
            RigidBody = Character.RigidBody,     # type: ignore
            )
        Character = Main.createComplexObject("Character", 
            Controller = Character.Controller,     # type: ignore
            ConfigData = Character.ConfigData,      # type: ignore
            Transform = Character.Transform,      # type: ignore
            Renderer = Character.Renderer,      # type: ignore
            Collider = Character.Collider,      # type: ignore
            RigidBody = Character.RigidBody,      # type: ignore
            Character = Character.Character     # type: ignore
            )
        return Character

    @initializationWrapper
    def __initialize(self, dependencies, **kwargs) -> None:
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
        self.wallCollisions = None
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

    def __update(self):
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
            self.walljump(self.wallCollisions)

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

    def walljump(self, wallCollisions):
        if wallCollisions[0] and wallCollisions[1]:
            self.Transform.yVelocity = self.jumppower
        elif wallCollisions[0]:
            self.Transform.xVelocity = -7
            self.Transform.yVelocity = self.jumppower
        elif wallCollisions[1]:
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

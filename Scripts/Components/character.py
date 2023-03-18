import pygame as pyg
import Scripts.Components.components as MainComponent
import Scripts.timer  as Timer
import Scripts.boards as Boards
import Scripts.input  as Input
from Scripts.componentManager import *
Main = __import__("__main__")


#This is responsible for all of the actions a Character can do
#Mostly used for the player character
@dependencyWrapper_(requiredDependencies={
    "Transform" : MainComponent.Transform ,
    "Renderer"  : MainComponent.Renderer  ,
    "Controller": MainComponent.Controller,
    "ConfigData": MainComponent.ConfigData,
    "Collider"  : MainComponent.Collider  ,
    "RigidBody" : MainComponent.RigidBody ,
}) # type: ignore
class Character():
    init_ = {
        'OnStart': True,
        'OnCollision': False
    }

    def start__():
        return Character.create__()

    @initalizeOnStartWrapper_
    def create__() -> MainComponent.DependenciesTemplate:
        character = Main.createObject("Character")
        character.ConfigData = MainComponent.ConfigData(     # type: ignore
            dirFileName = 'CharacterProperties',
            fileType = "toml"
            )
        character.Transform = MainComponent.Transform(     # type: ignore
            xPosition=character.ConfigData.configFile["body"]["xpos"],     # type: ignore
            yPosition=character.ConfigData.configFile["body"]["ypos"],     # type: ignore
            zPosition=character.ConfigData.configFile["body"]["zpos"],     # type: ignore
            )
        character.Renderer = MainComponent.Renderer(     # type: ignore
            Transform = character.Transform,     # type: ignore
            xOffset=0,
            yOffset=0,
            xLength=20,
            yLength=20,
            path="Assets\\Images\\hehe.png",
            tier=5,
            )
        character.Controller = MainComponent.Controller()     # type: ignore
        character.Collider = MainComponent.Collider(     # type: ignore
            Transform = character.Transform,     # type: ignore
            xLength = 20,
            yLength = 20,
            Objects = Main.Objects,
            )
        character.RigidBody = MainComponent.RigidBody(     # type: ignore
            Transform = character.Transform,     # type: ignore
            Collider = character.Collider,     # type: ignore
            mass = 5,
            )
        character.character=Character(     # type: ignore
            ConfigData = character.ConfigData,     # type: ignore
            Transform = character.Transform,     # type: ignore
            Renderer = character.Renderer,     # type: ignore
            Controller = character.Controller,     # type: ignore
            Collider = character.Collider,     # type: ignore
            RigidBody = character.RigidBody,     # type: ignore
            )
        character = Main.createComplexObject("Character", type=Character,
            Controller = character.Controller,     # type: ignore
            ConfigData = character.ConfigData,      # type: ignore
            Transform = character.Transform,      # type: ignore
            Renderer = character.Renderer,      # type: ignore
            Collider = character.Collider,      # type: ignore
            RigidBody = character.RigidBody,      # type: ignore
            character = character.Character     # type: ignore
            )
        return character

    @initializationWrapper_
    def initialize__(self, dependencies, **kwargs) -> None:
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
        self.direction = 'left'
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

    def update__(self):
        #Makes checks to see if the character is able to reset the dash
        if Timer.get('dashcool') == True \
            and self.RigidBody.grounded \
            and self.dashState == False \
            and self.dashLeave == False:

            self.dashes = 1            
            self.color = self.Renderer.colors["red"]

        #Left and right movement
        if self.Controller.getKeyHeld('left') \
            and not self.Controller.getKeyHeld('right'):
            self.direction = 'left'
            
            if  self.Transform .xVelocity >- self.speed:
                self.Transform .xVelocity -= self.acc
        
            else:
                self.Transform .xVelocity += self.decel

        elif    self.Controller.getKeyHeld('right') \
            and not self.Controller.getKeyHeld('left' ) :
            self.direction = 'right'

            if  self.Transform .xVelocity <  self.speed:
                self.Transform .xVelocity += self.acc
        
            else:
                self.Transform .xVelocity -= self.decel
        
        else:
            if  self.Transform.xVelocity <=-self.decel:
                self.Transform.xVelocity += self.decel * self.dashSlow
            
            elif self.Transform.xVelocity >= self.decel:
                self.Transform.xVelocity -= self.decel * self.dashSlow
            
            else:
                self.Transform.xVelocity = 0

        

        #Increases gravity if down is held
        if self.Controller.getKeyHeld("down"):
            self.RigidBody.mass = 14
        else:
            self.RigidBody.mass = 7

        #Actions
        if self.Controller.getKeyHeld("jump") \
            and self.RigidBody.grounded \
        or self.Controller.getKeyHeld("jump") \
            and Timer.get("CoyoteTime", True) < Main.p.coyoteTime:
            print("Jump!")
            Timer.set("CoyoteTime", Main.p.coyoteTime, True)
            self.jump()

        elif self.Controller.getKeyHeld("jump") \
            and self.canWalljump:
            print("Walljump!")
            self.walljump(self.wallCollisions)

        if self.Controller.getKeyHeld("dash") \
            and self.dashes > 0 \
            and Timer.get("dashcool"):
            Timer.set("dashcool", self.dashCooldown )
            Timer.set("dash", self.dashLength )
            self.dashState = True
            Main.fREEZEFRAMES += 2
            self.dash()            

        self.dashManager()

        #Resets it afterward so that it doesn't last after it is necessary
        self.canWalljump = False
        
        #Death from void        
        if self.Transform.yPosition > Main.level.height:
            self.die()

        #Wrap the character around if they reach the end, but only one way
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
        print("Jump!")
        if self.dashLeave or self.dashState:
            print("Dash Cancel!")
            if not self.Transform.xVelocity == 0:
                self.Transform.xVelocity = abs(self.Transform.xVelocity)/ self.Transform.xVelocity * 24
                if self.dashList[3] == True:
                    print("Hyper!")
                    self.Transform.yVelocity  = -13
                    self.Transform.xVelocity *=  3

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

    def resetDash(self):
        self.dashes = 1
        self.dashState = False
        self.dashLeave = False
        Timer.set("dashLeave", True)
        Timer.set("dash", True)
        Timer.set("dashcool", True)

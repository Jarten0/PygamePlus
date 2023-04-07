import pygame as pyg
from Scripts import Input
from Scripts.componentManager import newComponent
from main import *
from typing import Type
#This is responsible for all of the actions a Character can do
#Mostly used for the player character
@newComponent
class Character():
    import Scripts.Components.components as cmp
    requiredDependencies = {
        'ConfigData': cmp.ConfigData,    
        'Transform' : cmp.Transform,      
        'Renderer'  : cmp.Renderer,      
        'Collider'  : cmp.Collider,      
        'RigidBody' : cmp.RigidBody,
    }
    optionalArguments = {
        'ConfigData',    
        'Transform',      
        'Renderer',      
        'Collider',      
        'RigidBody',
    }
    @classmethod
    def create(cls, name:str="Character") -> object:
        ConfigData = Component.new('components\\ConfigData',
            dirFileName = 'CharacterProperties',
            fileType = "toml"
            )
        Transform = Component.new('components\\Transform',
            xPosition=ConfigData.configFile["body"]["xpos"],     # type: ignore
            yPosition=ConfigData.configFile["body"]["ypos"],     # type: ignore
            zPosition=ConfigData.configFile["body"]["zpos"],     # type: ignore
            )
        Renderer = Component.new('components\\Renderer',
            Transform = Transform,  
            xOffset=0,
            yOffset=0,
            xLength=20,
            yLength=20,
            path="\\Assets\\Images\\hehe.png",
            tier=5,
            )
        Collider = Component.new('components\\Collider',
            Transform = Transform,    
            xLength = 20,
            yLength = 20,
            )
        RigidBody = Component.new('components\\RigidBody',
            Transform = Transform,    
            Collider = Collider,    
            mass = 5,
            )
        return name, cls, \
           {'ConfigData': ConfigData,
            'Transform': Transform,
            'Renderer': Renderer,
            'Collider': Collider,
            'RigidBody': RigidBody}
            
    def init(self, 
            ConfigData,    
            Transform ,      
            Renderer  ,      
            Collider  ,      
            RigidBody , 
            *args, **kwargs) -> None:
        from main import settings, level, delta
        self.ConfigData = ConfigData    
        self.Transform = Transform      
        self.Renderer = Renderer      
        self.Collider = Collider     
        # self.RigidBody = RigidBody   

        configFile = self.ConfigData.configFile
        self.settings = settings
        self.level = level
        
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
        self.color = self.Renderer.colors["red"] # type: ignore
        self.DCsuper = 0
        self.DChyper = 0
        self.delta = delta

    def update(self) -> None:
        from main import delta
        print(delta, "Hehe")
        if Input.getHeld('left'):
            self.Transform.xPosition -= self.speed * delta
        if Input.getHeld('right'):
            self.Transform.xPosition += self.speed * delta
        if Input.getHeld('up'):
            self.Transform.yPosition -= self.speed * delta
        if Input.getHeld('down'):
            self.Transform.yPosition += self.speed * delta
        return
        #Makes checks to see if the character is able to reset the dash
        if Timer.getValue('dashcool', inc=False) \
            and self.RigidBody.grounded \
            and self.dashState == False \
            and self.dashLeave == False:

            self.dashes = 1            
            self.color = self.Renderer.colors["red"]

        #Left and right movement
        if Input.getHeld('left') \
            and not Input.getHeld('right'):
            self.direction = 'left'
            
            if  self.Transform .xVelocity >- self.speed:
                self.Transform .xVelocity -= self.acc
        
            else:
                self.Transform .xVelocity += self.decel

        elif    Input.getHeld('right') \
            and not Input.getHeld('left' ) :
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
        if Input.getHeld("down"):
            self.RigidBody.mass = 14
        else:
            self.RigidBody.mass = 7

        #Actions
        if Input.getHeld("jump"):
            if Timer.getValue("CoyoteTime", False) < settings['coyoteTime'] or self.RigidBody.grounded:
                self.jump()

        elif Input.getHeld("jump") \
            and self.canWalljump:
            print("Walljump!")
            self.walljump(self.wallCollisions)

        if Input.getHeld("dash") \
            and self.dashes > 0 \
            and Timer.get("dashcool"):
            Timer.set("dashcool", self.dashCooldown )
            Timer.set("dash", self.dashLength )
            self.dashState = True
            # Main.fREEZEFRAMES += 2
            self.dash()            

        self.dashManager()

        #Resets it afterward so that it doesn't last after it is necessary
        self.canWalljump = False
        
        #Death from void        
        if self.Transform.yPosition > self.level.height: # type: ignore
            self.die()

        #Wrap the character around if they reach the end, but only one way
        if self.Transform.xPosition < 0:
            self.Transform.xPosition = 0
        elif self.Transform.xPosition > settings.screen_width + level.length: # type: ignore
            self.Transform.xPosition = 0
"""
    def die(self):
        self.Transform.xPosition = 500        
        self.Transform.yPosition = 0
        self.Transform.xVelocity = 0
        self.Transform.yVelocity = 1
        self.dead = True

    def jump(self):
        print("Jump!")
        Timer.setDec("CoyoteTime", 0)

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
            if Input.getHeld(input[i]):
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
        Timer.setDec("dashLeave", True)
        Timer.setDec("dash",      True)
        Timer.setDec("dashcool",  True)
    """
# pyright: reportGeneralTypeIssues=false
from Scripts import Input
import Scripts.Components.Collider
import Scripts.Components.Renderer
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
        'Renderer'  : Scripts.Components.Renderer.Renderer,      
        'Collider'  : Scripts.Components.Collider.Collider,      
        'RigidBody' : Scripts.Components.Collider.RigidBody,
    }
    optionalArguments = {
        'ConfigData',    
        'Transform',      
        'Renderer',      
        'Collider',      
        'RigidBody',
    }
            
    def init(self, 
            ConfigData,    
            Transform ,      
            Renderer  ,      
            Collider  ,      
            RigidBody , 
            *args, **kwargs) -> None:
        from main import settings, level
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

    def update(self) -> None:
        print(Input.getHeld('left'))
        if Input.getHeld('left'):
            self.Transform.xVel -= self.speed * self.Scene.delta
        if Input.getHeld('right'):
            self.Transform.xVel += self.speed * self.Scene.delta
        if Input.getHeld('up'):
            self.Transform.yVel -= self.speed * self.Scene.delta
        if Input.getHeld('down'):
            self.Transform.yVel += self.speed * self.Scene.delta
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
            
            if  self.Transform .xVel >- self.speed:
                self.Transform .xVel -= self.acc
        
            else:
                self.Transform .xVel += self.decel

        elif    Input.getHeld('right') \
            and not Input.getHeld('left' ) :
            self.direction = 'right'

            if  self.Transform .xVel <  self.speed:
                self.Transform .xVel += self.acc
        
            else:
                self.Transform .xVel -= self.decel
        
        else:
            if  self.Transform.xVel <=-self.decel:
                self.Transform.xVel += self.decel * self.dashSlow
            
            elif self.Transform.xVel >= self.decel:
                self.Transform.xVel -= self.decel * self.dashSlow
            
            else:
                self.Transform.xVel = 0

        

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
        if self.Transform.yPos > self.level.height: # type: ignore
            self.die()

        #Wrap the character around if they reach the end, but only one way
        if self.Transform.xPos < 0:
            self.Transform.xPos = 0
        elif self.Transform.xPos > settings.screen_width + level.length: # type: ignore
            self.Transform.xPos = 0
"""
    def die(self):
        self.Transform.xPos = 500        
        self.Transform.yPos = 0
        self.Transform.xVel = 0
        self.Transform.yVel = 1
        self.dead = True

    def jump(self):
        print("Jump!")
        Timer.setDec("CoyoteTime", 0)

        self.Transform.yVel = self.jumppower
        self.RigidBody.grounded = False
        self.dashSlow = 1
        self.Transform.xVel *= 2
        print("Jump!")
        if self.dashLeave or self.dashState:
            print("Dash Cancel!")
            if not self.Transform.xVel == 0:
                self.Transform.xVel = abs(self.Transform.xVel)/ self.Transform.xVel * 24
                if self.dashList[3] == True:
                    print("Hyper!")
                    self.Transform.yVel  = -13
                    self.Transform.xVel *=  3

    def walljump(self, wallCollisions):
        if wallCollisions[0] and wallCollisions[1]:
            self.Transform.yVel = self.jumppower
        elif wallCollisions[0]:
            self.Transform.xVel = -7
            self.Transform.yVel = self.jumppower
        elif wallCollisions[1]:
            self.Transform.xVel = 7
            self.Transform.yVel = self.jumppower

        if self.dashLeave or self.dashState:
            if self.dashList[0]:
                print("Dash Cancel")
                self.Transform.yVel *= 1.2
                self.Transform.xVel *= 1.5
                
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
                if self.Transform.yVel > -self.dashSpeed:
                    self.Transform.yVel = -self.dashSpeed
            if self.dashList[1]:
                if self.Transform.xVel > -self.dashSpeed:
                    self.Transform.xVel = -self.dashSpeed
            if self.dashList[2]:
                if self.Transform.xVel < self.dashSpeed:
                    self.Transform.xVel = self.dashSpeed
            if self.dashList[3]:
                if self.Transform.yVel < self.dashSpeed:
                    self.Transform.yVel = self.dashSpeed
            if self.dashList[3]:
                if self.dashList[0]:
                    self.Transform.yVel = 0
#                    self.Transform.xVel *= 1.2
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
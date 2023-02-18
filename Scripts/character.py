import Scripts.boards as Boards
import Scripts.cameramanager as cam
from Scripts.timer import Timer 
import tomllib, os
#import main
colors = {
    "red":   (255,0,  0  ),
    "green": (0,  255,0  ),
    "blue":  (0,  0,  255),
    "gray":  (30, 30, 30 ),
}
class create():
    def __init__(self):
        with open(os.getcwd()+'\ConfigFiles\characterProperties.toml', "rb") as f:
            configFile = tomllib.load(f)
            print(configFile)
        self.x = configFile['body']['xpos']
        self.y = configFile['body']['ypos']
        self.xl = configFile['body']['xlength']
        self.yl = configFile['body']['ylength']
        self.xv = 0
        self.yv = 0
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
        self.x = 500        
        self.y = 0
        self.xv = 0
        self.dashes = 1
        self.dead = True

    def jump(self):
        self.yv = self.jumppower
        self.gr = False
        self.dashslow = 1
        self.xv * 2
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

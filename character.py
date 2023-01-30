import boards as Boards
import cameramanager as cam
from timer import Timer 
#import main
colors = {
    "red":   (255,0,  0  ),
    "green": (0,  255,0  ),
    "blue":  (0,  0,  255),
}
class create():
    def __init__(self, x, y, xl, yl, xv = 0, yv = 0, gr = False, st = 0, wj = False):
        self.x = x
        self.y = y
        self.xl = xl
        self.yl = yl
        self.xv = xv
        self.yv = yv
        self.gr = gr
        self.st = st
        self.wj = wj
        self.w = None
        self.speed = 6
        self.acc = 1
        self.decel = 0.5
        self.dyndecel = 1
        self.jumppower = -18
        self.gravity = 7
        self.dashes = 1
        self.dashstate = False
        self.dashleave = True
        self.dashlength = 10
        self.dashcooldown = 8
        self.dashspeed = 18
        self.dashlist = [False, False, False, False]
        self.dashslow = 1
        self.color = colors["red"]

    def die(self, yspawn = 10000, jumpOnSpawn = True, xspawn = 500):
        self.x = xspawn        
        self.y = yspawn
        self.xv = 0
        self.dashes = 1

        if jumpOnSpawn:
            self.yv = -30
        

    def jump(self):
        self.yv = self.jumppower
        self.gr = False
        self.dashslow = 1
        self.xv * 1.2
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

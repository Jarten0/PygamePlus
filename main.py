#Import And Initialize ===========================================================================================================
import pygame as pyg, EZPickle as FileManager, input as InputManager
import platforms as platform, character, boards as Boards, cameramanager as cam
from timer import Timer
from sys import exit
pyg.init()

#Add names of files here: -----------------------------
platformfilename = 'PgPlatforms.dat'


lis = {
"scwd": 1000,
"schi": 1000,
"bgcol": (100, 100, 255),
"fps": 240,
"renderfps": 60,
"grid": 10,
"Coyote Time": 10,
}

#Setup ====================================================================================================================
#Main Functions =========================================
#Get Input --------------------------------------------
    
    
class dev():
    def cmd():
        while True:
            ans = input(">")
            if ans == "cv":
                ans = input("Name>")
                if ans in lis:
                    lis[ans] = int(input("Value>"))
                    p = defaultPropereties(lis)
                    FileManager.save(p, 'prop.dat')
            if ans == "cf":
                ans = input("File:")
                    
            if ans == "exit" or ans == "" or ans == "z":
                return p

class defaultPropereties(): 
    def __init__(self, lis):
        self.lis = lis
        print(lis)
        #Screen -----------------------------------------------
        self.screen_width = lis["scwd"]
        self.screen_height = lis["schi"]
        self.bg_color = lis["bgcol"]
        self.grid = lis["grid"]
        
        #Clock ------------------------------------------------
        self.fps = lis["fps"]
        self.renderfps = lis["renderfps"]
        self.game_timer = 0
        self.total_ticks = 0

        #Colors -----------------------------------------------
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        #Character
        self.coyoteTime = lis["Coyote Time"]

        #Misc
        self.SceneType = "main"
        
#Load propereties ---------------------------------------------
p = FileManager.load('prop.dat')
p = False
if p == False: 
    p = defaultPropereties(lis)
FileManager.save(p, 'prop.dat')

char = character.create(p.screen_width/2, 0, 20, 20)

clock = pyg.time.Clock()
# - Screen init -
screen = pyg.display.set_mode((p.screen_width, p.screen_height))
pyg.display.set_caption('Platformer')

class Level():
    def __init__(self, name, plat, length = 200, width = 200):
        self.name = name
        self.plat = plat
        self.length = length * 20
        self.width = width * 5


#Platforms ----------------------------------------------------
platData = {
    0: None,
#100 - 199 are levels in the game
    100: {},
#200 - 299 are names of the levels
    200: "Level 0",
}


#---------------------------------------------------------------------------------------------------------------------------
#Platforming Mode ==========================================================================================================
def inPlatScene():
    placestage = 0
    mousedown = False
    select = 0
    p = FileManager.load('prop.dat')
    level = Level("Level 0", platData[100], 500, 500)
    Timer.set("dashcool", 20)
    Timer.set("grace", 0, True)
    Timer.set("CoyoteTime", 0, True)
    Timer.set("dash", True)
    Timer.set("dashleave", 4)
    Timer.__str__()
    print(Timer.get("CoyoteTime", True))
    delta = ((1 * p.fps) / 60) * 4
    fREEZEFRAMES = 0

    data = FileManager.load(platformfilename)
    level = Level(data[100], data[100])

    while p.SceneType == "main":
        
        renderframeavg = p.fps / p.renderfps
        #print(renderframeavg, p.fps, p.renderfps, p.total_ticks, p.total_ticks % round(renderframeavg) )
        if p.total_ticks % renderframeavg == 0:
            renderFrame = True
            
            #print("rendered")
        else:
            renderFrame = False
            #print("not rendered")
#        print(renderFrame)
        if fREEZEFRAMES > 0:
            fREEZEFRAMES -= 1
            pyg.display.flip()
            clock.tick(p.fps)
            continue

        mousepos = pyg.mouse.get_pos()
        mousepos = (mousepos[0] + cam.xpos, mousepos[1] + cam.ypos)
        mouseposx = round((mousepos[0]/p.grid), 0)*p.grid
        mouseposy = round((mousepos[1]/p.grid), 0)*p.grid
        mouselist = pyg.mouse.get_pressed(num_buttons=5)
        Ev = pyg.event.get()
        Evh = pyg.key.get_pressed()



#Input From Player =========================================================================================================
        input = ["up", "left", "right", "down", "jump", "dash", "dash", "LEFT", "RIGHT", "UP", "DOWN"]
        letter = ["w", "a", "d", "s", "k", "k", "o",            "LEFT", "RIGHT", "UP", "DOWN"]    
        for i in range(len(input)):
            if InputManager.kh(letter[i], Evh):
                Boards.apP(True, input[i])
            else:
                Boards.apP(False, input[i])

        if InputManager.k("z", Ev):
            platData[100] = level.plat
            FileManager.save(platData, platformfilename)
            print("Saved Platform Data")
        if InputManager.k("x", Ev):
            data = FileManager.load(platformfilename)
            level = Level(data[100], data[100])
        if InputManager.k("c", Ev):
            level.plat = {}
        if InputManager.k("q", Ev):
            pyg.quit()
            exit()
        if InputManager.k("r", Ev):
            p = defaultPropereties(lis)
            FileManager.save(p, 'prop.dat')
            print("Saved Propereties")        
        #if InputManager.k("e", Ev):

        for i in range(10):
            if InputManager.k(str(i), Ev):
                select = i
            

        if InputManager.k("a", Ev):
            Boards.apP(True, "left")
        if InputManager.k("d", Ev):
            Boards.apP(True, "left")
        if InputManager.k("TAB", Ev):
            p = dev.cmd()
        if InputManager.k("`", Ev):
            FileManager.save(p, "prop.dat")
            print("Saved Propereites")

        if mouselist[0]:
            if not mousedown:
                print("Click!")
                if select == 0:
                    for i in level.plat:
                        if platform.collision.check(mouseposx, mouseposy, 1, 1, level.plat[i].x, level.plat[i].y, level.plat[i].xl, level.plat[i].yl):
                            del level.plat[i]
                            break
                
                elif placestage == 0:
                    placestage = 1
                    tempx = mouseposx
                    tempy = mouseposy
                    print(f"({tempx}, {tempy})")
                    
                
                elif placestage == 1:
                    tempx2 = mouseposx
                    tempy2 = mouseposy
                    if tempx > tempx2:
                        xstate = tempx2
                    else:
                        xstate = tempx
                    if tempy > tempy2:
                        ystate = tempy2
                    else:
                        ystate = tempy
                    
                    if platform.placeprop[select]["#HasPlaceReq"]:
                        if not platform.placeprop["xl"] == False:
                            tempx2 = platform.placeprop["xl"]
                            tempx = 0
                        if not platform.placeprop["yl"] == False:
                            tempy2 = platform.placeprop["yl"]
                            tempy = 0

                    if not abs(tempx2 - tempx) == 0 and not abs(tempy2 - tempy) == 0:
                        level.plat[platform.NextID(level.plat)] = platform.create(xstate, ystate, abs(tempx2 - tempx), abs(tempy2 - tempy), select)  
                    placestage = 0
                mousedown = True
        else:
            mousedown = False

#Movement/Collisions =========================================================================================================
        if Timer.get("dashcool") == True and char.gr and char.dashstate == False and char.dashleave == False:
            char.dashes = 1            
            char.color = character.colors["red"]
        if Boards.getP('left') and not Boards.getP('right'):
            if char.xv > -char.speed:
                char.xv -= char.acc/( p.fps * delta)
            else:
                char.xv += char.decel/( p.fps * delta)
        elif Boards.getP('right') and not Boards.getP('left'):
            if char.xv < char.speed:
                char.xv += char.acc/( p.fps * delta)
            else:
                char.xv -= char.decel/( p.fps * delta)
        else:
            if   char.xv <=-char.decel:
                 char.xv += char.decel * char.dashslow
            elif char.xv >= char.decel:
                 char.xv -= char.decel * char.dashslow
            else:
                char.xv = 0

        if Boards.getP("jump") and char.gr or Boards.getP("jump") and Timer.get("CoyoteTime", True) < p.coyoteTime:
            print("Jump!")
            Timer.set("CoyoteTime", p.coyoteTime, True)
            char.jump()

        elif Boards.getP("jump") and char.wj:
            print("Walljump!")
            char.walljump(char.w)

        if Boards.getP("dash") and char.dashes > 0 and Timer.get("dashcool"):
            Timer.set("dashcool", char.dashcooldown * renderframeavg)
            Timer.set("dash", char.dashlength * renderframeavg)
            char.dashstate = True
            fREEZEFRAMES += 2
            char.dash()            

        

        if char.yv < char.gravity and char.gr == False:
            char.yv += 1 /( p.fps * delta)
        
        #print("Speed: ", char.speed)
        #print("Dash: ",Timer.getvalue("dash", False), "   Dashcool: ", Timer.getvalue("dashcool", False))
        if not Timer.get("dash") and char.dashstate:
            char.color = character.colors["green"]
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
            Timer.set("dashleave", char.dashcooldown* renderframeavg)
        if Timer.get("dashleave") == False:
            if char.gr:
                char.dashes = 1   

        if Timer.get("dashleave") == True:
            char.dashlist = [False, False, False, False]
            char.dashleave = False
            char.color = character.colors["blue"]

        if char.dashes > 0:
            char.color = character.colors["red"]
        
        if char.dashslow > 1:
            char.dashslow / 1.066
        if char.dashslow < 1:
            char.dashslow = 1
        #print(char.dashlist, Timer.get("dash"))

        char.x += char.xv /( p.fps * delta)
        char.y += char.yv /( p.fps * delta)
        #print(delta*p.fps)
        
        
        
        if char.y > p.screen_height:
            char.die()
        if char.x < 0:
            char.x = p.screen_width
        elif char.x > p.screen_width + level.length:
            char.x = 0
        
        
        #Platform checker, uses pre-determined checking of which parts of the wall have been collided with
        char.gr = False
        char.wj = False
        for platformToBeChecked in range(len(level.plat)):
            pTBC = level.plat[platformToBeChecked]
            wallcheck = platform.collision.check(char.x, char.y, char.xl, char.yl, pTBC.x, pTBC.y, pTBC.xl, pTBC.yl)
            if pTBC.type == 1:
                platform.types.wall(char, wallcheck, pTBC),
            if pTBC.type == 2:
                platform.types.passthrough(char, wallcheck, pTBC),
            if pTBC.type == 3:
                platform.types.lava(char, wallcheck, pTBC),
            if pTBC.type == 4:
                platform.types.bounce(char, wallcheck, pTBC)

    #Render Scene ===============================================================================================================
        if renderFrame:
            if Boards.getP("LEFT"):
                cam.xoffset -= 10
            elif Boards.getP("RIGHT"):
                cam.xoffset += 10


            if char.x > p.screen_width / 2 and char.x < level.length - p.screen_width / 2 :
                cam.xdefault = char.x - p.screen_width / 2    
            else:
                if char.x < p.screen_width:
                    cam.x = 0
                else:
                    cam.x = level.length
            
            cam.xpos = cam.xdefault + cam.xoffset
            #print(level.length, cam.xpos, char.x)
            #print(char.x > p.screen_width / 2 , char.x < level.length - p.screen_width / 2)

            screen.fill(p.bg_color)

    #Render Player ------------------------------------
            pyg.draw.rect(screen, char.color, (char.x - cam.xpos, char.y - cam.ypos, char.xl, char.yl))

    #Render Platforms ---------------------------------
            for platID in range(len(level.plat)):
                pyg.draw.rect(screen, level.plat[platID].color , (level.plat[platID].x - cam.xpos, level.plat[platID].y - cam.ypos, level.plat[platID].xl, level.plat[platID].yl))

    #Render Temporary Platform ------------------------
            if placestage > 0:
                (abs(mousepos[0]) + mousepos[0])/2
                tempx2 = mouseposx
                tempy2 = mouseposy
                
                #Find the values that are closer to the origin
                if tempx < tempx2:
                    LTempx = tempx2
                    STempx = tempx
                else:
                    LTempx = tempx
                    STempx = tempx2
                if tempy < tempy2:
                    LTempy = tempy2
                    STempy = tempy
                else:
                    LTempy = tempy
                    STempy = tempy2
                if LTempy - STempy < 10:
                    temptype = 1
                else:
                    temptype = 0

                if platform.placeprop[select]["#HasPlaceReq"]:
                        if not platform.placeprop[select]["xl"] == False:
                            LTempx = platform.placeprop[select]["xl"]
                            STempx = 0
                        if not platform.placeprop[select]["yl"] == False:
                            LTempy = platform.placeprop[select]["yl"]
                            STempy = 0

                pyg.draw.rect(screen, platform.platcolors[select], (STempx - cam.xpos, STempy - cam.ypos, LTempx - STempx, LTempy - STempy))
            #Indicator Dot for Grid Placment
            pyg.draw.rect(screen, p.red, (mouseposx - 2 - cam.xpos, mouseposy - 2 - cam.ypos, 4, 4))
            
            
            pyg.display.flip()
        #print(char.dashlist, Timer.get("dashleave"), Timer.getvalue("dashleave", False))

        Timer.tick()
        clock.tick(p.fps)
        
        p.game_timer += ((1 * p.fps) / 60) / 60
        p.total_ticks += 1
        delta = (((1 * p.fps) / 60) / 60) / renderframeavg 

inPlatScene()
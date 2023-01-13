#Import And Initialize ===========================================================================================================
import pygame as pyg
import EZPickle as FileManager
from sys import exit
pyg.init()

#Add names of files here: -----------------------------
pgplfile = 'PgPlatforms.dat'

lis = {
"scwd": 500,
"schi": 500,
"bgcol": (100, 100, 255),
"fps": 60,
"grid": 10,
}

# -----------------------------------------------------
#Setup ====================================================================================================================
#Main Functions =========================================
#Save and Load ----------------------------------------
"""
class FileManager():
    def save(value, file):
        try:    
            with open(file, "wb") as filename:
                pkd(value, filename)    
        except FileNotFoundError:
            file = open(file, "x")
            pkd(value, file)
    def load(file):
        try:
            with open(file, "rb") as filename:
                value = pkl(filename)
            return value
        except FileNotFoundError:
            print("Failed to load data: No file currently present. Creating a new one...")
            open(file, "x")
            with open(file, "wb") as filename:
                pkd(False, filename)
            return False
        except EOFError:
            print("File data error, resetting propereties to default...")
            open(file, "w")
            with open(file, "wb") as filename:
                pkd(False, filename)
            return False
"""
#Get Input --------------------------------------------
class getInput():
    kbl = {
        "z": pyg.K_z,
        "x": pyg.K_x,
        "c": pyg.K_c,
        "q": pyg.K_q,
        "r": pyg.K_r,
        "w": pyg.K_w,
        "a": pyg.K_a,
        "s": pyg.K_s,
        "d": pyg.K_d,
        "k": pyg.K_k,
        "TAB": pyg.K_TAB,
        "`": pyg.K_RALT
        }

    def k(input, events, keybindlist = kbl):
        for event in events:
            if event.type == pyg.KEYDOWN:
                if event.key == keybindlist[input]:
                    return True
                else:
                    return False
            else:
                return False

    def kh(input, events, keybindlist = kbl):
        if events[getInput.kbl[input]]:
            return True
        else:
            return False
    
# Boards ----------------------------------------------
class Boards():
    temp = {}
    perm = {
        "jump": False,
        "jumpbuffer": 5,
        "left": False,
        "right": False,
        "dash": False,
        "dashcool": 0,
    }
    
    def apT(value, key = None):
        if not key == None:
            try:
                Boards.temp[key] = value
                return key
            except KeyError:
                Boards.temp[len(Boards.temp)] = value
                return len(Boards.temp) - 1    
        else:
            Boards.temp[len(Boards.temp)] = value
            return len(Boards.temp) - 1
    def apP(value, key = ""):
        if not key == None:
            try:
                Boards.perm[key] = value
                return key
            except KeyError:
                Boards.perm[len(Boards.temp)] = value
                return len(Boards.perm) - 1    
        else:
            Boards.perm[len(Boards.temp)] = value
            return len(Boards.perm) - 1
    def getT(key):
        return Boards.perm[key]
    def getP(key):
        return Boards.perm[key]

class Timers():
    UpList = {}
    DownList = {}

    def tick():
        for i in Timers.UpList:
            Timers.UpList[i] += 1
        for i in Timers.DownList:
            if not Timers.DownList[i]:
                Timers.DownList[i] -= 1
            if Timers.Downlist[i] == 0:
                Timers.DownList[i] = True

    def set(name = False, value = None, up = False):
        if value == None or up:
            if name == False:
                keylist = Timers.UpList.keys()
                for i in Timers.UpList:
                    if not keylist[Timers.UpList.index(i)] == i:
                        name = Timers.UpList[i]
                        print(name)
            Timers.UpList[name] = 0
        else:
            Timers.DownList[name] = value

    def get(name, up = False):
        if up:
            return Timers.UpList[name]
        return Timers.DownList[name] 

class character():
    def __init__(self, x, y, xl, yl, xv = 0, yv = 0, gr = False, st = 0):
        self.x = x
        self.y = y
        self.xl = xl
        self.yl = yl
        self.xv = xv
        self.yv = yv
        self.gr = gr
        self.st = st

class platform():
    def __init__(self, x, y, xl, yl) -> None:
        self.x = x
        self.y = y
        self.xl = xl
        self.yl = yl

class dev():
    def cmd():
        while True:
            ans = input(">")
            if ans == "cv":
                ans = input("Name>")
                if ans in lis:
                    lis[ans] = int(input("Value>"))
                    p = propereties(lis)
                    FileManager.save(p, 'prop.dat')
            if ans == "cf":
                ans = input("File:")
                    
            if ans == "exit" or ans == "" or ans == "z":
                return p

class propereties(): 
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
        self.game_timer = 0

        #Colors -----------------------------------------------
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        #Misc
        self.SceneType = "main"
        
#Load propereties ---------------------------------------------
p = FileManager.load('prop.dat')
if p == False: 
    p = propereties(lis)
FileManager.save(p, 'prop.dat')

char = character(p.screen_width/2, 0, 10, 10)
clock = pyg.time.Clock()
start_ticks = pyg.time.get_ticks()
p1 = pyg.Rect(100, 100, 100, 100)
# - Screen init -
screen = pyg.display.set_mode((p.screen_width, p.screen_height))
pyg.display.set_caption('Platformer')

#Platform Collision -------------------------------------------
class Plat():
    def colcheck(cx, cy, cxl, cyl, px, py, pxl, pyl):
        if cy + cyl >= py and cy <= py + pyl:
            if cx + cxl >= px and cx <= px + pxl:
                if cy + cyl > py - 5:
                    return 1
                elif cx + cxl > px + 20:
                    return 2
                elif cx < px + pxl - 20:
                    return 3                
                return 1
            else:
                return 0
        else:
            return 0

#Platforms ----------------------------------------------------
scene1platforms = {}

propLoc = {
    0: None,
    100: scene1platforms
}

#---------------------------------------------------------------------------------------------------------------------------
#Platforming Mode ==========================================================================================================
def inPlatScene():
    scene1platforms = {}
    placestage = 0
    mousedown = False
    p = FileManager.load('prop.dat')
    
    Timers.set("dashcool", 20)
    while p.SceneType == "main":
        pyg.display.flip()
        mousepos = pyg.mouse.get_pos()
        mousepos[0] = round((mousepos[0]/p.grid), 0)*p.grid
        mousepos[1] = round((mousepos[1]/p.grid), 0)*p.grid
        mouselist = pyg.mouse.get_pressed(num_buttons=5)
        Ev = pyg.event.get()
        Evh = pyg.key.get_pressed()

#Input From Player =========================================================================================================
        input = ["left", "right", "jump", "dash"]
        letter = ["a", "d", "w", "k"]    
        for i in range(len(input)):
            if getInput.kh(letter[i], Evh):
                Boards.apP(True, input[i])
            else:
                Boards.apP(False, input[i])

        if getInput.k("z", Ev):
            FileManager.save(scene1platforms, pgplfile)
        if getInput.k("x", Ev):
            scene1platforms = FileManager.load(pgplfile)
        if getInput.k("c", Ev):
            scene1platforms = {}
        if getInput.k("q", Ev):
            pyg.quit()
            exit()
        

        if getInput.k("a", Ev):
            Boards.apP(True, "left")
        if getInput.k("d", Ev):
            Boards.apP(True, "left")
        if getInput.k("TAB", Ev):
            p = dev.cmd()
        if getInput.k("`", Ev):
            FileManager.save(p, "prop.dat")

        if mouselist[0]:
            if not mousedown:
                print("Click!")
                if placestage == 0:
                    placestage = 1
                    tempx = mousepos[0]
                    tempy = mousepos[1]
                    print(f"({tempx}, {tempy})")
                elif placestage == 1:
                    tempx2 = mousepos[0]
                    tempy2 = mousepos[1]
                    if tempx > tempx2:
                        xstate = tempx2
                    else:
                        xstate = tempx
                    if tempy > tempy2:
                        ystate = tempy2
                    else:
                        ystate = tempy
                    scene1platforms[len(scene1platforms)] = platform(xstate, ystate, abs(tempx2 - tempx), abs(tempy2 - tempy))  
                    placestage = 0
                mousedown = True
        else:
            mousedown = False

#Movement/Collisions =========================================================================================================
        if char.yv < 9 and char.gr == False:
            char.yv += 1
        

        for i in range(len(scene1platforms)):
            ycheck = Plat.colcheck(char.x, char.y, char.xl, char.yl, scene1platforms[i].x, scene1platforms[i].y, scene1platforms[i].xl, scene1platforms[i].yl)
            if ycheck == 1:
                if char.y > scene1platforms[i].y:
                    char.xv = 0
                char.gr = True
                char.yv = 0
                char.y = scene1platforms[i].y - char.yl
                break
            else:
                char.gr = False


        if Boards.getP('left') and not Boards.getP('right'):
            if char.xv > -4:
                char.xv -= 1
        elif Boards.getP('right'):
            if char.xv < 4:
                char.xv += 1
        else:
            if char.xv < -0.5:
                char.xv += 1
            elif char.xv > 0.5:
                char.xv -= 1
            else:
                char.xv = 0

        if Boards.getP("jump") and Boards.getP("jumpbuffer") > 0 and char.gr:
            print("Jump!")
            char.yv -= 15
            char.gr = False
            Boards.apP(1, "jumpbuffer")  

        if Boards.getP("dash") and Boards.getP("dashcool") == 0 or Boards.getP("dash") and Boards.getP("dashcool") == 20 and char.gr:
            print("Dash!")
            Boards.apP(30, "dashcool")
            if char.xv == 0:
                char.xv += 1
            elif Boards.getP("right"):
                if char.xv < 10:
                    char.xv = 10
                char.yv = -1
            elif Boards.getP("left"):       
                if char.xv > -10:
                    char.xv = -10
                char.yv = -1 
            
            
        else:
            if Boards.getP("dashcool") > 0:
                Boards.apP(Boards.getP("dashcool") - 1, "dashcool")
            else:
                Boards.apP(0, "dashcool")



        char.x += char.xv
        char.y += char.yv
        if char.y > p.screen_height:
            #char.y = 0
            char.x = p.screen_width / 2
            char.yv = -15
        if char.x < 0:
            char.x = p.screen_width
        elif char.x > p.screen_width:
            char.x = 0

        
#Render Scene ================================================================================================================
        screen.fill(p.bg_color)

#Render Player ------------------------------------
        pyg.draw.rect(screen, p.red, (char.x, char.y, char.xl, char.yl))

#Render Platforms ---------------------------------
        for platID in range(len(scene1platforms)):
            pyg.draw.rect(screen, p.green, (scene1platforms[platID].x, scene1platforms[platID].y, scene1platforms[platID].xl, scene1platforms[platID].yl))

#Render Temporary Platform ------------------------
        if placestage > 0:
            (abs(mousepos[0]) + mousepos[0])/2
            tempx2 = mousepos[0]
            tempy2 = mousepos[1]
            
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
            pyg.draw.rect(screen, p.green, (STempx, STempy, LTempx - STempx, LTempy - STempy))


        clock.tick(p.fps)
        p.game_timer += ((1 * p.fps) / 60) / 60

inPlatScene()
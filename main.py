#Import And Initialize ===========================================================================================================
import pygame as pyg
from pickle import dump as pkd
from pickle import load as pkl
from sys import exit

pyg.init()

#Add names of files here: -----------------------------
pgplfile = 'PgPlatforms.dat'

lis = {
    "scwd": 500,
    "schi": 500,
    "bgcol": (100, 100, 255),
    "fps": 60,
}


# -----------------------------------------------------
#Setup ====================================================================================================================
#Main Functions =========================================
#Save and Load ----------------------------------------
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
            print(
                "Failed to load data: No file currently present. Creating a new one..."
            )
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


#Get Input --------------------------------------------
class PInput():
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
        "TAB": pyg.K_TAB,
        "`": pyg.K_RALT
    }

    def k(input, events, keybindlist=kbl):
        for event in events:
            if event.type == pyg.KEYDOWN:
                if event.key == keybindlist[input]:
                    return True
                else:
                    return False
            else:
                return False

    def kh(input, events):
        return events[PInput.kbl[input]]


# Boards ----------------------------------------------
class Boards():
    temp = {}
    perm = {
        "jump": False,
        "jumpbuffer": 5,
        "left": False,
        "right": False,
    }

    def apT(value, key=None):
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

    def apP(value, key=""):
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


class character():

    def __init__(self, x, y, xl, yl, xv=0, yv=0, gr=False, st=0):
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

char = character(p.screen_width / 2, 0, 10, 10)
clock = pyg.time.Clock()
start_ticks = pyg.time.get_ticks()
p1 = pyg.Rect(100, 100, 100, 100)
# - Screen init -
screen = pyg.display.set_mode((p.screen_width, p.screen_height))
pyg.display.set_caption('Platformer')

#Platforms --------------------------------------------
scene1platforms = {}

propLoc = {0: None, 100: scene1platforms}


#---------------------------------------------------------------------------------------------------------------------------
#Platforming Mode ==========================================================================================================
def inPlatScene():
    scene1platforms = {}
    placestage = 0
    mousedown = False
    p = FileManager.load('prop.dat')
    while p.SceneType == "main":
        pyg.display.flip()
        mousepos = pyg.mouse.get_pos()
        mouselist = pyg.mouse.get_pressed(num_buttons=5)
        Ev = pyg.event.get()
        Evh = pyg.key.get_pressed()

        #Input From Player =========================================================================================================
        input = ["left", "right", "jump"]
        letter = ["a", "d", "w"]
        for i in range(len(input)):
            if PInput.kh(letter[i], Evh):
                Boards.apP(True, input[i])
            else:
                Boards.apP(False, input[i])

        if PInput.k("z", Ev):
            FileManager.save(scene1platforms, pgplfile)
        if PInput.k("x", Ev):
            scene1platforms = FileManager.load(pgplfile)
        if PInput.k("c", Ev):
            scene1platforms = {}
        if PInput.k("q", Ev):
            pyg.quit()
            exit()
        if PInput.k("w", Ev):
            Boards.apP(True, "jump")
            Boards.apP(5, "jumpbuffer")
        else:
            Boards.apP(False, "jump")
            Boards.apP(0, "jumpbuffer")
        if PInput.k("a", Ev):
            Boards.apP(True, "left")
        if PInput.k("d", Ev):
            Boards.apP(True, "left")
        if PInput.k("TAB", Ev):
            p = dev.cmd()
        if PInput.k("`", Ev):
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
                    scene1platforms[len(scene1platforms)] = platform(
                        xstate, ystate, abs(tempx2 - tempx),
                        abs(tempy2 - tempy))
                    placestage = 0
                mousedown = True
        else:
            mousedown = False

#Movement/Collisions =========================================================================================================
        if char.yv < 9 and char.gr == False:
            char.yv += 1
            if char.yv > 8:
                char.yv = 8

        for i in range(len(scene1platforms)):
            if char.y + char.yl >= scene1platforms[
                    i].y and char.y + char.yl <= scene1platforms[
                        i].y + scene1platforms[i].yl:
                char.gr = True
                char.yv = 0
                char.y = scene1platforms[i].y - char.yl
            else:
                char.gr = False

        if Boards.getP('left') and not Boards.getP('right'):
            char.xv -= 1
        elif Boards.getP('right'):
            char.xv += 1
        else:
            if char.xv < -0.5:
                char.xv += 2
            elif char.xv > 0.5:
                char.xv -= 2
            else:
                char.xv = 0

        if Boards.getP("jump") and char.gr:
            print("Jump!")
            char.yv -= 15
            char.gr = False
            Boards.apP(0, "jumpbuffer")

        char.x += char.xv
        char.y += char.yv
        if char.y > 500:
            char.y = 490
            char.yv = -10
            char.x = p.screen_width/2
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
            pyg.draw.rect(
                screen, p.green,
                (scene1platforms[platID].x, scene1platforms[platID].y,
                 scene1platforms[platID].xl, scene1platforms[platID].yl))


#Render Temporary Platform ------------------------
        if placestage > 0:
            (abs(mousepos[0]) + mousepos[0]) / 2
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
            pyg.draw.rect(screen, p.green,
                          (STempx, STempy, LTempx - STempx, LTempy - STempy))

        clock.tick(p.fps)
        p.game_timer += ((1 * p.fps) / 60) / 60

inPlatScene()
"""
pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
"""

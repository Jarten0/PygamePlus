print(__name__, "Main")
import time
class BenchMark():
    start = time.perf_counter()
    laps = {}
    avgLis = []
    def lap():
        BenchMark.laps[len(BenchMark.laps)] = time.perf_counter() - BenchMark.start
    def getLap():
        print(BenchMark.laps[len(BenchMark.laps) - 1].strftime("%S:%f"))        
    def gpl():
        BenchMark.lap()
        BenchMark.getLap()
    def getavg():
        if len(BenchMark.avgLis) >= 10:
            del BenchMark.avgLis[0]
        BenchMark.avgLis.append(time.now() - BenchMark.start)
        n = time.now() - time.now()
        print("\n"*100)
        for i in range(len(BenchMark.avgLis)):
            #print(BenchMark.avgLis[i], BenchMark.laps)
            n += BenchMark.avgLis[i]
        print(n)
BenchMark.lap()
BenchMark.getLap()
#Import And Initialize ===========================================================================================================
import Scripts.EZPickle as FileManager
import Scripts.input as InputManager
import Scripts.cutsceneManager as CutsceneManager

import os
import pygame as pyg
import Scripts.dev as dev

import Scripts.platforms as platform
import Scripts.character as character

import Scripts.boards as Boards
import Scripts.defaultPropereties as defaultProperties

from Scripts.timer import Timer
from Scripts.cameramanager import Camera
from sys import exit

pyg.init()



#Add names of files here: -----------------------------
programPath = os.getcwd()
platformfilename = 'Save Data/platform info.dat'
properetiesFileName = 'Save Data/saved properties.dat'
inputsFileName = 'Save Data/input mappings.dat'

#Setup ====================================================================================================================
class Level():
    def __init__(self, name, plat, length = 200, height = 200):
        self.name = name
        self.plat = plat
        self.length = length * 20
        self.height = height * 20

def NextID(platformList) -> int:
    keylist = platformList.keys()
    #print(keylist, platformList)
    for i in range(len(platformList)):
        if not i in keylist:
            name = i
            return name
    return len(platformList)






#---------------------------------------------------------------------------------------------------------------------------
#Platforming Mode ==========================================================================================================
def drawCurrentFrame(placestage, level,mousepos, mouseposx, mouseposy, tempx, tempy, select):
    getCameraPosition()
#Render Background
    screen.fill(p.bg_color)
    drawImage(sky, 0, 0)

#Render Player ------------------------------------
    drawRect(char.color, char.x, char.y, char.xl, char.yl)
    
#Render Platforms ---------------------------------
    for platformToBeDrawn in level.plat.values():
        drawRect(platformToBeDrawn.color, platformToBeDrawn.x, platformToBeDrawn.y, platformToBeDrawn.xl, platformToBeDrawn.yl)

#Render Temporary Platform ------------------------
    if placestage > 0:
        tempPlat = dev.createTempPlat(mousepos, mouseposx, mouseposy, tempx, tempy, select)
        drawRect(tempPlat[0],tempPlat[1],tempPlat[2],tempPlat[3],tempPlat[4])
#Indicator Dot for Grid Placment
    drawRect(p.red, mouseposx - 2, mouseposy - 2, 4, 4)            
    pyg.display.flip()


def getCameraPosition():
    if Boards.getP("LEFT"):
        cam.xoffset -= 10
    elif Boards.getP("RIGHT"):
        cam.xoffset += 10
    if Boards.getP("UP"):
        cam.yoffset -= 10
    elif Boards.getP("DOWN"):
        cam.yoffset += 10

    if Boards.getP("up") or Boards.getP("down") or Boards.getP("left") or Boards.getP("right"):
        cam.xoffset = 0
        cam.yoffset = 0

    if char.x + 1 >= p.screen_width / 2 and char.x < level.length - p.screen_width / 2:
        cam.xdefault = char.x - p.screen_width / 2    
    else:
        if char.x <= p.screen_width / 2:
            cam.xdefault = 0
        else:
            cam.xdefault = level.length - p.screen_width

    if char.y +1 >= p.screen_height / 2 and char.y < level.height - p.screen_height / 2:
        cam.ydefault = char.y - p.screen_height / 2    
    else:
        if char.y < p.screen_height / 2:
            cam.ydefault = 0
        else:
            cam.ydefault = level.height - p.screen_height   
            
    cam.xpos = cam.xdefault + cam.xoffset
    cam.ypos = cam.ydefault + cam.yoffset

def drawRect(color, x, y, xl, yl):
    pyg.draw.rect(screen, color, (x - cam.xpos, y - cam.ypos, xl, yl))

def drawImage(imageObject, x, y, xOffset = 0, yOffset = 0):
    screen.blit(imageObject, (x - xOffset - cam.xpos, y - yOffset - cam.ypos))



















# ===== ===== ===== ===== =====
# =       =   =   = =   =   =
# =====   =   ===== =====   =
#     =   =   =   = = =     =
# =====   =   =   = =   =   =

def startPlatformingScene():
    global level
    global p
    global delta
    global renderframeavg
    global devMode
    devMode = False
    placestage = 0
    mousedown = False
    select = 1
    p = FileManager.load(properetiesFileName)
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

    input = FileManager.load(inputsFileName)
    if input == False:
        input = InputManager.defaultInputs
    currentInputs = {
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

    CutsceneManager.init()
    cutscenePropRefDict = {
        "char": char,
        "plat": level.plat,
        "input": currentInputs,
    }

    data = FileManager.load(platformfilename)
    if data == False:
        data = platData
    level = Level(data[100], data[100])
    tempx = 0
    tempy = 0 
















    while p.SceneType == "main":
        print("\n")
        BenchMark.getavg()

        if dev.devpause:
            textRect = p.font.get_rect()
            inputFromKeyboard = 0
            letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "BACKSPACE", "TAB"]    
            for i in range(len(input)):
                if InputManager.k(letter[i], eventsGet):
                    if letter[i] == "BACKSPACE":
                        inputFromKeyboard.pop()
                    elif letter[i] == "TAB":
                        dev.devpause = False
                    else:
                        inputFromKeyboard.append(letter[i])
            text = font.render(inputFromKeyboard, True, p.white)
            screen.blit(text, textRect)
            renderFrame(placestage, level,mousepos, mouseposx, mouseposy, tempx, tempy, select)
            pyg.display.flip()
            clock.tick(60)
            continue
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
        eventsGet = pyg.event.get()
        eventsGetHeld = pyg.key.get_pressed()
        #print(Boards.perm)











#Extra Input From Player (For dev use) =========================================================================================================
        currentInputs = {
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
        for actionToCheck in InputManager.defaultInputKeys:
            for keyToCheck in range(len(input[actionToCheck])):
                if InputManager.kh(input[actionToCheck][keyToCheck], eventsGetHeld):
                    Boards.apP(True, actionToCheck)
                    currentInputs[actionToCheck] = True
                    break
                else:
                    Boards.apP(False, actionToCheck)

        if devMode == True:
            if InputManager.k("z", eventsGet):
                platData[100] = level.plat
                FileManager.save(platData, platformfilename)
                print("Saved Platform Data")
            if InputManager.k("x", eventsGet):
                data = FileManager.load(platformfilename)
                level = Level(data[100], data[100])
            if InputManager.k("c", eventsGet):
                level.plat = {}
            if InputManager.k("q", eventsGet):
                pyg.quit()
                exit()
            if InputManager.k("r", eventsGet):
                p = defaultProperties(defaultProperties.lis)
                FileManager.save(p, properetiesFileName)
                print("Saved Propereties")        
            if InputManager.k("`", eventsGet):
                FileManager.save(p, "prop.dat")
                print("Saved Propereites")

        for i in range(10):
            if InputManager.kh(str(i), eventsGetHeld):
                select = i
                print(i)
            
        if InputManager.k("TAB", eventsGet):
            devMode = True
            # p = dev.cmd()
        
        if mouselist[0]:
            if not mousedown:
                print("Click!")
                if select == 0:
                    for platformThing in level.plat:
                        platformToBeDeleted = level.plat[platformThing]
                        if platform.collision.check(mouseposx, mouseposy, 1, 1, platformToBeDeleted.x, platformToBeDeleted.y, platformToBeDeleted.xl, platformToBeDeleted.yl)[0]:
                            del level.plat[platformThing]
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
                        if not platform.placeprop[select]["xl"] == False:
                            tempx2 = platform.placeprop[select]["xl"]
                            tempx = 0
                        if not platform.placeprop[select]["yl"] == False:
                            tempy2 = platform.placeprop[select]["yl"]
                            tempy = 0
                    if platform.placeprop[select]["#object"]:
                        level.plat[platform.NextID(level.plat)] = platform.create(mouseposx, mouseposy, tempx2, tempy2, select)
                    elif not abs(tempx2 - tempx) == 0 and not abs(tempy2 - tempy) == 0:
                        level.plat[platform.NextID(level.plat)] = platform.create(xstate, ystate, abs(tempx2 - tempx), abs(tempy2 - tempy), select)  
                    placestage = 0
                mousedown = True
        else:
            mousedown = False

















#Cutscene Handler =================================================
        for cutscene in CutsceneManager.cutsceneList.values():
            
            cutsceneStartResult = cutscene.startCheck(cutscenePropRefDict)
            
            if cutsceneStartResult is bool:
                if cutsceneStartResult:
                    CutsceneManager.cutsceneActive = True
                    cutscene.start(cutscenePropRefDict)
            
            elif cutsceneStartResult is dict:
                if cutsceneStartResult["trigger"]:
                    if platform.collision.check(char.x, char.y, char.xl, char.yl, cutsceneStartResult["triggerHitbox"]["x"], cutsceneStartResult["triggerHitbox"]["y"], cutsceneStartResult["triggerHitbox"]["xl"], cutsceneStartResult["triggerHitbox"]["yl"])[0]:
                        CutsceneManager.cutsceneActive = True
                        cutscene.start(cutscenePropRefDict)
        
        if CutsceneManager.cutsceneActive:
            cutscene = CutsceneManager.cutsceneList[CutsceneManager.cutsceneID]
            
            cutscene.update(cutscenePropRefDict)
            if cutscene.endCheck(cutscenePropRefDict):
                CutsceneManager.cutsceneActive = False
                cutscene.end(cutscenePropRefDict)









        if char.allowControl == False:
            for actionToCheck in InputManager.defaultInputKeys:
                Boards.apP(False, actionToCheck)










#Movement/Collisions =========================================================================================================
#Ideally the best course of action is to have all of the movements before
# the collisions so that the player's momentum doesn't push the character
# into the ground after the collision checks have already taken place
# leaving the character in the ground as the frame ends 

#Movement
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

#Gravity
        if Boards.getP("down"):
            char.gravity = 14
        else:
            char.gravity = 7

        if char.yv < char.gravity and char.gr == False:
            char.yv += 1 /(p.fps * delta)
        elif char.gr == False and char.yv > char.gravity + 1:
            char.yv -= 1

#Actions
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
        char.dashManager()

#Momentum to actual movement
        char.x += char.xv /( p.fps * delta)
        char.y += char.yv /( p.fps * delta)
        char.gr = False
        char.wj = False
        
#Death from void        
        if char.y > level.height:
            char.die()

        if char.x < 0:
            char.x = 0
        elif char.x > p.screen_width + level.length:
            char.x = 0
        
        
#Platform checker, uses pre-determined checking of which parts of the wall have been collided with
        
#Run functions
        for platformToBeChecked in level.plat.values():
            wallcheck = platform.collision.check(char.x, char.y, char.xl, char.yl, platformToBeChecked.x, platformToBeChecked.y, platformToBeChecked.xl, platformToBeChecked.yl)
            platform.types.functionList[platformToBeChecked.type]({
                "char": char, 
                "wallcheck": wallcheck, 
                "platformToBeChecked": platformToBeChecked, 
                "cam": cam}
                )

            
    #Render Scene ===============================================================================================================
        if renderFrame:
            drawCurrentFrame(placestage, level ,mousepos, mouseposx, mouseposy, tempx, tempy, select)
        #print(char.dashlist, Timer.get("dashleave"), Timer.getvalue("dashleave", False))

        Timer.tick()
        clock.tick(p.fps)
        
        p.game_timer += ((1 * p.fps) / 60) / 60
        p.total_ticks += 1
        delta = (((1 * p.fps) / 60) / 60) / renderframeavg 








def main():
    global p    
    global char
    global clock
    global screen
    global font
    global platData
    global sky
    global cam

    cam = Camera()
    p = FileManager.load(properetiesFileName)
    if p == False:
        p = defaultProperties(dev.lis)
    FileManager.save(p, properetiesFileName)


    char = character.create()
    font = pyg.font.Font('freesansbold.ttf', 32)
    clock = pyg.time.Clock()
    screen = pyg.display.set_mode((p.screen_width, p.screen_height))
    pyg.display.set_caption('Platformer')
    sky = pyg.image.load(programPath+r"\Assets\Images\SkyBox.png").convert()
    
    
    
    platData = {
        0: None,
    #100 - 199 are levels in the game
        100: {},
    #200 - 299 are names of the levels
        200: "Level 0",
    }
    


    startPlatformingScene()

        




if __name__ == "__main__":
    BenchMark.lap()
    BenchMark.getLap()
    main()
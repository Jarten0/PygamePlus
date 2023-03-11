#Import And Initialize ===========================================================================================================
import Scripts.EZPickle as FileManager
import Scripts.input as InputManager
import Scripts.cutsceneManager as CutsceneManager

import os
import asyncio
import time
import pygame as pyg # type: ignore
import Scripts.dev as dev

import Scripts.components as Component
import Scripts.platforms as platform
import Scripts.character as character

import Scripts.boards as Boards
import Scripts.defaultPropereties as defaultProperties
import Scripts.timer as Timer

from sys import exit
from copy import copy

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

def timeFunction(func):
    def timerWrapper():
        start = time.time()
        func()
        end = time.time()
        print(f"{func.__name__} took {start - end} seconds to run")
    return timerWrapper

def createObject(object=Component.DependencyTemplate(Component.Transform())):
    Objects[object.__name__] = object
    return object

def NextID(itemList) -> int:
    keylist = itemList.keys()
    for i in range(len(itemList)):
        if not i in keylist:
            name = i
            return name
    return len(itemList)

def renderWithDict(dictObj):
    if isinstance(dictObj["path"], type(None)):
        drawRect(dictObj["color"], dictObj["xPosition"], dictObj["yPosition"], dictObj["xLength"], dictObj["yLength"], )
        return
    try:
        drawImage(dictObj["path"], dictObj["xPosition"], dictObj["yPosition"], dictObj["xOffset"], dictObj["yOffset"])
    except FileNotFoundError as fnfe:
        drawImage(r"Assets\Images\MissingImage.png", dictObj["xPosition"], dictObj["yPosition"], dictObj["xOffset"], dictObj["yOffset"])

def renderWithObj(rendererObj):
    drawImage(rendererObj.path, rendererObj.Transform.xPosition, rendererObj.Transform.yPosition, rendererObj.xOffset, rendererObj.yOffset)

    
#---------------------------------------------------------------------------------------------------------------------------
@timeFunction
async def drawCurrentFrame(renderQueue, **kwargs):
    drawImage(sky, 0, 0)
    sortRenderQueue(renderQueue)
    getCameraPosition()
    asyncioRenderTasks = []
    for i in renderQueue:
        if isinstance(i, dict):
            asyncio.create_task(renderWithDict(i)), 
        elif isinstance(i, Component.Renderer):
            asyncio.create_task(renderWithObj(i)), 
        else:
            print(f"RenderQueue: {i} does not have a function for rendering and thus failed to render.")
    done, pending = await asyncio.wait(asyncioTasks)

    pyg.display.flip()

def sortRenderQueue(renderQueue) -> dict:
    tempRenderQueue = []
    returnedRenderQueue = {}
    for i in renderQueue:
        tempRenderQueue.append((renderQueue[i].tier, renderQueue[i].Transform.zPosition, renderQueue[i]))
    tempRenderQueue.sort()
    for i in tempRenderQueue:
        tier, zPosition, value = i
        returnedRenderQueue[tempRenderQueue.index(i)] = value
    return returnedRenderQueue


def getCameraPosition(cam):
    if Boards.getP("LEFT"):
        cam.xOffset -= 10
    elif Boards.getP("RIGHT"):
        cam.xOffset += 10
    if Boards.getP("UP"):
        cam.yOffset -= 10
    elif Boards.getP("DOWN"):
        cam.yOffset += 10

    if Boards.getP("up") or Boards.getP("down") or Boards.getP("left") or Boards.getP("right"):
        cam.xOffset = 0
        cam.yOffset = 0

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
            
    cam.xpos = cam.xdefault + cam.xOffset
    cam.ypos = cam.ydefault + cam.yOffset

def drawRect(color, x, y, xl, yl):
    pyg.draw.rect(screen, color, (x - cam.xpos, y - cam.ypos, xl, yl))

def drawImage(imageObject, x, y, xOffset = 0, yOffset = 0):
    screen.blit(imageObject, (x - xOffset - cam.xpos, y - yOffset - cam.ypos))

#---------------------------------------------------------------------------------------------------------------------------
@timeFunction
def startPlatformingScene() -> str:
    devMode = False
    placestage = 0
    select = 1

    #Initialize several timers 
    for i in { ("dashcool", 20, False), ("grace", 0, True),
("CoyoteTime", 0, True), ("dash", 0, False), ("dashleave", 4, False)}:
        (name, value, up) = i
        Timer.set(name, value, up)
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

    p = FileManager.load(properetiesFileName)
    level = Level("Level 0", platData[100], 500, 500)
    data = FileManager.load(platformfilename)
    if data == False:
        data = platData
    level = Level(data[100], data[100])

    Mouse.tempx = 0
    Mouse.tempy = 0 
    Mouse.down = False

async def platformingTick():
    print("\n")

    if dev.devpause:
        textRect = p.font.get_rect()
        inputFromKeyboard = ''
        letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "BACKSPACE", "TAB"]    
        for i in range(len(input)):
            if InputManager.k(letter[i], eventsGet):
                if letter[i] == "BACKSPACE":
                    inputFromKeyboard.pop()
                elif letter[i] == "TAB":
                    dev.devpause = False
                else:
                    inputFromKeyboard.join(letter[i])
        text = font.render(inputFromKeyboard, True, p.white)
        screen.blit(text, textRect)
        pyg.display.flip()
        clock.tick(60)
        return "freezeframe"
    renderframeavg = p.fps / p.renderfps

    if fREEZEFRAMES > 0:
        fREEZEFRAMES -= 1
        pyg.display.flip()
        clock.tick(p.fps)
        return "early"

    Mouse.pos = pyg.mouse.get_pos()
    Mouse.pos = (Mouse.pos[0] + cam.xpos, Mouse.pos[1] + cam.ypos)
    Mouse.posx = round((Mouse.pos[0]/p.grid), 0)*p.grid
    Mouse.posy = round((Mouse.pos[1]/p.grid), 0)*p.grid
    Mouse.list = pyg.mouse.get_pressed(num_buttons=5)


#Extra Input From Player (For dev use) =========================================================================================================

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
    
    if Mouse.list[0]:
        if not Mouse.down:
            print("Click!")
            if select == 0:
                for platformThing in level.plat:
                    platformToBeDeleted = level.plat[platformThing]
                    if platform.collision.check(Mouse.posx, Mouse.posy, 1, 1, platformToBeDeleted.x, platformToBeDeleted.y, platformToBeDeleted.xl, platformToBeDeleted.yl)[0]:
                        del level.plat[platformThing]
                        break
            
            elif placestage == 0:
                placestage = 1
                Mouse.tempx = Mouse.posx
                Mouse.tempy = Mouse.posy
                print(f"({Mouse.tempx}, {Mouse.tempy})")
                
            
            elif placestage == 1:
                Mouse.tempx2 = Mouse.posx
                Mouse.tempy2 = Mouse.posy
                if Mouse.tempx > Mouse.tempx2:
                    Mouse.xstate = Mouse.tempx2
                else:
                    Mouse.xstate = Mouse.tempx
                if Mouse.tempy > Mouse.tempy2:
                    Mouse.ystate = Mouse.tempy2
                else:
                    Mouse.ystate = Mouse.tempy
                
                if platform.placeprop[select]["#HasPlaceReq"]:
                    if not platform.placeprop[select]["xl"] == False:
                        Mouse.tempx2 = platform.placeprop[select]["xl"]
                        Mouse.tempx = 0
                    if not platform.placeprop[select]["yl"] == False:
                        Mouse.tempy2 = platform.placeprop[select]["yl"]
                        Mouse.tempy = 0
                if platform.placeprop[select]["#object"]:
                    level.plat[platform.NextID(level.plat)] = platform.create(Mouse.posx, Mouse.posy, Mouse.tempx2, Mouse.tempy2, select)
                elif not abs(Mouse.tempx2 - Mouse.tempx) == 0 and not abs(Mouse.tempy2 - Mouse.tempy) == 0:
                    level.plat[platform.NextID(level.plat)] = platform.create(Mouse.xstate, Mouse.ystate, abs(Mouse.tempx2 - Mouse.tempx), abs(Mouse.tempy2 - Mouse.tempy), select)  
                placestage = 0
            Mouse.down = True
    
    else:
        Mouse.down = False

#Component Handler
    for objectToRender in Objects:
        if Component.Renderer in dir(objectToRender):
            renderQueue[str(objectToRender)] = objectToRender.Renderer

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

    for platformToBeChecked in level.plat.values():
        wallcheck = platform.collision.check(char.x, char.y, char.xl, char.yl, platformToBeChecked.x, platformToBeChecked.y, platformToBeChecked.xl, platformToBeChecked.yl)
        platform.types.functionList[platformToBeChecked.type]({
            "char": char, 
            "wallcheck": wallcheck, 
            "platformToBeChecked": platformToBeChecked, 
            "cam": cam}
            )

        
#Render Scene ===============================================================================================================
    #if renderFrame:
    #     drawCurrentFrame({}, placestage, level ,Mouse.pos, Mouse.posx, Mouse.posy, Mouse.tempx, Mouse.tempy, select)
    #print(char.dashlist, Timer.get("dashleave"), Timer.getvalue("dashleave", False))

    Timer.tick()
    clock.tick(p.fps)
    
    p.game_timer += ((1 * p.fps) / 60) / 60
    p.total_ticks += 1
    delta = (((1 * p.fps) / 60) / 60) / renderframeavg 

#---------------------------------------------------------------------------------------------------------------------------
async def main():
    global p, char, clock, screen, font, platData, sky, cam, Mouse, \
    fREEZEFRAMES, level, p,delta, devMode, input, currentInputs, cutscenePropRefDict
    
    pyg.init()
    cam = Component.Camera()
    p = FileManager.load(properetiesFileName)
    if p == False:
        p = defaultProperties(dev.lis)
    FileManager.save(p, properetiesFileName)

    Mouse = None
    char = character.create()
    font = pyg.font.Font('freesansbold.ttf', 32)
    clock = pyg.time.Clock()
    screen = pyg.display.set_mode((p.screen_width, p.screen_height))
    pyg.display.set_caption('Platformer')
    sky = pyg.image.load(programPath+r"\Assets\Images\SkyBox.png").convert()
    

    Objects = {}

    Character = createObject(Component.DependenciesTemplate(
        ConfigData=Component.ConfigData(
            filename = r".\ConfigFiles\CharacterProperties.toml",
            filetype = "toml",
            ),
        Transform=Component.Transform(
            xPosition=ConfigData.configFile["body"]["xpos"],
            yPosition=ConfigData.configFile["body"]["ypos"],
            zPosition=ConfigData.configFile["body"]["zpos"],
            ),
        Renderer=Component.Renderer(
            xOffset=0,
            yOffset=0,
            xLength=20,
            yLength=20,
            path=r"Assets\Images\hehe.png",
            tier=5,
            ),
        Collider=Component.Collider(
            xLength = 20,
            yLength = 20,
            Objects = Objects,
            ),
        RigidBody=Component.Rigidbody(
            mass=5,
            ),
        Character=Component.Character(
            ConfigData=ConfigData,
            Transform=Transform,
            ),
        )
    )
    
    platData = {
        0: None,
    #100 - 199 are levels in the game
        100: {},
    #200 - 299 are names of the levels
        200: "Level 0",
    }




    global renderQueue
    renderQueue = {    }

    startPlatformingScene()
    #Run physics 20 times per second

    while True:
        asyncioTasks = [
            asyncio.create_task(platformingTick()), 
            asyncio.create_task(drawCurrentFrame(copy(renderQueue)))]
        done, pending = await asyncio.wait(asyncioTasks)
        for task in done:
            if not task.result() == None:
                print(
                    "Done:", done, "\n",
                    "Result:", task.result(), "\n",
                    )
        clock.tick(60)
        
if __name__ == "__main__":
    asyncio.run(main())
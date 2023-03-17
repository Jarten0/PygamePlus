print("\n" * 10)
#Import And Initialize ===========================================================================================================
import Scripts.EZPickle as FileManager
import Scripts.input as InputManager
import Scripts.cutsceneManager as CutsceneManager
import Scripts.componentManager as ComponentManager

import os
import asyncio
import time
import pygame as pyg # type: ignore
import Scripts.dev as dev

import Scripts.Components.character as CharacterComponent
import Scripts.Components.components as MainComponent 
import Scripts.platforms as platform

import Scripts.boards as Boards
import Scripts.timer as Timer

from sys import exit
from copy import copy

programPath = os.getcwd()

Settings = FileManager.load('\ConfigFiles\settings.toml', 'toml')
if isinstance(Settings, bool):
    raise Exception('Critical file missing!: \ConfigFiles\settings.toml')
LogInConsole = Settings['LogInConsole']

#Setup ====================================================================================================================
class Level():
    def __init__(self, name, plat, length = 200, height = 200):
        self.name = name
        self.plat = plat
        self.length = length * 20
        self.height = height * 20

def timeFunction(func):
    def timerWrapper() -> None:
        start = time.time()
        func()
        end = time.time()
        print(f"{func.__name__} took {start - end} seconds to run")
    return timerWrapper

def NextID(itemList) -> int:
    keylist = itemList.keys()
    for i in range(len(itemList)):
        if not i in keylist:
            name = i
            return name
    return len(itemList)

def createObject(name="") -> MainComponent.Template: #type: ignore
    if name == "" or name in Objects:
        name = NextID(Objects)
    object = MainComponent.Template()
    Objects[name] = object #type: ignore
    return object

def createComplexObject(name, *args, **kwargs) -> MainComponent.DependenciesTemplate:
    object = MainComponent.DependenciesTemplate(*args, **kwargs) # type: ignore
    Objects[name.__name__] = object
    return object

#---------------------------------------------------------------------------------------------------------------------------
@timeFunction
async def drawCurrentFrame(renderQueue, **kwargs) -> None:
    
    sortRenderQueue(renderQueue)
    
    asyncioRenderTasks = []
    
    drawImage(sky, x=0, y=0, xOffset=0, yOffset=0)

    for i in renderQueue:
        if isinstance(i, dict):
            asyncioRenderTasks [ NextID(asyncioRenderTasks) ] = asyncio.create_task( renderWithDict(i) )
        elif isinstance(i, MainComponent.Renderer):
            asyncioRenderTasks [ NextID(asyncioRenderTasks) ] = asyncio.create_task( renderWithObj(i)  ) 
        else:
            print(f"RenderQueue: {i} does not have a function for rendering and thus failed to render.")
    
    await asyncio.wait(asyncioRenderTasks)
    
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

async def renderWithDict(dictObj) -> None:
    if isinstance(dictObj["path"], type(None)):
        drawRect(dictObj["color"], dictObj["xPosition"], dictObj["yPosition"], dictObj["xLength"], dictObj["yLength"], )
        return
    try:
        drawImage(dictObj["path"], dictObj["xPosition"], dictObj["yPosition"], dictObj["xOffset"], dictObj["yOffset"])
    except FileNotFoundError as fnfe:
        drawImage(r"Assets\Images\MissingImage.png", dictObj["xPosition"], dictObj["yPosition"], dictObj["xOffset"], dictObj["yOffset"])

async def renderWithObj(rendererObj) -> None:
    drawImage(rendererObj.path, rendererObj.Transform.xPosition, rendererObj.Transform.yPosition, rendererObj.xOffset, rendererObj.yOffset
    rendererObj.alpha)

def drawRect(color, x, y, xl, yl):
    pyg.draw.rect(screen, color, (x - Camera.xpos, y - Camera.ypos, xl, yl))

def drawImage(imageObject, x, y, xOffset = 0, yOffset = 0, alpha=0):
    screen.blit(imageObject, (x - xOffset - Camera.xpos, y - yOffset - Camera.ypos), special_flags=)

#---------------------------------------------------------------------------------------------------------------------------
@timeFunction
def startPlatformingScene() -> str:
    devMode = False
    
    for i in { ("dashcool", 20, False), ("grace", 0, True),
        ("CoyoteTime", 0, True), ("dash", 0, False), ("dashleave", 4, False)}:
        (name, value, up) = i
        Timer.set(name, value, up)
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

    ComponentManager.init()

    CutsceneManager.init()
    settings = FileManager.load('ConfigFiles\settings.toml', type="toml")
    level = Level("Level 0", platData[100], 500, 500)
    data = FileManager.load('Save Data\platform info.dat')
    if data == False:
        data = platData
    level = Level(data[100], data[100])

    Mouse.placestage = 0
    Mouse.select = 1
    Mouse.tempx = 0
    Mouse.tempy = 0 
    Mouse.down = False
    return "Done"

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

    if fREEZEFRAMES > 0:
        fREEZEFRAMES -= 1
        return "early"

    Mouse.pos = pyg.mouse.get_pos()
    Mouse.pos = (Mouse.pos[0] + Camera.xpos, Mouse.pos[1] + Camera.ypos)
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
            settings= defaultProperties(defaultProperties.lis)
            FileManager.save(p, properetiesFileName)
            print("Saved Propereties")        
        if InputManager.k("`", eventsGet):
            FileManager.save(p, "prop.dat")
            print("Saved Propereites")

    for i in range(10):
        if InputManager.keyDownHeld(str(i), eventsGetHeld):
            select = i
            print(i)
        
    if InputManager.k("TAB", eventsGet):
        devMode = True
        # settings= dev.cmd()
    
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
        if MainComponent.Renderer in dir(objectToRender):
            renderQueue[str(objectToRender)] = objectToRender.Renderer

    for obj in Object.values():
        obj.update()
    


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



    Timer.tick()
    clock.tick(p.fps)
    
    p.game_timer += ((1 * p.fps) / 60) / 60
    p.total_ticks += 1
    delta = (((1 * p.fps) / 60) / 60) / renderframeavg 

#---------------------------------------------------------------------------------------------------------------------------
async def main():
    global settings, clock, screen, font, platData, sky, Camera, Mouse, Objects, LogInConsole, \
    fREEZEFRAMES, level, p, delta, devMode, input, currentInputs, \
    Character
    
    pyg.init()

    Objects = {}


    Camera = createObject(MainComponent.Camera())
    settings= FileManager.load('\ConfigFiles\settings.toml', 'toml')
    
    FileManager.save(p, properetiesFileName)

    Mouse = createObject()
    font = pyg.font.Font('freesansbold.ttf', 32)
    clock = pyg.time.Clock()
    screen = pyg.display.set_mode((p.screen_width, p.screen_height))
    pyg.display.set_caption('Platformer')
    sky = createObject()
    sky = createComplexObject()
    sky.surface = pyg.image.load(programPath+'\Assets\Images\SkyBox.png').convert()


    
    print("HeHa!")

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
            asyncio.create_task(drawCurrentFrame(copy(renderQueue)))]     # type: ignore
        done, pending = await asyncio.wait(asyncioTasks)
        for task in done:
            if not task.result() == None:
                print(
                    "Done:", done, "\n",
                    "Result:", task.result(), "\n",
                    )
        clock.tick(60)
        
if __name__ == "__main__":
    print("\n"*3)
    asyncio.run(main())
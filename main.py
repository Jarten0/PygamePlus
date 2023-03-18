if __name__ == "__main__":
    LogInConsole = True
    print("\n" * 10)

#Import And Initialize ===========================================================================================================
import os
import asyncio
import time

import Scripts.EZPickle as FileManager
import Scripts.input as InputManager
import Scripts.cutsceneManager as CutsceneManager
import Scripts.componentManager as ComponentManager

import pygame as pyg # type: ignore
import Scripts.dev as dev


import Scripts.Components.character as CharacterComponent
import Scripts.Components.components as MainComponent 
import Scripts.Components.camera as CameraComponent
import Scripts.platforms as platform

import Scripts.boards as Boards
import Scripts.timer as Timer

from sys import exit
from copy import copy

#Setup ====================================================================================================================
def timeFunction(func):
    def timerWrapper() -> None:
        start = time.time()
        func()
        end = time.time()
        print(f"{func.__name__} took {start - end} seconds to run")
    timerWrapper.__name__ = func.__name__
    return timerWrapper

def NextID(itemList:dict, name:str='') -> str:
    keylist = itemList.keys()
    for i in range(len(itemList)):
        if not name+str(i) in keylist:
            return name+str(i)
    return name+str(len(itemList))

def createObject(
name:str | int = "", 
class_:type = MainComponent.Template, 
*args, **kwargs) -> object:

    condition = 'create__' in dir(class_)
    print("CCC", class_, condition, dir(class_))
    if condition:
        object, name = class_.create__(*args, **kwargs) #type: ignore
    else:
        print("Success?", class_.__name__, args, kwargs)
        object = class_(*args, **kwargs)
        print("Yes?")
    if name == "" or name in Objects:
        name = NextID(Objects, 'New Object')
    Objects[name] = object
    return object

def createComplexObject(
name:str = '', 
class_:type = MainComponent.DependenciesTemplate, 
*args, **kwargs) ->  type | bool:
    print("Creating Complex Object: ", class_)
    object = class_(*args, **kwargs)
    if not isinstance(object, class_):
        return False
    Objects[name] = object
    return object

async def loadingScreen():
    loadingImage = pyg.image.load(programPath+'\\Assets\\Images\\loading.png').convert()
    while readyToGo == False:
        screen.blit(source=loadingImage, 
        dest=(10, 10))
        clock.tick(50)
#---------------------------------------------------------------------------------------------------------------------------
@timeFunction
async def drawCurrentFrame(renderQueue, **kwargs) -> None:
    
    sortRenderQueue(renderQueue)
    
    asyncioRenderTasks = {}
    
    drawImage(sky.surface, x=0, y=0, xOffset=0, yOffset=0)

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
    if not 'image' in dictObj \
        and 'path' in dictObj:
        
        try:
            dictObj['image'] = pyg.image.load(dictObj['path'])
        except FileNotFoundError as fnfe:
            dictObj['image'] = missingImage
    
    if not 'path' in dictObj:
        drawRect(dictObj["color"], dictObj["xPosition"], dictObj["yPosition"], dictObj["xLength"], dictObj["yLength"], )
        return
    
    drawImage(dictObj['image'], dictObj["xPosition"], dictObj["yPosition"], dictObj["xOffset"], dictObj["yOffset"])
        
async def renderWithObj(rendererObj) -> None:
    drawImage(rendererObj.surface, rendererObj.Transform.xPosition, rendererObj.Transform.yPosition, rendererObj.xOffset, rendererObj.yOffset,
    )

def drawRect(color: tuple[int, int, int], x: float|int, y: float|int, xl: float|int, yl: float|int) -> None:
    pyg.draw.rect(screen, color, (int(x) - int(Camera.xpos), int(y) - int(Camera.ypos), int(xl), int(yl)))

def drawImage(imageObject:pyg.Surface, x:int|float = 0, y:int|float = 0, xOffset:int|float = 0, yOffset:int|float = 0, alpha:int|float = 0) -> None:
    if 'Camera' in Objects:
        Camera = Objects['Camera']
    else:
        raise Exception("Camera object is not initialized! Render failed.")
    screen.blit(source=imageObject, dest=(int(x) - int(xOffset) - Camera.xpos, int(y) - int(yOffset) - Camera.ypos))

#---------------------------------------------------------------------------------------------------------------------------
@timeFunction
def startPlatformingScene() -> str:
    global fREEZEFRAMES, level, devMode, input, currentInputs, sky, \
    Settings, Character, Camera, renderQueue, missingImage, Mouse, font, \
    input, Objects, UpdateObjects




    devMode = False


    print("Not stuck!")
    Objects = {}
    UpdateObjects = {}
    renderQueue = {}

    
    Character = createObject("Character", CharacterComponent.Character)
    print("Camera.")
    Camera = createObject("Camera", CameraComponent.Camera)

    print("Here")

    missingImage = pyg.image.load(programPath+"\\Assets\\Images\\MissingImage.png").convert()
    print("There")

    Mouse = createObject('Mouse', MainComponent.Mouse)
    print("aha!")
    font = pyg.font.Font('freesansbold.ttf', 32)
    print("Everywhere")

    sky = createObject\
    (
    'sky', 
        MainComponent.Renderer \
        ( 
            surface = pyg.image.load \
            (
                programPath+'\\Assets\\Images\\SkyBox.png'
            ).convert()
        )               #type: ignore
    )

    platData = {
        0: None,
    #100 - 199 are levels in the game
        100: {},
    #200 - 299 are names of the levels
        200: "Level 0",
    }


    
    #Just initialize all the timers that need it
    for i in { ("dashcool", 20, False), ("grace", 0, True),
        ("CoyoteTime", 0, True), ("dash", 0, False), ("dashleave", 4, False)}:
        (name, value, up) = i
        Timer.set(name, value, up)
    fREEZEFRAMES = 0

    
    input = FileManager.load(programPath+"\\Save Data\\input mappings.dat")
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

    

    ComponentManager._init()
    CutsceneManager.init()
    Settings = FileManager.load('ConfigFiles\settings.toml', type="toml")
    level = Level("Level 0", platData[100], 500, 500)
    data = FileManager.load('Save Data\platform info.dat')
    if data == False:
        data = platData
    level = Level(name=data[100], plat=data[100], length=20000, height=20000)

    
    #Add all objects with update__ functions to main
    for i in Objects:
        if 'update__' in dir(Objects[i]):
            UpdateObjects[i] = Objects[i]
    
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
        return "devpause"

    if fREEZEFRAMES > 0:
        fREEZEFRAMES -= 1
        return "freezeFrame"

    


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

    for obj in UpdateObjects.values():
        obj.update__()
    




    Timer.tick()
    
    Settings['gameTimer' ] += 1 / 60 # type: ignore
    Settings['totalTicks'] += 1  # type: ignore

    return 'complete'

#---------------------------------------------------------------------------------------------------------------------------
async def main():
    global Settings, clock, screen, LogInConsole, programPath, readyToGo

    programPath = os.getcwd()
    Settings = FileManager.load(programPath+"\\ConfigFiles\\settings.toml", 'toml')
    if isinstance(Settings, bool):
        raise Exception('Critical file missing!: \\ConfigFiles\\settings.toml')
    LogInConsole = Settings['LogInConsole']
    
    pyg.init()
    screen = pyg.display.set_mode((Settings["Screen"]["screen_width"], Settings["Screen"]["screen_height"]))
    pyg.display.set_icon(pyg.image.load(programPath+"\\Assets\\Images\\loading.png").convert())
    pyg.display.set_caption('Platformer')

    clock = pyg.time.Clock()
    readyToGo = False



    #Activate Loading screen
    # asyncioTasks = [asyncio.create_task(loadingScreen())] 

    

    startPlatformingScene()
    
    print("Did we make it?")

    #Leave loading screen
    readyToGo = True
    # await asyncio.wait(asyncioTasks)

    print("We did?!")

    #Run physics 60 times per second
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
    
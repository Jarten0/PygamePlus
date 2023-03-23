if __name__ == "__main__": LogInConsole_ = True; print("\n" * 10)
else: raise ImportError("You cannot import main! do 'from main import *' to get main interfaces.")

#Import And Initialize ===========================================================================================================
import os
import asyncio
import time

from Scripts.EZPickle import FileManager
import Scripts.cutsceneManager as CutsceneManager
import Scripts.componentManager as ComponentManager

import pygame as pyg # type: ignore
import Scripts.dev as dev


import Scripts.Components.character as CharacterComponent
import Scripts.Components.components as MainComponent 
import Scripts.Components.camera as CameraComponent
import Scripts.platforms as platform

from Scripts.boards     import  Boards
from Scripts.timer      import  Timer
from Scripts.inputMapper import Input


from sys import exit
from copy import copy, deepcopy

#Setup ====================================================================================================================
def logFunc(func):
    def wrapper(*args, **kwargs):
        print(f"""LOGFUNC: 
funcName: {func.__name__}
funcStr : {func.__str__()}
funcArgs: {args, kwargs}
""")
        func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

def timeFunction(func):
    def timerWrapper(*args2, **kwargs2) -> None:
        start = time.time()
        func(*args2, **kwargs2)
        end = time.time()
        print(f"{func.__name__} took {start - end} seconds to run")
    timerWrapper.__name__ = func.__name__
    return timerWrapper

def NextID(itemList:dict, name:str|int='') -> str:
    name = str(name)
    keylist = itemList.keys()
    for i in range(len(itemList)):
        if not name+str(i) in keylist:
            return name+str(i)
    return name+str(len(itemList))    

def _newComponent(_class:type = MainComponent.Transform, *args, **kwargs) -> object:
    """Creates a component instance using its built in initializer

\n  Input the components class from its module by using Component.get statments
  and feed it into the _class argument

\n  The component it returns will NOT be stored elsewhere, so make sure you assign it to a variable
  or use it right away

\n  You can also leave _class blank to get a new simple Transform component.
\n  If the component has any dependencies, make sure you feed them
  in as keyword arguments. 

\n  Example use case:

\n  from main import *       #imports the Component interface
\n<...component initiation...>
\ndef create__()
\n  transformComponent= Component.new()         #empty parenthesis creates a transform component by default
\n  colliderComponent = Component.new(Component.get('Collider'), xLength)      #you can either use Component.get('componentName') or
simply type in the string. Any keywords will also go directly to the object's initializer

\n  rigidBodyComponent = Component.new(Component.get('RigidBody'),
\n\t  Transform= transformComponent,
\n\t  Collider = colliderComponent, 
    \t)
\n)

\n  SquareObject = Object.new() 
"""
    return _class(*args, **kwargs)

def _getComponent(_name:int|str) -> type:
    """Fetches a class using a name or the component's ID.
    Returns the class so you can initialize it or set attributes
    Example"""
    if isinstance(_name, str):
        _ID = _ComponentNames[_name]
    component = _Components[_ID]
    return component

def _newObject(
name_:str | int | None = None, 
class_:type = MainComponent.DependenciesTemplate, 
*args, **kwargs) -> object:
    """Takes in a name and optionally a class/component and returns an instance of it. \n
    If the class/component has a create__() function it will automatically detect it and 
    attempt to use it to create the object. Otherwise, it will rely on the class's initialize function. \n
    You can also feed in args/keyword args that will go directly to the component's initializer"""


    if name_ == None or name_ in _Objects:
        name_ = NextID(_Objects, 'New Object')

    if 'create__' in dir(class_):
        try:
            createdObject:object = class_.create__(*args, **kwargs) #type: ignore
        except:
            print("\n\n!!!!!!!!!!\n", class_.__name__, " create__ error: Something went wrong, go fix it.\n", sep='')
            raise
        if not isinstance(createdObject, class_):
            raise Exception(f"{dir(class_), args, kwargs}\n\n\nError?? {createdObject, class_.__name__} had an issue. It should only return an object. Check to see if its ")
        _Objects[name_] = createdObject
    
        return createdObject

    else:
        return _createFromTemplate(name=name_, class_=class_, *args, **kwargs)

def _getObject(name) -> object|None:
    """Finds an object via it's name\n
    If no such object exists, returns None."""
    if name in _Objects: return _Objects[name]
    else: return None

def _returnObjects():
    return _Objects

def _createFromTemplate(name:str|int="", 
        class_:type=MainComponent.DependenciesTemplate,
        *args, **kwargs) -> object:
    """Used to initialize a simple object"""
    if name == "" or name in _Objects:
        if name == "":
            NextID(_Objects, 'New Object') 
        else:
            NextID(_Objects, name=name)
    object_:object = class_(*args, **kwargs)
    _Objects[name] = object_
    return object_

def _createSpecialObject(
    name:str = '', 
    class_:type = MainComponent.DependenciesTemplate, 
    *args, **kwargs) -> object:
    """ Used by components and 
    Takes in a name and a class and returns an instance of that object
    while also adding it to the Objects dictionary. You can also input arguments and
    keyword arguments if the object's initialize function uses them. 
    If the init function returns something other than the instance it will raise a default 
    Exception in order to prevent wrong types from leaking. """
    print("Creating Complex Object: ", class_)
    object_:object = class_(*args, **kwargs)
    if not isinstance(object, class_):
        raise Exception("He")
    _Objects[name] = object_
    return object_

async def _loadingScreen() -> None:
    """Manually displays a loading screen to keep busy while the game starts up"""
    loadingImage = pyg.image.load(programPath+'\\Assets\\Images\\loading.png')
    state = 0
    while _readyToGo == False:
        _Screen.fill((0,0,0))
        _Screen.blit(source=loadingImage, dest=(10, 10), area=pyg.Rect(state*64, 0, 64, 64))
        pyg.display.flip()
        _Clock.tick(24)
        state += 1
        if state >= 8:
            state = 0

@timeFunction
async def _drawCurrentFrame(renderQueue:dict) -> None:
    
    renderQueue = _sortRenderQueue(renderQueue)
    
    asyncioRenderTasks = {}
    
    
    for i in reversed(renderQueue):
        if isinstance(i, MainComponent.Renderer):
            asyncioRenderTasks [ NextID(asyncioRenderTasks) ] = asyncio.create_task( _renderWithObj(i)  ) 
        elif isinstance(i, dict):
            asyncioRenderTasks [ NextID(asyncioRenderTasks) ] = asyncio.create_task( _renderWithDict(i) )
        else:
            print(f"RenderQueue: {i.__name__} does not have a function for rendering and thus failed to render.")
    
    await asyncio.wait(asyncioRenderTasks)
    pyg.display.flip()

def _sortRenderQueue(renderQueue: dict[str, MainComponent.Renderer]) -> dict:
    """Takes a dict and for each item takes each objects tier, zPosition, and self and sorts the dictionary using those values
    in priority of tier>zposition>object"""
    tempRenderQueue = []
    returnedRenderQueue = {}

    for i in renderQueue:
        tempRenderQueue.append((renderQueue[i].tier, renderQueue[i].Transform.zPosition, renderQueue[i]))
    tempRenderQueue.sort()
    
    for i in tempRenderQueue:
        _, _, value = i
        returnedRenderQueue[tempRenderQueue.index(i)] = value

    return returnedRenderQueue

async def _renderWithDict(dictObj:dict) -> None:
    if not 'image' in dictObj \
        and 'path' in dictObj:
        
        try:
            dictObj['image'] = pyg.image.load(dictObj['path'])
        except FileNotFoundError as fnfe:
            dictObj['image'] = missingImage
    
    if not 'path' in dictObj:
        _drawRect(dictObj["color"], dictObj["xPosition"], dictObj["yPosition"], dictObj["xLength"], dictObj["yLength"], )
        return
    
    _drawImage(dictObj['image'], dictObj["xPosition"], dictObj["yPosition"], dictObj["xOffset"], dictObj["yOffset"])
        
async def _renderWithObj(rendererObj:object) -> None:
    _drawImage(rendererObj.surface, rendererObj.Transform.xPosition, rendererObj.Transform.yPosition, rendererObj.xOffset, rendererObj.yOffset,
    )

def _drawRect(color: tuple[int, int, int], x: float|int, y: float|int, xl: float|int, yl: float|int) -> None:
    pyg.draw.rect(_Screen, color, (int(x) - int(Camera.Transform.xPosition), int(y) - int(Camera.Transform.yPosition), int(xl), int(yl)))

def _drawImage(imageObject:pyg.Surface, x:int|float = 0, y:int|float = 0, xOffset:int|float = 0, yOffset:int|float = 0, alpha:int|float = 0) -> None:
    
    if 'Camera' in _Objects:
        Camera = _Objects['Camera']
    else:
        raise Exception("Camera object is not initialized! Render failed.")
    _Screen.blit(source=imageObject, dest=(int(x) - int(xOffset) - Camera.xpos, int(y) - int(yOffset) - Camera.ypos))

@timeFunction
def _startPlatformingScene() -> str:
    global fREEZEFRAMES, level, devMode, sky, \
    Settings, Character, Camera, missingImage, Mouse, font

    devMode = False
    ComponentManager._init()
    CutsceneManager.init()


    Character = _newObject(name_="Character", class_=Component.get('Character'))

    missingImage = pyg.image.load(programPath+"\\Assets\\Images\\MissingImage.png").convert()

    Mouse = _newObject('Mouse', MainComponent.Mouse)
    font = pyg.font.Font('freesansbold.ttf', 32)
    sky = _newObject('sky', 
        Component.new('Renderer', 
            tier = 99,
            zPosition=99,
            surface = pyg.image.load(
                programPath+'\\Assets\\Images\\SkyBox.png'
            ).convert()   )   )

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

    

    

    Settings = FileManager.load('ConfigFiles\settings.toml', type="toml")
    level = Level("Level 0", platData[100], 500, 500)
    data = FileManager.load('Save Data\platform info.dat')
    if data == False:
        data = platData
    level = Level(name=data[100], plat=data[100], length=20000, height=20000)

    
    #Add all objects with update__ functions to main
    for i in _Objects:
        if 'update__' in dir(_Objects[i]):
            _UpdateObjects[i] = _Objects[i]
    
    return "Done"

async def _platformingTick():
    print("\n")

    if dev.devpause:
        textRect = p.font.get_rect()
        inputFromKeyboard = ''
        letter = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", 
            "BACKSPACE", "TAB"]    
        for i in range(len(input)):
            if InputManager.k(letter[i], eventsGet):
                if letter[i] == "BACKSPACE":
                    inputFromKeyboard.pop()
                elif letter[i] == "TAB":
                    dev.devpause = False
                else:
                    inputFromKeyboard.join(letter[i])
        text = font.render(inputFromKeyboard, True, p.white)
        _Screen.blit(text, textRect)
        pyg.display.flip()
        _Clock.tick(60)
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
    for objectToRender in _Objects:
        if MainComponent.Renderer in dir(objectToRender):
            _renderQueue[str(objectToRender)] = objectToRender.Renderer

    for obj in _UpdateObjects.values():
        obj.update__()
    




    Timer.tick()
    _Clock.tick(60)
    
    Settings['gameTimer' ] += 1 / 60 # type: ignore
    Settings['totalTicks'] += 1  # type: ignore

    return 'complete'

#---------------------------------------------------------------------------------------------------------------------------
async def _main():

    programPath = os.getcwd()
    
    Settings:dict = FileManager.load(programPath+"\\ConfigFiles\\settings.toml", 'toml')
    if isinstance(Settings, bool): raise Exception('Critical file missing!: \\ConfigFiles\\settings.toml')
    LogInConsole_ = Settings['LogInConsole']
    
    pyg.init()

    _Screen = pyg.display.set_mode((Settings["Screen"]["screen_width"], Settings["Screen"]["screen_height"]))
    pyg.display.set_icon(pyg.image.load(programPath+"\\Assets\\Images\\loading.png").convert())
    pyg.display.set_caption('Platformer')

    _Clock = pyg.time.Clock()
    _readyToGo = False



    #Activate Loading screen
    asyncioTasks = [asyncio.create_task(_loadingScreen())] 
    

    print("Hiya")
    _startPlatformingScene()
    
    print("Did we make it?")

    #Leave loading screen
    _Clock.tick(0.2)
    _readyToGo = True
    await asyncio.wait(asyncioTasks)

    print("We did?!")

    #Run physics 60 times per second
    while True:
        asyncioTasks = [
            asyncio.create_task(_platformingTick()), 
            asyncio.create_task(_drawCurrentFrame(deepcopy(_renderQueue)))]     
        done, pending = await asyncio.wait(asyncioTasks)

_Objects: dict[str|int, object] = {}
_UpdateObjects: dict[str|int, object] = {}
_renderQueue: dict[str|int, object|dict] = {}
_Components: dict[int, object] = {}
_ComponentNames: dict[str, int] = {}

class Object():
    new:function = _newObject
    get:function = _getObject
    getAll = _returnObjects
  
class Component():
    new:function = _newComponent
    get:function = _getComponent

if __name__ == "__main__": asyncio.run(_main())
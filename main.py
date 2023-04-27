if __name__ == "__main__": logInConsole = True; print("\n"*60)
else: logInConsole = False

from os import system
system('pip3 install pygame')
system('cls')

import os, time, asyncio, pygame as pyg
from copy import deepcopy
from sys import exit
from typing import NoReturn as _NoReturn, Any
from Scripts import FileManager, Board, Camera, Input, Level, Timer, dev
from Scripts.componentManager import newComponent, newPrefab
programPath: str    = os.getcwd()
FreezeFrames: int   = 0
logInConsole: bool  = True
ReadyToGo: bool     = False
level: Any          = Level.new("Level uno", 2000, 2000)
settings:      dict[str, Any]        = FileManager.load(programPath+"\\ConfigFiles\\settings.toml", 'toml', _returnType=dict)
delta: float = 1.0
RenderQueue:   set [object|dict]     = set({})


def NextID(itemList:dict, name:str|int='') -> str:
    name = str(name)
    keylist = itemList.keys()
    for i in range(len(itemList)):
        if not name + str(i) in keylist: return name+str(i)
    return name+str(len(itemList))    

def addComponent(component, name, id) -> None:
    """Adds a new component to the list. NOT TO BE USED BY USER, but by the component dependency wrapper."""
    if not 'componentID' in dir(component): exit("Do not use the add component function")
    Component.Components[id] = component
    Component.ComponentNames[name] = id

def addPrefab(prefab, name, id):
    if not 'prefabID' in dir(prefab): exit("Do not use the add prefab function")
    gameObject.Prefabs[id] = prefab
    gameObject.PrefabNames[name] = id

def addScene(): pass

async def _loadingScreen(programPath) -> None:
    """Manually displays a loading screen to keep busy while the game starts up"""
    loadingImage = pyg.image.load(programPath+'\\Assets\\Images\\loading.png')
    state = 0
    i = 0
    while ReadyToGo == False and i < 99:
        i += 1
        Screen.fill((0,0,0))
        Screen.blit(source=loadingImage, dest=(10, 10), area=pyg.Rect(state*64, 0, 64, 64))
        pyg.display.flip()
        await asyncio.sleep(0.05)
        state += 1
        if state >= 8:
            state = 0

async def _loadStuff() -> None:
    await asyncio.sleep(0.2)
    global ReadyToGo
    try:
        _startNewScene()
    except: print("OhNo"); raise
    ReadyToGo = True

class gameObject:
    Scenes:     dict[str,     type  ] = {}
    Prefabs:    dict[int,     type  ] = {}
    PrefabNames:dict[str,     int   ] = {}
    
    @classmethod
    def getPrefab(cls, prefabName: str) -> type:
        """Finds a prefab via it's name\n
        If no such prefab exists, returns None."""
        try:
            if isinstance(prefabName, int): _ID = prefabName
            elif isinstance(prefabName, str): _ID = cls.PrefabNames[prefabName]
            else: exit("Prefab name is invalid type")
            return cls.Prefabs[_ID]
        except KeyError as ke:
            if isinstance(prefabName, int): raise KeyError(f"Prefab Key error: {prefabName} is not a valid ID.")
            print("List of all prefabs: ", cls.PrefabNames.keys())
            append = ""
            for i in cls.PrefabNames:
                if i.split(sep="\\")[-1].lower() == prefabName.lower():
                    if append: append += " Or maybe "
                    append += f"Did you mean: {i}?"
            
            raise KeyError(f"{prefabName} is not a valid name. {append}" )

    @classmethod    
    def getAllPrefabs(cls) -> tuple[dict[int, type], dict[str, int]]:
        return cls.Prefabs, cls.PrefabNames
    
    @classmethod
    def newScene(cls, sceneName:str):
        from Scripts.Components.components import Scene as sc
        Scene = sc(sceneName, None, None)
        gameObject.Scenes[sceneName] = Scene
        return Scene
    
class Component:
    Components:    dict[int,     type  ] = {}
    ComponentNames:dict[str,     int   ] = {}
    @classmethod
    def new(cls, class_:type|str, *args, **kwargs) -> object:
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
        if isinstance(class_, str):
            class_ = cls.get(class_)
        return class_(*args, **kwargs)

    @classmethod
    def get(cls, _name:int|str) -> type:
        """Fetches a class using a name or the component's ID.
        Returns the class so you can initialize it or set attributes
        Example"""
        try:
            if isinstance(_name, int): _ID = _name
            elif isinstance(_name, str): _ID = cls.ComponentNames[_name]
            else: exit() 
            return cls.Components[_ID]
        except KeyError as ke:
            if isinstance(_name, int): raise KeyError(f"Key error: {_name} is not a valid ID.")
            print(cls.ComponentNames.keys())
            append = ""
            for i in cls.ComponentNames:
                if i.split(sep="\\")[-1].lower() == _name.lower():
                    if append: append += " Or maybe "
                    append += f"Did you mean: {i}?"
                
            raise KeyError(f"{_name} is not a valid name. {append}" )

    @classmethod    
    def getAll(cls) -> tuple[dict[int, type], dict[str, int]]:
        return cls.Components, cls.ComponentNames

class Render():
    @classmethod
    async def _drawCurrentFrame(cls, renderQueue:set) -> None:
        
        readyRenderQueue = cls._sortRenderQueue(renderQueue)
        
        asyncioRenderTasks = []
        Screen.fill((50, 50, 50))
        for i in reversed(readyRenderQueue):
            if 'render' in dir(readyRenderQueue[i]):
                asyncioRenderTasks.append( asyncio.create_task( cls._renderWithObj(readyRenderQueue[i]) )) 
            else:
                print(f"RenderQueue: {readyRenderQueue[i].__name__} does not have a function for rendering and thus failed to render.")
        if len(asyncioRenderTasks) > 0:
            await asyncio.wait(asyncioRenderTasks)
        pyg.display.flip()

    @classmethod
    def _sortRenderQueue(cls, renderQueue) -> dict:
        """Takes a dict/set and for each item takes each objects tier, zPosition, and self and sorts the dictionary using those values
        in priority of tier>zposition>object"""
        tempRenderQueue = []
        returnedRenderQueue = {}

        for i in renderQueue:
            
            tempRenderQueue.append((i.tier, i.Transform.zPosition, i))
        tempRenderQueue.sort()
        
        for i in tempRenderQueue:
            _, _, value = i
            returnedRenderQueue[tempRenderQueue.index(i)] = value

        return returnedRenderQueue

    @classmethod     
    async def _renderWithObj(cls, rendererObj) -> None:
        rendererObj.render(Screen=Screen, Camera=Camera) # type: ignore

    @classmethod
    def _drawRect(cls, color: tuple[int, int, int], x: float|int, y: float|int, xl: float|int, yl: float|int) -> None:
        pyg.draw.rect(Screen, color, (int(x) - int(Camera.xPosition), int(y) - int(Camera.yPos), int(xl), int(yl)))

def _startNewScene() -> str:
    global Scene, devMode, sky, \
    Character, missingImage, Mouse, Font, \
    MainComponent, CharacterComponent, PlatformComponent

    devMode = False    

    Scene = gameObject.newScene("MainScene")
  

    from Scripts import componentManager as ComponentManager, cutsceneManager as CutsceneManager

    import Scripts.Components.character as CharacterComponent
    import Scripts.Components.components as MainComponent
    import Scripts.Components.platforms as PlatformComponent
    

    Component.Components, Component.ComponentNames, gameObject.Prefabs, gameObject.PrefabNames \
        = ComponentManager.init()
    Input.init()
    Camera.init()
    # CutsceneManager.init()


    missingImage = pyg.image.load(programPath+"\\Assets\\Images\\MissingImage.png").convert()


    # import componentDependencyFinder


    Character = Scene.newObject(nameInput="Character", prefabInput='characterPrefab\\Character', )
    Mouse = Component.new(Component.get('components\\Mouse'))
    Font = pyg.font.Font('freesansbold.ttf', 32)
    # sky = Component.new(
    #     'sky', prefabInput = Component.get('components\\Renderer'), 
    #     tier=99,
    #     path = "Assets\\Images\\SkyBox.png",

    #     Transform=Component.new(
    #         Component.get('components\\Transform'),
    #         xPosition= -500,
    #         zPosition=99,
    #     )
    # )   
    
    return "Done"

async def _platformingTick():
    if Input.getDown('jump'):
        exit(system('cls'))

    if dev.devpause:
        textRect = Font.get_rect() # type: ignore
        inputFromKeyboard = ''
        letter = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", 
            "BACKSPACE", "TAB"]    
        text = Font.render(inputFromKeyboard, True, (255,255,255))
        Screen.blit(text, textRect)
        pyg.display.flip()
        Clock.tick(60)
        return "devpause"

    """if FreezeFrames > 0:
        FreezeFrames -= 1
        return "freezeFrame"

    


Extra Input From Player (For dev use) =========================================================================================================

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
        Mouse.down = False"""

    Input.update()
    Scene.updateObjects()

    return 'complete'

async def _main() -> _NoReturn|None:
    global logInConsole, Screen, Clock, ReadyToGo
    global delta
    print(delta)
    delta = 0
    print(delta)
    if not isinstance(settings, dict): raise Exception('Critical file missing!: \\ConfigFiles\\settings.toml')
    logInConsole = settings['LogInConsole']
    
    pyg.init()

    Screen = pyg.display.set_mode((settings["Screen"]["screen_width"], settings["Screen"]["screen_height"]))
    pyg.display.set_icon(pyg.image.load(programPath+"\\Assets\\Images\\hehe.png").convert())
    pyg.display.set_caption('Platformer')

    Clock = pyg.time.Clock()
    
    #Activate Loading screen
    
    await asyncio.gather(_loadingScreen(programPath), _loadStuff())


    #Run physics 60 times per second
    while True:        
        start = time.time()

        done = await asyncio.gather(
            _platformingTick(), 
            Render._drawCurrentFrame(RenderQueue),
            # asyncio.sleep(1)
        )
            
        Timer.tick()
        try: raise
        except RuntimeError as re: pass

        end = time.time()
        system('cls')
        print(f"tick took {end - start} seconds")
        setattr(_main, 'delta', end - start)
try:
    if __name__ == "__main__": asyncio.run(_main())
except SystemExit:
    exit()
print("Hi")
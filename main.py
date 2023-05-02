if __name__ == "__main__": logInConsole = True; print("\n"*60)
else: logInConsole = False

from os import system
system('pip3 install pygame')
system('cls')

import os, time, asyncio, pygame as pyg #type: ignore
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
settings: dict[str, Any] = FileManager.load(programPath+"\\ConfigFiles\\debugSettings.toml", 'toml', _returnType=dict)
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

async def _loadingScreen(programPath) -> None:
    """Manually displays a loading screen to keep busy while the game starts up"""
    loadingImage = pyg.image.load(programPath+'\\Assets\\Images\\loading.png')
    state = 0
    i = 0
    while ReadyToGo == False and i < 99:
        i += 1
        Render.Screen.fill((0,0,0))
        Render.Screen.blit(source=loadingImage, dest=(10, 10), area=pyg.Rect(state*64, 0, 64, 64))
        pyg.display.flip()
        await asyncio.sleep(0.05)
        state += 1
        if state >= 8:
            state = 0

async def _loadStuff() -> None:
    await asyncio.sleep(0.2)
    global ReadyToGo
    try:
        _sceneStart()
    except: print("OhNo"); raise
    ReadyToGo = True

class gameObject:
    Scenes:     dict[str,     type  ] = {}
    currentScene                      = None
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
    def newScene(cls, sceneName:str="New Scene"):
        from Scripts.Components.components import Scene as sc
        if sceneName in gameObject.Scenes: sceneName = NextID(gameObject.Scenes, sceneName)
        Scene = sc(sceneName, None, None)
        gameObject.Scenes[sceneName] = Scene
        gameObject.currentScene = Scene
        return Scene
    
class Component:
    Components:    dict[int,     type  ] = {}
    ComponentNames:dict[str,     int   ] = {}
    Scene = None

    @classmethod
    def new(cls, class_:type|str, *args, **kwargs) -> object:
        if isinstance(class_, str):
            try:
                class_ = cls.get(class_)
            except KeyError: raise
        return class_(cls.Scene, *args, **kwargs)

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
    Screen: pyg.Surface

    @classmethod
    async def _drawCurrentFrame(cls, renderQueue:set) -> None:
        
        renderQueue = Scene.RenderQueue

        readyRenderQueue = cls._sortRenderQueue(renderQueue)
        
        asyncioRenderTasks = []
        cls.Screen.fill((50, 50, 50))
        for i in reversed(readyRenderQueue):
            if 'render' in dir(readyRenderQueue[i]):
                asyncioRenderTasks.append( asyncio.create_task( cls._renderWithObj(readyRenderQueue[i]) )) 
            else:
                print(f"RenderQueue: {readyRenderQueue[i].__name__} does not have a function for rendering and thus failed to render.")
        if len(asyncioRenderTasks) > 0:
            await asyncio.wait(asyncioRenderTasks)
        if settings['devMode']:
            cls._renderDev()
        pyg.display.flip()

    @classmethod
    def _renderDev(cls):
        cls.font = pyg.font.Font('freesansbold.ttf', 20)
        cls._drawRect((0,0,0), 1000, 0, 600, 1000)
        ids, prefabs = gameObject.getAllPrefabs()
        cids, components = Component.getAll()
        i = 0
        cls._drawText("Prefabs: ", y=i)
        for prefab in prefabs:
            i += 20
            cls._drawText(prefab, y=i)

        i += 32
        cls._drawText("Components: ", y=i)

        for component in components:
            i += 20
            cls._drawText(component, y=i)
            



    @classmethod
    def _sortRenderQueue(cls, renderQueue) -> dict:
        """Takes a dict/set and for each item takes each objects tier, zPosition, and self and sorts the dictionary using those values
        in priority of tier>zposition>object"""
        tempRenderQueue = []
        returnedRenderQueue = {}

        for i in renderQueue:
            tempRenderQueue.append((i.tier, i.Transform.zPos, i))
        tempRenderQueue.sort()
        
        for i in tempRenderQueue:
            _, _, value = i
            returnedRenderQueue[tempRenderQueue.index(i)] = value

        return returnedRenderQueue

    @classmethod     
    async def _renderWithObj(cls, rendererObj) -> None:
        rendererObj.render(Screen=cls.Screen, Camera=Camera) # type: ignore

    @classmethod
    def _drawRect(cls, color: tuple[int, int, int], x: float|int, y: float|int, xl: float|int, yl: float|int) -> None:
        pyg.draw.rect(cls.Screen, color, (int(x) - int(Camera.xPosition), int(y) - int(Camera.yPos), int(xl), int(yl)))

    @classmethod
    def _drawText(cls, string, x=1000, y=0, xl=600, yl=1000):
        cls.Screen.blit(cls.font.render(string, True, (255,255,255)), pyg.Rect(x, y, xl, yl))

def _sceneStart() -> str:
    global Scene, devMode, sky, \
    Character, missingImage, Mouse, Font, \
    MainComponent, CharacterComponent, PlatformComponent

    devMode = False    

    from Scripts import componentManager as ComponentManager, cutsceneManager as CutsceneManager

    import Scripts.Components.character as CharacterComponent
    import Scripts.Components.components as MainComponent
    import Scripts.Components.platforms as PlatformComponent
    
    Scene = gameObject.newScene("MainScene")
    Component.Scene = Scene

    Component.Components, Component.ComponentNames, gameObject.Prefabs, gameObject.PrefabNames = ComponentManager.init()
    Input.init()
    Camera.init()
    # CutsceneManager.init()


    missingImage = pyg.image.load(programPath+"\\Assets\\Images\\MissingImage.png").convert()


    # import componentDependencyFinder


    Character = Scene.newObject(nameInput="Character", prefabInput='characterPrefab\\Character', )
    Mouse = Scene.newObject('components\\Mouse')
    Font = pyg.font.Font('freesansbold.ttf', 32)

    
    return "Done"

async def _sceneTick(delta):
    if Input.getDown('jump'):
        exit(system('cls'))

    Input.update()
    Timer.tick()
    Scene.delta = delta
    Scene.updateObjects()

    return 'complete'

async def _main() -> _NoReturn|None:
    global logInConsole, Clock, ReadyToGo
    if not isinstance(settings, dict): raise Exception('Critical file missing!: \\ConfigFiles\\settings.toml')
    logInConsole = settings['LogInConsole']
    delta = 1
    pyg.init()

    Render.Screen = pyg.display.set_mode((settings["Screen"]["screen_width"], settings["Screen"]["screen_height"]))

    pyg.display.set_icon(pyg.image.load(programPath+"\\Assets\\Images\\hehe.png").convert())
    pyg.display.set_caption('Platformer')

    Clock = pyg.time.Clock()
    
    await asyncio.gather(_loadingScreen(programPath), _loadStuff())

    while True:        
        start = time.time()

        done = await asyncio.gather(
            _sceneTick(delta), 
            Render._drawCurrentFrame(RenderQueue))
            
        try: raise
        except RuntimeError as re: pass

        end = time.time()
        delta = end - start
        system('cls')
        print(f"tick took {end - start} seconds")

try:
    if __name__ == "__main__": asyncio.run(_main())
except SystemExit:
    exit()
print("Hi")
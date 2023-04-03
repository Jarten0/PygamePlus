if __name__ == "__main__": logInConsole = False; print("\n"*60)

import os, time, asyncio, pygame as pyg
from copy import deepcopy
from sys import exit
from typing import NoReturn as _NoReturn, Any
from Scripts import FileManager, Board, Camera, Input, Level, Timer, dev

programPath: str    = os.getcwd()
FreezeFrames: int   = 0
logInConsole: bool  = True
ReadyToGo: bool     = False
level: Any          = Level.new("Level uno", 2000, 2000)
settings:      dict[str, Any]        = FileManager.load(programPath+"\\ConfigFiles\\settings.toml", 'toml', _returnType=dict)
Objects:       dict[str|int, object] = {}
UpdateObjects: dict[str|int, object] = {}
Components:    dict[int,     type  ] = {}
ComponentNames:dict[str,     int   ] = {}
RenderQueue:   set [object|dict]     = set({})

def timeFunction(func):
    def timerWrapper(*args2, **kwargs2) -> None:
        print(f"Timing {func.__name__}...")
        start = time.time()
        func(*args2, **kwargs2)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds to run")
    timerWrapper.__name__ = func.__name__
    return timerWrapper

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

def NextID(itemList:dict, name:str|int='') -> str:
    name = str(name)
    keylist = itemList.keys()
    for i in range(len(itemList)):
        if not name + str(i) in keylist: return name+str(i)
    return name+str(len(itemList))    

def returnGlobals(var='all'):
    if var == 'all': return {
        'obj':Objects, 
        'updobj':UpdateObjects, 
        'renque':RenderQueue, 
        'com':Components, 
        'comnam':ComponentNames, 
        'rdytg':ReadyToGo}
    else: 
        if var in {
        'obj':Objects, 
        'updobj':UpdateObjects, 
        'renque':RenderQueue, 
        'com':Components, 
        'comnam':ComponentNames, 
        'rdytg':ReadyToGo}:
            return {
        'obj':Objects, 
        'updobj':UpdateObjects, 
        'renque':RenderQueue, 
        'com':Components, 
        'comnam':ComponentNames, 
        'rdytg':ReadyToGo}[var]
        else: return None

def addComponent(component, name, id) -> None:
    """Adds a new component to the list. NOT TO BE USED BY USER, but by the component dependency wrapper."""
    if not 'ID' in dir(component): exit("Do not use the add function")
    Components[id] = component
    ComponentNames[name] = id
    if True: returnGlobals()

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
        _startPlatformingScene()
    except: print("OhNo"); raise
    ReadyToGo = True

class Object():
    @classmethod
    def new(cls,
    name_:str | int | None, 
    class_:type|str, 
    addToList_:bool = True,
    *args, **kwargs) -> object:
        """Takes in a name and optionally a class/component and returns an instance of it. \n
        If the class/component has a create__() function it will automatically detect it and 
        attempt to use it to create the object. Otherwise, it will rely on the class's initialize function. \n
        You can also feed in args/keyword args that will go directly to the component's initializer"""

        if isinstance(class_, str): class_ = Component.get(class_)

        if name_ == None or name_ in Objects: name_ = NextID(Objects, 'New Object')

        if 'create' in dir(class_):
            try: createdObject:object = class_.create__(name_, *args, **kwargs) #type: ignore
            except: print("\n\n!!!!!!!!!!\n\n", class_.__name__, " create error: Something went wrong, go fix it.\n", sep=''); raise
            # print(createdObject.NAME) 
            # for i in dir(createdObject): 
            #     if list(i)[0] == "_": continue 
            #     else: print(i)
            # time.sleep(3)
            if not isinstance(createdObject, class_):
                raise Exception(f"{class_.__name__}\n\n\nError?? {createdObject} had an issue. It should only return an object. Check to see if it is properly returning a value. ")
            return createdObject

        else:
            return cls.initialize(name=name_, class_=class_, addToList_=addToList_,*args, **kwargs)
    
    @classmethod
    def get(cls, name) -> object|None:
        """Finds an object via it's name\n
        If no such object exists, returns None."""
        if name in Objects: return Objects[name]
        else: return None
    
    @classmethod
    def getAll(cls) -> dict[str | int, object]:
        return Objects
    
    @classmethod
    def initialize(cls, name:str|int, 
            class_:type, addToList_:bool,
            *args, **kwargs) -> object:
        if name == "" or name in Objects:
            if name == "":
                NextID(Objects, 'New Object') 
            else:
                NextID(Objects, name=name)

        object_:object = class_(*args, **kwargs)
        if addToList_: Objects[name] = object_
        return object_

    @classmethod
    def _createSpecialObject(cls,
        name:str, 
        class_:type, 
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
        Objects[name] = object_
        return object_

class Component():
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
            elif isinstance(_name, str): _ID = ComponentNames[_name]
            else: exit() 
            return Components[_ID]
        except KeyError as ke:
            if isinstance(_name, int): raise KeyError(f"Key error: {_name} is not a valid ID.")
            print(ComponentNames.keys())
            append = ""
            for i in ComponentNames:
                if i.split(sep="\\")[-1].lower() == _name.lower():
                    if append: append += " Or maybe "
                    append += f"Did you mean: {i}?"
                
            raise KeyError(f"{_name} is not a valid name. {append}" )

    @classmethod    
    def getAll(cls) -> tuple[dict[int, type], dict[str, int]]:
        return Components, ComponentNames

class Render():
    @classmethod
    async def _drawCurrentFrame(cls, renderQueue:set) -> None:
        
        readyRenderQueue = cls._sortRenderQueue(renderQueue)
        
        asyncioRenderTasks = []
        Screen.fill((10, 10, 10))
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
        pyg.draw.rect(Screen, color, (int(x) - int(Camera.xPosition), int(y) - int(Camera.yPosition), int(xl), int(yl)))

def _startPlatformingScene() -> str:
    global level, devMode, sky, \
    Character, missingImage, Mouse, Font, \
    Components, ComponentNames, \
    MainComponent, CharacterComponent, PlatformComponent

    devMode = False
        
    from Scripts import componentManager as ComponentManager, cutsceneManager as CutsceneManager

    import Scripts.Components.character as CharacterComponent
    import Scripts.Components.components as MainComponent
    import Scripts.Components.platforms as PlatformComponent
    
    Components, ComponentNames = ComponentManager.init()
    Input.init()
    Camera.init()
    CutsceneManager.init()
    missingImage = pyg.image.load(programPath+"\\Assets\\Images\\MissingImage.png").convert()


    # import componentDependencyFinder


    Character = Object.new(name_="Character", class_=Component.get('character\\Character'))


    Mouse = Object.new('Mouse', Component.get('components\\Mouse'))
    Font = pyg.font.Font('freesansbold.ttf', 32)
    sky = Object.new(
        'sky', class_ = Component.get('components\\Renderer'), 
        tier=99,
        path = "Assets\\Images\\SkyBox.png",

        Transform=Component.new(
            Component.get('components\\Transform'),
            xPosition= -500,
            zPosition=99,
        )
    )   

    platData = {
        0: None,
    #100 - 199 are levels in the game
        100: {},
    #200 - 299 are names of the levels
        200: "Level 0",
    }


    #Add all objects with update__ functions to main
    for i in Objects:
        if 'update__' in dir(Objects[i]):
            UpdateObjects[i] = Objects[i]
    
    return "Done"

async def _platformingTick():
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

    # if FreezeFrames > 0:
    #     FreezeFrames -= 1
    #     return "freezeFrame"

    


#Extra Input From Player (For dev use) =========================================================================================================

    # if devMode == True:
    #     if InputManager.k("z", eventsGet):
    #         platData[100] = level.plat
    #         FileManager.save(platData, platformfilename)
    #         print("Saved Platform Data")
    #     if InputManager.k("x", eventsGet):
    #         data = FileManager.load(platformfilename)
    #         level = Level(data[100], data[100])
    #     if InputManager.k("c", eventsGet):
    #         level.plat = {}
    #     if InputManager.k("q", eventsGet):
    #         pyg.quit()
    #         exit()
    #     if InputManager.k("r", eventsGet):
    #         settings= defaultProperties(defaultProperties.lis)
    #         FileManager.save(p, properetiesFileName)
    #         print("Saved Propereties")        
    #     if InputManager.k("`", eventsGet):
    #         FileManager.save(p, "prop.dat")
    #         print("Saved Propereites")

    # for i in range(10):
    #     if InputManager.keyDownHeld(str(i), eventsGetHeld):
    #         select = i
    #         print(i)
        
    # if InputManager.k("TAB", eventsGet):
    #     devMode = True
    #     # settings= dev.cmd()
    
    # if Mouse.list[0]:
    #     if not Mouse.down:
    #         print("Click!")
    #         if select == 0:
    #             for platformThing in level.plat:
    #                 platformToBeDeleted = level.plat[platformThing]
    #                 if platform.collision.check(Mouse.posx, Mouse.posy, 1, 1, platformToBeDeleted.x, platformToBeDeleted.y, platformToBeDeleted.xl, platformToBeDeleted.yl)[0]:
    #                     del level.plat[platformThing]
    #                     break
            
    #         elif placestage == 0:
    #             placestage = 1
    #             Mouse.tempx = Mouse.posx
    #             Mouse.tempy = Mouse.posy
    #             print(f"({Mouse.tempx}, {Mouse.tempy})")
                
            
    #         elif placestage == 1:
    #             Mouse.tempx2 = Mouse.posx
    #             Mouse.tempy2 = Mouse.posy
    #             if Mouse.tempx > Mouse.tempx2:
    #                 Mouse.xstate = Mouse.tempx2
    #             else:
    #                 Mouse.xstate = Mouse.tempx
    #             if Mouse.tempy > Mouse.tempy2:
    #                 Mouse.ystate = Mouse.tempy2
    #             else:
    #                 Mouse.ystate = Mouse.tempy
                
    #             if platform.placeprop[select]["#HasPlaceReq"]:
    #                 if not platform.placeprop[select]["xl"] == False:
    #                     Mouse.tempx2 = platform.placeprop[select]["xl"]
    #                     Mouse.tempx = 0
    #                 if not platform.placeprop[select]["yl"] == False:
    #                     Mouse.tempy2 = platform.placeprop[select]["yl"]
    #                     Mouse.tempy = 0
    #             if platform.placeprop[select]["#object"]:
    #                 level.plat[platform.NextID(level.plat)] = platform.create(Mouse.posx, Mouse.posy, Mouse.tempx2, Mouse.tempy2, select)
    #             elif not abs(Mouse.tempx2 - Mouse.tempx) == 0 and not abs(Mouse.tempy2 - Mouse.tempy) == 0:
    #                 level.plat[platform.NextID(level.plat)] = platform.create(Mouse.xstate, Mouse.ystate, abs(Mouse.tempx2 - Mouse.tempx), abs(Mouse.tempy2 - Mouse.tempy), select)  
    #             placestage = 0
    #         Mouse.down = True
    
    # else:
    #     Mouse.down = False

#Component Handler
    for obj in UpdateObjects.values():
        obj.update__() # type: ignore


    print(Objects.keys())
    for obj in Objects.values():
        if 'update' in dir(obj): obj.update() # type: ignore
        for componentName in dir(obj):
            objComponent = obj.__getattribute__(componentName)
            if 'ID' not in dir(objComponent): continue
            if isinstance(objComponent, type): continue
            print(objComponent.NAME)
            if 'update' in dir(objComponent):
                # if objComponent.NAME == 'Character': continue
                objComponent.update()
    
            if 'render' in dir(objComponent):
                RenderQueue.add(objComponent)
        



    
    
    # settings['gameTimer' ] += 1 / 60 # type: ignore
    # settings['totalTicks'] += 1  # type: ignore

    return 'complete'

#---------------------------------------------------------------------------------------------------------------------------
async def _main() -> _NoReturn|None:
    global logInConsole, Screen, Clock, ReadyToGo

    if not isinstance(settings, dict): raise Exception('Critical file missing!: \\ConfigFiles\\settings.toml')
    logInConsole = settings['LogInConsole']
    
    pyg.init()

    Screen = pyg.display.set_mode((settings["Screen"]["screen_width"], settings["Screen"]["screen_height"]))
    pyg.display.set_icon(pyg.image.load(programPath+"\\Assets\\Images\\hehe.png").convert())
    pyg.display.set_caption('Platformer')

    Clock = pyg.time.Clock()
    
    #Activate Loading screen
    
    await asyncio.gather(_loadingScreen(programPath), _loadStuff())



    i=0
    #Run physics 60 times per second
    while True:        
        i += 1
        done = await asyncio.gather(
            _platformingTick(), 
            Render._drawCurrentFrame(RenderQueue),
            asyncio.sleep(1/60)
        )
        # print(done)
            
        Timer.tick()
        try: raise
        except RuntimeError as re: pass
        if i > 60*60*1/2: break
if __name__ == "__main__": asyncio.run(_main())

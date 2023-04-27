import os, importlib.util
from typing import Any, Callable
import random

def _findNextAvailableID(List_:dict, randomize:bool = False) -> int:
    """Will find an available key in a list. 
    \nSet randomize to attempt to pick a random ID, and it will set a number between 1 and 10,000,000,000
    If the size somehow exceeds that length, the list will exit. It also has a cap of such.
    \nAlso, the list is slightly weird in that it has an impossibly small chance of failing if the
    amount of attempts to find an untaken ID goes over 10 billion. 
    You can inspect the code to see what I mean, but it's so insignificant you don't have to worry
    about it unless your list is for whatever reason billions of items large
    \nAnd it has a lengthOfList/10billion chance to delay for a completley insignificant amount of time.
    \nJust know that it's not a perfect solution but that the chances of it going wrong are so small
    that it basically doesn't even matter at all."""
    if randomize == False:
        for i in range(len(List_) + 1):
            if not i in List_:
                return i
    else:
        attempts:set = set(())
        while True:
            i = int(random.random()*(10**10))
            if not i in List_: return i
            if i in attempts: continue
            if len(List_) > 10**10 or len(attempts) > 10**10: raise Exception("This list is really big. Like, REALLY BIG. Bigger than 10^10 items. Thats more than 80 GIGABYTES. What in the WORLD did you do to fill it up THIS much?")
            attempts.add(i)
    
    raise Exception("This list is really big. Like, REALLY BIG. Bigger than 10^10 items. Thats more than 80 GIGABYTES. What in the WORLD did you do to fill it up THIS much?")

def init():
    from main import Component, gameObject
    import typing, main
    Components, ComponentNames = Component.Components, Component.ComponentNames
    Prefabs, PrefabNames = gameObject.Prefabs, gameObject.PrefabNames
    blacklist = {'__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__',}
    pfbblacklist = {'__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__',}
    filesChecked = []
    filesCheckedTwo = []

    componentDirectories = {
        "\\Scripts\\Components",
        "\\Assets\\Components"
    }
    prefabDirectories = {
        "\\Assets\\Prefabs",
        "\\Scripts\\Components",
    }

    for directory in componentDirectories:
        for file in os.listdir(os.getcwd()+directory):
            filesChecked.append(file)
            _getComponentsFromFile(directory, file, blacklist, Components, ComponentNames, main)

    for directory in prefabDirectories:
        for file in os.listdir(os.getcwd()+directory):
            filesCheckedTwo.append(file)
            _getPrefabsFromFile(directory, file, pfbblacklist, Prefabs, PrefabNames, main)

    print("Checked all of these files:\n", filesChecked, "\n", filesCheckedTwo)
    return Components, ComponentNames, Prefabs, PrefabNames 

def _getComponentsFromFile(directory, file, blacklist, Components, ComponentNames, main:Any=None) -> None:
    if file in {"templateComponent.py", "__pycache__"}: return

    moduleSpec = importlib.util.spec_from_file_location(name=file, location=os.getcwd() + directory + "\\" + file)
    
    if isinstance(moduleSpec, type(None)): return
    if isinstance(moduleSpec.loader, None.__class__): return

    module = importlib.util.module_from_spec(moduleSpec)
    moduleSpec.loader.exec_module(module)

    for componentStr in set(dir(module)):

        if componentStr in blacklist: continue
        blacklist.add(componentStr) 

        component = getattr(module, componentStr)
        if not 'componentID' in dir(component): continue 

        file = file.removesuffix(".py")
        main.addComponent(component, file + "\\" + componentStr, component.componentID)

def _getPrefabsFromFile(directory, file, blacklist, Components, ComponentNames, main:Any=None) -> None:
    if file in {"templatePrefab.py", "__pycache__"}: return

    moduleSpec = importlib.util.spec_from_file_location(name=file, location=os.getcwd() + directory + "\\" + file)
    
    if isinstance(moduleSpec, type(None)): return
    if isinstance(moduleSpec.loader, None.__class__): return

    module = importlib.util.module_from_spec(moduleSpec)
    moduleSpec.loader.exec_module(module)

    for prefabStr in set(dir(module)):

        prefab = getattr(module, prefabStr)
        if not 'prefabID' in dir(prefab): continue

        if prefabStr in blacklist: continue
        blacklist.add(prefabStr) 

 

        file = file.removesuffix(".py")
        main.addPrefab(prefab, file + "\\" + prefabStr, prefab.prefabID)

        if 'start__' in dir(prefab):
            prefab.start__()


def newPrefab(initialPrefab) -> Any:
    name = initialPrefab.__name__
    class NewPrefab(initialPrefab):
        from main import gameObject, RenderQueue, NextID
        _Prefabs, _PrefabNames = gameObject.getAllPrefabs()
        prefabID = _findNextAvailableID(_Prefabs, randomize=True)
        NAME = initialPrefab.__name__


        def __init__(self, name, parent, Scene, *args, **kwargs) -> None:
            self.enclosedObjects = {}
            self.NAME = name
            self.parent = parent
            if not isinstance(Scene, type(self)): 
                Scene = self
            self.scene = Scene
            components = self.init(*args, **kwargs)
            
            if components == None: 
                components = {}
            for componentName in components:
                setattr(self, componentName, components[componentName])
            

        def newObject(self,
            nameInput:str|None = None, 
            prefabInput:type|str|None = None, 
            tagsInput: set[str] = set(),
            *args, **kwargs) -> object:
        
            """Takes in a name and a prefab and returns an instance of the prefab. \n
            You can also feed in args/keyword args that will go directly to the prefabs's initializer\n
            The prefab will be in charge of initializing all of the components, so if it needs any arguments
            be sure to feed them in."""

            if isinstance(prefabInput, type(None)): prefab = self.gameObject.getPrefab("componenets\\BasicObject")
            elif isinstance(prefabInput, str): prefab = self.gameObject.getPrefab(prefabInput)
            elif isinstance(prefabInput, type): prefab = prefabInput
            else: exit("Invalid prefab input type! Must be either a string, the prefab class, or None for a basic object") 

            if nameInput == None: name = NewPrefab.NextID(self.enclosedObjects, 'New Object')
            elif nameInput in self.enclosedObjects: name = NewPrefab.NextID(self.enclosedObjects, nameInput)
            else: name = nameInput

            if not 'prefabID' in dir(prefab): exit(name+f" initialization did not get a prefab, instead got {prefab} which is not a prefab class; make sure your input is either a prefab class or leads to a prefab and not a component")
            if not 'init' in dir(prefab): exit(name+"("+prefab.__name__+")"+": Invalid prefab initialization; prefab is missing init function")

            try: createdObject = prefab(name, parent=self, Scene=self.scene, *args, **kwargs)
            
            except: print("\n\n!!!!!!!!!!\n\n", prefab.__name__, " create error: Something went wrong, go fix it.\n", sep=''); raise
            if not isinstance(createdObject, prefab): print(createdObject.NAME, prefab.__name__); raise Exception(f"{prefab.__name__}\n\n\n{nameInput}:{prefabInput} create error; It should return an object. Check to see if it is properly returning a value. ") # type: ignore
            
            self.enclosedObjects[name] = createdObject
            
            self.Tags = tagsInput
            
            Scene = self.scene

            for tag in tagsInput:
                if tag not in Scene.SceneTags: Scene.SceneTags[tag] = {}
                Scene.SceneTags[tag][self.NAME] = self
            print(f"Created {name} object:{createdObject} in {self.NAME}!!")
            
            return createdObject



        def addTag(self, tag):
            if self is NewPrefab.Scene:
                self.SceneTags[tag] = {}
            else:
                if tag not in NewPrefab.Scene.SceneTags: NewPrefab.Scene.SceneTags[tag] = {}
                NewPrefab.Scene.SceneTags[tag][self.NAME] = self

        def removeTag(self, tag):
            if tag in self.Tags:
                self.Tags.remove(tag)



        def getObject(self, objName:str) -> object|None:
            """Finds an object via it's name\n
            If no such object exists, returns None."""
            objName.removeprefix("\\")
            objectHeirList = []
            splitName = ''
            for char in list(objName):
                if char == "\\":
                    objectHeirList.append(splitName)
                    continue
                splitName += char
            obj = self

            for name in objectHeirList:
                if name not in obj.enclosedObjects: print(f"{name} is not inside of {obj.NAME}"); return None
                obj = obj.enclosedObjects[name]
                if not 'enclosedObjects' in dir(obj): print(f"{name} is not an object"); return None                
            return obj

        def updateObjects(self):
            for obj in self.enclosedObjects.values():
                if 'earlyUpdate' in dir(obj): obj.earlyUpdate()
                for componentName in dir(obj):
                    objComponent = obj.__getattribute__(componentName)
                    if 'ID' not in dir(objComponent): continue
                    if isinstance(objComponent, type): continue
                    if 'update' in dir(objComponent):
                        objComponent.update()
            
                    if 'render' in dir(objComponent):
                        NewPrefab.RenderQueue.add(objComponent)
                if 'updateObjects' in dir(obj): obj.updateObjects()                
                if 'update' in dir(obj): obj.update()




    newPrefab.__name__ = name+"(Prefab)"
    return NewPrefab

def newComponent(initialComponent) -> Any:
    """Add this decorater to your class to automatically add in component functionality.
    \nSome specific useful functions:
    \ninit(self, **kwargs): Will run on creation of component, used to initialize values and set flags and whatnot.
    \ncreate(cls, name=''): Will run on creation of an object, used to initialize multiple components and to run scripts upon
    object creation. Read the doc for more detail.
    \nupdate(self): Run on every frame for every component. Do whatever you want with this.
    \nrender(self, Screen, Camera): Can be used to create custom rendering components, runs on every frame if it exists
    and allows you to render objects however you will via the Pygame engine.
    """
    name = initialComponent.__name__
    if not 'requiredDependencies' in dir(initialComponent):
        initialComponent.requiredDependencies = {}

    class NewComponent(initialComponent):  
        missLog_ = []
        if not "requiredDependencies" in dir(initialComponent): requiredDependencies = {} 
        if not "optionalArguments" in dir(initialComponent): optionalArguments = {} 
        from main import gameObject, Component
        _Components, _ComponentNames = Component.getAll()
        componentID = _findNextAvailableID(_Components, randomize=True)
        NAME = initialComponent.__name__

        def __new__(cls, *args, **kwargs) -> Any: 
            for reqDependency in cls.requiredDependencies.keys():              
                if reqDependency in NewComponent.optionalArguments:
                    continue
                
                if reqDependency not in kwargs:
                    NewComponent.missLog_.append(cls.requiredDependencies[reqDependency])
                    continue

                if not isinstance(kwargs[reqDependency], cls.requiredDependencies[reqDependency]):
                    NewComponent.missLog_.append(cls.requiredDependencies[reqDependency])
                continue

            return super(NewComponent, cls).__new__(cls)
        
        def __init__(self, *args, **kwargs) -> None:
            for missedComponent in NewComponent.missLog_:
                try:
                    kwargs[f"{missedComponent.NAME}"] = NewComponent.Component.new(missedComponent)
                except:
                    print("Dependency Adder failed! Make sure that:")
                    for missedComponent in NewComponent.missLog_:
                        print(missedComponent.__name__)
                    print("Are all present inside of:", name)
                    raise
        
            try:
                initialComponent.init(self, *args, **kwargs)

            except AttributeError as ae:
                error = f"InitializationFunctionMissing: No initialize function in {name}! Add missing function using template (run script as main for template)"
                print(error)
                raise ae
            except TypeError as te:
                error = f"InitializationWrapperMissing: No init decorater in {name}! Add missing @decorater using template (run script as main for template)"
                print(error)
                raise te
            
        def rename_(self, newName:str) -> None:
            """Takes in a name to set the object as and tries to set the object's name as it.
            \nIf it is already taken, it will try appending parenthesis with 
            a number to try to find an available key. It will return the new name
            \nExample: \n
            object.rename_() """
            pass

    NewComponent.__name__ = name+"(Component)"
    return NewComponent

def _main() -> None:
    print("""
    DEFAULT TEMPLATE:
from componentDependencyDecorators import *
@__dependencyWrapper(requiredDependencies= {
    "<required dependency name>": True,
    "<optional dependency name>": False, 
    } )
class <componentName>:            
    @__initializationWrapper
    def _initialize(self, dependencies):
        <add below for each dependency>
        self.<dependencyName> = dependencies["<dependencyName>"]  """)


if __name__ == '__main__':
    _main()

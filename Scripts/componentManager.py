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
    from main import Component
    import typing, main
    Components, ComponentNames = Component.Components, Component.ComponentNames
    blacklist = {'__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__',
    }

    directories = {
        "\\Scripts\\Components"
    }

    for directory in directories:
        for file in os.listdir(os.getcwd()+directory):
            _getComponentsFromFile(directory, file, blacklist, Components, ComponentNames, main)

    return Components, ComponentNames

def _getComponentsFromFile(directory, file, blacklist, Components, ComponentNames, main:Any=None) -> None:
    if file in {"templateCutscene.py", "__pycache__"}: return

    moduleSpec = importlib.util.spec_from_file_location(name=file, location=os.getcwd() + directory + "\\" + file)
    
    if isinstance(moduleSpec, type(None)): return
    if isinstance(moduleSpec.loader, None.__class__): return

    module = importlib.util.module_from_spec(moduleSpec)
    moduleSpec.loader.exec_module(module)

    for componentStr in set(dir(module)):

        if componentStr in blacklist: continue
        blacklist.add(componentStr) 

        component = getattr(module, componentStr)
        if not 'ID' in dir(component): continue 

        file = file.removesuffix(".py")
        main.addComponent(component, file + "\\" + componentStr, component.ID)

        if 'start__' in dir(component):
            component.start__()

def newComponent(initialComponent) -> type:
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
        from main import Object, Component
        _Components, _ComponentNames = Component.getAll()
        ID = _findNextAvailableID(_Components, randomize=True)
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
            

        @classmethod
        def create__(cls, name, *args, **kwargs) -> object:
            """Initializes a new object and sends it back using a create script. Returns None if no create script exists"""
            if not 'create' in dir(initialComponent): raise Exception("Uhoh: Ran create__ on a non-object component.")
            name, cls, kwargs = initialComponent.create(name)
            return NewComponent.Object.initialize(name, NewComponent, addToList_=True, *args, **kwargs)


        def rename_(self, newName:str) -> None:
            """Takes in a name to set the object as and tries to set the object's name as it.
            \nIf it is already taken, it will try appending parenthesis with 
            a number to try to find an available key. It will return the new name
            \nExample: \n
            object.rename_() """
            NewComponent.Object.get(self)


    NewComponent.__name__ = name+"(Wrapped)"
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

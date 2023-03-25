import os, importlib.util
from typing import Any, Callable
import random
from main import _ComponentNames, _Components
from main import *

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

def _init() -> None:
    blacklist = {'__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__'}
    for i in os.listdir(os.getcwd()+"\\Scripts\\Components"):
        if i in {"templateCutscene.py", "__pycache__"}:continue

        moduleSpec = importlib.util.spec_from_file_location(name=i, location=os.getcwd()+"\\Scripts\\Components\\" + i)
        
        if isinstance(moduleSpec, None.__class__):continue
        if isinstance(moduleSpec.loader, None.__class__):continue

        module = importlib.util.module_from_spec(moduleSpec)
        moduleSpec.loader.exec_module(module)
        
        for componentStr in set(dir(module)):
            component = module.__getattr__(componentStr)
            if i in blacklist: continue 
            _Components[component.ID] = component
            _ComponentNames[i] = component.ID
        
        if 'init_' in module.__dir__():        
            if module.init__['OnStart'] == True:
                module.create__()
        
        if 'start__' in module.__dir__():
            module.start__()

def initializationWrapper_(componentInitFunc: Callable[..., None]) -> Callable[..., Callable[..., None]]:
    if __import__('__main__').LogInConsole: 
        print("Loaded Component: ", [componentInitFunc])

    def wrapper(dependencyAdder) -> Callable[..., None]:
        
        #Run on creation of object
        def initialize(self, *args, **kwargs) -> None:
            self.__name__ = componentInitFunc.__class__.__name__+" > Instance"

            dependencyAdder(self, *args, **kwargs)
            componentInitFunc(self=self, dependencies=self.dependencies, *args, **kwargs)

        return initialize
    wrapper.__name__ = 'initialize__'
    return wrapper

def initializeOnStartWrapper_(componentCreate__Func, *args, **kwargs) -> Callable[..., None]:
    def wrapper(*args2, **kwargs2) -> None:
        return componentCreate__Func(*args, *args2, **kwargs, **kwargs2)
    wrapper.__name__ = componentCreate__Func.__name__
    return wrapper

def dependencyWrapper_(initialComponent):
    """Add this decorater to your class to automatically add in custom initialize functions."""
    name = initialComponent.__name__
    if not 'requiredDependencies' in dir(initialComponent):
        initialComponent.requiredDependencies = {}
        if LogInConsole_: print(f"'requiredDependencies' dictionary is missing in {name} definition!") 

    class Component(initialComponent):  
        missLog_ = []
        ID = _findNextAvailableID(_Components, randomize=True)

        def __new__(cls, givenDependencies:dict={}, *args, **kwargs) -> Any: 
            for i in initialComponent.requiredDependencies.keys():              
                try:
                    if kwargs[i] == None \
                    and initialComponent.requiredDependencies[i] == True:
                        Component.missLog_.append(initialComponent.requiredDependencies[i])
                except KeyError as ke:
                    Component.missLog_.append(initialComponent.requiredDependencies[i])
            if len(Component.missLog_) > 0:            
                if LogInConsole_: print(f"ComponentDependencyError: Missing dependencies for {name} initialization!")
            return super(Component, cls).__new__(cls)
        
        try:
            @initialComponent.initialize__
            def __init__(self, *args, **kwargs) -> None:
                self.dependencies = {}
                for i in Component.missLog_:
                    try:
                        self.dependencies[f"{i}"] = i()
                    except:
                        print("Dependency Adder failed! Make sure that:")
                        for i in Component.missLog_:
                            print(i.__name__)
                        print("Are all present inside of:", name)
                        raise
                for i in initialComponent.requiredDependencies:
                    self.dependencies[f"{i}"] = i

        except AttributeError as ae:
            error = f"InitializationFunctionMissing: No initialize function in {name}! Add missing function using template (run script as main for template)"
            raise Exception(error)
        except TypeError as te:
            error = f"InitializationWrapperMissing: No @initializationWrapper_ decorater in {name}! Add missing @decorater using template (run script as main for template)"
            raise Exception(error)


        def rename_(self, newName:str):
            """Takes in a name to set the object as and tries to set the object's name as it.
            \nIf it is already taken, it will try appending parenthesis with 
            a number to try to find an available key. It will return the new name
            \nExample: \n
            object.rename_() """
            main.Object.get(self)


    Component.__name__ = name+"(Wrapped)"
    return Component

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

class ComponentTools():
    newClass = dependencyWrapper_
    init = initializationWrapper_
    create = initializeOnStartWrapper_

if __name__ == '__main__':
    _main()
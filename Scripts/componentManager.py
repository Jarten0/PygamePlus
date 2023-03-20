import os, importlib.util
from typing import Any, Callable
Main = __import__('__main__')
def _findNextAvailableID(List) -> int:
    KeyList = List.keys()
    for i in range(len(List) + 1):
        if not i in KeyList:
            return i
    return len(List)
                
componentList = {}

def _init() -> None:
    for i in os.listdir(os.getcwd()+"\\Scripts\\Components"):
        if i in {"templateCutscene.py", "__pycache__"}:
            continue
        moduleSpec = importlib.util.spec_from_file_location(name=i, location=os.getcwd()+"\\Scripts\\Components\\" + i)
        if isinstance(moduleSpec, None.__class__):
            continue
        if isinstance(moduleSpec.loader, None.__class__):
            continue
        module = importlib.util.module_from_spec(moduleSpec)
        moduleSpec.loader.exec_module(module)
        componentList[i] = module
        if 'init_' in module.__dir__():        
            if module.init__['OnStart'] == True:
                module.create__()
        if 'start__' in module.__dir__():
            module.start__()
        print(module.__name__, dir(module))
    

# def _parametrized(dec: Callable[..., Any]) -> Callable[Any, Callable[Any, None]]: #This is not my code but it works #type: ignore
#     def layer(*args2, **kwargs2) -> Callable[..., None]:

#         def repl(f) -> Any:
#             return dec(f, *args2, **kwargs2)

#         return repl
#     return layer 

def initializationWrapper_(componentInitFunc) -> Callable[..., Callable[..., None]]:
    if __import__('__main__').LogInConsole: 
        print("Loaded Component: ", [componentInitFunc])
    def wrapper(dependencyAdder) -> Callable[..., None]:
        
        #Run on creation of object
        def initialize(self, *args, **kwargs) -> None:
            # if __import__('__main__').LogInConsole:
                # print("Created", self.__str__(), args, kwargs)

            self.__name__ = self.__str__()+"Instance"
            dependencyAdder(self, *args, **kwargs)
            componentInitFunc(self=self, dependencies=self.dependencies, *args, **kwargs)

        return initialize
    return wrapper

def initializeOnStartWrapper_(componentCreate__Func, *args, **kwargs) -> Callable[..., None]:
    def wrapper(*args2, **kwargs2) -> None:
        return componentCreate__Func(*args, *args2, **kwargs, **kwargs2)
    wrapper.__name__ = componentCreate__Func.__name__
    return wrapper

def dependencyWrapper_(initialComponent):
    name = initialComponent.__name__
    if not 'requiredDependencies' in dir(initialComponent):
        initialComponent.requiredDependencies = {}
        if Main.LogInConsole: print(f"'requiredDependencies' dictionary is missing in {name} definition!") 

    class Component(initialComponent):  
        missLog = []
        active = True
        def __new__(cls, givenDependencies:dict={}, *args, **kwargs) -> Any: 
            for i in initialComponent.requiredDependencies.keys():              
                try:
                    if kwargs[i] == None \
                    and initialComponent.requiredDependencies[i] == True:
                        Component.missLog.append(initialComponent.requiredDependencies[i])
                except KeyError as ke:
                    Component.missLog.append(initialComponent.requiredDependencies[i])
            if len(Component.missLog) > 0:            
                if Main.LogInConsole: print(f"ComponentDependencyError: Missing dependencies for {name} initialization!")
            return super(Component, cls).__new__(cls)
        
        try:
            @initialComponent.initialize__
            def __init__(self, *args, **kwargs) -> None:
                self.dependencies = {}
                for i in Component.missLog:
                    try:
                        self.dependencies[f"{i}"] = i()
                    except:
                        print("Dependency Adder failed! Make sure that:")
                        for i in Component.missLog:
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

if __name__ == '__main__':
    _main()
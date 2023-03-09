def parametrized(dec): #This is not my idea but it works
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer #okay but the rest of it was made solo by me after an unnecessarily long time like it took ~12 attempts and ~10 hours for FIFTY lines of code like serioursly this was a pain
def initializationWrapper(componentInitFunc):
    def wrapper(dependencies, *args, **kwargs):
        def initialize( *args, **kwargs):
            self = args[0]
            dependencies = kwargs["givenDependencies"]
            componentInitFunc(self, dependencies)        
        return initialize
    return wrapper
@parametrized
def dependencyWrapper(Component, requiredDependencies):
    defaultTemplate = {"""
from componentDependencyDecorators import *
@dependencyWrapper(requiredDependencies= {
    "<required dependency name>": True,
    "<optional dependency name>": False, 
    } )
class <componentName>:            
    @initializationWrapper
    def initialize(self, dependencies):
        <add below for each dependency>
        self.<dependencyName> = dependencies["<dependencyName>"]  """
    }
    name = Component.__name__
    class Component():    
        def __new__(cls, givenDependencies): 
            missLog = []    
            
            for i in requiredDependencies.keys(): 
                if givenDependencies[i] == None \
                    and requiredDependencies[i] == True:
                    missLog.append(i)
            if len(missLog) > 0:            
                raise ModuleNotFoundError(f"ComponentDependencyError: Missing {missLog} in {name}!")
                
            return super(Component, cls).__new__(cls)
        try:
            @Component.initialize
            def __init__(self, givenDependencies):
                pass
        except AttributeError as ae:
            error = f"InitializationFunctionMissing: No initialization function in {name}! Add missing function using template (run script as main for template)"
            raise ModuleNotFoundError(error)
                
        def printDefaultTemplate():
            print(defaultTemplate)
    Component.__name__ = name+"(Wrapped)"
    return Component
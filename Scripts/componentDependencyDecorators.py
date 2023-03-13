

def parametrized(dec, *args, **kwargs): #This is not my code but it works
    def layer(*args2, **kwargs2):
        def repl(f, *args3, **kwargs3):
            return dec(f, *args2, **kwargs2)
        return repl
    return layer #okay but the rest of it was made solo by me after an unnecessarily long time like it took ~12 attempts and ~10 hours for FIFTY lines of code like serioursly this was a pain

def initializationWrapper(componentInitFunc):
    if __import__('__main__').LogInConsole:
        print("Loaded Component: ", [componentInitFunc])
    def wrapper(dependencyAdder):
        def initialize(self, *args, **kwargs) -> None:
            self.__name__ = self.__str__()+"Instance"
            dependencyAdder(self, *args, **kwargs)
            componentInitFunc(self=self, dependencies=self.dependencies, *args, **kwargs)
            if __import__('__main__').LogInConsole:
                print("Created", self.__name__)    
        return initialize
    return wrapper

@parametrized
def dependencyWrapper(initialComponent: classmethod, requiredDependencies:dict={}, *args, **kwargs):
    name = initialComponent.__name__
    class Component():  
        missLog = []
        active = True
        def __new__(cls, givenDependencies:dict={}, *args, **kwargs): 
            for i in requiredDependencies.keys(): 
                try:
                    if kwargs[i] == None \
                    and requiredDependencies[i] == True:
                        Component.missLog.append(requiredDependencies[i])
                except KeyError as ke:
                    Component.missLog.append(requiredDependencies[i])

            if len(Component.missLog) > 0:            
                print(f"ComponentDependencyError: Missing {Component.missLog} in {name}!")
            return super(Component, cls).__new__(cls)
        
        try:
            @initialComponent.initialize # type: ignore
            def __init__(self, *args, **kwargs) -> None:
                self.dependencies = {}
                for i in Component.missLog:
                    self.dependencies[f"{i}"] = i()
                for i in requiredDependencies:
                    self.dependencies[f"{i}"] = i
        
        except AttributeError as ae:
            error = f"InitializationFunctionMissing: No initialize function in {name}! Add missing function using template (run script as main for template)"
            raise Exception(error)
        except TypeError as te:
            error = f"InitializationWrapperMissing: No @initializationWrapper decorater in {name}! Add missing @decorater using template (run script as main for template)"
            raise Exception(error)

    Component.__name__ = name+"(Wrapped)"
    return Component

def main() -> None:
    print("""
    DEFAULT TEMPLATE:
from componentDependencyDecorators import *
@dependencyWrapper(requiredDependencies= {
    "<required dependency name>": True,
    "<optional dependency name>": False, 
    } )
class <componentName>:            
    @initializationWrapper
    def initialize(self, dependencies):
        <add below for each dependency>
        self.<dependencyName> = dependencies["<dependencyName>"]  """)

if __name__ == '__main__':
    main()
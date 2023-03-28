import os, importlib.util
def _generateDependencyList():
    Components, ComponentNames = {}, {}
    
    blacklist = {'__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__',
    }

    directories = {
        "\\Scripts\\Components"
    }

    for directory in directories:
        for file in os.listdir(os.getcwd()+directory):
            _heh(directory, file, blacklist, Components, ComponentNames)

    for componentClass in Components.values():
        component = componentClass.__name__
        print(component.removesuffix("(Wrapped)"))
        
        if len(componentClass.requiredDependencies) > 0:
            print("Dependencies:")
            for i in componentClass.requiredDependencies:
                print("  -", i)
        else: print("No Dependencies")

        if 'arguments' in dir(componentClass):
            print("Arguments: ")
            for i in componentClass.arguments:
                print("  -", i, ":\n    ", type(componentClass.arguments[i]), " = ", componentClass.arguments[i], sep="")
        else:
            print("No Arguments")
        
        print()



def _heh(directory, file, blacklist, Components, ComponentNames):
    if file in {"templateCutscene.py", "__pycache__"}: return

    moduleSpec = importlib.util.spec_from_file_location(name=file, location=os.getcwd() + directory + "\\" + file)
    
    if isinstance(moduleSpec, None.__class__): return
    if isinstance(moduleSpec.loader, None.__class__): return

    module = importlib.util.module_from_spec(moduleSpec)
    moduleSpec.loader.exec_module(module)

    for componentStr in set(dir(module)):

        if componentStr in blacklist: continue
        blacklist.add(componentStr) 

        component = getattr(module, componentStr)
        if not 'ID' in dir(component): continue 

        file = file.removesuffix(".py")


        name, id = file + "\\" + componentStr, component.ID
        if not 'ID' in dir(component): exit("Do not use the add function")
        Components[id] = component
        ComponentNames[name] = id

_generateDependencyList()

      
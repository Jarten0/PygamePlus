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
            _loadComponent(directory, file, blacklist, Components, ComponentNames)

    ifOptionalInArg = lambda com, i : ", #Optional" * int((i in com.optionalArguments))
    ifNoStr = lambda obj: (int('<' in obj) * ("'" + obj.removeprefix('<').removesuffix('>') + "'")) + (int(not '<' in obj) * obj)
    with open(os.getcwd()+"\\componentDependencies.py", "w") as writeFile:
        writeFile.write("from main import gameObject, Component\n")
        writeFile.write("Scene = gameObject.newScene('TemplateScene')\n\n")


        importStatment = ""
        for name in ComponentNames: importStatment += "from Scripts.Components."+name.removeprefix("\\").partition("\\")[0]+" import "+name.removeprefix("\\").partition("\\")[2]+"\n"
        writeFile.write(importStatment.removesuffix(", \\")+"\n")
        
        success = False
        for componentClass in Components.values():
            component = componentClass.__name__
            
            if 'create' in dir(componentClass):
                writeFile.write("Scene.new(name_='"+component.removesuffix("(Wrapped)")+" Object', class_="+component.removesuffix("(Wrapped)")+", addToList_=False,\n")
            else:
                writeFile.write("Object.newComponent("+component.removesuffix("(Wrapped)")+",\n")
            append = ''
            if len(componentClass.requiredDependencies) > 0:
                for dependency in componentClass.requiredDependencies:
                    if 'optionalArguments' in dir(componentClass): 
                        if dependency in componentClass.optionalArguments: continue
                    append += ("    "+ dependency+ "    = "+ dependency + 
                        "("+
                        str(set([i+" = "+i+"("+""+")" for i in componentClass.requiredDependencies[dependency].requiredDependencies])).replace("set()", '').replace("'", '').replace("{", '').replace("}", '')
                        +"),\n"
                                    )
            if not append == '': writeFile.write("\t#Dependencies\n"+append)
            else: writeFile.write("\t#No Dependencies\n")


            if 'arguments' in dir(componentClass) and 'optionalArguments' in dir(componentClass):
                writeFile.write("\t#Arguments\n")

                for dependency in componentClass.arguments:
                    writeFile.write("    "+ dependency+  " = "+ ifNoStr(str(componentClass.arguments[dependency]))+ ",        #"+ str(type(componentClass.arguments[dependency]))+ ifOptionalInArg(componentClass, dependency)+"\n")

            else:
                writeFile.write("\t#No Arguments\n")

            writeFile.write("\n)\n")
        writeFile.close()
    import componentDependencies


def _loadComponent(directory, file, blacklist, Components, ComponentNames):
    if file in {"templateCutscene.py", "__pycache__"}: return

    moduleSpec = importlib.util.spec_from_file_location(name=file, location=os.getcwd() + directory + "\\" + file)
    
    if isinstance(moduleSpec, type(None)): return
    if isinstance(moduleSpec.loader, type(None)): return

    module = importlib.util.module_from_spec(moduleSpec)
    moduleSpec.loader.exec_module(module)

    for componentStr in set(dir(module)):

        if componentStr in blacklist: continue
        blacklist.add(componentStr) 

        component = getattr(module, componentStr)
        if not 'ID' in dir(component): continue 

        file = file.removesuffix(".py")

        name, id = file + "\\" + componentStr, component.ID

        Components[id] = component
        ComponentNames[name] = id

_generateDependencyList()

      
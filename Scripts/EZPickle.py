from pickle import dump as pkd, load as pkl
import tomllib
from typing import Any
from os import getcwd

#Used to easily pickle/save a single variable in a particular file
#Use by calling EZPickle.save([variable you wish to save], [file you wish to save it in])
#If you want to save multiple variables, then learn to get creative with lists/dictionaries/tuples
def _save(value, filename) -> None:
    try:    
        with open(filename, "wb") as file:
            pkd(value, file)
    except FileNotFoundError as fnfe:
        with open(filename, 'x') as file:
            pkd(value, file) #type: ignore

#Used to easily fetch a single pickled variable in a specified file
#Use by calling EZPickle.load([name of the file where data is stored])
def _load(file, _filetype = "pickle", _returnType:type = dict) -> Any:
    if _filetype == "toml":
        with open(file, "rb") as f:
            return tomllib.load(f)
    elif _filetype == "pickle":
        try:
            with open(file, "rb") as filename:
                value = pkl(filename)
            return value
        except FileNotFoundError as fnfe:
            print(f"{file}: FileNotFoundError(Excepted): Failed to load data, no file currently present. To continue, you must create a new one")
            if not input("Handle the error? >[Y/n, default n] >").lower() == 'y': raise fnfe
            datatypeNames: dict[str, type] = {
                "str": str,
                "int": int,
                "bool": bool,
                "list": list,
                "dict": dict,
                "set":  set,
                "none": type(None),
            }
            print("Data type names: ", datatypeNames)
            dt = input('What data type do you want to use >')
            datatype = datatypeNames[dt] 
            value = datatype(input("What value do you want to put in (it will make a string to the datatype conversion) >"))
            with open(file, "xw") as f:
                pkd(value, f)
        
        except EOFError:
            print("File data error, resetting propereties to default...")
            input("Press Enter to continue, but if you wish to preserve the file data, hit Ctrl+C to exit. >")
            open(file, "w")
            with open(file, "wb") as filename:
                pkd(False, filename)
            return False
    return False

class FileManager():
    save = _save
    load = _load
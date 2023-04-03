from pickle import dump as pkd, load as pkl
import tomllib
from typing import Any
from os import getcwd

#Used to easily pickle/save a single variable in a particular file
#Use by calling EZPickle.save([variable you wish to save], [file you wish to save it in])
#If you want to save multiple variables, then learn to get creative with lists/dictionaries/tuples
def save(value, filename) -> None:
    try:    
        with open(filename, "wb") as file:
            pkd(value, file)
    except FileNotFoundError as fnfe:
        with open(filename, 'x') as file:
            pkd(value, file) #type: ignore


def load(file, _filetype = "pickle", _returnType:type = Any, _defaultValue=None) -> Any:
    """
    Used to easily fetch a single pickled variable in a specified file
    Use by calling FileManager.load([name of the file where data is stored])
    If no file is found and no default value is set, it will ask the user to handle the error.
\n    You can fetch variables from other supported file types, like TOML files. Specify if so in _filetype.
\n    You can add a type checker to block any unallowed values from entering. Set _returnType to the value to set the intended return value, 
or leave it empty to let any value in.
\n    If a file is not found, you can set a default value to handle the error auto matically and return the default. Use by setting
_defaultValue to whatever you wish. It does not have to follow the return typegh c
    """
    if _filetype == "toml":
        with open(file, "rb") as f:
            return tomllib.load(f)
    elif _filetype == "pickle":
        try:
            with open(file, "rb") as filename:
                value = pkl(filename)
                if not type(value) == _returnType: raise ValueError(
                    f"{file} returned an unallowed value {value} and was blocked. If this is intended, change _returnType from {_returnType} to {type(value)} or Any")
            return value
        except FileNotFoundError as fnfe:
            if not _defaultValue == None: return _defaultValue
            print(f"{file}: FileNotFoundError(Excepted): Failed to load data, no file currently present. To continue, you must create a new one")
            if not input("Handle the error? >[Y/n, default n] >").lower() == 'y': raise fnfe
            if _returnType == Any:
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
            else: datatype = _returnType
            value = datatype(input(f"What value do you want to put in (it will make a string to the datatype conversion) \nData type conversion: str -> {datatype} >"))
            with open(file, "w") as f:
                pkd(value, f) # type: ignore
        
        except EOFError:
            print("File data error, resetting propereties to default...")
            input("Press Enter to continue, but if you wish to preserve the file data, hit Ctrl+C to exit. >")
            open(file, "w")
            with open(file, "wb") as filename:
                pkd(False, filename)
            return False
    return False

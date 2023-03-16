from pickle import dump as pkd, load as pkl
import tomllib
from os import getcwd

#Used to easily pickle/save a single variable in a particular file
#Use by calling EZPickle.save([variable you wish to save], [file you wish to save it in])
#If you want to save multiple variables, then learn to get creative with lists/dictionaries/tuples
def save(value, filename):
    try:    
        with open(filename, "wb") as file:
            pkd(value, file)
    except FileNotFoundError as fnfe:
        with open(filename, 'x') as file:
            pkd(value, file) #type: ignore

#Used to easily fetch a single pickled variable in a specified file
#Use by calling EZPickle.load([name of the file where data is stored])
def load(file, type = "pickle", programPath=getcwd()) -> dict | bool:
    if type == "toml":
        with open(file, "rb") as f:
            return tomllib.load(f)
    elif type == "pickle":
        try:
            with open(file, "rb") as filename:
                value = pkl(filename)
            return value
        except FileNotFoundError:
            print(f"{file}: FileNotFoundError(Excepted): Failed to load data, no file currently present. Creating a new one...")
            open(file, "x")
            with open(file, "wb") as filename:
                pkd(False, filename)
            return False
        except EOFError:
            print("File data error, resetting propereties to default...")
            open(file, "w")
            with open(file, "wb") as filename:
                pkd(False, filename)
            return False
    return False
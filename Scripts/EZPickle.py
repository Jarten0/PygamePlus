from pickle import dump as pkd
from pickle import load as pkl

for i in range(1):
    #Used to easily pickle/save a single variable in a particular file
    #Use by calling EZPickle.save([variable you wish to save], [file you wish to save it in])
    #If you want to save multiple variables, then learn to get creative with lists/dictionaries
    def save(value, file):
        try:    
            with open(file, "wb") as filename:
                pkd(value, filename)    
        except FileNotFoundError:
            file = open(file, "x")
            pkd(value, file)
    
    #Used to easily fetch a single pickled variable in a specified file
    #Use by calling EZPickle.load([name of the file where data is stored])
    def load(file, type = "pickle"):
        if type == "toml":
            with open(file, "rb") as f:
                return f
        elif type == "pickle":
            try:
                with open(file, "rb") as filename:
                    value = pkl(filename)
                return value
            except FileNotFoundError:
                print("Failed to load data: No file currently present. Creating a new one...")
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
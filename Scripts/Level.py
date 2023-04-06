""" Is responsible for containing all of a room's data
"""

class level:
    def __init__(self, levelName:str, plat: dict, length: int = 20000, height: int = 20000) -> None:
        self.name = levelName
        self.plat = plat
        self.length = length
        self.height = height

def new(name:str, length:int, height:int) -> level:
    return level(levelName=name, plat={}, length= length, height=height)

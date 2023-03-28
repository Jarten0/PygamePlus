class Level():
    """ Is responsible for containing all of a room's data
    """
    @classmethod
    def createNewLevel(cls, name:str, length:int, height:int) -> None:
        return cls.initialize(cls(), levelName=name, plat={}, length= length, height=height)

    def initialize(self, levelName:str, plat: dict, length: int = 20000, height: int = 20000):
        self.name = levelName
        self.plat = plat
        self.length = length
        self.height = height

    def __init__(self) -> None:
        pass
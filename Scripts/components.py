# self. = kwargs[""]

#Handles all positioning aspects of an object in world space
class Transform():
    def __init__(self, **kwargs) -> None:
        self.xPosition = kwargs["x"]
        self.yPosition    = kwargs["y"]
        self.z = kwargs["z"]
        self.xVelocity = kwargs["xVelocity"]
        self.yVelocity = kwargs["yVelocity"]
        self.zVelocity = kwargs["zVelocity"]


#Used to check as to whether the selected item is colliding with the object
#This will NOT handle collisions, incase it should be used as a collisionless trigger that has an
#activation area. If you want to add collisions, use this in tangent with RigidBody
class Collider():
    def __init__(self, **kwargs) -> None:
        self.xLength = kwargs["xLength"]
        self.yLength = kwargs["yLength"]

    def check(self, item) -> list[bool, bool, bool, bool, bool]:
        lis = [False, False, False, False, False]
        if not item.yPosition    + item.yLength >= self.yPosition and item.yPosition <= self.yPosition + self.yLength and item.xPosition + item.xLength >= self.xPosition and item.xPosition <= self.xPosition + self.xl:
            return lis
        
        lis[0] = True
        #
        if item.yPosition + item.yLength   < self.yPosition + 10 and item.xPosition + item.xLength     > self.xPosition and item.xPosition < self.xPosition + self.xl:
            lis[1] = True
        #
        if item.xPosition + item.xLength   < self.xPosition + 20 and item.yPosition + item.yLength - 5 > self.yPosition and item.yPosition < self.yPosition + self.yl:
            lis[2] = True
        #
        if item.yPosition > self.yPosition + self.yLength - 10   and item.xPosition + item.xLength     > self.xPosition and item.xPosition < self.xPosition + self.xl:
            lis[3] = True
        #
        if item.xPosition > self.xPosition + self.xLength - 20   and item.yPosition + item.yLength - 5 > self.yPosition and item.yPosition < self.yPosition + self.yl:
            lis[4] = True         
        
        return lis


#Used to handle collisions and other physical forces
#Use with a Collider to properly collide with other objects that have Colliders 
class RigidBody():
    dependancies = {
        "Transform",
        "Collider",
    }
    def __init__(self, **kwargs) -> None:
        self.mass = kwargs["mass"]
        
    
    def check(self, item) -> list[bool, bool, bool, bool, bool]:
        lis = [False, False, False, False, False]
        if not item.yPosition    + item.yLength >= self.yPosition and item.yPosition <= self.yPosition + self.yLength and item.xPosition + item.xLength >= self.xPosition and item.xPosition <= self.xPosition + self.xl:
            return lis
        
        lis[0] = True
        #
        if item.yPosition + item.yLength   < self.yPosition + 10 and item.xPosition + item.xLength     > self.xPosition and item.xPosition < self.xPosition + self.xl:
            lis[1] = True
        #
        if item.xPosition + item.xLength   < self.xPosition + 20 and item.yPosition + item.yLength - 5 > self.yPosition and item.yPosition < self.yPosition + self.yl:
            lis[2] = True
        #
        if item.yPosition > self.yPosition + self.yLength - 10   and item.xPosition + item.xLength     > self.xPosition and item.xPosition < self.xPosition + self.xl:
            lis[3] = True
        #
        if item.xPosition > self.xPosition + self.xLength - 20   and item.yPosition + item.yLength - 5 > self.yPosition and item.yPosition < self.yPosition + self.yl:
            lis[4] = True         
        
        return lis
        

#Renders an object either via image or rectangle
class Renderer():
    dependancies = {
        "Transform",
    }

    def __init__(self, **kwargs) -> None:
        self.log = []
        try:
            self.xLength = kwargs["xLength"]
            self.yLength = kwargs["yLength"]
        except KeyError as ke:
            self.log.append("length variables missing. add length variable to paramaters of the initializer")

        self.xOffset = kwargs["xOffset"]
        self.yOffset = kwargs["yOffset"]
        self.path = kwargs["path"]
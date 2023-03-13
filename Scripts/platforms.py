import Scripts.timer as Timer
import Scripts.boards as Boards
#from main import kill
platcolors = {
    0: (0,   0,   0),
    1: (0,   255, 0),
    2: (50,  50,  0),
    3: (255, 0,   0),
    4: (255, 150, 0),
    
}

placeprop = {
    0: {
        "#HasPlaceReq": False,
        "#object": False,},
    1: {
        "#HasPlaceReq": False,
        "#object": False,},
    2: {
        "#HasPlaceReq": True,
        "xl": False,
        "yl": 7,
        "#object": False,},
    3: {
        "#HasPlaceReq": True,
        "xl": False,
        "yl": False,
        "#object": False,},
    4: {
        "#HasPlaceReq": True,
        "xl": 30,
        "yl": 10,
        "#object": True},
}

#Finds next available ID for platform listing, so that when a platform gets
#deleted, that spot is detected and used instead of never getting used
def NextID(platformList) -> int:
    keylist = platformList.keys()
    #print(keylist, platformList)
    for i in range(len(platformList)):
        if not i in keylist:
            name = i
            return name
    return len(platformList)

class create():
    def __init__(self, x, y, xl, yl, type = 0) -> None:
        self.x = x
        self.y = y
        self.xl = xl
        self.yl = yl
        self.type = type
        self.color = platcolors[self.type]


    def collider(self, item) -> list[bool]:
        lis = [False, False, False, False, False]
        if item.y + item.yl >= self.y and item.y <= self.y + self.yl:
            if item.x + item.xl >= self.x and item.x <= self.x + self.xl:
                lis[0] = True
                if item.y + item.yl < self.y + 10 and item.x + item.xl > self.x and item.x < self.x + self.xl:
                    lis[1] = True
                if item.x + item.xl < self.x + 20 and item.y + item.yl - 5 > self.y and item.y < self.y + self.yl:
                    lis[2] = True
                if item.y > self.y + self.yl - 10 and item.x + item.xl > self.x and item.x < self.x + self.xl:
                    lis[3] = True
                if item.x > self.x + self.xl - 20 and item.y + item.yl - 5> self.y and item.y < self.y + self.yl:
                    lis[4] = True         
        return lis

    

class collision():
    #C = Character, P = Platform, L = Length
    def check(self, cx, cy, cxl, cyl, px, py, pxl, pyl) -> list[bool]: #Checks
        lis = [False, False, False, False, False]
        if cy + cyl >= py and cy <= py + pyl:
            if cx + cxl >= px and cx <= px + pxl:
                lis[0] = True
                if cy + cyl < py + 10 and cx + cxl > px and cx < px + pxl:
                    lis[1] = True
                if cx + cxl < px + 20 and cy + cyl - 5 > py and cy < py + pyl:
                    lis[2] = True
                if cy > py + pyl - 10 and cx + cxl > px and cx < px + pxl:
                    lis[3] = True
                if cx > px + pxl - 20 and cy + cyl - 5> py and cy < py + pyl:
                    lis[4] = True         
                #print(lis, " | ", cx, cy, cxl, cyl, px, py, pxl, pyl)  
        return lis

class types():
    def wall(self, prop) -> None:
        wallcheck = prop["wallcheck"]
        char = prop["char"]
        pTBC = prop["platformToBeChecked"]
        if wallcheck[1]:       
            char.gr = True
            char.y = pTBC.y - char.yl  
            char.yv = 0
            #Timer.set("dashcool", True)
            Timer.set("CoyoteTime", 0, True)
        
        #Left
        if wallcheck[2]:
            char.x = pTBC.x - char.yl
            if Timer.get("grace", True) > 5:
                char.xv = 0
        else:
            Timer.set("grace", 0, True)
        #Bottom
        if wallcheck[3]:
            char.yv = 0
            char.y = pTBC.y + pTBC.yl
        #Right
        if wallcheck[4]:
            char.x = pTBC.x + pTBC.xl                
            if Timer.get("grace", True) > 5:
                char.xv = 0
        else:
            Timer.set("grace", 0, True) 

        if wallcheck[2] or wallcheck[4]:
                char.wj = True
                char.w = [wallcheck[2], wallcheck[4]]
    
    def passthrough(self, prop) -> None:
        wallcheck = prop["wallcheck"]
        char = prop["char"]
        pTBC = prop["platformToBeChecked"]
        if wallcheck[1]:
            if char.yv >= 0 and not Boards.getFromPerm("down"):           
                char.gr = True
                char.y = pTBC.y - char.yl  
                char.yv = 0
                #Timer.set("dashcool", True)
                Timer.set("CoyoteTime", 0, True)

    def lava(self, prop) -> None:
        if prop["wallcheck"][0]:
            prop["char"].die()
    
    def bounce(self, prop) -> None:
        char = prop["char"]
        if prop["wallcheck"][0]:
            char.resetDash()
            char.yv = -22
            if char.xv > char.speed:
                char.xv = char.speed
            elif char.xv < -char.speed:
                char.xv = -char.speed     
            
    functionList = {
        1: wall,
        2: passthrough,
        3: lava,
        4: bounce,
    }
                   
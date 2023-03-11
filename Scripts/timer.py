from main import NextID

UpList = {}
DownList = {}

def tick() -> None:
    for i in UpList:
        UpList[i] += 1
    for i in DownList:
        if not DownList[i] == True:
            DownList[i] -= 1
        if DownList[i] == 0:
            DownList[i] = True

def set(name = None, value = None, up = None) -> None:
    if value == None or not up == True:
        DownList[name] = value
        return

    if name == None:
        name = NextID(UpList)

    if value == None:
        value = 0

    UpList[name] = value
    return

def get(name, up = False) -> bool:
    if up:
        return UpList[name]
    if DownList[name] == True:
        return True 
    else:
        return False

def getvalue(name, up) -> int:
    if up:
        return UpList[name]
    return DownList[name]

def __str__() -> None:
    print("Current Timers:")
    for i in UpList:
        print(UpList)
        print(i,":", UpList[i])
    for i in DownList:
        print(i,":", DownList[i])
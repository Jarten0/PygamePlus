def _NextID(itemList:dict, name:str='') -> str:
    keylist = itemList.keys()
    for i in range(len(itemList)):
        if not name+str(i) in keylist:
            return name+str(i)
    return name+str(len(itemList))

_UpList = {}
_DownList = {}

def _tick() -> None:
    for i in _UpList:
        _UpList[i] += 1
    for i in _DownList:
        if not _DownList[i] == True:
            _DownList[i] -= 1
        if _DownList[i] == 0:
            _DownList[i] = True

def _set(name = None, value = None, up = None) -> None:
    if value == None or not up == True:
        _DownList[name] = value
        return

    if name == None:
        name = _NextID(_UpList)

    if value == None:
        value = 0

    _UpList[name] = value
    return

def _get(name, up = False) -> bool:
    if up:
        return _UpList[name]
    if _DownList[name] == True:
        return True 
    else:
        return False

def _getvalue(name, up) -> int:
    if up:
        return _UpList[name]
    return _DownList[name]

def ___str__() -> None:
    print("Current Timers:")
    for i in _UpList:
        print(_UpList)
        print(i,":", _UpList[i])
    for i in _DownList:
        print(i,":", _DownList[i])

class Timer():
    set = _set
    get = _get
    getValue = _getvalue
    tick = _tick
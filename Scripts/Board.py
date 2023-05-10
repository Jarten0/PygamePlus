from typing import Any
_temp: dict[str|int, Any] = {}
_perm: dict[str|int, Any] = {
    "jump": False,
    "jumpbuffer": 5,
    "left": False,
    "right": False,
    "up": False,
    "down": False,
    "dash": False,
    "dashcool": 0,
    "EXIT": False,
    "RESTART": False,
}

def _appendToTemp(value, key: str|None = None) -> str | int:
    if not key == None:
        try:
            _temp[key] = value
            return key
        except KeyError:
            _temp[len(_temp)] = value
            return len(_temp) - 1    
    else:
        _temp[len(_temp)] = value
        return len(_temp) - 1

def _appendToPerm(value, key: str|None = None) -> str | int:
    if not key == None:
        try:
            _perm[key] = value
            return key
        except KeyError:
            _perm[len(_perm)] = value
            return len(_perm) - 1    
    else:
        _perm[len(_temp)] = value
        return len(_perm) - 1

def _getFromTemp(key):
    return _perm[key]

def _getFromPerm(key):
    return _perm[key]

class Boards():
    appendToTemp = _appendToTemp
    appendToPerm = _appendToPerm
    getFromTemp = _getFromTemp
    getFromPerm = _getFromPerm 
temp = {}
perm = {
    "jump": False,
    "jumpbuffer": 5,
    "left": False,
    "right": False,
    "up": False,
    "down": False,
    "dash": False,
    "dashcool": 0,
}

def apT(value, key = None):
    if not key == None:
        try:
            temp[key] = value
            return key
        except KeyError:
            temp[len(temp)] = value
            return len(temp) - 1    
    else:
        temp[len(temp)] = value
        return len(temp) - 1
def apP(value, key = ""):
    if not key == None:
        try:
            perm[key] = value
            return key
        except KeyError:
            perm[len(temp)] = value
            return len(perm) - 1    
    else:
        perm[len(temp)] = value
        return len(perm) - 1
def getT(key):
    return perm[key]
def getP(key):
    return perm[key]
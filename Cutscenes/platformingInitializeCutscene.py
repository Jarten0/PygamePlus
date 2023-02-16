length = 10


def start(prop) -> None:
    print("Hello World!")
    prop["cam"].ypos = 0
    prop["char"].dead = False

def update(prop) -> None:
    prop["char"].yv = 50
    

def end(prop) -> None:
    prop["char"].allowControl = True
    print("Ended")

def startCheck(prop) -> bool or dict:
    if prop["char"].dead == True:
        return True
    return False


def endCheck(prop) -> bool:
    if prop["char"].y > 3500:
        return True
    return False
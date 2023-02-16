def start(prop) -> None:
    pass

def update(prop) -> None:
    pass

def end(prop) -> None:
    pass

def startCheck(prop) -> bool or dict:
    return {
        "trigger": False,
        "triggerHitbox": {
            "x": 0,
            "y": 0,
            "xl": 0,
            "yl": 0,
            }
        }

def endCheck(prop) -> bool:
    return False

from Scripts import Input
from typing import Any

xPosition = 0
yPosition = 0

class _cam():
    _Settings: Any
    _xOffset: float
    _yOffset: float
    _Transform: Any
    _level: Any
    _focusPointTransform: Any

    @classmethod
    def _init(cls) -> None:
        import main
        from main import settings, Object#, level
        from Scripts.Components.components import Transform
        _cam._Settings = settings
        _cam._xOffset = 0
        _cam._yOffset = 0
        # _cam._level = level
        _cam._Transform = Object.new('Transform', Transform)
        _cam._focusPointTransform = Object.new('Transform', Transform)

def setFocusPoint(_obj:object|None = None, xPos:float=0, yPos:float=0):
    if isinstance(_obj, type(None)):
        _cam._focusPointTransform.xPosition = xPos
        _cam._focusPointTransform.yPosition = yPos
    else:
        _cam._focusPointTransform = _obj

def update() -> None:
    if Input.getHeld("LEFT"):
        _cam._xOffset -= 10
    elif Input.getHeld("RIGHT"):
        _cam._xOffset += 10
    if Input.getHeld("UP"):
        _cam._yOffset -= 10
    elif Input.getHeld("DOWN"):
        _cam._yOffset += 10

    if Input.getHeld("up") or Input.getHeld("down") or Input.getHeld("left") or Input.getHeld("right"):
        _xOffset = 0
        _yOffset = 0



    # _xSpeed = _cam._Transform.xVelocity
    # _xPosition = _cam._focusPointTransform.xPosition + _cam._xOffset
    # _yPosition = _cam.ydefault + _cam._yOffset

    
    # if _xPosition < 0:
    #     _xPosition = 0
    # elif _xPosition > _cam._level.xLength - _cam._Settings['screen_width']:
    #     _xPosition = _cam._level.xLength - _cam._Settings['screen_width']

def get() -> tuple[int|float, int|float]:
    return (_cam._Transform.xPosition, _cam._Transform.yPosition)

def init() -> None:
    _cam._init()

import pygame as pyg
import Scripts.Components.components as MainComponent
import Scripts.Components.character  as CharacterComponent
from Scripts.timer          import Timer
from Scripts.boards         import Boards
from Scripts.inputMapper    import Input
from main   import *

class _cam():
    _Settings = Settings
    _xOffset:float = 0
    _yOffset:float = 0
    _level:  Any|None = level
    _focusPointTransform = Object.new()
    
def _setFocusPoint(_obj:object|None = None, xPos:float=0, yPos:float=0):
    if isinstance(_obj, type(None)):
        _cam._focusPointTransform.xPosition = xPos
        _cam._focusPointTransform.yPosition = yPos
    else:
        _cam._focusPointTransform = _obj

def _update() -> None:
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


    
    _xPosition = _cam._focus + _cam._xOffset
    _yPosition = _cam.ydefault + _cam._yOffset

    
    if _xPosition < 0:
        _xPosition = 0
    elif _xPosition > _cam._level.xLength - _cam._Settings['screen_width']:
        _xPosition = _cam._level.xLength - _cam._Settings['screen_width']




class Camera():
    init = _init
    update = _update
    setFocusPoint = _setFocusPoint
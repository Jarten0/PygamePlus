import pygame as pyg
import Scripts.Components.components as MainComponent
from Scripts.timer import Timer
from Scripts.boards import Boards
from Scripts.inputMapper  import Input
from Scripts.componentManager import ComponentTools as comTools

@comTools.newClass
class devTools():

    def create(self): pass
        
    @comTools.init #type: ignore
    def initialize__(self) -> None:
        pass
# pyright: reportGeneralTypeIssues=false

from Scripts.Components.Collider import Collider
from main import Component, newPrefab
from Scripts.Components.components import Transform

@newPrefab
class Platform:
    def init(self):
        self.Transform = self.newObject("components\\Transform")
        self.Collider  = self.newObject("components\\Collider")
        return {
            'Transform': Transform,
            'Collider': Collider
        }
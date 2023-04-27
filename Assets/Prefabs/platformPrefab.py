from Scripts.Components.Collider import Collider
from main import Component, newPrefab
from Scripts.Components.components import Transform

@newPrefab
class Platform:
    def init(self):
        self.Transform = Component.new("components\\Transform")
        self.Collider  = Component.new("components\\Collider")
        return {
            'Transform': Transform,
            'Collider': Collider
        }
from main import Component, newPrefab, newComponent

@newPrefab
class ButtonObj: # type: ignore
    def init(self):
        Transform = Component.new("components\\Renderer")
        Renderer = Component.new("Renderer\\Renderer")
        Collider = Component.new("Collider\\Collider")

        return {
            "Transform": Transform,
            "Renderer": Renderer,
            "Collider": Collider
        }

@newComponent
class Button:
    def init(self, components):
        self.Renderer = components['Renderer']

@newPrefab
class devInterface(): pass

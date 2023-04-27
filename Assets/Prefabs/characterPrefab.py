from main import Component, newPrefab

@newPrefab
class Character():
    def init(self) -> object:
        ConfigData = Component.new('components\\ConfigData',
            dirFileName = 'CharacterProperties',
            fileType = "toml"
            )
        Transform = Component.new('components\\Transform',
            xPos=ConfigData.configFile["body"]["xpos"],     # type: ignore
            yPos=ConfigData.configFile["body"]["ypos"],     # type: ignore
            zPos=ConfigData.configFile["body"]["zpos"],     # type: ignore
            )
        Renderer = Component.new('components\\Renderer',
            Transform = Transform,  
            xOffset=0,
            yOffset=0,
            xLength=20,
            yLength=20,
            path="\\Assets\\Images\\hehe.png",
            tier=5,
            )
        Collider = Component.new('components\\Collider',
            Transform = Transform,    
            xLength = 20,
            yLength = 20,
            )
        RigidBody = Component.new('components\\RigidBody',
            Transform = Transform,    
            Collider = Collider,    
            mass = 5,
            )
        return {
            'ConfigData': ConfigData,
            'Transform': Transform,
            'Renderer': Renderer,
            'Collider': Collider,
            'RigidBody': RigidBody
            }
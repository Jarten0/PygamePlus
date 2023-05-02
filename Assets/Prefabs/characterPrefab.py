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
        Renderer = Component.new('Renderer\\Renderer',
            Transform = Transform,  
            color = (255, 0,0),
            xOffset=0,
            yOffset=0,
            xLength=50,
            yLength=20,
            path="\\Assets\\Images\\hehe.png",
            tier=5,
            )
        Collider = Component.new('Collider\\Collider',
            Transform = Transform,
            xLength = 0,
            yLength = 20,
            )
        RigidBody = Component.new('Collider\\RigidBody',
            Transform = Transform,    
            Collider = Collider,    
            mass = 5,
            )
        Character = Component.new('character\\Character',
            ConfigData = ConfigData,    
            Transform = Transform,      
            Renderer  = Renderer,      
            Collider  = Collider,      
            RigidBody = RigidBody,
        )
        return {
            'Character': Character,
            'ConfigData': ConfigData,
            'Transform': Transform,
            'Renderer': Renderer,
            'Collider': Collider,
            'RigidBody': RigidBody
            }
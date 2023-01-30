class defaultPropereties(): 
    lis = {
    "scwd": 1000,
    "schi": 1000,
    "bgcol": (100, 100, 255),
    "fps": 240,
    "renderfps": 60,
    "grid": 10,
    "Coyote Time": 10,
    }
    def __init__(self, lis):
        self.lis = lis
        print(lis)
        #Screen -----------------------------------------------
        self.screen_width = lis["scwd"]
        self.screen_height = lis["schi"]
        self.bg_color = lis["bgcol"]
        self.grid = lis["grid"]
        
        
        #Clock ------------------------------------------------
        self.fps = lis["fps"]
        self.renderfps = lis["renderfps"]
        self.game_timer = 0
        self.total_ticks = 0

        #Colors -----------------------------------------------
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        #Character
        self.coyoteTime = lis["Coyote Time"]

        #Misc
        self.SceneType = "main"
import pygame as pyg
input = {
#To add or modify an input, simply add or modify a string in the array
#Keybinds for dev tools (save, load, etc.) are currently not modifiable
#If your keybind does not have an entry in the keybindlist, add it in the next list below
#Example line: 
#  "action": ["input", "optional input", "optional input"]
    "up":    ["w",     ], 
    "left":  ["a",     ], 
    "right": ["d",     ],
    "down":  ["s",     ], 
    "jump":  ["k",     ], 
    "dash":  ["o",     ], 
    "LEFT":  ["LEFT",  ], 
    "RIGHT": ["RIGHT", ], 
    "UP":    ["UP",    ], 
    "DOWN":  ["DOWN",  ],
    }
inputKeys = input.keys()   
        


keyBindList = {
    #If you wish to use a button not displayed here, add it by following the examples shown
    #Use pygame documentation if you need to add a unique button
        "a": pyg.K_a,
        "b": pyg.K_b,
        "c": pyg.K_c,
        "d": pyg.K_d,
        "e": pyg.K_e,
        "f": pyg.K_f,
        "g": pyg.K_g,
        "h": pyg.K_h,
        "i": pyg.K_i,
        "j": pyg.K_j,
        "k": pyg.K_k,
        "l": pyg.K_l,
        "m": pyg.K_m,
        "n": pyg.K_n,
        "o": pyg.K_o,
        "p": pyg.K_p,
        "q": pyg.K_q,
        "r": pyg.K_r,
        "s": pyg.K_s,
        "t": pyg.K_t,
        "u": pyg.K_u,
        "v": pyg.K_v,
        "w": pyg.K_w,
        "x": pyg.K_x,
        "y": pyg.K_y,
        "z": pyg.K_z,

        "0": pyg.K_0,
        "1": pyg.K_1,
        "2": pyg.K_2,
        "3": pyg.K_3,
        "4": pyg.K_4,
        "5": pyg.K_5,
        "6": pyg.K_6,
        "7": pyg.K_7,
        "8": pyg.K_8,
        "9": pyg.K_9,

        "LEFT": pyg.K_LEFT,
        "RIGHT": pyg.K_RIGHT,
        "UP": pyg.K_UP,
        "DOWN": pyg.K_DOWN,
        "SHIFT": pyg.K_LSHIFT,
        "SPACE": pyg.K_SPACE,
        "TAB": pyg.K_TAB,
        "BACKSPACE": pyg.K_BACKSPACE,
        "`": pyg.K_RALT
        
        }
#================================================================================================
#===== FURTHER CODE SHOULD NOT BE MODIFIED IF YOU ONLY WISH TO CHANGE KEYBINDS ==================
#================================================================================================
def k(input, events):
    for event in events:
        if event.type == pyg.KEYDOWN:
            if event.key == keyBindList[input]:
                return True
            else:
                return False
        else:
            return False

def kh(input, events):
    if events[keyBindList[input]]:
        return True
    else:
        return False
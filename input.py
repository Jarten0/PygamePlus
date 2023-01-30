import pygame as pyg
defaultInputs = {
#To add or modify an input, simply add or modify a string in the array
#Keybinds for dev tools (save, load, etc.) are currently not modifiable
#If your keybind does not have an entry in the keybindlist, add it in the next list below
#Example line: 
#  "action": ["input", "optional input", "optional input"]
    "up":    ["w",     ], 
    "left":  ["a",     ], 
    "down":  ["s",     ], 
    "right": ["d",     ],
    "jump":  ["k",     ], 
    "dash":  ["o",     ], 
    "UP":    ["UP",    ], 
    "LEFT":  ["LEFT",  ], 
    "DOWN":  ["DOWN",  ],
    "RIGHT": ["RIGHT", ], 
    }
defaultInputKeys = defaultInputs.keys()   
        
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
keyBindListKeys = keyBindList.keys()
#================================================================================================
#===== FURTHER CODE SHOULD NOT BE MODIFIED IF YOU ONLY WISH TO CHANGE KEYBINDS ==================
#================================================================================================
def k(input, events):
    for event in events:
        if event.type == pyg.KEYDOWN:
            if event.key == keyBindList[input]:
                print(input)
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


def main():
    import EZPickle as FileManager
    mappedInputs = FileManager.load('Save Data/input mappings.dat')
    if mappedInputs== False:
        mappedInputs = defaultInputs
    
    stop = False
    Info = """
    This program is a script intended on being used to adjust what keybinds are to correlate to whichever actions are best suited in the user's preference
    Or frankly, a keybinding configuration script to allow you to add however many buttons on your keyboard to whatever actions you want
    To be more specific, you can bind as many buttons as you want to any particular action, and you can add buttons that can do multiple actions at once (at the exact same time, delays between actions are still on you)
    Now, the way Pygame works can cause some confusion as to how keybinds are set and the process of setting up many keybinds grows increasingly tedious
    So not all buttons on any particular keyboard will be set up. Instead, I've opted to focus on some of the more used ones.
    This shouldn't cause too many problems with simple keybind setups, but more advanced ones may require use of some buttons not currently set up.
    If a button in particular would be useful, you can either open input.py with a text editor and try to figure it out using some of the comments I've provided
    Or send me a message on Discord ( Jarten#4513 ). I'll be adding some more bindings as development continues. 
    But for now, all letters, arrows and row numbers are available, alongside a few random extra ones I've used in development.
    
    NOTE: when it comes to ACTIONS, the lowercase directions are for movement, WHILE THE UPPERCASE DIRECTIONS ARE FOR CAMERA MOVEMENT
        and when it comes to buttons, LEFT, RIGHT, UP, and DOWN are for arrow keys
        sorry for screaming, just thought it would help correlate the difference between the two actions better

    ALSO NOTE: Some keybinds are used for development! It would not be ideal to use some of the selected buttons while dev mode is on.
        It should be off by default, but you can always toggle it by pressing TAB.

    This program works by selecting one action, giving you a set of commands allowing you to change the buttons set to that one action
    To swap to the next action 
    
    Now for some command clairifications:
    'Add' will always put the new command at the top of the list, and 'Pop' will also always remove from the top of the list
    Keep that in mind if your constantly changing keybinds
    'Pop' is called the way it is since that is the name of the command for doing that action for an list/array in Python
    'Save' may not be guarunteed to work so make sure to check if it states whether saving was successful.
    'Reset' will reset the selected keybind back to default, not to blank. do 'pop' after if you want to clear
    when doing 'Add' or 'Remove', using 'list' can help figure out what text goes with what button since you can't really press ctrl to describe CTRL in text form

    Alright, that should do it. Leave a comment on GitHub or message me on Discord (again, Jarten#4513) if you have any suggestions


    SCROLL UP TO READ THE LARGE BLOCK OF TEXT
    """
    print("\n")
    print("Initialized input mapper.")
    print("\n")
    while True:
        if stop:
            break
        for i in defaultInputKeys:
            if stop:
                break
            while True:
                print("\n")
                word = ''
                for i2 in defaultInputKeys:
                    if i == i2:
                        word += ">"
                    word += i2 
                    word += " "
                print(word)
                print(f"Current action: {i}")
                print(f"Current keybinds set to {i}: {mappedInputs[i]}")
                print("Leave input blank and press enter to select next action")
                print("Type in a command or the number correlating to the below command")
                inputFromUser = input("Add: 1, Remove: 2, Pop: 3, Reset: 4, Save: 5, Exit: 6, Help: 7 \n> ")
                print("\n" * 7)
                if inputFromUser.lower() == "add" or inputFromUser == "1":
                    while True:
                        print("Extra commands: 'cancel', 'list': show available buttons you can use for keybindings")
                        inputFromUser = input("Add which letter/number? > ")
                        if inputFromUser == 'cancel':
                            break
                        elif inputFromUser == 'list':
                            print("Available input options: ", keyBindListKeys)
                        elif inputFromUser in keyBindListKeys:
                            print(f"Binded {inputFromUser} to {i}")
                            mappedInputs[i].append(inputFromUser)
                            break
                elif inputFromUser.lower() == "remove" or inputFromUser == "2":
                    while True:
                        print("Extra commands: 'cancel', 'list': show mapped buttons")
                        inputFromUser = input("Which mapping to remove? > ")
                        if inputFromUser == 'cancel':
                            break
                        elif inputFromUser == 'list':
                            print(f"Current mapped buttons to {i}: {mappedInputs[i]}")
                        elif inputFromUser in mappedInputs[i]:
                            print(f"Removed {inputFromUser} from {i}")
                            mappedInputs[i].remove(inputFromUser)
                            break
                elif inputFromUser.lower() == "pop" or inputFromUser == "3":
                    if len(mappedInputs[i]) > 0:
                        print(f"Removed {mappedInputs[i]} from the top of the list")
                        mappedInputs[i].pop()
                    else:
                        print(f"No buttons currently mapped to {i}")
                elif inputFromUser.lower() == "reset" or inputFromUser == "4":
                    print(f"Reset {i} to default bindings")
                    mappedInputs[i] = defaultInputKeys[i]
                elif inputFromUser.lower() == "save" or inputFromUser == "5":
                    print(f"Saving current progress...")
                    FileManager.save(mappedInputs, 'Save Data/input mappings.dat')
                    if mappedInputs == FileManager.load('Save Data/input mappings.dat'):
                        print("Saved successfully.")
                    else:
                        print("Save failure! Panic!")
                        print(mappedInputs, FileManager.load('Save Data/input mappings.dat'))
                elif inputFromUser.lower() == "exit" or inputFromUser == "6":
                    inputFromUser = input("Are you sure? [Y/n]> ")
                    if inputFromUser.upper() == "Y":
                        print("Exited input mapper. \n\n\n")
                        stop = True
                        break
                elif inputFromUser.lower() == "help" or inputFromUser == "7":
                    print(Info)
                elif inputFromUser == "next" or inputFromUser == "":
                    break
        
if __name__ == "__main__":
    main()


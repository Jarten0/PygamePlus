import EZPickle as FileManager
import platforms as platform
lis = {
"scwd": 1000,
"schi": 1000,
"bgcol": (100, 100, 255),
"fps": 240,
"renderfps": 60,
"grid": 10,
"Coyote Time": 10,
}
devpause = False
def cmd():
    devpause = True
    """
    from main import defaultPropereties
    while True:
        ans = input(">")
        if ans == "cv":
            ans = input("Name>")
            if ans in lis:
                lis[ans] = int(input("Value>"))
                p = defaultPropereties(lis)
                FileManager.save(p, 'prop.dat')
        if ans == "cf":
            ans = input("File:")
                    
        if ans == "exit" or ans == "" or ans == "z":
            return p
    """

def renderTempPlat(mousepos, mouseposx, mouseposy, tempx, tempy, select):
    for i in [0]:
        (abs(mousepos[0]) + mousepos[0])/2
        tempx2 = mouseposx
        tempy2 = mouseposy
        if tempx < tempx2:
            LTempx = tempx2
            STempx = tempx
        else:
            LTempx = tempx
            STempx = tempx2
        if tempy < tempy2:
            LTempy = tempy2
            STempy = tempy
        else:
            LTempy = tempy
            STempy = tempy2
        if LTempy - STempy < 10:
            temptype = 1
        else:
            temptype = 0

            if platform.placeprop[select]["#HasPlaceReq"]:
                if not platform.placeprop[select]["xl"] == False:
                    LTempx = platform.placeprop[select]["xl"]
                    STempx = 0
                if not platform.placeprop[select]["yl"] == False:
                    LTempy = platform.placeprop[select]["yl"]
                    STempy = 0

                pyg.draw.rect(screen, platform.platcolors[select], (STempx - cam.xpos, STempy - cam.ypos, LTempx - STempx, LTempy - STempy))

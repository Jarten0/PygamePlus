# Pygame-Platformer
Small Prototype for a platformer to test coding skills


This is a small project to test my coding skills in Python and to see what I can do
This platformer is simple. Still in development, infact. Sloppy behaviour, unpolished graphics, all the works.
But every aspect of it is coded using the engine Pygame, meaning that almost every aspect of it has been hardcoded, or written by hand by me.
The only things Pygame takes care of is displaying images to the screen, obtaining input, and a few small other things.
Everything else has been programmed by me. Pygame is more of a framework, anyway.
But enough talking, if you want to try it out yourself, your going to need to take care of a few things first.



# Installation
You need to have Python 3.10+ and Pygame installed to run this project.

To check if you have Python 
If you are using a Windows system, press Windows Key + R, then in the prompt type `cmd` and hit Enter. It will open up the Command Prompt.
Type `python --version`. If it is installed, it will tell you `Python x.x.x`, the x's being the version number. Most recently tested version is 3.11.1
If it is not installed, go to `https://www.python.org` and follow the download instructions there.

If you are on a Linux system, then you should know how to do this already. If not, lookitup. You should already be familiar with dealing with Windows users


To check if you have Pygame
For the Windows users, following the above instructions to open cmd, once you are there you can type `python`, hit Enter, and then type `import pygame` to test whether pygame is installed.
If you get an ImportError, then simply exit python by pressing Crtl+Z and pressing enter.
Now if you have Python v3.10.x or specific older versions, you can simply type `pip install pygame`, and it will install. 
However, for those on the more recent patch v3.11.x, you need to add --pre to the end, resulting in `pip install pygame --pre` in order to install a development release of Pygame.
Now try importing Pygame again
If you get this from the command prompt or similar then you have pygame installed and can run the script.
`pygame 2.1.3.dev8 (SDL 2.0.22, Python 3.11.1)`
`Hello from the pygame community. https://www.pygame.org/contribute.html`

Linux users, it's late for me and I don't want to go through this process for a whole different OS for the 5% of you guys. I trust you can deal with this on your own, and if not, my discord account is Jarten#4513 and you can yell at me there.



# Running the code
Now that you have all of the missing dependencies, it's time to run the file. Extract the .zip file, open it so that you can see all of the files inside of it, and copy the folder path.
Once you have it copied, open `cmd` using the above instructions and type `cd [paste the path here]` then hit enter.
Then type in `.\main.py` to run the file. It should be good to go!



# Playing the game
Took long enough to get here, but you did it! 
...it's kind of underwhelming, huh?

Use WASD to move, K to jump, and O to quickly dash in a direction.
You can use the mouse to place tiles, and you can press 1-4 to select what kind of tile to place. You can also press 0 to delete platforms you click on.

To make use of Dev Commands, press TAB. You can then press Z to save your level data, X to load the saved data, and C to clear the level. You can then press Q to quit

Oh also, if the set inputs aren't good, you can alter them by doing all of the same instructions in Running the code (aside from extracting it), and entering `.\input.py` instead of `.\main.py`. This will open the input mapper. Change them to your hearts content. Type help for more info when you're there.

Thats it. Enjoy!

I regularly release small updates in the dev branch on github, and save some of the more significant releases for the main branch. And DM me on discord (Jarten#4513) if you have anything to comment about this project.
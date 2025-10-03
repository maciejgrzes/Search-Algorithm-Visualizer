To run this program, the PyGame module needs to be installed as well as pygame_gui.
than simply run "python main.py" in terminal.

When you press "Solve Maze" twice on the same maze without generating a new one it throws an error, yeah i know im just not bothered enough to fix that for now ;)

Also feel free to use this code in your own projects


UPDATE READ THIS!!
The newest version of pygame_gui is clashing with the pygame module as it wants to use DIRECTION_LTR from pygame-ce (pygame's community edition) but since pygame doesnt have this it will error out HOWEVER when you install pygame-ce it will also error out this time becouse pygame-ce doesn't have the surface submodule now i don't know what is going on but editing pygame_gui/core/interfaces/colour_gradient_interface.py line 18 from pygame.surface.Surface to pygame.Surface seemed to work but i cannot guarantee it will work. I don't know what is going on with pygame and pygame_gui but i don't care enough so if you REALLY want to run this you will have to figure something out i'm done.
Maybe ill fix it but most likely not.

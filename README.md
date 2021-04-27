# Bootshuze-GUI
OBJ to XML converter for Spiral Knights. [Bootshuze](https://github.com/Puzovoz/Bootshuze) fork adding a graphical user interface.
Requires [SpiralView](https://github.com/lucas-allegri/spiralview/releases) for further model modification.

<img src="https://cdn.discordapp.com/attachments/594154423744200714/836598434180890624/unknown.png">

## Features

The script will:
  - Convert OBJ file's indices and vertices to XML format Spiral Knights uses.
  - Recognize the primitives mode the input file uses (lines, triangles, quads).
  - Calculate bounds for the model.
 
The script will NOT:
  - Change any data that can be changed with SpiralSpy after creation (material, texture, etc).
  - Normalize the model size. If the model is too big, you can scale it down in SpiralSpy by creating a new Compound model and using the model you just created as one of the assets.
  - Rotate the model. Can also be fixed by creating a Compound model.
  - Create new texture UV mapping. That should be done in any 3D model editor you're using.
  
## Getting started
  1. Download the latest release, and open either the .exe file or the .py file (the latter requires Python 3 with PySimpleGUI package installed).
  1. A simple interface window should appear. Select your OBJ model with "Browse" button.
  1. Press "Submit" and wait. The script should create an XML file inside the directory.
  1. With [SpiralView](https://github.com/lucas-allegri/spiralview/releases) open Model Viewer, Resource Editor (Ctrl+R), `File → Import from XML...` and point to the new XML you created with the script. That should provide info to the resource editor.
  1. Save the model (Ctrl+A) in any directory and open in the model viewer.
  
  Congratulations, you've imported a model and can create new mods with new models that never existed in the game before.

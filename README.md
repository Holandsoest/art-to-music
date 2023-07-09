# art-to-music

## Install

### Manual downloads  

Windows:

> 1. [Download ffmpeg](https://phoenixnap.com/kb/ffmpeg-windows)  
> 2. [Download Ghostscript](https://ghostscript.com/releases/gsdnld.html) *For GUI only*  
> 3. [Python 3.11.4](https://www.python.org/downloads/) (or up) **Do not forget to: '`Add to path`'**  
> 4. Reboot your pc...
> 5. Open the start-menu and type `powershell`, right click the blue icon and `run as administrator`  
> 6. `python3.11 -m pip install virtualenv && git clone https://github.com/Holandsoest/art-to-music.git && cd ./art-to-music && python3.11 -m venv .venv && source .venv/bin/activate && python3.11 -m pip install --require-virtualenv -r requirements.txt`

Debian-like-OS's (like Ubuntu) :

> 1. Open a terminal
> 2. `ctrl`+`shift`+`V` the following in the terminal: `sudo apt install ffmpeg ghostscript python3.11-dev python3.11-venv python3.11-tk fluidsynth && python3.11 -m pip install virtualenv && git clone https://github.com/Holandsoest/art-to-music.git && cd ./art-to-music && python3.11 -m venv .venv && source .venv/bin/activate && python3.11 -m pip install --require-virtualenv -r requirements.txt` to install everything. *This might take a while.*  

MacOS:
Is not supported.

### Nvidea Jetson Nano only  

- create a file in `art-to-music/files/enable_jetson_gpio.flag` to enable the GPIO (for the animations)  

## GUI

*(<ins>**G**</ins>raphical <ins>**U**</ins>ser <ins>**I**</ins>nterface) an interface where you can use the mouse.*  

If you do not have a webcam at hand there is also the fallback GUI that can be started by running `gui.py` instead of `main.py`.  
The `gui.py` will also automatically start if something went wrong with grabbing your webcam in `main.py`.  

### controls

The left of the GUI there is a pallet.  

- On the top of this pallet are some colors that you can drag to shapes already placed or click to select that color.
- Below that there are shapes that you can click and drag to the *art-area* whenever you grab an item from the pallet the item will be replenished.
- An item can be dragged back into the pallet to destroy it.

The center is the area that where you can create your art. The "Art-area" so to speak.

- You can drag and drop shapes to move them.
- **Press** '**R**' while hovering above the said shape **to rotate** the said shape.
- **Scroll** with the **mouse-wheel** or **Press** '**-**', '**+**', '**Q**', '**E**' while hovering above the said shape to **rescale** the said shape.
- The last touched shape will be on top, and the tools prefer to grab the smallest shapes.

The right of the GUI is the action-panel.

- Click "Play" to interpret art to music
- If the AI does not work for you, As it sometimes does not understand when things are too close to each other... Click "Play (without ai)" to interpret art to music in a more cheaty way
- Or just let the AI interpret your art by importing a file ('.PNG' is preferred)

### issues

When no shapes are placed, there will be no sound playing.  
For sound your default sound device will be used.  

After pressing play you might get the `"Bypassing ai..."` message if your system does not have `Ghostscript` installed. [Download Ghostscript](https://ghostscript.com/releases/gsdnld.html).  
Also only Windows and Linux are supported for this functionality.  

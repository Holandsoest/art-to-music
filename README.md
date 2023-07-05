# art-to-music

## Install

- [ffmpeg  Windows](https://phoenixnap.com/kb/ffmpeg-windows)  

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

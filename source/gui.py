#!/usr/bin/env python3
"""A library that covers how the GUI should respond / work

Use `app = Gui()` to get started.

In this version you cannot rotate & resize the shapes yet"""
# Want to learn about Tkinter gui tool? https://youtu.be/mop6g-c5HEY It coverers about everything. ;)
import common.shapes as shapes
import common.location as loc
import common.midi_creation
import common.midi_processing
import common.image_properties
import image_processing
import image_processing_ai
import multiprocessing as mp
import os
import cv2
import psutil
import numpy as np

from enum import Enum # Keep enums UPPER_CASE according to https://docs.python.org/3/howto/enum.html  
import math
import tkinter
from tkinter import ttk, filedialog

class PalletItem(Enum):
    """The pallet in on the left. This are the items that are on it."""
    NONE = -1
    YELLOW = 0
    ORANGE = 1
    RED = 2
    GREEN = 3
    PURPLE = 4
    BLUE = 5
    CIRCLE = 6
    HALF_CIRCLE = 7
    SQUARE = 8
    HEART = 9
    STAR = 10
    TRIANGLE = 11
    TRASH_CAN = 12
def pallet_item_to_rgb(pallet_item:PalletItem) -> tuple:
    """Returns the color in `tuple(int,int,int)` `0-255`"""
    match (pallet_item):
        case PalletItem.YELLOW: return (255,255,0)
        case PalletItem.ORANGE: return (255,165,0)
        case PalletItem.RED:    return (255,0,0)
        case PalletItem.GREEN:  return (0,255,0)
        case PalletItem.PURPLE: return (255,0,255)
        case PalletItem.BLUE:   return (0,0,255)
        case _:
            raise RuntimeError(f'{pallet_item.name} is not a color!')
def save_img(tkinter_canvas:tkinter.Canvas, path_filename:str, as_png=False, as_jpg=False, as_gif=False, as_bmp=False, as_eps=False) -> None:
    """Saves the `tkinter.Canvas` object as a image, on the location of `path_filename` as the chosen formats.
    
    ### WARNING this requires Ghostscript, please install https://ghostscript.com/releases/gsdnld.html, and restart your PC 
    - `tkinter_canvas` The canvas that has to be saved as an image.
    - `path_filename` The (absolute) path that point to the image file without the extension. Example:`r'C:\Program Files\my_project\my_folder_with_images\image_1'`
    - `as_###` The bool that can be true to export that file format. This allows multiple at once. At least one is required."""
    if not ( as_png or as_jpg or as_gif or as_bmp or as_eps ): raise UserWarning('Did not got any formats to save. I did not save anything.')

    # Create that directory if it does not exists yet
    parent_path = os.path.split(path_filename)[0] # 1 directory up
    if not os.path.exists(parent_path): os.makedirs(parent_path)


    from PIL import Image, ImageTk, EpsImagePlugin
    if as_eps:
        tkinter_canvas.postscript(file = path_filename + '.eps')
        img = Image.open(path_filename + '.eps')
    else:
        import io
        postscript = tkinter_canvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(postscript.encode('utf-8')))


    # Warning this requires Ghostscript that has to be installed manually on your operating system
    #
    # Error: `OSError: Unable to locate Ghostscript on paths`
    #
    # Official guide: https://ghostscript.com/docs/9.54.0/Install.htm
    #
    # My guide:
    # 1. CRY
    # 2. https://ghostscript.com/releases/gsdnld.html Just brrrr install this as x64
    # 3. This took me 5.5 hours :'(
    if psutil.WINDOWS:
        expected_install_location = r'C:\Program Files\gs\gs10.01.1\bin\gswin64c'
        if not os.path.exists(expected_install_location+'.exe'):
            raise RuntimeError(f'Missing Ghostscript files in: ({str(expected_install_location)}),\n Please install Ghostscript get it from the official website: (https://ghostscript.com/releases/gsdnld.html) to make photos of your Tkinter.Canvas')
    elif psutil.LINUX:
        expected_install_location = 'usr/bin/ghostscript'
        if not os.path.exists(expected_install_location):
            raise RuntimeError(f'Missing Ghostscript files in: ({str(expected_install_location)}),\n Please install Ghostscript get it from the official website: (https://ghostscript.com/releases/gsdnld.html) or if you are on Ubuntu or another Debian system please try: (`sudo apt install ghostscript`) to make photos of your Tkinter.Canvas')
    else:   raise RuntimeError('Missing implementations for this operating system of Ghostscript to take photos of your Tkinter.Canvas')
    EpsImagePlugin.gs_windows_binary = expected_install_location # This is the default location, Telling PIL that it should be here

    if as_png: img.save(path_filename + '.png', 'png')
    if as_gif: img.save(path_filename + '.gif', 'gif')
    if as_bmp: img.save(path_filename + '.bmp', 'bmp')
    if as_jpg: img.save(path_filename + '.jpg', 'JPEG')  

class Gui(tkinter.Tk):
    """This is the whole GUI of the art-to-music application. And is of course separate standalone from the real webcam/camera implementation.
    
    `app.mainloop()` to run it (blocking, will continue after `alt + F4` was pressed)"""
    def __init__(self) -> None:
        super().__init__()
        self.title('art-to-music | R to rotate | scroll to resize | drag to place')
        self.minsize(width=528,height=360)

        # Declare objects
        self.canvas = MainCanvas(master=self, background_color='white')
        self.actions = GuiActions(master=self, background_color='white')

        # Bind actions
        self.actions.play.configure(command=lambda : self.canvas.play_music(bypass_ai=False) )
        self.actions.bypass.configure(command=lambda : self.canvas.play_music(bypass_ai=True) )
        self.actions.image.configure(command=lambda : self.canvas.import_image() )
class MainCanvas(tkinter.Canvas):
    def __init__(self, master, background_color:str):
        super().__init__(master, background=background_color, borderwidth=2, relief='raised')
        self.pack(side = 'left', fill = 'both', expand=True)
        self.update()

        # Declare
        self.list_of_canvas_shapes = []
        self.in_hand = []
        self.verbose_events = True

        self.last_color = PalletItem.YELLOW
        def get_pallet_item(canvas_pos:loc.Pos) -> PalletItem:
            """Checks what was selected by the pointer and returns that object, as long as it is part of the pallet
            See `PalletItem` for options"""
            if canvas_pos.x > self.pallet_item_size().x: return PalletItem.NONE
            pallet_item_number = int(canvas_pos.y / self.pallet_item_size().y) # Gives the PalletItemNumber
            return PalletItem(pallet_item_number)

        # Bind behavior https://www.pythontutorial.net/tkinter/tkinter-event-binding/
        self.pallet_elements = []
        def redraw_pallet_elements() -> None:
            """Redraw the UI if you need to due to a resize or something"""
            for shape in self.pallet_elements:
                shape.remove_shape(self)
            self.pallet_elements.clear()
            self.update()
            

            color = self.last_color.name.lower()
            self.pallet_elements.append(shapes.RoundedRectangle( loc.Box(x=0, y= 0,                      width=self.pallet_item_size().x, height=self.pallet_item_size().y), 'yellow', 'yellow'))
            self.pallet_elements.append(shapes.RoundedRectangle( loc.Box(x=0, y=   self.pallet_item_size().y, width=self.pallet_item_size().x, height=self.pallet_item_size().y), 'orange', 'orange'))
            self.pallet_elements.append(shapes.RoundedRectangle( loc.Box(x=0, y= 2*self.pallet_item_size().y, width=self.pallet_item_size().x, height=self.pallet_item_size().y), 'red', 'red'))
            self.pallet_elements.append(shapes.RoundedRectangle( loc.Box(x=0, y= 3*self.pallet_item_size().y, width=self.pallet_item_size().x, height=self.pallet_item_size().y), 'green', 'green'))
            self.pallet_elements.append(shapes.RoundedRectangle( loc.Box(x=0, y= 4*self.pallet_item_size().y, width=self.pallet_item_size().x, height=self.pallet_item_size().y), 'purple', 'purple'))
            self.pallet_elements.append(shapes.RoundedRectangle( loc.Box(x=0, y= 5*self.pallet_item_size().y, width=self.pallet_item_size().x, height=self.pallet_item_size().y), 'blue', 'blue'))
            self.pallet_elements.append(shapes.Circle(           loc.Box(x=0, y= 6*self.pallet_item_size().y, width=self.pallet_item_size().x, height=self.pallet_item_size().y), color, 'black'))
            self.pallet_elements.append(shapes.HalfCircle(       loc.Box(x=0, y= 7*self.pallet_item_size().y, width=self.pallet_item_size().x, height=self.pallet_item_size().y), color, 'black'))
            self.pallet_elements.append(shapes.Square(           loc.Box(x=0, y= 8*self.pallet_item_size().y, width=self.pallet_item_size().x, height=self.pallet_item_size().y), color, 'black'))
            self.pallet_elements.append(shapes.Heart(            loc.Box(x=0, y= 9*self.pallet_item_size().y, width=self.pallet_item_size().x, height=self.pallet_item_size().y), color, 'black'))
            self.pallet_elements.append(shapes.Star(             loc.Box(x=0, y=10*self.pallet_item_size().y, width=self.pallet_item_size().x, height=self.pallet_item_size().y), color, 'black'))
            self.pallet_elements.append(shapes.SymmetricTriangle(loc.Box(x=0, y=11*self.pallet_item_size().y, width=self.pallet_item_size().x, height=self.pallet_item_size().y), color, 'black'))
            
            for shape in self.pallet_elements:
                shape.draw_shape(self, location_offset=loc.Pos())
            self.update()
        redraw_pallet_elements()
        self.bind("<Configure>", lambda event: redraw_pallet_elements())

        def pick_up(event) -> None:
            if (self.verbose_events): print(f'<pick_up> at {event.x},{event.y}')
            pallet_item = get_pallet_item(loc.Pos(event.x, event.y))

            if pallet_item != PalletItem.NONE:
                if PalletItem.YELLOW.value <= pallet_item.value <= PalletItem.BLUE.value: # It is an color
                    self.last_color = pallet_item
                    redraw_pallet_elements()
                self.in_hand.append(pallet_item)
                if (self.verbose_events): print (f'Picked up {pallet_item.name}')
                return
            
            # Pick_up event did not happen in the pallet
            event.x -= self.pallet_item_size().x
            smallest_shape_in_range = get_smallest_shape_on_position(from_list=self.list_of_canvas_shapes,
                                                                     position=loc.Pos(event.x, event.y))
            if smallest_shape_in_range == None and self.verbose_events:
                print ('No shape in the region')
                return
            self.in_hand.append(smallest_shape_in_range)
            smallest_shape_in_range.remove_shape(self)
            self.list_of_canvas_shapes.remove(smallest_shape_in_range)
            if (self.verbose_events): print (f'Shape picked up from: {smallest_shape_in_range.box}')
            return
        def let_go(event) -> None:
            if (self.verbose_events): print(f'<let_go> at {event.x},{event.y}')
            pallet_item = get_pallet_item(loc.Pos(event.x, event.y))

            # Letting go in the pallet destroys the hand
            if pallet_item != PalletItem.NONE:
                print (f"Tossed: {len(self.in_hand)} item's in the garbage can.")
                self.in_hand.clear()
                return
            
            # Let go on the canvas
            event.x -= self.pallet_item_size().x
            for item in self.in_hand:
                item_is_color = isinstance(item, PalletItem) and PalletItem.YELLOW.value <= item.value <= PalletItem.BLUE.value
                item_is_shape = isinstance(item, PalletItem) and PalletItem.CIRCLE.value <= item.value <= PalletItem.TRIANGLE.value

                # Relocate (move) the shape that we have in our hand     
                if not item_is_color and not item_is_shape:
                    rotation_rad = 0.0
                    depth_percentage = 0
                    try:
                        rotation_rad = item.rotation_rad
                        depth_percentage = item.depth_percentage
                    except: pass
                    new_shape = get_new_shape(shape=PalletItem(int(item.class_id)+PalletItem.CIRCLE.value),
                                              center_pos=loc.Pos(event.x, event.y),
                                              size=item.box.size,
                                              color=PalletItem[item.fill_color.upper()],
                                              rotation_rad=rotation_rad,
                                              depth_percentage=depth_percentage)
                    self.list_of_canvas_shapes.append(new_shape)
                    new_shape.draw_shape(tkinter_canvas=self,
                                         location_offset=loc.Pos(x=self.pallet_item_size().x,y=0))
                    self.in_hand.remove(item)
                    continue
                
                # Data for new shape
                new_shape_color = self.last_color.name.lower()
                new_shape_shape = ''        # Declared here as empty to be filled in later
                new_shape_pos   = loc.Pos() # Declared here as empty to be filled in later
                new_shape_radius=10
                new_shape_rot_rad=0.0
                new_shape_depth =70

                # Apply properties to existing shape
                found = False
                if item_is_color:
                    smallest_shape_in_range = get_smallest_shape_on_position(from_list=self.list_of_canvas_shapes,
                                                                             position=loc.Pos(event.x, event.y))
                    found = smallest_shape_in_range != None
                # Create a new shape
                new_shape=None
                if not found:
                    if item_is_color: # TODO: Change background
                        self.in_hand.remove(item)
                        continue
                    # else place a new shape
                    new_shape = get_new_shape(shape=item,
                                              center_pos=loc.Pos(event.x, event.y),
                                              size=None, color=None)
                elif item_is_color: # Apply color to shape 
                    new_shape_shape = shapes.object_names_array[int(smallest_shape_in_range.class_id)].replace(' ', '_')
                    if item_is_color:   new_shape_color = pallet_item.name.lower()
                    if item_is_shape:   new_shape_shape = pallet_item.name.lower()

                    smallest_shape_in_range.remove_shape(self)
                    self.list_of_canvas_shapes.remove(smallest_shape_in_range)
                    new_shape = get_new_shape(shape=PalletItem(int(smallest_shape_in_range.class_id)+PalletItem.CIRCLE.value),
                                            center_pos=smallest_shape_in_range.center_pos,
                                            size=smallest_shape_in_range.box.size, color=item)
                else: # Apply shape to shape 
                    new_shape = get_new_shape(shape=item,
                                            center_pos=smallest_shape_in_range.center_pos,
                                            size=smallest_shape_in_range.box.size, color=PalletItem[smallest_shape_in_range.fill_color.upper()])
                new_shape.draw_shape(tkinter_canvas=self,
                                     location_offset=loc.Pos(x=self.pallet_item_size().x,y=0))
                self.list_of_canvas_shapes.append(new_shape)
                self.in_hand.remove(item)
        self.bind('<Button-1>',         lambda event: pick_up(event))
        self.bind('<ButtonRelease-1>',  lambda event: let_go (event))

        def scroll(event) -> None:
            if (self.verbose_events): print(f'<scroll> at {event.x},{event.y} for {event.delta}')

            event.x -= self.pallet_item_size().x
            smallest_shape_in_range = get_smallest_shape_on_position(from_list=self.list_of_canvas_shapes,
                                                                     position=loc.Pos(event.x, event.y))
            found = smallest_shape_in_range != None
                
            # Copy
            new_size = loc.Size(x=max(10, min(2000, (math.sqrt(smallest_shape_in_range.box.size.x) + event.delta/240)**2)),
                                y=max(10, min(2000, (math.sqrt(smallest_shape_in_range.box.size.y) + event.delta/240)**2)))
            new_shape = get_new_shape(shape=PalletItem(int(smallest_shape_in_range.class_id)+PalletItem.CIRCLE.value),
                                      center_pos=smallest_shape_in_range.center_pos,
                                      size=new_size,
                                      color=PalletItem[smallest_shape_in_range.fill_color.upper()],
                                      rotation_rad=smallest_shape_in_range.rotation_rad)
            
            # Replace
            smallest_shape_in_range.remove_shape(self)
            self.list_of_canvas_shapes.remove(smallest_shape_in_range)
            new_shape.draw_shape(tkinter_canvas=self,
                                    location_offset=loc.Pos(x=self.pallet_item_size().x,y=0))
            self.list_of_canvas_shapes.append(new_shape)
            return
        self.bind("<MouseWheel>",       lambda event: scroll(event))

        def rotate(event) -> None:
            if (self.verbose_events): print(f'<Key> {event.char} at {event.x},{event.y}')
            if event.char != "r": return

            for shape in self.in_hand:
                if isinstance(shape, PalletItem): continue
                try: shape.rotation_rad -= math.pi / 10
                finally:pass
            event.x -= self.pallet_item_size().x
            smallest_shape_in_range = get_smallest_shape_on_position(from_list=self.list_of_canvas_shapes,
                                                                     position=loc.Pos(event.x, event.y))
            found = smallest_shape_in_range != None
                
            # Copy
            new_shape = get_new_shape(shape=PalletItem(int(smallest_shape_in_range.class_id)+PalletItem.CIRCLE.value),
                                      center_pos=smallest_shape_in_range.center_pos,
                                      size=smallest_shape_in_range.box.size,
                                      color=PalletItem[smallest_shape_in_range.fill_color.upper()],
                                      rotation_rad=smallest_shape_in_range.rotation_rad - math.pi / 10)
            
            # Replace
            smallest_shape_in_range.remove_shape(self)
            self.list_of_canvas_shapes.remove(smallest_shape_in_range)
            new_shape.draw_shape(tkinter_canvas=self,
                                 location_offset=loc.Pos(x=self.pallet_item_size().x,y=0))
            self.list_of_canvas_shapes.append(new_shape)
            return
        self.bind_all("r",lambda event:rotate(event))

        def get_smallest_shape_on_position(from_list:list, position:loc.Pos) -> None|shapes.Circle|shapes.HalfCircle|shapes.Square|shapes.Heart|shapes.Star|shapes.SymmetricTriangle:
            """Returns `None` when no shape was found, otherwise returns the smallest shape as the shape class that has `position` inside it's `loc.Box`
            
            also it prefers shapes with grater index"""
            smallest_shape = []
            for shape in from_list:
                if position.x < shape.box.pos.x: continue                      # Left of shape.box  (out of range)
                if position.x > shape.box.pos.x + shape.box.size.x: continue   # Right of shape.box (out of range)
                if position.y < shape.box.pos.y: continue                      # Top of shape.box   (out of range)
                if position.y > shape.box.pos.y + shape.box.size.y: continue   # Bottom of shape.box(out of range)
                if len(smallest_shape) != 0 and shape.box.size > smallest_shape[0].box.size: continue # Get the smallest one (and also the last of the same area) (except for when we dont have one yet)
                smallest_shape.clear()
                smallest_shape.append(shape)
            if len(smallest_shape) == 0: return None
            return smallest_shape[0]
        def get_new_shape(shape:PalletItem, center_pos:loc.Pos, size:loc.Size|None, color:PalletItem|None, rotation_rad=0.0, depth_percentage=70) -> shapes.Circle|shapes.HalfCircle|shapes.Square|shapes.Heart|shapes.Star|shapes.SymmetricTriangle:
            """Creates a new shape
            ## Args
            - `shape` One of the 6 shapes to create a pallet item from
            - `center_pos` Where you let go i guess
            - `size` the size of the shape (Optional: Leave empty to get default size)
            - `color` One of the 6 colors (Optional: Leave empty for last color)
            - `rotation_rad` The number of radiants that the shape should rotate from origin
            - `depth_percentage` Some shapes have a depth as a variable.
            ## Returns
            A shape"""
            # Get all new values prepped
            assert PalletItem.CIRCLE.value <= shape.value <= PalletItem.TRIANGLE.value
            new_shape_type = shape.name.lower().replace(' ', '_')

            if color is None:   new_color = self.last_color.name.lower()
            else:               new_color = color.name.lower()

            if size is None:    new_size = loc.Size(50, 50)
            else:               new_size = size
            center_pos.x -= new_size.x / 2
            center_pos.y -= new_size.y / 2
            new_box = loc.Box(x= center_pos.x,
                              y= center_pos.y,
                              width= new_size.x,
                              height=new_size.y)
            
            print( f'Got new_shape: [\n\tWith shape: `{new_shape_type}`\n\tOn the Box: {new_box}\n\tWith the Color: {new_color}\n]')
            
            # Get the shape
            match (new_shape_type):
                case 'circle':
                    new_shape = shapes.Circle(box=new_box, fill_color=new_color, outline_color=new_color)
                case 'half_circle':
                    new_shape = shapes.HalfCircle(box=new_box, fill_color=new_color, outline_color=new_color,
                                                  rotation_rad=rotation_rad)
                case 'square':
                    new_shape = shapes.Square(box=new_box, fill_color=new_color, outline_color=new_color,
                                              rotation_rad=rotation_rad)
                case 'heart':
                    new_shape = shapes.Heart(box=new_box,
                                             fill_color=new_color, outline_color=new_color,
                                             rotation_rad=rotation_rad,
                                             depth_percentage=depth_percentage)
                case 'star':
                    new_shape = shapes.Star(box=new_box,
                                            fill_color=new_color, outline_color=new_color,
                                            rotation_rad=rotation_rad,
                                            depth_percentage=depth_percentage)
                case _: # 'triangle'
                    new_shape = shapes.SymmetricTriangle(box=new_box,
                                                         fill_color=new_color, outline_color=new_color,
                                                         rotation_rad=rotation_rad)
            return new_shape
    def pallet_item_size(self) -> loc.Size:
        """Returns the size of each tool from the pallet"""
        return loc.Size(x= 64,  #TODO: Magic number
                        y= self.winfo_height()/(len(PalletItem)-1))
    def canvas_size(self) -> loc.Size:
        """Returns the usable space of the canvas (exclusive the pallet)"""
        return loc.Size(x=self.winfo_width()-self.pallet_item_size().x, y=self.winfo_height())
    def play_music(self, bypass_ai=False) -> None:
        img_size = self.canvas_size()

        # get a list of shapes
        list_of_shapes = []
        if not bypass_ai:
            cv2.imshow('Loading AI...', cv2.imread(os.path.join(os.getcwd(), 'files', 'gui', 'ai.png')))
            cv2.waitKey(1)# Displays the new image immediately
            try:
                save_img(tkinter_canvas=self,
                         path_filename=os.path.join(os.getcwd(), 'files', 'gui', 'temp'),
                         as_png=True)
            except RuntimeError as runtime_error:
                print(f'WARNING: Something caused a RuntimeError while saving the picture of the canvas.\n Reverting to bypassing the ai...,\n but if you are curious this was the problem: {runtime_error}')
                bypass_ai = True
            else: # did not fail to save_img.
                img = cv2.imread(os.path.join(os.getcwd(), 'files', 'gui', 'temp.png'))
                cropped = img[0:img_size.y, self.pallet_item_size().x:self.pallet_item_size().x+img_size.x]
                image_processing_ai.setup_ai()
                image_ai, list_of_shapes = image_processing_ai.detect_shapes_with_ai(cropped)
                cv2.destroyAllWindows()
                cv2.imshow('Building music...', image_ai)
                cv2.waitKey(1)# Displays the new image immediately
        if bypass_ai: # it is possible that in `if not bypass_ai:` we abort and end up here. A reason could be TODO:`not a windows machine` or `Ghostscript missing` what both causes us to not being able to make a photo of the canvas. and therefor the AI has to be bypassed
            cv2.imshow('Bypassing AI...', cv2.imread(os.path.join(os.getcwd(), 'files', 'gui', 'ai_bypass.png')))
            cv2.waitKey(1)# Displays the new image immediately
            for counter, shape in enumerate (self.list_of_canvas_shapes):
                shape_name = shapes.object_names_array[int(shape.class_id)]
                match(shape_name):
                    case "circle":      instrument = common.image_properties.ShapeType.CIRCLE
                    case "half circle": instrument = common.image_properties.ShapeType.HALF_CIRCLE
                    case "square":      instrument = common.image_properties.ShapeType.SQUARE
                    case "heart":       instrument = common.image_properties.ShapeType.HEART
                    case "star":        instrument = common.image_properties.ShapeType.STAR
                    case "triangle":    instrument = common.image_properties.ShapeType.TRIANGLE
                    case _:             raise RuntimeError("Chosen `shape_name` is out of bounds.")
                match(shape.fill_color):
                    case "yellow":  color = common.image_properties.ColorType.YELLOW
                    case "orange":  color = common.image_properties.ColorType.ORANGE
                    case "red":     color = common.image_properties.ColorType.RED
                    case "green":   color = common.image_properties.ColorType.GREEN
                    case "purple":  color = common.image_properties.ColorType.VIOLET
                    case "blue":    color = common.image_properties.ColorType.BLUE
                    case _:         raise RuntimeError("Chosen `fill_color` is out of bounds.")
                shape_ai = common.image_properties.Shape(shape=     shape_name,
                                                         counter=   counter,
                                                         instrument=instrument,
                                                         size=      int(image_processing.get_volume_from_size(shape.box.size.area(), img_size.area())),
                                                         color=     color,
                                                         x_axis=    float(image_processing.get_placement_of_note(shape.center_pos.x, img_size.x)), 
                                                         y_axis=    int(image_processing.get_pitch_from_y_axis(shape.center_pos.y, img_size.y)), 
                                                         box=       (int(shape.box.pos.x), int(shape.box.pos.y), int(shape.box.size.x), int(shape.box.size.y)))
                list_of_shapes.append(shape_ai)
        
        image_processing.display_list_of_shapes(list_of_shapes)

        # Create .midi -> .wav -> combined.wav -> play
        bpm = common.midi_creation.MakeSong(list_of_shapes)
        processes = [
            mp.Process(target=common.midi_processing.instrument, args=(bpm, "drum")),
            mp.Process(target=common.midi_processing.instrument, args=(bpm, "violin")),
            mp.Process(target=common.midi_processing.instrument, args=(bpm, "guitar")),
            mp.Process(target=common.midi_processing.instrument, args=(bpm, "flute")),
            mp.Process(target=common.midi_processing.instrument, args=(bpm, "saxophone")),
            mp.Process(target=common.midi_processing.instrument, args=(bpm, "clap")),
            mp.Process(target=common.midi_processing.instrument, args=(bpm, "piano"))
        ]
        for process in processes:
            process.start()
        for process in processes:
            process.join()
        common.midi_processing.audio_rendering(bpm)
        cv2.destroyAllWindows()
        if bypass_ai:   cv2.imshow('Playing audio... Any key return...', cv2.imread(os.path.join(os.getcwd(), 'files', 'gui', 'play.png')))
        else:           cv2.imshow('Playing audio... Any key return...', image_ai)
        cv2.waitKey(1)# Displays the new image immediately
        common.midi_processing.play_loop(os.path.join(os.getcwd(), 'files', 'audio_generator', 'created_song.mp3'),
                                               decay= 0.75,
                                               cutoff=0.05)
        cv2.destroyAllWindows()
    def import_image(self) -> None:
        file_path = filedialog.askopenfilename()
        
        img = cv2.imread(file_path)
        cv2.imshow('Loading AI...', img)
        cv2.waitKey(1)# Displays the new image immediately

        image_processing_ai.setup_ai()
        image_ai, list_of_shapes = image_processing_ai.detect_shapes_with_ai(img)
        cv2.destroyAllWindows()
        cv2.imshow('Building music...', image_ai)
        cv2.waitKey(1)# Displays the new image immediately

        image_processing.display_list_of_shapes(list_of_shapes)
        # Create .midi -> .wav -> combined.wav -> play
        bpm = common.midi_creation.MakeSong(list_of_shapes)
        processes = [
            mp.Process(target=common.midi_processing.instrument, args=(bpm, "drum")),
            mp.Process(target=common.midi_processing.instrument, args=(bpm, "violin")),
            mp.Process(target=common.midi_processing.instrument, args=(bpm, "guitar")),
            mp.Process(target=common.midi_processing.instrument, args=(bpm, "flute")),
            mp.Process(target=common.midi_processing.instrument, args=(bpm, "saxophone")),
            mp.Process(target=common.midi_processing.instrument, args=(bpm, "clap")),
            mp.Process(target=common.midi_processing.instrument, args=(bpm, "piano"))
        ]
        for process in processes:
            process.start()
        for process in processes:
            process.join()
        common.midi_processing.audio_rendering(bpm)
        cv2.destroyAllWindows()
        cv2.imshow('Playing audio... Any key return...', image_ai)
        cv2.waitKey(1)# Displays the new image immediately
        common.midi_processing.play_loop(os.path.join(os.getcwd(), 'files', 'audio_generator', 'created_song.mp3'),
                                               decay= 0.75,
                                               cutoff=0.05)
        cv2.destroyAllWindows()
class GuiActions(ttk.Frame):
    def __init__(self, master, background_color:str):
        super().__init__(master, borderwidth=2, relief='groove')

        # Declare
        self.settings_frame = ttk.Frame(master=self, borderwidth=2, relief='groove')
        self.play  =tkinter.Button(master=self.settings_frame, text = 'Play')# command in parent
        self.bypass  =tkinter.Button(master=self.settings_frame, text = 'Play\n(without ai)')
        self.image  =tkinter.Button(master=self.settings_frame, text = 'Import file')
        self.play.pack (expand=True, fill='both', pady=3)
        self.bypass.pack (expand=True, fill='both', pady=3)
        self.image.pack (expand=True, fill='both', pady=3)

        # Pack
        self.settings_frame.pack(expand=True, fill='y')
        self.pack(side = 'left', fill = 'y', padx = 3, pady = 3)

if __name__ == '__main__':
    app = Gui()
    app.mainloop()

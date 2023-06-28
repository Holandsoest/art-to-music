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
import cv2
import numpy as np

from enum import Enum # Keep enums UPPER_CASE according to https://docs.python.org/3/howto/enum.html  
import math
import tkinter
from tkinter import ttk


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
        

class Gui(tkinter.Tk):
    """This is the whole GUI of the art-to-music application. And is of course separate standalone from the real webcam/camera implementation.
    
    `app.mainloop()` to run it (blocking, will continue after `alt + F4` was pressed)"""
    def __init__(self) -> None:
        super().__init__()
        self.title('art-to-music')
        self.minsize(width=528,height=360)

        # Declare objects
        self.canvas = MainCanvas(master=self, background_color='white')
        self.actions = GuiActions(master=self, background_color='white')
        self.actions.play.configure(command=lambda : self.canvas.play_music(bypass_ai=True) )
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
            for shape in self.list_of_canvas_shapes:
                if event.x < shape.box.pos.x: continue                      # Left of shape.box  (out of range)
                if event.x > shape.box.pos.x + shape.box.size.x: continue   # Right of shape.box (out of range)
                if event.y < shape.box.pos.y: continue                      # Top of shape.box   (out of range)
                if event.y > shape.box.pos.y + shape.box.size.y: continue   # Bottom of shape.box(out of range)

                self.in_hand.append(shape)
                shape.remove_shape(self)
                self.list_of_canvas_shapes.remove(shape)
                if (self.verbose_events): print (f'Shape picked up from: {shape.box}')
                return
            if (self.verbose_events): print ('No shape in the region')
        def let_go(event) -> None:
            if (self.verbose_events): print(f'<let_go> at {event.x},{event.y}')
            pallet_item = get_pallet_item(loc.Pos(event.x, event.y))

            if pallet_item != PalletItem.NONE:
                print (f"Tossed: {len(self.in_hand)} item's in the garbage can.")
                self.in_hand.clear()
                return
            
            # Let go on the canvas
            event.x -= self.pallet_item_size().x
            for item in self.in_hand:
                # Relocate the shape        
                if not isinstance(item, PalletItem):
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

                # Apply properties to shape
                found = False
                for shape in self.list_of_canvas_shapes: # Find a shape where we drop
                    if event.x < shape.box.pos.x: continue                      # Left of box  (out of range)
                    if event.x > shape.box.pos.x + shape.box.size.x: continue   # Right of box (out of range)
                    if event.y < shape.box.pos.y: continue                      # Top of box   (out of range)
                    if event.y > shape.box.pos.y + shape.box.size.y: continue   # Bottom of box(out of range)

                    new_shape_shape = shapes.object_names_array[int(shape.class_id)].replace(' ', '_')
                    if PalletItem.YELLOW.value <= pallet_item.value <= PalletItem.BLUE.value:           new_shape_color = pallet_item.name.lower()
                    if PalletItem.CIRCLE.value <= pallet_item.value <= PalletItem.HALF_CIRCLE.value:    new_shape_shape = pallet_item.name.lower()

                    shape.remove_shape(self)
                    self.list_of_canvas_shapes.remove(shape)

                    found = True
                # Create a new shape
                new_shape=None
                if not found:
                    if PalletItem.YELLOW.value <= item.value <= PalletItem.BLUE.value: # TODO: Change background
                        self.in_hand.remove(item)
                        continue
                    # else place a new shape
                    new_shape = get_new_shape(shape=item,
                                              center_pos=loc.Pos(event.x, event.y),
                                              size=None, color=None)
                else:# So we did find it
                    if PalletItem.YELLOW.value <= item.value <= PalletItem.BLUE.value: # Apply color to shape 
                        new_shape = get_new_shape(shape=PalletItem(int(shape.class_id)+PalletItem.CIRCLE.value),
                                                  center_pos=shape.center_pos,
                                                  size=shape.box.size, color=item)
                    else: # Apply shape to shape 
                        new_shape = get_new_shape(shape=item,
                                                  center_pos=shape.center_pos,
                                                  size=shape.box.size, color=PalletItem[shape.fill_color.upper()])
                new_shape.draw_shape(tkinter_canvas=self,
                                     location_offset=loc.Pos(x=self.pallet_item_size().x,y=0))
                self.list_of_canvas_shapes.append(new_shape)
                self.in_hand.remove(item)
        self.bind('<Button-1>',         lambda event: pick_up(event))
        self.bind('<ButtonRelease-1>',  lambda event: let_go (event))

        def scroll(event) -> None:
            if (self.verbose_events): print(f'<scroll> at {event.x},{event.y} for {event.delta}')

            event.x -= self.pallet_item_size().x
            for shape in self.list_of_canvas_shapes:
                if event.x < shape.box.pos.x: continue                      # Left of shape.box  (out of range)
                if event.x > shape.box.pos.x + shape.box.size.x: continue   # Right of shape.box (out of range)
                if event.y < shape.box.pos.y: continue                      # Top of shape.box   (out of range)
                if event.y > shape.box.pos.y + shape.box.size.y: continue   # Bottom of shape.box(out of range)
                
                # Copy
                new_size = loc.Size(x=max(10, min(2000, (math.sqrt(shape.box.size.x) + event.delta/240)**2)),
                                    y=max(10, min(2000, (math.sqrt(shape.box.size.y) + event.delta/240)**2)))
                new_shape = get_new_shape(shape=PalletItem(int(shape.class_id)+PalletItem.CIRCLE.value),
                                          center_pos=shape.center_pos,
                                          size=new_size,
                                          color=PalletItem[shape.fill_color.upper()],
                                          rotation_rad=shape.rotation_rad)
                
                # Replace
                shape.remove_shape(self)
                self.list_of_canvas_shapes.remove(shape)
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
            for shape in self.list_of_canvas_shapes:
                if event.x < shape.box.pos.x: continue                      # Left of shape.box  (out of range)
                if event.x > shape.box.pos.x + shape.box.size.x: continue   # Right of shape.box (out of range)
                if event.y < shape.box.pos.y: continue                      # Top of shape.box   (out of range)
                if event.y > shape.box.pos.y + shape.box.size.y: continue   # Bottom of shape.box(out of range)
                
                # Copy
                new_shape = get_new_shape(shape=PalletItem(int(shape.class_id)+PalletItem.CIRCLE.value),
                                        center_pos=shape.center_pos,
                                        size=shape.box.size,
                                        color=PalletItem[shape.fill_color.upper()],
                                        rotation_rad=shape.rotation_rad - math.pi / 10)
                
                # Replace
                shape.remove_shape(self)
                self.list_of_canvas_shapes.remove(shape)
                new_shape.draw_shape(tkinter_canvas=self,
                                     location_offset=loc.Pos(x=self.pallet_item_size().x,y=0))
                self.list_of_canvas_shapes.append(new_shape)
                return
            self.update()
        self.bind_all("r",lambda event:rotate(event))



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
        img_size = loc.Size(self.grid_size()[0],self.grid_size()[1])

        # get a list of shapes
        list_of_shapes = []
        if not bypass_ai:
            pass # take picure
        else:
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
                shape_ai = common.image_properties.Shape(shape_name, counter, instrument,
                                                         int(image_processing.get_volume_from_size(shape.box.size.x*shape.box.size.y, img_size.area())),
                                                         color,
                                                         float(image_processing.get_placement_of_note(shape.center_pos.x, img_size.x)), 
                                                         int(image_processing.get_pitch_from_y_axis(shape.center_pos.y, img_size.y)), 
                                                         (int(shape.box.pos.x), int(shape.box.pos.y)), int(shape.box.size.x), int(shape.box.size.y))
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
        
        # Start all processes
        for process in processes:
            process.start()

        # Wait for all processes to finish
        for process in processes:
            process.join()
            
        common.midi_processing.audio_rendering(bpm)

        cv2.destroyAllWindows()
        cv2.imshow('Playing audio... Any key continue...', image_ai)
        cv2.waitKey(1)# Displays the new image immediately
        take_image.set_jetson_busy(busy=False)
        key = midi_processing.play_loop(os.path.join(os.getcwd(), 'files', 'audio_generator', 'created_song.mp3'),
                                                    decay= 0.75,
                                                    cutoff=0.05)
            
class GuiActions(ttk.Frame):
    def __init__(self, master, background_color:str):
        super().__init__(master, borderwidth=2, relief='groove')

        # Declare
        self.settings_frame = ttk.Frame(master=self, borderwidth=2, relief='groove')
        self.play  =tkinter.Button(master=self.settings_frame, text = 'Play')# command in parent
        self.ai  =ttk.Label(master=self.settings_frame, text = 'AI' ,background = background_color)
        self.play.pack (expand=True, fill='both', pady=3)
        self.ai.pack   (expand=True, fill='both', pady=3)

        # Pack
        self.settings_frame.pack(expand=True, fill='y')
        self.pack(side = 'left', fill = 'y', padx = 3, pady = 3)

if __name__ == '__main__':
    app = Gui()
    app.mainloop()

#!/usr/bin/env python3
"""A library that covers how the GUI should respond / work"""
# Want to learn about Tkinter gui tool? https://youtu.be/mop6g-c5HEY It coverers about everything. ;)
import common.shapes as shapes
import common.location as loc

from enum import Enum # Keep enums UPPER_CASE according to https://docs.python.org/3/howto/enum.html  
import math
import tkinter
from tkinter import ttk

class Gui(tkinter.Tk):
    def __init__(self) -> None:
        """The GUI of the art-to-music application.
        - #### `size`   The size of the GUI.
            Possible options:  
            - `None`    Take up the size of screen_0 (full-screen).
            - `Size`    The screen will become this size, but placed anywhere on the screen."""
        super().__init__()
        self.title('art-to-music')
        self.minsize(width=528,height=360)

        # Declare objects
        self.canvas = MainCanvas(master=self, background_color='white')
        self.actions = GuiActions(master=self, background_color='white')
class MainCanvas(tkinter.Canvas):
    def __init__(self, master, background_color:str):
        super().__init__(master, background=background_color, borderwidth=2, relief='raised')
        self.pack(side = 'left', fill = 'both', expand=True)
        self.update()

        # Declare
        self.list_of_canvas_shapes = []
        self.in_hand = []
        self.verbose_events = True

        # Defining the Pallet
        class PalletItem(Enum):
            NONE = -1
            YELLOW = 0
            ORANGE = 1
            RED = 2
            GREEN = 3
            PURPLE = 4
            BLUE = 5
            CIRCLE = 6
            SQUARE = 7
            TRIANGLE = 8
            STAR = 9
            HEART = 10
            HALF_CIRCLE = 11
            TRASH_CAN = 12
        self.last_color = PalletItem.YELLOW
        def pallet_item_size() -> loc.Size:
            """Returns the size of each tool from the pallet"""
            return loc.Size(x= 64,  #TODO: Magic number
                            y= self.winfo_height()/(len(PalletItem)-1))
        def canvas_size() -> loc.Size:
            """Returns the usable space of the canvas (exclusive the pallet)"""
            return loc.Size(x=self.winfo_width()-pallet_item_size().x, y=self.winfo_height())
        def get_pallet_item(canvas_pos:loc.Pos) -> PalletItem:
            """Checks what was selected by the pointer and returns that object, as long as it is part of the pallet
            See `PalletItem` for options"""
            if canvas_pos.x > pallet_item_size().x: return PalletItem.NONE
            pallet_item_number = int(canvas_pos.y * 13 / self.winfo_height()) # Gives the PalletItemNumber
            return PalletItem(pallet_item_number)
        # TODO: Add the shapes and colors here

        # Bind behavior https://www.pythontutorial.net/tkinter/tkinter-event-binding/
        def pick_up(event):
            if (self.verbose_events): print(f'<pick_up> at {event.x},{event.y}')
            pallet_item = get_pallet_item(loc.Pos(event.x, event.y))

            if pallet_item != PalletItem.NONE:
                if PalletItem.YELLOW.value <= pallet_item.value <= PalletItem.BLUE.value: # It is an color
                    self.last_color = pallet_item
                self.in_hand.append(pallet_item)
                if (self.verbose_events): print (f'Picked up {pallet_item.name}')
                return
            
            # Pick_up event did not happen in the pallet
            event.x -= pallet_item_size().x
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
        def let_go(event):
            if (self.verbose_events): print(f'<let_go> at {event.x},{event.y}')
            pallet_item = get_pallet_item(loc.Pos(event.x, event.y))

            if pallet_item == PalletItem.TRASH_CAN:
                print ('Tossed:\n\t' + self.in_hand + '\nIn the garbage can.')
                self.in_hand.clear()
                return
            if pallet_item != PalletItem.NONE: return

            # Let go on the canvas
            event.x -= pallet_item_size().x
            for item in self.in_hand:
                # Relocate the shape        
                if not isinstance(item, PalletItem):
                    match (shapes.object_names_array[int(item.class_id)]):
                        case 'circle':
                            new_shape = shapes.Circle(box=loc.Box(x=event.x - item.box.size.x / 2,
                                                                y=event.y - item.box.size.y / 2,
                                                                width=item.box.size.x,
                                                                height=item.box.size.y),
                                                      fill_color=item.fill_color, outline_color=item.outline_color)
                        case 'half circle':
                            new_shape = shapes.HalfCircle(box=loc.Box(x=event.x - item.box.size.x / 2,
                                                                y=event.y - item.box.size.y / 2,
                                                                width=item.box.size.x,
                                                                height=item.box.size.y),
                                                      fill_color=item.fill_color, outline_color=item.outline_color,
                                                    rotation_rad=item.rotation_rad)
                        case 'square':
                            new_shape = shapes.Square(box=loc.Box(x=event.x - item.box.size.x / 2,
                                                                y=event.y - item.box.size.y / 2,
                                                                width=item.box.size.x,
                                                                height=item.box.size.y),
                                                      fill_color=item.fill_color, outline_color=item.outline_color,
                                                    rotation_rad=item.rotation_rad)
                        case 'heart':
                            new_shape = shapes.Heart(box=loc.Box(x=event.x - item.box.size.x / 2,
                                                                y=event.y - item.box.size.y / 2,
                                                                width=item.box.size.x,
                                                                height=item.box.size.y),
                                                      fill_color=item.fill_color, outline_color=item.outline_color,
                                                    rotation_rad=item.rotation_rad,
                                                    depth_percentage=item.depth_percentage)
                        case 'star':
                            new_shape = shapes.Star(box=loc.Box(x=event.x - item.box.size.x / 2,
                                                                y=event.y - item.box.size.y / 2,
                                                                width=item.box.size.x,
                                                                height=item.box.size.y),
                                                    fill_color=item.fill_color, outline_color=item.outline_color,
                                                    rotation_rad=item.rotation_rad,
                                                    depth_percentage=item.depth_percentage)
                        case _: # 'triangle'
                            new_shape = shapes.SymmetricTriangle(box=loc.Box(x=event.x - item.box.size.x / 2,
                                                                y=event.y - item.box.size.y / 2,
                                                                width=item.box.size.x,
                                                                height=item.box.size.y),
                                                      fill_color=item.fill_color, outline_color=item.outline_color,
                                                    rotation_rad=item.rotation_rad)
                    self.list_of_canvas_shapes.append(new_shape)
                    new_shape.draw_shape(tkinter_canvas=self,
                                         location_offset=loc.Pos(x=pallet_item_size().x,y=0))
                    self.in_hand.remove(item)
                    continue
                
                # Data for new shape
                new_shape_color = self.last_color.name.lower()
                new_shape_shape = ''        # ILLEGAL
                new_shape_pos   = loc.Pos() # ILLEGAL
                new_shape_radius=10
                new_shape_rot_rad=0.0
                new_shape_depth =70

                # Apply properties to shape
                found = False
                for shape in self.list_of_canvas_shapes:
                    if event.x < shape.box.pos.x: continue                # Left of box  (out of range)
                    if event.x > shape.box.pos.x + shape.box.size.x: continue   # Right of box (out of range)
                    if event.y < shape.box.pos.y: continue                # Top of box   (out of range)
                    if event.y > shape.box.pos.y + shape.box.size.y: continue   # Bottom of box(out of range)

                    new_shape_shape = shapes.object_names_array[int(shape.class_id)].replace(' ', '_')
                    if PalletItem.YELLOW.value <= pallet_item.value <= PalletItem.BLUE.value:           new_shape_color = pallet_item.name.lower()
                    if PalletItem.CIRCLE.value <= pallet_item.value <= PalletItem.HALF_CIRCLE.value:    new_shape_shape = pallet_item.name.lower()

                    shape.remove_shape(self)
                    self.list_of_canvas_shapes.remove(shape)

                    found = True
                if not found and PalletItem.YELLOW.value <= pallet_item.value <= PalletItem.BLUE.value:
                    self.in_hand.remove(item) # TODO: Implement background
                    continue
                new_shape_shape = item.name.lower().replace(' ', '_')
                print(f'`new_shape_shape` = `{new_shape_shape}`')
                
                new_box = loc.Box(x= event.x - 25,
                                  y= event.y - 25,
                                  width= 50,
                                  height= 50)
                match (new_shape_shape):
                    case 'circle':
                        new_shape = shapes.Circle(box=new_box, fill_color=self.last_color.name.lower(), outline_color=self.last_color.name.lower())
                    case 'half circle':
                        new_shape = shapes.HalfCircle(box=new_box, fill_color=self.last_color.name.lower(), outline_color=self.last_color.name.lower(),
                                                rotation_rad=0)
                    case 'square':
                        new_shape = shapes.Square(box=new_box, fill_color=self.last_color.name.lower(), outline_color=self.last_color.name.lower(),
                                                rotation_rad=0)
                    case 'heart':
                        new_shape = shapes.Heart(box=new_box,
                                                    fill_color=self.last_color.name.lower(), outline_color=self.last_color.name.lower(),
                                                rotation_rad=0,
                                                depth_percentage=50)
                    case 'star':
                        new_shape = shapes.Star(box=new_box,
                                                fill_color=self.last_color.name.lower(), outline_color=self.last_color.name.lower(),
                                                rotation_rad=0,
                                                depth_percentage=50)
                    case _: # 'triangle'
                        new_shape = shapes.SymmetricTriangle(box=new_box,
                                                    fill_color=self.last_color.name.lower(), outline_color=self.last_color.name.lower(),
                                                rotation_rad=0)
                new_shape.draw_shape(tkinter_canvas=self,
                                     location_offset=loc.Pos(x=pallet_item_size().x,y=0))
                self.list_of_canvas_shapes.append(new_shape)
                self.in_hand.remove(item)

        self.bind ('<Button-1>',        lambda event: pick_up(event))
        self.bind ('<ButtonRelease-1>', lambda event: let_go (event))
        # self.bind ('<Motion>',          lambda event: temp   (event))

        self.list_of_canvas_shapes.append(shapes.Square(           loc.Box(x=0, y= 0,                      width=pallet_item_size().x, height=pallet_item_size().y), 'yellow', 'yellow', rotation_rad=math.pi/4))
        self.list_of_canvas_shapes.append(shapes.Square(           loc.Box(x=0, y=   pallet_item_size().y, width=pallet_item_size().x, height=pallet_item_size().y), 'orange', 'orange', rotation_rad=math.pi/4))
        self.list_of_canvas_shapes.append(shapes.Square(           loc.Box(x=0, y= 2*pallet_item_size().y, width=pallet_item_size().x, height=pallet_item_size().y), 'red', 'red', rotation_rad=math.pi/4))
        self.list_of_canvas_shapes.append(shapes.Square(           loc.Box(x=0, y= 3*pallet_item_size().y, width=pallet_item_size().x, height=pallet_item_size().y), 'green', 'green', rotation_rad=math.pi/4))
        self.list_of_canvas_shapes.append(shapes.Square(           loc.Box(x=0, y= 4*pallet_item_size().y, width=pallet_item_size().x, height=pallet_item_size().y), 'purple', 'purple', rotation_rad=math.pi/4))
        self.list_of_canvas_shapes.append(shapes.Square(           loc.Box(x=0, y= 5*pallet_item_size().y, width=pallet_item_size().x, height=pallet_item_size().y), 'blue', 'blue', rotation_rad=math.pi/4))
        self.list_of_canvas_shapes.append(shapes.Circle(           loc.Box(x=0, y= 6*pallet_item_size().y, width=pallet_item_size().x, height=pallet_item_size().y), 'yellow', 'yellow'))
        self.list_of_canvas_shapes.append(shapes.Square(           loc.Box(x=0, y= 7*pallet_item_size().y, width=pallet_item_size().x, height=pallet_item_size().y), 'yellow', 'yellow', rotation_rad=math.pi/4))
        self.list_of_canvas_shapes.append(shapes.SymmetricTriangle(loc.Box(x=0, y= 8*pallet_item_size().y, width=pallet_item_size().x, height=pallet_item_size().y), 'yellow', 'yellow', rotation_rad=math.pi/2))
        self.list_of_canvas_shapes.append(shapes.Star(             loc.Box(x=0, y= 9*pallet_item_size().y, width=pallet_item_size().x, height=pallet_item_size().y), 'yellow', 'yellow', rotation_rad=math.pi/2))
        self.list_of_canvas_shapes.append(shapes.Heart(            loc.Box(x=0, y=10*pallet_item_size().y, width=pallet_item_size().x, height=pallet_item_size().y), 'yellow', 'yellow'))
        self.list_of_canvas_shapes.append(shapes.HalfCircle(       loc.Box(x=0, y=11*pallet_item_size().y, width=pallet_item_size().x, height=pallet_item_size().y), 'yellow', 'yellow'))
        for shape in self.list_of_canvas_shapes:
            shape.draw_shape(self, location_offset=loc.Pos())
        self.update()
        
class GuiActions(ttk.Frame):
    def __init__(self, master, background_color:str):
        super().__init__(master, borderwidth=2, relief='groove')

        # Declare
        self.settings_frame = ttk.Frame(master=self, borderwidth=2, relief='groove')
        self.play  =ttk.Label(master=self.settings_frame, text = 'Play' ,background = background_color)
        self.ai  =ttk.Label(master=self.settings_frame, text = 'AI' ,background = background_color)
        self.play.pack (expand=True, fill='both', pady=3)
        self.ai.pack   (expand=True, fill='both', pady=3)

        # Pack
        self.settings_frame.pack(expand=True, fill='y')
        self.pack(side = 'left', fill = 'y', padx = 3, pady = 3)


app = Gui()
app.mainloop()

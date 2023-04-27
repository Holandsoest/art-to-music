#!/usr/bin/env python3
"""A library that covers how the GUI should respond / work"""
# Want to learn about Tkinter gui tool? https://youtu.be/mop6g-c5HEY It coverers about everything. ;)
import common.shapes as shapes
import common.location as loc

from enum import Enum # Keep enums UPPER_CASE according to https://docs.python.org/3/howto/enum.html  

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
        def pallet_width() -> int:
            """Returns the width of the pallet as a integer"""
            return 64
        def get_pallet_item(canvas_pos:loc.Pos) -> PalletItem:
            """Checks what was selected by the pointer and returns that object, as long as it is part of the pallet
            See `PalletItem` for options"""
            if canvas_pos.x > pallet_width(): return PalletItem.NONE
            pallet_item_number = canvas_pos.y * 13 / self.winfo_height() # Gives the PalletItemNumber
            return PalletItem[pallet_item_number]
        # TODO: Add the shapes and colors here

        # Bind behavior https://www.pythontutorial.net/tkinter/tkinter-event-binding/
        def pick_up(event):
            if (self.verbose_events): print(f'<pick_up> at {event.x},{event.y}')
            pallet_item = get_pallet_item(loc.Pos(event.x, event.y))

            if pallet_item != PalletItem.NONE:
                if PalletItem.YELLOW <= pallet_item <= PalletItem.BLUE: # It is an color
                    self.last_color = pallet_item
                self.in_hand.append(pallet_item)
                if (self.verbose_events): print (f'Picked up {pallet_item.name}')
                return
            # Pick_up event did not happen in the pallet
            event.x -= pallet_width()
            for shape in self.list_of_canvas_shapes:
                box = shape.annotation.box
                if event.x < box.pos.x: continue                # Left of box  (out of range)
                if event.x > box.pos.x + box.size.x: continue   # Right of box (out of range)
                if event.y < box.pos.y: continue                # Top of box   (out of range)
                if event.y > box.pos.y + box.size.y: continue   # Bottom of box(out of range)

                self.in_hand.append(shape)
                shape.remove_shape(self)
                self.list_of_canvas_shapes.remove(shape)
                if (self.verbose_events): print (f'Shape picked up from: {box}')
                return
            if (self.verbose_events): print ('No shape in the region')
        def let_go(event):
            if (self.verbose_events): print(f'<let_go> at {event.x},{event.y}')

            
            for item in self.in_hand:
                if parent == 'trash_can':               # Delete the hand
                    self.in_hand.remove(item)
                    continue
                elif parent != 'main_canvas':           # Drag shape to pallet??? Wut?
                    if isinstance(item, str): continue   #Cannot overwrite pallet !
                    self.list_of_canvas_shapes.append(item)
                    item.draw_shape(tkinter_canvas=self.main_canvas, outline_color='gray', fill_color='gray', width_outline=1, location_offset=loc.Pos()) # TODO: I loose the info of the `outline_color`, `fill_color`, `width_outline` !
                    self.in_hand.remove(item)
                    continue
                
                if not isinstance(item, str):           # Dropping shape from hand
                    match (shapes.object_names_array[int(item.annotation.class_id)]):
                        case 'circle':
                            new_shape = shapes.Circle(loc.Size(),
                                                      center_pos=loc.Pos(event.x, event.y),
                                                      size_in_pixels=item.size_in_pixels)
                        case 'half circle':
                            new_shape = shapes.HalfCircle(loc.Size(),
                                                      center_pos=loc.Pos(event.x, event.y),
                                                      size_in_pixels=item.size_in_pixels,
                                                      rotation_rad=item.rotation_rad)
                        case 'square':
                            new_shape = shapes.Square(loc.Size(),
                                                      center_pos=loc.Pos(event.x, event.y),
                                                      size_in_pixels=item.size_in_pixels,
                                                      rotation_rad=item.rotation_rad)
                        case 'heart':
                            new_shape = shapes.Heart(loc.Size(),
                                                      center_pos=loc.Pos(event.x, event.y),
                                                      size_in_pixels=item.size_in_pixels,
                                                      rotation_rad=item.rotation_rad,
                                                      depth_percentage=item.depth_percentage)
                        case 'star':
                            new_shape = shapes.Star(loc.Size(),
                                                      center_pos=loc.Pos(event.x, event.y),
                                                      size_in_pixels=item.size_in_pixels,
                                                      rotation_rad=item.rotation_rad,
                                                      depth_percentage=item.depth_percentage)
                        case _: # 'triangle'
                            new_shape = shapes.SymmetricTriangle(loc.Size(),
                                                      center_pos=loc.Pos(event.x, event.y),
                                                      size_in_pixels=item.size_in_pixels,
                                                      rotation_rad=item.rotation_rad)
                    self.in_hand.remove(item)
                    self.list_of_canvas_shapes.append(new_shape)
                    new_shape.draw_shape(tkinter_canvas=self.main_canvas,
                                         outline_color='gray', fill_color='gray', width_outline=1, # TODO: I loose the info of the `outline_color`, `fill_color`, `width_outline` !
                                         location_offset=loc.Pos())
                    continue
                pass # TODO: UNDER CONSTRUCTION DRAGGING DATA TO EXISTING SHAPE
        self.bind ('<Button-1>',        lambda event: pick_up(event))
        self.bind ('<ButtonRelease-1>', lambda event: let_go (event))
        # self.bind ('<Motion>',          lambda event: temp   (event))

        self.list_of_canvas_shapes.append(shapes.Star(loc.Size(500,500), loc.Pos(60,100), size_in_pixels=64, rotation_rad=2.0))
        for shape in self.list_of_canvas_shapes:
            shape.draw_shape(self.main_canvas, 'blue','red', width_outline=1, location_offset=loc.Pos())
        
        self.pack(side = 'left', fill = 'both', expand=True)
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

#!/usr/bin/env python3
"""A library that covers how the GUI should respond / work"""
# Want to learn about Tkinter gui tool? https://youtu.be/mop6g-c5HEY It coverers about everything. ;)
import common.shapes as shapes
import common.location as loc

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
        self.pallet = GuiPallet(master=self, background_color='white')
        self.main_canvas = tkinter.Canvas(master=self, background='white', borderwidth=2, relief='raised')
        self.main_canvas.pack(side='left', expand=True, fill='both')
        self.actions = GuiActions(master=self, background_color='white')

        # Bind behavior https://www.pythontutorial.net/tkinter/tkinter-event-binding/ 
        self.list_of_canvas_shapes = []
        self.in_hand = []
        self.verbose_events = True
        def pick_up(event, parent:str):
            if (self.verbose_events): print(f'<pick_up> at {event.x},{event.y} in {parent}')

            if parent is not 'main_canvas':
                self.last_pick_up = parent
                return
            
            # Get tuple of closest shapes
            for shape in self.list_of_canvas_shapes:
                box = shape.annotation.box
                if event.x < box.pos.x: continue                # Left of box  (out of range)
                if event.x > box.pos.x + box.size.x: continue   # Right of box (out of range)
                if event.y < box.pos.y: continue                # Top of box   (out of range)
                if event.y > box.pos.y + box.size.y: continue   # Bottom of box(out of range)

                self.in_hand.append(shape)
                shape.remove_shape(self.main_canvas)
                self.list_of_canvas_shapes.remove(shape)
                print(box)
                return
        self.pallet.yellow.bind     ('<Button-1>', lambda event: pick_up(event, parent='yellow'))
        self.pallet.orange.bind     ('<Button-1>', lambda event: pick_up(event, parent='orange'))
        self.pallet.red.bind        ('<Button-1>', lambda event: pick_up(event, parent='red'))
        self.pallet.green.bind      ('<Button-1>', lambda event: pick_up(event, parent='green'))
        self.pallet.purple.bind     ('<Button-1>', lambda event: pick_up(event, parent='purple'))
        self.pallet.blue.bind       ('<Button-1>', lambda event: pick_up(event, parent='blue'))
        self.pallet.circle.bind     ('<Button-1>', lambda event: pick_up(event, parent='circle'))
        self.pallet.square.bind     ('<Button-1>', lambda event: pick_up(event, parent='square'))
        self.pallet.triangle.bind   ('<Button-1>', lambda event: pick_up(event, parent='triangle'))
        self.pallet.star.bind       ('<Button-1>', lambda event: pick_up(event, parent='star'))
        self.pallet.heart.bind      ('<Button-1>', lambda event: pick_up(event, parent='heart'))
        self.pallet.half_circle.bind('<Button-1>', lambda event: pick_up(event, parent='half_circle'))
        self.pallet.trash_can.bind  ('<Button-1>', lambda event: pick_up(event, parent='trash_can'))
        self.actions.play.bind      ('<Button-1>', lambda event: pick_up(event, parent='play'))
        self.actions.ai.bind        ('<Button-1>', lambda event: pick_up(event, parent='ai'))
        self.main_canvas.bind       ('<Button-1>', lambda event: pick_up(event, parent='main_canvas'))
        def let_go(event, parent:str):
            if (self.verbose_events): print(f'<let_go> at {event.x},{event.y} in {parent}')
            
        self.pallet.yellow.bind     ('<ButtonRelease-1>', lambda event: let_go(event, parent='yellow'))
        self.pallet.orange.bind     ('<ButtonRelease-1>', lambda event: let_go(event, parent='orange'))
        self.pallet.red.bind        ('<ButtonRelease-1>', lambda event: let_go(event, parent='red'))
        self.pallet.green.bind      ('<ButtonRelease-1>', lambda event: let_go(event, parent='green'))
        self.pallet.purple.bind     ('<ButtonRelease-1>', lambda event: let_go(event, parent='purple'))
        self.pallet.blue.bind       ('<ButtonRelease-1>', lambda event: let_go(event, parent='blue'))
        self.pallet.circle.bind     ('<ButtonRelease-1>', lambda event: let_go(event, parent='circle'))
        self.pallet.square.bind     ('<ButtonRelease-1>', lambda event: let_go(event, parent='square'))
        self.pallet.triangle.bind   ('<ButtonRelease-1>', lambda event: let_go(event, parent='triangle'))
        self.pallet.star.bind       ('<ButtonRelease-1>', lambda event: let_go(event, parent='star'))
        self.pallet.heart.bind      ('<ButtonRelease-1>', lambda event: let_go(event, parent='heart'))
        self.pallet.half_circle.bind('<ButtonRelease-1>', lambda event: let_go(event, parent='half_circle'))
        self.pallet.trash_can.bind  ('<ButtonRelease-1>', lambda event: let_go(event, parent='trash_can'))
        self.actions.play.bind      ('<ButtonRelease-1>', lambda event: let_go(event, parent='play'))
        self.actions.ai.bind        ('<ButtonRelease-1>', lambda event: let_go(event, parent='ai'))
        self.main_canvas.bind       ('<ButtonRelease-1>', lambda event: let_go(event, parent='main_canvas'))

        def drag(event):
            if (self.verbose_events): print(f'<drag> at {event.x},{event.y}')

        self.list_of_canvas_shapes.append(shapes.Star(loc.Size(500,500), loc.Pos(60,100), size_in_pixels=64, rotation_rad=2.0))
        for shape in self.list_of_canvas_shapes:
            shape.draw_shape(self.main_canvas, 'blue','red', width_outline=1, location_offset=loc.Pos())

class GuiPallet(ttk.Frame):
    def __init__(self, master, background_color:str):
        super().__init__(master, borderwidth=2, relief='groove')

        # Declare
        self.colors_frame = ttk.Frame(master=self, borderwidth=2, relief='groove')
        self.yellow  =ttk.Label(master=self.colors_frame, text = 'Yellow' ,background = background_color)
        self.orange  =ttk.Label(master=self.colors_frame, text = 'Orange' ,background = background_color)
        self.red     =ttk.Label(master=self.colors_frame, text = 'Red'    ,background = background_color)
        self.green   =ttk.Label(master=self.colors_frame, text = 'Green'  ,background = background_color)
        self.purple  =ttk.Label(master=self.colors_frame, text = 'Purple' ,background = background_color)
        self.blue    =ttk.Label(master=self.colors_frame, text = 'Blue'   ,background = background_color)
        self.yellow.pack (expand=True, fill='both', pady=3)
        self.orange.pack (expand=True, fill='both', pady=3)
        self.red.pack    (expand=True, fill='both', pady=3)
        self.green.pack  (expand=True, fill='both', pady=3)
        self.purple.pack (expand=True, fill='both', pady=3)
        self.blue.pack   (expand=True, fill='both', pady=3)
        self.shapes_frame=ttk.Frame(master=self, borderwidth=2, relief='groove')
        self.circle      =ttk.Label(master=self.shapes_frame, text = 'Circle' ,background = background_color)
        self.square      =ttk.Label(master=self.shapes_frame, text = 'Square' ,background = background_color)
        self.triangle    =ttk.Label(master=self.shapes_frame, text = 'Triangle'    ,background = background_color)
        self.star        =ttk.Label(master=self.shapes_frame, text = 'Star'  ,background = background_color)
        self.heart       =ttk.Label(master=self.shapes_frame, text = 'Heart' ,background = background_color)
        self.half_circle =ttk.Label(master=self.shapes_frame, text = 'Half_circle'   ,background = background_color)
        self.circle.pack     (expand=True, fill='both', pady=3)
        self.square.pack     (expand=True, fill='both', pady=3)
        self.triangle.pack   (expand=True, fill='both', pady=3)
        self.star.pack       (expand=True, fill='both', pady=3)
        self.heart.pack      (expand=True, fill='both', pady=3)
        self.half_circle.pack(expand=True, fill='both', pady=3)
        self.trash_can      =ttk.Label(master=self, text = 'Trash_can' ,background = background_color)

        # Pack
        self.colors_frame.pack(expand=True, fill='both')
        self.shapes_frame.pack(expand=True, fill='both')
        self.trash_can.pack   (expand=True, fill='both', pady=3)
        self.pack(side = 'left', fill = 'y', padx = 10, pady = 10)
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
        self.pack(side = 'left', fill = 'y', padx = 10, pady = 10)


app = Gui()
app.mainloop()

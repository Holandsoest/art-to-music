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
            self.unbind_all('<Button-1>')
            self.unbind_all('<ButtonRelease-1>')
            bind()

            if parent != 'main_canvas':
                self.in_hand.append(parent)
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
                print ('Item picked up')
                return
        # FOUND BUG: event and parent are incorrect when `let_go`
        def let_go(event, parent:str):
            if (self.verbose_events): print(f'<let_go> at {event.x},{event.y} in {parent}')

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
        def bind():
            self.pallet.yellow.bind     ('<Button-1>', lambda event: pick_up(event, 'yellow'))
            self.pallet.orange.bind     ('<Button-1>', lambda event: pick_up(event, 'orange'))
            self.pallet.red.bind        ('<Button-1>', lambda event: pick_up(event, 'red'))
            self.pallet.green.bind      ('<Button-1>', lambda event: pick_up(event, 'green'))
            self.pallet.purple.bind     ('<Button-1>', lambda event: pick_up(event, 'purple'))
            self.pallet.blue.bind       ('<Button-1>', lambda event: pick_up(event, 'blue'))
            self.pallet.circle.bind     ('<Button-1>', lambda event: pick_up(event, 'circle'))
            self.pallet.square.bind     ('<Button-1>', lambda event: pick_up(event, 'square'))
            self.pallet.triangle.bind   ('<Button-1>', lambda event: pick_up(event, 'triangle'))
            self.pallet.star.bind       ('<Button-1>', lambda event: pick_up(event, 'star'))
            self.pallet.heart.bind      ('<Button-1>', lambda event: pick_up(event, 'heart'))
            self.pallet.half_circle.bind('<Button-1>', lambda event: pick_up(event, 'half_circle'))
            self.pallet.trash_can.bind  ('<Button-1>', lambda event: pick_up(event, 'trash_can'))
            self.actions.play.bind      ('<Button-1>', lambda event: pick_up(event, 'play'))
            self.actions.ai.bind        ('<Button-1>', lambda event: pick_up(event, 'ai'))
            self.main_canvas.bind       ('<Button-1>', lambda event: pick_up(event, 'main_canvas'))

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
            # self.actions.play.bind      ('<ButtonRelease-1>', lambda event: let_go(event, parent='play'))
            # self.actions.ai.bind        ('<ButtonRelease-1>', lambda event: let_go(event, parent='ai'))
            self.main_canvas.bind       ('<ButtonRelease-1>', lambda event: let_go(event, parent='main_canvas'))
            self.main_canvas.bind       ('<Motion>', lambda event: let_go(event, parent='main_canvas'))
        bind()

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
        self.pack(side = 'left', fill = 'y', padx = 3, pady = 3)
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

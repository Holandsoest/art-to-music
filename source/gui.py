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
        pallet = GuiPallet(master=self, background_color='white')
        main_canvas = tkinter.Canvas(master=self, background='white', borderwidth=2, relief='raised')
        main_canvas.pack(side='left', expand=True, fill='both')
        actions = GuiActions(master=self, background_color='white')

        # Bind behavior
        
class GuiPallet(ttk.Frame):
    def __init__(self, master, background_color:str):
        super().__init__(master, borderwidth=2, relief='groove')

        # Declare
        colors_frame = ttk.Frame(master=self, borderwidth=2, relief='groove')
        yellow  =ttk.Label(master=colors_frame, text = 'Yellow' ,background = background_color)
        orange  =ttk.Label(master=colors_frame, text = 'Orange' ,background = background_color)
        red     =ttk.Label(master=colors_frame, text = 'Red'    ,background = background_color)
        green   =ttk.Label(master=colors_frame, text = 'Green'  ,background = background_color)
        purple  =ttk.Label(master=colors_frame, text = 'Purple' ,background = background_color)
        blue    =ttk.Label(master=colors_frame, text = 'Blue'   ,background = background_color)
        yellow.pack (expand=True, fill='both', pady=3)
        orange.pack (expand=True, fill='both', pady=3)
        red.pack    (expand=True, fill='both', pady=3)
        green.pack  (expand=True, fill='both', pady=3)
        purple.pack (expand=True, fill='both', pady=3)
        blue.pack   (expand=True, fill='both', pady=3)
        shapes_frame=ttk.Frame(master=self, borderwidth=2, relief='groove')
        circle      =ttk.Label(master=shapes_frame, text = 'Circle' ,background = background_color)
        square      =ttk.Label(master=shapes_frame, text = 'Square' ,background = background_color)
        triangle    =ttk.Label(master=shapes_frame, text = 'Triangle'    ,background = background_color)
        star        =ttk.Label(master=shapes_frame, text = 'Star'  ,background = background_color)
        heart       =ttk.Label(master=shapes_frame, text = 'Heart' ,background = background_color)
        half_circle =ttk.Label(master=shapes_frame, text = 'Half_circle'   ,background = background_color)
        circle.pack     (expand=True, fill='both', pady=3)
        square.pack     (expand=True, fill='both', pady=3)
        triangle.pack   (expand=True, fill='both', pady=3)
        star.pack       (expand=True, fill='both', pady=3)
        heart.pack      (expand=True, fill='both', pady=3)
        half_circle.pack(expand=True, fill='both', pady=3)
        trash_can      =ttk.Label(master=self, text = 'Trash_can' ,background = background_color)

        # Pack
        colors_frame.pack(expand=True, fill='both')
        shapes_frame.pack(expand=True, fill='both')
        trash_can.pack   (expand=True, fill='both', pady=3)
        self.pack(side = 'left', fill = 'y', padx = 10, pady = 10)
class GuiActions(ttk.Frame):
    def __init__(self, master, background_color:str):
        super().__init__(master, borderwidth=2, relief='groove')

        # Declare
        settings_frame = ttk.Frame(master=self, borderwidth=2, relief='groove')
        play  =ttk.Label(master=settings_frame, text = 'Play' ,background = background_color)
        ai  =ttk.Label(master=settings_frame, text = 'AI' ,background = background_color)
        play.pack (expand=True, fill='both', pady=3)
        ai.pack   (expand=True, fill='both', pady=3)

        # Pack
        settings_frame.pack(expand=True, fill='y')
        self.pack(side = 'left', fill = 'y', padx = 10, pady = 10)
        

app = Gui()
app.mainloop()

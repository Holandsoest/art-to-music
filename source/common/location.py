#!/usr/bin/env python3
"""Common functions and classes about sizes and positions"""

class Pos:
    """A simple class that can be used to store an x & y variables as a position or as a size."""

    # Defining
    def __init__(self, x=0, y=0, force_int=False):
        if force_int:
            self.x = int(round(x))
            self.y = int(round(y))
        else:
            self.x = x
            self.y = y
    def __str__(self) -> str:
        return f'x:{self.x}, y:{self.y}'
    def __eq__(self, other) -> bool:
        if (self.x != other.x): return False
        if (self.y != other.y): return False
        return True
    def __add__(self, other) -> int|float:
        return Pos(x= self.x + other.x,
                   y= self.y + other.y)
    def __sub__(self, other) -> int|float:
        return Pos(x= self.x - other.x,
                   y= self.y - other.y)
    
    # Basic math functions
    def min(self) -> int | float:
        """returns the minimum value from x or y"""
        return min(self.x, self.y)
    def max(self) -> int | float:
        """returns the maximum value from x or y"""
        return max(self.x, self.y)
    def add(self) -> int | float:
        """returns x + y"""
        return self.x + self.y
    def count(self) -> int | float:
        """returns x * y"""
        return self.x * self.y
    
    # Parsing outwards
    def get_as_list(self) -> list:
        return [self.x, self.y]
class Size(Pos):
    def __str__(self) -> str:
        return f'w:{self.x}, h:{self.y}'
class Box:
    def __init__(self, x, y, width, height):
        self.pos = Pos(x,y)
        self.size = Size(width,height)
    def __str__(self) -> str:
        return f'{self.pos},  {self.size}'
    def overlaps(self, other) -> bool:
        """Checks if this box overlaps with the `other` Box,
        
        Touching does not count as an overlap."""
        if self.pos.x + self.size.x < other.pos.x:  return False # self is left of other
        if self.pos.y + self.size.y < other.pos.y:  return False # self is above other
        if self.pos.x > other.pos.x + other.size.x: return False # self is right of other
        if self.pos.y > other.pos.y + other.size.y: return False # self is below other
        return True

def get_screensize() -> Size:
    """Uses tkinter to grab the screensize of the primary screen, returns a Pos class with the x and y values as length=x and hight=y"""
    import tkinter
    root = tkinter.Tk()
    return Size(x=root.winfo_screenwidth(), y=root.winfo_screenheight())
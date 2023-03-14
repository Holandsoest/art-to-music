class Pos:
    """A simple class that can be used to store an x & y variables as a position or as a size."""

    # Defining
    def __init__(self, x=0, y=0, force_int=False):
        if force_int:
            self.x = int(x)
            self.y = int(y)
        else:
            self.x = x
            self.y = y
    def __str__(self) -> str:
        return f'x:{self.x}, y:{self.y}'
    
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
    
def get_screensize() -> Pos:
    """Uses tkinter to grab the screensize of the primary screen, returns a Pos class with the x and y values as length=x and hight=y"""
    import tkinter
    root = tkinter.Tk()
    return Pos(x=root.winfo_screenwidth(), y=root.winfo_screenheight())
from tkinter import *
from PIL import ImageGrab

root = Tk()

cv= Canvas(root, width=850, height=560, bg="white")
cv.pack(pady=20)

cv.create_rectangle(60,60,100,100)
#cv.create_line([0, 10, 10, 10], fill='green')

cv.update()
#print(root.winfo_width())
def getter(widget):
    x=root.winfo_rootx()+widget.winfo_x()
    print(x)
    y=root.winfo_rooty()+widget.winfo_y()
    print(y)
    x1=x+widget.winfo_width()
    print(x1)
    y1=y+widget.winfo_height()
    print(y1)
    ImageGrab.grab().crop((x,y,x1,y1)).save("em.jpg")

getter(cv)
my_button = Button(root, text="Red Hart", command= getter(widget=cv))
my_button.place(x=350, y=620 )

root.mainloop()
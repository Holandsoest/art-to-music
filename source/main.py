from tkinter import * 
import tkinter as tk

root =  Tk()
#title of the gui
root.title('gui test')
#size of vester
root.geometry("900x700")
#put text into the gui
my_label1 = Label(root, text = 'shapes regognision').pack()
#make a icon for the map itself
root.iconbitmap('triangle.ico')

#canvas with shapes in it

#make the canvas so we can add shapes in it
my_canvas= Canvas(root, width=850, height=560, bg="white")
my_canvas.pack(pady=20)

#create line
#my_canvas.create_line(x1, y1, x2, y2, fill="color")
#my_canvas.create_line(0, 100, 300, 100, fill="red")

#create rectangle/square
#my_canvas.create_rectangle(350, 400, 500, 550, fill="red")

#create oval/circle
#my_canvas.create_oval(600, 40, 700, 80, fill="red")

#my_circle = my_canvas.create_oval(0, 0, 60, 60, fill="red")
# img = PhotoImage(file="triangle.png")
# my_image = my_canvas.create_image(260,125, anchor=NW, image=img)

# Initialize our basic shapes for the demo
import shapes
my_canvas.create_image(70,100, anchor=CENTER, image=shapes.img_heart) # TODO: Fix anchor to the center of the image.
my_canvas.create_image(80,150, anchor=CENTER, image=shapes.img_heart) # TODO: Fix anchor to the center of the image.
my_canvas.create_image(90,200, anchor=CENTER, image=shapes.img_heart) # TODO: Fix anchor to the center of the image.
my_canvas.create_image(100,250, anchor=CENTER, image=shapes.img_triangle) # TODO: Fix anchor to the center of the image.
my_canvas.create_image(110,300, anchor=CENTER, image=shapes.img_triangle) # TODO: Fix anchor to the center of the image.
my_canvas.create_image(140, 350, anchor=CENTER, image=shapes.img_star)
my_canvas.create_image(160, 380, anchor=CENTER, image=shapes.img_trianglered)

import tkinter as tk

# class Main():

#     def __init__(self, root):
#         self.root = root
#         self.count = 0

#         btn = Button(root, text ='click me')
#         btn.bind('<Button-1>', self.click)
#         btn.place(x=350, y=620 )

#     def click(self, event):
#         self.count += 1
#         self.lbl.config(text=f'count {self.count}')




# my_button = Button(root, text="up", command=movement1.movementx( a= +30))
# my_button.place(x=350, y=620 )

S1 =20

# Move the closest image to the mouse to the location of the mouse TODO(if they are in range)
# def drag(mouse):
#     closest_shape = my_canvas.find_closest(mouse.x, mouse.y)
#     shape_x, shape_y = my_canvas.coords(closest_shape)
#     my_canvas.moveto(closest_shape, mouse.x, mouse.y)

def drag(mouse):
    closest_shape = my_canvas.find_closest(mouse.x, mouse.y)
    shape_x, shape_y = my_canvas.coords(closest_shape)
    if (shape_x - S1 < mouse.x < shape_x + S1 and shape_y - S1 < mouse.y < shape_y + S1):
        my_canvas.moveto(closest_shape, mouse.x-30, mouse.y-30)
    else :
        print("nothing close enough")    

# # Changes the size of the shape, with scrolling the mouse
# def mouse_wheel(event):
#     # respond to Linux or Windows wheel event
#     delta = 0
#     if event.num == 5 or event.delta == -120: delta = 1
#     elif event.num == 4 or event.delta == 120: delta = -1
#     else: print("Something went wrong while scrolling: " + str(event))

#     # Get current scale as a double
#     closest_shape = my_canvas.find_closest(event.x, event.y)
    

my_label = Label(root, text="")
my_label.pack(pady=20)

my_canvas.bind('<B1-Motion>', drag) # Create a callback. Whenever we hold `LMB` and move the mouse this function is called.

#my_canvas.bind("<MouseWheel>", mouse_wheel) # with Windows OS, Create a callback, Whenever ... call this function.
#my_canvas.bind("<Button-4>", mouse_wheel) # with Linux OS, Create a callback, Whenever ... call this function.
#my_canvas.bind("<Button-5>", mouse_wheel) # with Linux OS, Create a callback, Whenever ... call this function.

#button for quitting the program
#button_quit = Button(root, text="Exit", command=root.quit)
#button_quit.pack()

root.mainloop()
print('exited')

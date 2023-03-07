from tkinter import * 
from PIL import ImageTk, Image
from PIL import ImageGrab
root =  Tk()
#title of the gui
root.title('gui test')
#size of vester
root.geometry("900x700")
#put text into the gui
#my_label = Label(root, text = 'Git Fetch Bitch!').pack()
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


thislist=[]
class shapes:
    def __init__(self, xs, ys):
        self.xs=xs
        self.ys=ys
thislist.append(shapes(20,20))

# img2 = PhotoImage(file="hart.png")
# my_image = my_canvas.create_image(260,125, anchor=NW, image=img2)
my_canvas.update()
x = 0
y=0
def move(e):
    global x 
    global y
    e.x
    e.y
    x = e.x
    y = e.y
    print(x)
    print(y)

for i in thislist:
    if i.xs < x <i.xs+20 and i.ys < y < i.ys+20:
        i.xs = x
        i.ys = y
    img5 = Image.open("hart.png")
    resized3 = img5.resize((60,60), Image.Resampling.LANCZOS)
    img6 = ImageTk.PhotoImage(resized3)
    my_image3 = my_canvas.create_image(i.xs, i.ys, anchor=NW, image=img6)

    #global img
    #global img2
    #image 1
    # img = PhotoImage(file="triangle.png")
    # my_image = my_canvas.create_image(e.x, e.y, image=img)
    #image 2
    #img2 = PhotoImage(file="hart.png")
    #my_image = my_canvas.create_image(e.x, e.y, image=img2)
    #configureation of the coordinates
    # my_label.config(text="coordinates x " + str(e.x) + " y " + str(e.y))

my_label = Label(root, text="")
my_label.pack(pady=20)

my_canvas.bind('<B1-Motion>', move)


#class shapes:
#    def check_if_works(self):
#        if self.marks >= 260



#button for quitting the program
#button_quit = Button(root, text="Exit", command=root.quit)
#button_quit.pack()

root.mainloop()


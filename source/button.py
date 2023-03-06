from tkinter import * 
from PIL import ImageTk, Image
# root =  Tk()

# root.title('gui test')
# root.geometry("900x700")
# root.iconbitmap('triangle.ico')

# my_canvas= Canvas(root, width=850, height=560, bg="white")
# my_canvas.pack(pady=20)

# a = 20
# b = 50
# S1 = 60
# S2 = 50

# #resized picture 1


# a2 = 150
# b2 = 150
# S3 = 60
# S4 = 60


# a3 = 100
# b3 = 100
# S5 = 60
# S6 = 60



# def thing1():
#     my_image = my_canvas.create_image(a, b, anchor=NW, image=img2)

# img = Image.open("triangle.png")
# resized = img.resize((S1,S2), Image.Resampling.LANCZOS)
# img2 = ImageTk.PhotoImage(resized)


# my_button = Button(root, text="Red Hart", command=thing1)
# my_button.place(x=200, y=620 )


# def thing2():
#     my_image2 = my_canvas.create_image(a2, b2, anchor=NW, image=img4)

# img3 = Image.open("hart.png")
# resized2 = img3.resize((S3,S4), Image.Resampling.LANCZOS)
# img4 = ImageTk.PhotoImage(resized2)


# my_button = Button(root, text="Red Hart", command=thing2)
# my_button.place(x=350, y=620 )



# def thing3():
#     my_image3 = my_canvas.create_image(a3, b3, anchor=NW, image=img6)

# img5 = Image.open("star.png")
# resized3 = img5.resize((S5,S6), Image.Resampling.LANCZOS)
# img6 = ImageTk.PhotoImage(resized3)


# my_button = Button(root, text="Red Hart", command=thing3)
# my_button.place(x=500, y=620 )


# mainloop()


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

class Shapes:
    def __init__(shape, size_x, size_y, x_axis, y_axis, coller):
        shape.size_x = size_x
        shape.size_y = size_y
        shape.x_axis = x_axis
        shape.y_axes = y_axis
        shape.coller = coller
    def thing1 (size_x, size_y, x_axis, y_axis, coller):
        my_canvas.create_rectangle(size_x, size_y, x_axis, y_axis, fill=coller)
    def thing2 (size_x, size_y, x_axis, y_axis, coller):
        my_canvas.create_rectangle(size_x, size_y, x_axis, y_axis, fill=coller)

# my_canvas.create_rectangle.(350, 400, 500, 550, fill="red")
class coller:
    def collor(kleur, rood, groen, blauw)
        kleur.rood = rood
        kleur.groen = groen
        kleur.blauw = blauw
    def keuzen(rood, groen, blauw)
        if(button1 == 1)

my_button = Button(root, text="Red Hart", command=thing2)
my_button.place(x=350, y=620 )

my_button = Button(root, text="Red Hart", command=thing2)
my_button.place(x=350, y=620 )

my_button = Button(root, text="Red Hart", command=thing2)
my_button.place(x=350, y=620 )

triangle = Shapes.thing1(20, 20, 50 , 150, "red")
triangle = Shapes.thing2(130, 130, 110 , 150 , "blue")

mainloop()


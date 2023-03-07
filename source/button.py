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
    def __init__(shape, size_x, size_y, x_axis, y_axis):
        shape.size_x = size_x
        shape.size_y = size_y
        shape.x_axis = x_axis
        shape.y_axes = y_axis
    def thing1 (size_x, size_y, x_axis, y_axis):
        my_canvas.create_rectangle(size_x, size_y, x_axis, y_axis)
    def thing2 (size_x, size_y, x_axis, y_axis):
        my_canvas.create_rectangle(size_x, size_y, x_axis, y_axis)


star = Shapes.thing2(20, 50, 60 , 50) 

# a3 = 20
# b3 = 50
# S5 = 60
# S6 = 50

# my_image3 = my_canvas.create_image(a3, b3, anchor=NW, image=img6)
# img5 = Image.open("star.png")
# resized3 = img5.resize((S5,S6), Image.Resampling.LANCZOS)
# img6 = ImageTk.PhotoImage(resized3)


a3 = 100
b3 = 100
S5 = 60
S6 = 60

img5 = Image.open("hart.png")
resized3 = img5.resize((60,60), Image.Resampling.LANCZOS)
img6 = ImageTk.PhotoImage(resized3)
my_image3 = my_canvas.create_image(a3, b3, anchor=NW, image=img6)



w=600
h=400
x=w//2
y=h//2
a = 10
b = 10

my_circle = my_canvas.create_oval(x,y, x+a, y+b)
# my_canvas.create_rectangle.(350, 400, 500, 550, fill="red")
# class coller:
#     def collor(kleur, rood, groen, blauw)
#         kleur.rood = rood
#         kleur.groen = groen
#         kleur.blauw = blauw
#     def keuzen(rood, groen, blauw)
#         if(button1 == 1)

def pressing():
    d = 0
    if (my_button6 == ".!button"):
        d = d+10
    print(d)


my_button6 = Button(root, text="up", command=pressing)
my_button6.place(x=800, y=620 )
    
# class movement1:
#     def __init__(mv, a, b):
#         mv.a = a
#         mv.b = b
#     def movementx(a):
#         triangle = Shapes.thing1(20 - a, 20, 30 + a , 30 , "green")
#     def movementy(b):
#         triangle = Shapes.thing1(20 , 20 - b, 30 , 30 + b, "green")
    # def presseing(a):
    #     if (my_button == 1):
    #         a = 30  
    #     else:
    #         print("none")
    




# my_button = Button(root, text="up", command=movement1.movementx( a= +30))
# my_button.place(x=350, y=620 )

# my_button2 = Button(root, text="down", command=movement1.movementx(a = -30))
# my_button2.place(x=390, y=620 )

# my_button3 = Button(root, text="left", command=movement1.movementy(b =+30))
# my_button3.place(x=430, y=620 )

# my_button4 = Button(root, text="left", command=movement1.movementy(b = -30))
# my_button4.place(x=470, y=620 )



# my_button = Button(root, text="blue", command=thing2)
# my_button.place(x=350, y=620 )

# my_button = Button(root, text="red", command=thing2)
# my_button.place(x=350, y=620 )







# def thing1():
#     my_image = my_canvas.create_image(a, b, anchor=NW, image=img2)
#     img = Image.open("triangle.png")
#     resized = img.resize((S1,S2), Image.Resampling.LANCZOS)
#     img2 = ImageTk.PhotoImage(resized)

# my_label1 = Label(root,image=img2)
# my_button = Button(root, text="triangle", command=thing1)
# my_button.place(x=200, y=620 )


mainloop()


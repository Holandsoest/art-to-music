from tkinter import * 
from PIL import ImageTk, Image
root =  Tk()

root.title('gui test')
root.geometry("900x700")
root.iconbitmap('triangle.ico')

my_canvas= Canvas(root, width=850, height=560, bg="white")
my_canvas.pack(pady=20)

a = 20
b = 50
S1 = 60
S2 = 50

#resized picture 1


a2 = 150
b2 = 150
S3 = 60
S4 = 60


a3 = 100
b3 = 100
S5 = 60
S6 = 60



def thing1():
    my_image = my_canvas.create_image(a, b, anchor=NW, image=img2)

img = Image.open("triangle.png")
resized = img.resize((S1,S2), Image.Resampling.LANCZOS)
img2 = ImageTk.PhotoImage(resized)

my_label1 = Label(root,image=img2)
my_button = Button(root, text="Red Hart", command=thing1)
my_button.place(x=200, y=620 )


def thing2():
    my_image2 = my_canvas.create_image(a2, b2, anchor=NW, image=img4)

img3 = Image.open("hart.png")
resized2 = img3.resize((S3,S4), Image.Resampling.LANCZOS)
img4 = ImageTk.PhotoImage(resized2)

my_label2 = Label(root,image=img4)
my_button = Button(root, text="Red Hart", command=thing2)
my_button.place(x=350, y=620 )



def thing3():
    my_image3 = my_canvas.create_image(a3, b3, anchor=NW, image=img6)

img5 = Image.open("star.png")
resized3 = img5.resize((S5,S6), Image.Resampling.LANCZOS)
img6 = ImageTk.PhotoImage(resized3)

my_label3 = Label(root,image=img6)
my_button = Button(root, text="Red Hart", command=thing3)
my_button.place(x=500, y=620 )

mainloop()
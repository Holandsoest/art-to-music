# class Complex:
#     def __init__(self, real, imag):
#         self.real = real
#         self.imag = imag 

#     def add(self, number):
#         real = self.real + number.real
#         imag = self.imag + number.imag
#         result = Complex(real, imag)
#         return result
    
# n1 = Complex(5, 6)
# n2 = Complex(-4, 2)
# result = n1.add(n2) 
# print("real = ", result.real)
# print("imag = ", result.imag)


from tkinter import * 
from PIL import ImageTk, Image
root =  Tk()

root.title('gui test')
root.geometry("900x700")
root.iconbitmap('triangle.ico')



my_canvas= Canvas(root, width=850, height=560, bg="white")
my_canvas.pack(pady=20)

# a = 20
# b = 50
# S1 = 60
# S2 = 50

# #resized picture 1
# img = Image.open("triangle.png")
# resized = img.resize((S1,S2), Image.Resampling.LANCZOS)
# img2 = ImageTk.PhotoImage(resized)
# my_image = my_canvas.create_image(a, b, anchor=NW, image=img2)

# a2 = 150
# b2 = 150
# S3 = 60
# S4 = 60

# img3 = Image.open("hart.png")
# resized2 = img3.resize((S3,S4), Image.Resampling.LANCZOS)
# img4 = ImageTk.PhotoImage(resized2)
# my_image2 = my_canvas.create_image(a2, b2, anchor=NW, image=img4)

# a3 = 100
# b3 = 100
# S5 = 60
# S6 = 60

# img5 = Image.open("hart.png")
# resized3 = img5.resize((S5,S6), Image.Resampling.LANCZOS)
# img6 = ImageTk.PhotoImage(resized3)
# my_image3 = my_canvas.create_image(a3, b3, anchor=NW, image=img6)



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
7


class imageonsite:
    def __init__(e, X,Y):
        e.x = X
        e.y = Y   
    def move(e):
        if a < e.x < S1+a and b < e.y < S2+b:
            global img2
            img = Image.open("triangle.png")
            resized = img.resize((S1,S2), Image.Resampling.LANCZOS)
            img2 = ImageTk.PhotoImage(resized)
            my_image = my_canvas.create_image(e.x, e.y, image=img2)
            # a = e.x
            # print(a)
        elif a2 < e.x < S3+a2 and b2 < e.y < S4+b2: 
            global img4
            img3 = Image.open("hart.png")
            resized2 = img3.resize((S3,S4), Image.Resampling.LANCZOS)
            img4 = ImageTk.PhotoImage(resized2)
            my_image = my_canvas.create_image(e.x, e.y, image=img4)

        elif a3 < e.x < S5+a3 and b3 < e.y < S6+b3: 
            global img6
            img5 = Image.open("star.png")
            resized3 = img5.resize((S3,S4), Image.Resampling.LANCZOS)
            img6 = ImageTk.PhotoImage(resized3)
            my_image = my_canvas.create_image(e.x, e.y, image=img6)
    root.bind('<B1-Motion>', move)  

root.mainloop()





# class imageonsite:
#     def check_true_false(self):
#         if self.X == A:
#             return True
#         else: 
#             return False
        
#     def __init__(self, X, Y):
#         self.X = X
#         self.Y = Y

# imgA = imageonsite(10, 20)
# imgB = imageonsite(20, 10)
# didpas = imgA.check_true_false()
# print(didpas)
        
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

a = 20
b = 50
S1 = 60
S2 = 50

img = Image.open("triangle.png")
resized = img.resize((S1,S2), Image.Resampling.LANCZOS)
img2 = ImageTk.PhotoImage(resized)
#img2 = PhotoImage(file="triangle.png")


my_image = my_canvas.create_image(a, b, anchor=NW, image=img2)

class imageonsite:
    def move(e):
        if a < e.x < S1+a and b < e.y < S2+b:
            global img2
            img = Image.open("triangle.png")
            resized = img.resize((S1,S2), Image.Resampling.LANCZOS)
            img2 = ImageTk.PhotoImage(resized)
            my_image = my_canvas.create_image(e.x, e.y, image=img2)
            # a = e.x
            # print(a)
        else: 
            print("false")
            return False
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
        
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
root =  Tk()
#title of the gui
root.title('gui test')
#size of vester
root.geometry("900x700")
#put text into the gui
#my_label = Label(root, text = 'Git Fetch Bitch!').pack()
#my_label1 = Label(root, text = 'shapes regognision').pack()
#make a icon for the map itself
root.iconbitmap('triangle.ico')

my_canvas= Canvas(root, width=850, height=560, bg="white")
my_canvas.pack(pady=20)

a = 20
b = 50
img = PhotoImage(file="triangle.png")
my_image = my_canvas.create_image(a, b, anchor=NW, image=img)


class imageonsite:
    def move(e):
        if a < e.x < b and a < e.y < b:
            print("true")
            return True
        else: 
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
        
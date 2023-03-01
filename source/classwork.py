# class numbers:
#     def __init__(self, X,Y):
#         self.x = X
#         self.y = Y

#     def __str__(self):
#         return f"{self.x} {self.y}"

# p1 = numbers(10,  10)
# p1.x = 30
# print(p1)
from tkinter import * 
from PIL import ImageTk, Image
root =  Tk()

root.title('gui test')
root.geometry("900x700")
root.iconbitmap('triangle.ico')



my_canvas= Canvas(root, width=850, height=560, bg="white")
my_canvas.pack(pady=20)

def move():
    global x
    x = 6

root.bind('<B1-Motion>', move)  

move()
print(x)

root.mainloop()
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


print(key = move)

root.mainloop()


def my_function(x):
      return 5 * x

print(my_function(3)*2)
print(my_function(5))
print(my_function(9))



def tri_recursion(k):
    if(k > 0):
        result = k + tri_recursion(k - 1)
        print(result)
    else:
        result = 0
    return result

print("Recursion Example Results")
tri_recursion(6)

#https://www.w3schools.com/python/python_lambda.asp 

def myfunc(n):
      return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))





import random
print(random.randrange(1, 10))

a = "Hello, World!"
print(a[1])

for x in "banana":
  print(x)

txt = "The best things in life are free!"
print("expensive" not in txt)

#python list where i endend
#https://www.w3schools.com/python/python_lists.asp

thislist = [100, 50, 65, 82, 23]
thislist.sort()
print(thislist)




def myfunc(n):
      return abs(n - 50)

thislist = [100, 50, 65, 82, 23]

thislist.sort(key = myfunc)

print(thislist)


adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for x in adj:
  for y in fruits:
    print(x, y)

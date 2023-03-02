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

    
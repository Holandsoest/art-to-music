from tkinter import * 

root =  Tk()


root.title('gui test')
root.geometry("700x500")

my_label = Label(root, text = 'Git Fetch Bitch!').pack()
my_label1 = Label(root, text = 'hello ').pack()

root.iconbitmap('triangle.ico')

root.mainloop()
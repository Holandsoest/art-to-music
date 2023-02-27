from tkinter import * 

root =  Tk()


root.title('gui test')
root.geometry("900x700")

my_label = Label(root, text = 'Git Fetch Bitch!').pack()
my_label1 = Label(root, text = 'hello ').pack()

root.iconbitmap('triangle.ico')

#canvas with shapes in it

#make the canvas so we can add shapes in it
my_canvas= Canvas(root, width=600, height=500, bg="white")
my_canvas.pack(pady=20)




button_quit = Button(root, text="Exit", command=root.quit)
button_quit.pack()

root.mainloop()
from tkinter import * 
import csv
root =  Tk()
root.title('gui test')
root.geometry("900x700")
my_label1 = Label(root, text = 'shapes regognision').pack()
root.iconbitmap('triangle.ico')



my_canvas= Canvas(root, width=850, height=560, bg="white")
my_canvas.pack(pady=20)



with open('coordinates.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    with open('coordinates2.csv', 'w') as new_file:
        fieldnames = ['x', 'y']

        csv_writer = csv.DictWriter(new_file[1])

        csv_writer.writeheader()

        for line in csv_reader:
            csv_writer.writerow(line)

def move(e):
    my_label.config(text="coordinates x " + str(e.x) + " y " + str(e.y))

my_label = Label(root, text="")
my_label.pack(pady=20)

my_canvas.bind('<B1-Motion>', move)

root.mainloop()

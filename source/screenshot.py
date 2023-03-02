from tkinter import *
from PIL import ImageGrab

root = Tk()

cv= Canvas(root, width=850, height=560, bg="white")
cv.pack(pady=20)

cv.create_rectangle(60,60,100,100)
#cv.create_line([0, 10, 10, 10], fill='green')

cv.update()

def getter():
    x=root.winfo_rootx()
    print(x)
    y=root.winfo_rooty()
    print(y)
    x1=root.winfo_rootx()+850
    print(x1)
    y1=root.winfo_rootx()+560
    print(y1)
    ImageGrab.grab().crop((x,y,x1,y1)).save("em.jpg")


my_button = Button(root, text="Red Hart", command= getter)
my_button.place(x=350, y=620 )

root.mainloop()


# import math
# import PySimpleGUI as sg
# from PIL import ImageGrab
# from tkinter import *
# from PIL import ImageGrab

# def save_element_as_file(element, filename):
#     widget = element.Widget
#     box = (widget.winfo_rootx(),
#            widget.winfo_rooty(),
#            widget.winfo_rootx() + widget.winfo_width(),
#            widget.winfo_rooty() + widget.winfo_height()
#           )

#     grab = ImageGrab.grab(bbox=box)
#     grab.save(filename)


# layout = [
#     [sg.Graph(
#         canvas_size=(800, 600),
#         graph_bottom_left=(-105,-105),
#         graph_top_right=(105,105),
#         background_color='white',
#         key='graph')],
#     [sg.Push(), sg.Button('Save')],
# ]

# sg.set_options(dpi_awareness=True)

# window = sg.Window('Graph of Sine Function', layout, grab_anywhere=True, finalize=True)
# graph = window['graph']

# img = PhotoImage(file="triangle.png")
# my_image = graph.create_image(260,125, anchor=NW, image=img)



# while True:

#     event, values = window.read()

#     if event == sg.WIN_CLOSED:
#         break
#     elif event == 'Save':
#         filename='test.jpg'
#         save_element_as_file(graph, filename)

# window.close()

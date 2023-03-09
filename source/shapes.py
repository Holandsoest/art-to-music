from PIL import ImageTk, Image, ImageGrab

# Define images
img_heart = ImageTk.PhotoImage(Image.open("hart.png").resize((60,60), Image.Resampling.LANCZOS))
img_triangle = ImageTk.PhotoImage(Image.open("triangle.png").resize((60,60), Image.Resampling.LANCZOS))
img_triangle = ImageTk.PhotoImage(Image.open("star.png").resize((60,60), Image.Resampling.LANCZOS))
img_star = ImageTk.PhotoImage(Image.open("star.png").resize((60,60), Image.Resampling.LANCZOS))
img_trianglered = ImageTk.PhotoImage(Image.open("trianglered.png").resize((60,60), Image.Resampling.LANCZOS))
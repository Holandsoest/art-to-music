from PIL import ImageTk, Image, ImageGrab

# Define images
B=120
CircleBlue = ImageTk.PhotoImage(Image.open("CircleBlue.png").resize((B,B), Image.Resampling.LANCZOS))
CircleGreen = ImageTk.PhotoImage(Image.open("CircleGreen.png").resize((B,B), Image.Resampling.LANCZOS))
CircleOrange = ImageTk.PhotoImage(Image.open("CircleOrange.png").resize((B,B), Image.Resampling.LANCZOS))
CirclePurple = ImageTk.PhotoImage(Image.open("CirclePurple.png").resize((B,B), Image.Resampling.LANCZOS))
CircleYellow = ImageTk.PhotoImage(Image.open("CircleYellow.png").resize((B,B), Image.Resampling.LANCZOS))

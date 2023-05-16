import math

def get_bpm_from_color(x_axis, y_axis, image):
    """
    This function gets the RGB values of a pixel on the (x,y)-coordinates of an image and scales this to a number of the table of 30.
    It takes three arguments:
    - x_axis: the x axis coordinate of the pixel
    - y_axis: the y axis coordinate of the pixel
    - image:  the image that will be scanned for the pixel
    
    It returns a scaled value of the table of 30. This number will represent the beats per minute(BPM) of the instrument.
    """
    b, g, r = image[y_axis, x_axis]
    b = int(b)
    g = int(g)
    r = int(r)

    # # For now the rgb colorcode will represent a bpm match, but later on we will probably work with colorname to bpm
    # def get_shape_color(R,G,B):
    #         #Reading csv file with pandas and giving names to each column
    #     index=["color","color_name","hex","R","G","B"]
    #     absolute_path = os.path.join(os.getcwd(), 'files','image_processing', 'colors.csv')
    #     csv = pd.read_csv(absolute_path, names=index, header=None)

    #     minimum = 10000
    #     for i in range(len(csv)):
    #         d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
    #         if(d<=minimum):
    #             minimum = d
    #             cname = csv.loc[i,"color_name"]
    #     return cname
    
    # colorName = get_shape_color(r,g,b)

    def round_up_to_30(number):
        return min(((number + 29) // 30) * 30, 240)
    
    bpm = round_up_to_30((b + g + r) / 3)
    if bpm < 30:
        return 30
    else:
        return bpm

def get_placement_of_note(x_axis_middlepoint, img_width):
    """
    This function finds the ratio between the middle point of a shape and the total image width.
    It takes two arguments:
    - x_axis: the x_axis middle_point of the shape in the image
    - img_width: the width of the entire image
    
    It returns a scaled value between 0 and 4 based on the ratio of x_axis to img_width in steps of 0.25
    """
    ratio = x_axis_middlepoint / img_width
    scaled_value = min(math.ceil(ratio * 16) / 4, 4.0)
    return scaled_value

def get_volume_from_size(obj_size, img_size):
    """
    This function scales the size of an object in an image relative to the size of the entire image.img_size
    It takes two arguments:
    - obj_size: the size of the object in pixels
    - img_size: the size of the entire image in pixels
    
    It returns a scaled value between 20 - 255 based on the ratio of obj_size to img_size.
    It starts at 20 otherwise the smaller objects wouldn't even make a sound.
    """
    return min((((obj_size)+(img_size*0.2))/img_size)*255, 255)

def get_pitch_from_y_axis(y_axis, img_height):
    """
    This function scales the y_axis to the image height
    It takes two arguments:
    - y_axis: the size of the object
    - img_height: the size of the entire image
    
    It returns a scaled value between 0 - 100
    """
    return (y_axis/img_height)*100

def display_list_of_shapes(list_of_shapes):
    for shape in list_of_shapes:
        print(shape.counter, 
              "shape:", shape.shape, 
              "instrument:", shape.instrument, 
              "volume:", shape.volume, 
              "bpm:", shape.bpm, 
              "pitch:", shape.pitch, 
              "note_placement:", shape.note_placement, 
              sep='\t')
    
    return list_of_shapes
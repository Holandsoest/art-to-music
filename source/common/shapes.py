"""Defines how to draw shapes and their bounding boxes."""
import location as loc
import tkinter
import math

object_names_array=["circle", "half circle", "square", "heart", "star", "triangle"]
class Annotation:
    """An annotation is what machine learning uses to determine what something is.
    the syntax of our annotation goes as follows `class_id x y width height`  
    the class_id points to what shape it is.
    the rest is a float between 0 - 1"""
    def __init__(self, class_id:int, image_size:loc.Pos, coordinates:list) -> None:
        """## Constructor
        `class_id` a int between  0 - n, wherein n is the amount of machine learning objects there are. See `object_names_array` in the machine learning training model for more info.
        
        `image_size` the x=width and y=hight of the image in pixels
        
        `coordinates` a list of positions with x and y values"""
        assert class_id >= 0

        self.class_id=str(class_id)

        # Find most up, left, right, down. Coordinates
        pos_top_left = loc.Pos(coordinates[0].x, coordinates[0].y)
        pos_bottom_right = loc.Pos(coordinates[0].x, coordinates[0].y)
        for coordinate in coordinates:
            if coordinate.x < pos_top_left.x:      pos_top_left.x = coordinate.x
            if coordinate.y < pos_top_left.y:      pos_top_left.y = coordinate.y
            if coordinate.x > pos_bottom_right.x:  pos_bottom_right.x = coordinate.x
            if coordinate.y > pos_bottom_right.y:  pos_bottom_right.y = coordinate.y
        self.box = loc.Box(x=     pos_top_left.x,
                           y=     pos_top_left.y,
                           width= pos_bottom_right.x - pos_top_left.x,
                           height=pos_bottom_right.y - pos_top_left.y)

        pos_center = loc.Pos(x= pos_top_left.x + (pos_bottom_right.x - pos_top_left.x) / 2.0,
                             y= pos_top_left.y + (pos_bottom_right.y - pos_top_left.y) / 2.0)
        shape_size = loc.Pos(x= pos_bottom_right.x - pos_top_left.x,
                             y= pos_bottom_right.y - pos_top_left.y)
        
        self.x=float(pos_center.x)/float(image_size.x)
        self.y=float(pos_center.y)/float(image_size.y)

        self.width =  shape_size.x / float(image_size.x)
        self.height = shape_size.y / float(image_size.y)
    def __str__(self) -> str:
        """`class_id x y width height`"""
        return f'{self.class_id} {self.x} {self.y} {self.width} {self.height}'
    def collides(self, other) -> bool:
        """returns bool, true whenever the other collides."""

        self_lower_pos = loc.Pos(x=self.x-self.width/2, y=self.y-self.height/2)
        self_upper_pos = loc.Pos(x=self.x+self.width/2, y=self.y+self.height/2)
        other_lower_pos = loc.Pos(x=other.x-other.width/2, y=other.y-other.height/2)
        other_upper_pos = loc.Pos(x=other.x+other.width/2, y=other.y+other.height/2)
        
        if self_upper_pos.x < other_lower_pos.x: return False # Left of other
        if self_upper_pos.y < other_lower_pos.y: return False # Above other
        if self_lower_pos.x > other_upper_pos.x: return False # Right of other
        if self_lower_pos.y > other_upper_pos.y: return False # Under other
        return True

# Functions to help draw shapes
def calculate_arm_point_(start_pos:loc.Pos, length_trace=1, rotation_rad=0.0) -> loc.Pos:
    """uses the idea of the unit circle to calculate the position from a start position, rotation and length of the arm"""
    return loc.Pos(
        x= start_pos.x + length_trace * math.cos(rotation_rad),
        y= start_pos.y + length_trace * (-math.sin(rotation_rad)),
        force_int=True)
def calculate_shape_arms_(center_pos:loc.Pos, traces= 4, length_traces=10, rotation=0) -> list:
    """Calculates multiple arms out of one point that give a outline"""
    output = []

    trace_rad_spacing = math.pi * 2 / float(traces)

    for i in range(traces):
        output.append(calculate_arm_point_(
            start_pos=      center_pos,
            length_trace=   length_traces,
            rotation_rad=   rotation + i * trace_rad_spacing
        ))

    return output
def angle_mirror_(rad_angle:float, mirror_vertical=False)->float:
    # vertical mirror
    if mirror_vertical:
        rad_angle = math.pi - rad_angle
        rad_angle %= math.pi * 2
    return rad_angle

# Shapes
class Shape:
    def get_polygon_coordinates_(self, location_offset:loc.Pos) -> list:
        """Returns a list of coordinates that can be used by `tkinter` to draw a `polygon` on a `canvas`"""

        polygon_coordinates = []
        for node in self.outline_coordinates:
            polygon_coordinates.append(  int(round(  node.x + location_offset.x,  0  ))  )
            polygon_coordinates.append(  int(round(  node.y + location_offset.y,  0  ))  )
        return polygon_coordinates
    
    def draw_shape(self, tkinter_canvas:tkinter.Canvas, outline_color:str, fill_color:str, width_outline:int, location_offset:loc.Pos) -> int:
        """Returns an `object_ID` of the shape drawn on the `tkinter_canvas`"""
        if (width_outline < 0): raise RuntimeWarning('A `width_outline` cannot be negative.')

        return tkinter_canvas.create_polygon(self.get_polygon_coordinates_(location_offset),
                                             outline=outline_color, width=width_outline,
                                             smooth=1 if isinstance(self, Heart) or isinstance(self, HalfCircle) else 0,
                                             fill=fill_color)
    
    def draw_shadow(self, tkinter_canvas:tkinter.Canvas, depth_shadow_px:int, sun_rotation_rad:float, shadows_float=False) -> list[int]|None:
        """Returns a list of `object_ID`'s of the shapes drawn on the `tkinter_canvas`, unless the `depth_shadow_px` is zero then it returns a `None`"""
        if (depth_shadow_px < 0): raise RuntimeWarning('A `depth_shadow_px` cannot be negative.')
        if (depth_shadow_px == 0): return None
        sun_rotation_rad %= 2 * math.pi

        output_ids = []

        # End location
        output_ids.append(self.draw_shape(tkinter_canvas,
                                          outline_color='gray',
                                          fill_color='gray',
                                          width_outline=1,
                                          location_offset=calculate_arm_point_(start_pos=self.center_pos,
                                                                               length_trace=depth_shadow_px,
                                                                               rotation_rad=sun_rotation_rad) - self.center_pos))
        if shadows_float: return output_ids
        if depth_shadow_px - 1 <= 0: return output_ids
        for i in range(1,depth_shadow_px):
            output_ids.append(self.draw_shape(tkinter_canvas,
                                              outline_color='gray',
                                              fill_color='gray',
                                              width_outline=1,
                                              location_offset=calculate_arm_point_(start_pos=self.center_pos,
                                                                                   length_trace=i,
                                                                                   rotation_rad=sun_rotation_rad) - self.center_pos))
        return output_ids
    
class Star(Shape):
    def __init__(self, img_size:loc.Size, center_pos:loc.Pos, size_in_pixels=10, rotation_rad=0.0, depth_percentage=50):
        rotation_rad %= math.pi * 2 / 5 # Shape repeats every 72 degrees

        self.center_pos = center_pos
        self.size_in_pixels = size_in_pixels
        self.rotation_rad=rotation_rad
        self.depth_percentage=depth_percentage

        # store the outline in a list
        self.outline_coordinates = []

        outer_points = calculate_shape_arms_(center_pos=center_pos, traces=5, length_traces=size_in_pixels / 2, rotation=rotation_rad)
        inner_points = calculate_shape_arms_(center_pos=center_pos, traces=5, length_traces=size_in_pixels / 200 * depth_percentage,
                                         rotation=rotation_rad + (math.pi / float(5)))

        self.outline_coordinates.append(outer_points[0])
        self.outline_coordinates.append(inner_points[0])
        self.outline_coordinates.append(outer_points[1])
        self.outline_coordinates.append(inner_points[1])
        self.outline_coordinates.append(outer_points[2])
        self.outline_coordinates.append(inner_points[2])
        self.outline_coordinates.append(outer_points[3])
        self.outline_coordinates.append(inner_points[3])
        self.outline_coordinates.append(outer_points[4])
        self.outline_coordinates.append(inner_points[4])

        self.annotation=Annotation(4, image_size=img_size, coordinates=self.outline_coordinates)
class Square(Shape):
    def __init__(self, img_size:loc.Size, center_pos:loc.Pos, size_in_pixels=10, rotation_rad=0.0):
        rotation_rad %= math.pi * 2 / 4 # Shape repeats every 90 degrees

        self.center_pos = center_pos
        self.size_in_pixels = size_in_pixels
        self.rotation_rad=rotation_rad

        # store the outline in a list
        self.outline_coordinates = calculate_shape_arms_(center_pos=center_pos, traces=4, length_traces=size_in_pixels / 2, rotation=rotation_rad)

        self.annotation=Annotation(2, image_size=img_size, coordinates=self.outline_coordinates)
class SymmetricTriangle(Shape):
    def __init__(self, img_size:loc.Size, center_pos:loc.Pos, size_in_pixels=10, rotation_rad=0.0):
        rotation_rad %= math.pi * 2 / 3 # Shape repeats every 60 degrees

        self.center_pos = center_pos
        self.size_in_pixels = size_in_pixels
        self.rotation_rad=rotation_rad

        # store the outline in a list
        self.outline_coordinates = calculate_shape_arms_(center_pos=center_pos, traces=3, length_traces=size_in_pixels / 2, rotation=rotation_rad)

        self.annotation=Annotation(5, image_size=img_size, coordinates=self.outline_coordinates)
class Heart(Shape):
    def __init__(self, img_size:loc.Size, center_pos:loc.Pos, size_in_pixels=10, rotation_rad=0.0, depth_percentage=50):
        rotation_rad %= math.pi * 2 # Shape repeats every 360 degrees
        depth_percentage=min(95,max(40,depth_percentage)) # Limit depth percentage to 20-80

        self.center_pos = center_pos
        self.size_in_pixels = size_in_pixels
        self.rotation_rad=rotation_rad
        self.depth_percentage=depth_percentage

        radius = size_in_pixels / 2
        pi = math.pi

        # store the outline in a list
        shape_dict = {
            "point_1":      (3/2*pi,     radius),
            "under_arch_2": (65/36*pi,   radius*0.87),
            "right_3":      (1/9*pi,     radius*1.08),
            "top_right_4":  (1/4*pi,     radius*1.25),#1.41
            "top_5":        (31/90*pi,   radius*1.15),
            "top_center_6": (4/9*pi,     radius*0.95),
            "hole_7":       (1/2*pi,     size_in_pixels*depth_percentage/100) # use the point_pos as start_pos for this line
        }
        self.outline_coordinates = []

        # get location of the right side of the heart
        arm_rotation, arm_length = shape_dict["point_1"]
        point_pos = calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad)
        self.outline_coordinates.append(point_pos)
        self.outline_coordinates.append(point_pos)

        arm_rotation, arm_length = shape_dict["under_arch_2"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))
        arm_rotation, arm_length = shape_dict["right_3"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))
        arm_rotation, arm_length = shape_dict["top_right_4"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))
        arm_rotation, arm_length = shape_dict["top_5"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))
        arm_rotation, arm_length = shape_dict["top_center_6"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))

        arm_rotation, arm_length = shape_dict["hole_7"]
        hole_pos = calculate_arm_point_(point_pos, arm_length, arm_rotation + rotation_rad)
        self.outline_coordinates.append(hole_pos)

        # get location of the left side of the heart
        self.outline_coordinates.append(hole_pos)
        
        arm_rotation, arm_length = shape_dict["top_center_6"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, angle_mirror_(arm_rotation, mirror_vertical=True) + rotation_rad))
        arm_rotation, arm_length = shape_dict["top_5"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, angle_mirror_(arm_rotation, mirror_vertical=True) + rotation_rad))
        arm_rotation, arm_length = shape_dict["top_right_4"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, angle_mirror_(arm_rotation, mirror_vertical=True) + rotation_rad))
        arm_rotation, arm_length = shape_dict["right_3"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, angle_mirror_(arm_rotation, mirror_vertical=True) + rotation_rad))
        arm_rotation, arm_length = shape_dict["under_arch_2"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, angle_mirror_(arm_rotation, mirror_vertical=True) + rotation_rad))

        self.outline_coordinates.append(point_pos)
        self.outline_coordinates.append(point_pos)

        self.annotation=Annotation(3, image_size=img_size, coordinates=self.outline_coordinates)
class HalfCircle(Shape):
    def __init__(self, img_size:loc.Size, center_pos:loc.Pos, size_in_pixels=10, rotation_rad=0.0):
        rotation_rad %= math.pi * 2 # Shape repeats every 360 degrees

        self.center_pos = center_pos
        self.size_in_pixels = size_in_pixels
        self.rotation_rad=rotation_rad

        radius = size_in_pixels / 2
        pi = math.pi

        # store the outline in a list
        shape_dict = {
            "right_top":    (1/6*pi,    radius),
            "left_top":     (5/6*pi,    radius),
            "right_center": (0,         radius*0.75),
            "left_center":  (pi,        radius*0.75),
            "left_bottom":  (5/4*pi,    radius*0.5),
            "right_bottom": (7/4*pi,    radius*0.5)
        }
        self.outline_coordinates = []
        
        arm_rotation, arm_length = shape_dict["right_top"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))
        arm_rotation, arm_length = shape_dict["left_top"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))
        arm_rotation, arm_length = shape_dict["left_center"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))
        # self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))
        arm_rotation, arm_length = shape_dict["left_bottom"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))
        arm_rotation, arm_length = shape_dict["right_bottom"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))
        arm_rotation, arm_length = shape_dict["right_center"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))
        # self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))
        arm_rotation, arm_length = shape_dict["right_top"]
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))
        self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation + rotation_rad))

        self.annotation=Annotation(1, image_size=img_size, coordinates=self.outline_coordinates)
class Circle(Shape):
    def __init__(self, img_size:loc.Size, center_pos:loc.Pos, size_in_pixels=10):

        self.center_pos = center_pos
        self.size_in_pixels = size_in_pixels

        radius = size_in_pixels / 2
        pi = math.pi

        # store the outline in a list
        shape_dict = {
            "right_top":    (1/4*pi,    math.sqrt( (radius**2) * 2)),
            "left_top":     (3/4*pi,    math.sqrt( (radius**2) * 2)),
            "left_bottom":  (5/4*pi,    math.sqrt( (radius**2) * 2)),
            "right_bottom": (7/4*pi,    math.sqrt( (radius**2) * 2))
        }
        self.outline_coordinates = []
        for dot in shape_dict:
            arm_rotation, arm_length = shape_dict[dot]
            self.outline_coordinates.append(calculate_arm_point_(center_pos, arm_length, arm_rotation))

        self.annotation=Annotation(0, image_size=img_size, coordinates=self.outline_coordinates)

    def draw_shape(self, tkinter_canvas:tkinter.Canvas, outline_color:str, fill_color:str, width_outline:int, location_offset:loc.Pos) -> int:
        """Returns an `object_ID` of the shape drawn on the `tkinter_canvas`"""
        if (width_outline < 0): raise RuntimeWarning('A `width_outline` cannot be negative.')

        return tkinter_canvas.create_oval(self.annotation.box.pos.x + location_offset.x,
                                          self.annotation.box.pos.y + location_offset.y,
                                          self.annotation.box.pos.x + self.annotation.box.size.x + location_offset.x,
                                          self.annotation.box.pos.y + self.annotation.box.size.y + location_offset.y,
                                          outline=outline_color,
                                          width=1,
                                          fill=fill_color)

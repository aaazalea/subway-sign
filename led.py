from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw
import time

options = RGBMatrixOptions()
options.rows = 16
options.cols = 32
options.chain_length = 2
options.parallel = 1
options.gpio_slowdown = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

WHITE = (180, 180, 180)
YELLOW = (252,204,10)
BLUE = (0,57,166)
ORANGE = (255, 99, 25)
RED = (238, 53, 46)
GREEN = (0, 147, 60)
LIGHT_GREEN = (108, 190, 69)

GREY = (80, 80, 80)
PINK = (200, 30, 140)
ACTUAL_RED = (255,0,0)

def make_numbers():
    nums = [Image.new("RGB", (4, 7)) for i in range(10)]
    lines = [
        [(0,1,0,5),(1,0,1,0),(1,6,1,6),(2,1,2,5)],
        [(2,0,2,6)],
        [(0,6,2,6),(0,5,1,4),(2,1,2,3),(0,1,1,0)],
        [(0,1,1,0),(2,1,2,2),(1,3,1,3),(2,4,2,5),(1,6,0,5)],
        [(2,0,2,6),(1,3,1,3),(0,0,0,3)],
        [(0,0,2,0),(0,1,0,3),(1,3,1,3),(2,4,2,5),(0,6,1,6)],
        [(1,0,2,1),(0,1,0,5),(1,6,2,5),(2,4,1,3)],
        [(0,0,0,1),(1,0,2,0),(2,1,0,6)],
        [(1,0,0,1),(0,2,1,3),(1,3,0,4),(0,5,1,6),(2,1,2,2),(2,4,2,5)],
        [(1,0,0,1),(0,2,1,3),(2,1,2,5),(1,6,0,5)]
    ]
    for i,arr in enumerate(lines):
        draw = ImageDraw.Draw(nums[i])
        for line in arr:
            draw.line(line, fill=WHITE)
    return nums
    

def make_period():
    image = Image.new("RGB", (1, 7))
    draw = ImageDraw.Draw(image)
    draw.line((0,6,0,6), fill=WHITE)
    return image

def make_letters():
    letters = [
        ('Q',YELLOW,[(0,1,0,5),(1,0,3,0),(1,6,2,6),(2,4,4,6),(4,1,4,4)]),
        ('A',BLUE, [(0,1,0,6),(1,3,3,3),(1,0,3,0),(4,1,4,6)]),
        ('B',ORANGE, [(0,0,0,6),(1,0,3,0),(1,3,3,3),(1,6,3,6),(4,1,4,2),(4,4,4,5)]),
        ('D',ORANGE, [(0,0,0,6),(1,0,3,0),(1,6,3,6),(4,1,4,5)]),
        ('C',BLUE,[(0,1,0,5),(1,0,3,0),(4,1,4,1),(4,5,4,5),(1,6,3,6)]),
        ('N',YELLOW,[(0,0,0,6),(1,1,1,2),(2,3,2,3),(3,4,3,5),(4,0,4,6)]),
        ('R',YELLOW,[(0,0,0,6),(0,0,3,0),(4,1,4,2),(0,3,3,3),(1,3,4,6)]),
        ('2',RED,[(0,1,1,0),(1,0,3,0),(4,1,4,2),(4,2,0,6),(0,6,4,6)]),
        ('3',RED,[(0,1,1,0),(1,0,3,0),(4,1,4,2),(3,3,2,3),(4,4,4,5),(3,6,1,6),(1,6,0,5)]),
        ('4',GREEN,[(1,0,1,3),(1,3,4,3),(4,0,4,6)]),
        ('5',GREEN,[(4,0,0,0),(0,0,0,3),(0,3,3,3),(4,4,4,5),(1,6,3,6),(0,5,0,5)]),
        ('G',LIGHT_GREEN,[(1,0,3,0),(4,1,4,1),(0,1,0,5),(1,6,3,6),(4,5,4,4),(3,4,3,4)]),
        ('W',YELLOW, [(0,0,0,5),(1,5,1,6),(2,2,2,5),(3,5,3,6),(4,0,4,5)]),
        ('?',ACTUAL_RED, [(2,6,2,6),(2,3,2,4),(3,2,4,1),(1,0,3,0),(0,1,0,1)]),
    ]
    color_map = dict((x,y) for (x,y,z) in letters)
    lets = dict((x,Image.new("RGB",(5,7))) for x in 'ACBDNQRG2345?W')
    for ltr, col, lines in letters:
        draw = ImageDraw.Draw(lets[ltr])
        for line in lines:
            draw.line(line, fill=col)
    return lets,color_map

def make_arrow():
    image = Image.new("RGB", (3, 7))
    draw = ImageDraw.Draw(image)
    draw.line((0,2,2,4),fill=GREY)
    draw.line((2,4,0,6),fill=GREY)
    return image

def make_express():
    image = Image.new("RGB",(11,7))
    draw = ImageDraw.Draw(image)
    lines = [(0,1,2,1),(0,2,0,5),(1,3,1,3),(1,5,2,5),(4,5,6,3),(6,5,4,3),(8,6,8,3),(8,6,10,4),(9,3,9,3)]
    for line in lines:
        draw.line(line, fill=PINK)
    return image

def make_locs():
    loc_lines = [
            ('Qns',10,[(1,1,1,1),(0,2,0,4),(2,2,2,4),(1,5,2,6),(4,3,4,6),(4,3,6,3),(6,3,6,6),(8,3,9,3),(8,4,9,5),(9,6,8,6)]),
            ('Bk',7,[(0,1,0,6),(1,1,2,2),(1,3,2,4),(2,5,1,6),(4,3,4,6),(5,5,6,4),(6,6,6,6)]),
            ('M',5, [(0,1,0,6),(0,1,2,3),(2,3,4,1),(4,1,4,6)])
           ]
    locs = {}
    for loc, size, lines in loc_lines:
        locs[loc] = Image.new("RGB",(size,7))
        draw = ImageDraw.Draw(locs[loc])
        for line in lines:
            draw.line(line, fill=WHITE)
    return locs

def make_at():
    lines = [(1,2,2,2),(3,3,3,4),(2,4,2,4),(0,3,0,5),(1,6,2,6)]
    image = Image.new("RGB",(4,7))
    draw = ImageDraw.Draw(image)
    for line in lines:
        draw.line(line, fill=GREY)
    return image

def make_m():
    lines = [(0,4,4,4),(0,5,0,6),(2,5,2,6),(4,5,4,6)]
    image = Image.new("RGB",(5,7))
    draw = ImageDraw.Draw(image)
    for line in lines:
        draw.line(line, fill=WHITE)
    return image

def make_arr():
    lines = [(0,1,0,6),(1,0,1,0),(2,1,2,6),(1,4,1,4),(4,3,4,6),(5,4,5,4),(7,3,7,6),(8,4,8,4)]
    image = Image.new("RGB", (9, 7))
    draw = ImageDraw.Draw(image)
    for line in lines:
        draw.line(line, fill=ACTUAL_RED)
    return image

def make_locations():
    colors = [YELLOW, BLUE, GREEN, ORANGE, RED, LIGHT_GREEN, ACTUAL_RED]
    locs = [
            ('Dek',[(0,1,0,6),(0,1,2,1),(3,2,3,5),(0,6,2,6),(5,3,5,5),(6,2,7,3),(7,4,6,4),(7,6,6,6),(9,3,9,6),(9,6,11,4),(11,6,11,6)]),
            ('Ful',[(0,1,0,6),(1,1,2,1),(1,3,1,3),(3,4,3,6),(3,6,5,6),(5,4,5,6),(7,1,7,6)]),
            ('Nev',[(0,1,0,6),(1,2,1,3),(2,4,2,5),(3,1,3,6),(5,3,5,5),(6,2,7,3),(7,4,6,4),(7,6,6,6),(9,3,9,5),(11,3,11,5),(10,6,10,6)]),
            ('Atl',[(0,1,0,6),(2,1,2,6),(1,1,1,1),(1,4,1,4),(4,4,6,4),(5,3,5,6),(6,6,6,6),(8,3,8,6)]),
            ('H-S',[(0,1,0,6),(1,3,1,4),(2,1,2,6),(4,4,5,4),(10,2,10,2),(9,1,8,1),(7,2,10,5),(9,6,8,6),(7,5,7,5)]),
            ('Laf',[(0,1,0,6),(0,6,2,6),(4,5,5,4),(6,5,6,6),(5,6,5,6),(8,3,8,6),(9,2,9,2),(9,4,9,4)]),
    ]
    res = {}
    for col in colors:
        for name, lines in locs:
            img = Image.new("RGB", (12, 7))
            draw = ImageDraw.Draw(img)
            for line in lines:
                draw.line(line, fill=col)
            res[(name, col)] = img
    return res


nums = make_numbers()
period = make_period()
letters, color_map = make_letters()
express_letters = make_express()
arrow = make_arrow()
locs = make_locs()
at = make_at()
m = make_m()
arr = make_arr()
one = nums[1].crop((2,0,3,7))
locations = make_locations()

def draw_row(matrix, pos=0, num=1, line='Q',express=True,direction='M',station='Dek',time=9):
    express |= (len(line) > 1 and line[1] == 'X')
    x = 0
    y = 9 * pos # change this if display gets taller
    if num >= 10:
        matrix.SetImage(nums[num // 10], x, y)
        x += 4
    matrix.SetImage(nums[num % 10], x, y)
    x += 4
    
    matrix.SetImage(period, x, y)
    x += 2

    matrix.SetImage(letters.get(line[0], letters['?']), x, y)
    x += 6
    
    if express:
        matrix.SetImage(express_letters, x, y)
        x += 11

    matrix.SetImage(arrow, x, y)
    x += 4

    direction_image = locs[direction]
    matrix.SetImage(direction_image, x, y)
    x += direction_image.width + 1

    matrix.SetImage(at, x, y)
    x += 5

    matrix.SetImage(locations[(station, color_map.get(line[0], ACTUAL_RED))], x, y)

    if time == 0:
        x = 54
        matrix.SetImage(arr, x, y)
    else:
        x = 53
        if time >= 10:
            matrix.SetImage(one, x, y)
        x += 2
        matrix.SetImage(nums[time % 10], x, y)
        x += 4
        matrix.SetImage(m, x, y)
    

def draw_ip(s):
    matrix.Clear()
    x = 0
    y = 0
    for c in s:
        im =  period
        ct = 2
        if c in '1234567890':
            ct = 4
            im = nums[int(c)]
        matrix.SetImage(im, x, y)
        x += ct
        
            



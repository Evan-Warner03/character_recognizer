#----------------------------------------------------------#
# character_finder.py

# Given an image, character_finder.py can be used
# to split this image into images of individual characters

# Created: December 09, 2020
# Evan Warner
#----------------------------------------------------------#

from PIL import Image
import time


# functions for opening the image, and splitting it into characters
# -----------------------------------------------------------------
def get_pixels(img):
    """
    get_pixels(Image) -> List
    
    Returns a list of rows of columns of pixels in a given Image
    """
    
    im = Image.open(img)
    # in case the given image is not in RGB form, convert it
    im = im.convert("RGB")
    
    #iterate through the image, and append each individual pixel to our list
    pixels = []
    for row in range(im.height):
        temp_row = []
        for col in range(im.width):
            temp_row.append(im.getpixel((col,row)))
            
        pixels.append(temp_row)
    
    return pixels



def black_and_white(pixels):
    """
    black_and_white(List) -> List
    
    Given a list of pixels, sets every pixel to be either pure white, or
    pure black
    """
    
    # iterate through each pixel in pixels
    for row in range(len(pixels)):
        for col in range(len(pixels[row])):
            
            #check if the pixel is near enough to black
            if sum(pixels[row][col]) < 465:
                #if it is, set it to pure black
                pixels[row][col] = (0,0,0)
                
            else:
                #otherwise set it to pure white
                pixels[row][col] = (255,255,255)
    
    return pixels
    
    

def increase_size(pixels):
    """
    increase_size(List) -> List
    
    Replaces each pixel in pixels with a 3x3 square of itself
    """
    
    # iterate through each row in pixels
    new_pixels = []
    for row in range(len(pixels)):
        # replace each row with its new scaled row
        new_row = increase_size_row(pixels[row])
        new_pixels.extend(new_row)
    
    return new_pixels



def increase_size_row(row):
    """
    increase_size_row(List) -> List
    
    Replaces each pixels in row of pixels with a 3x3 square of itself
    """
    
    new_row = []
    for pixel in row:
        new_row.extend([pixel]*3)
    
    return [new_row]*3    
    


def split_lines(pixels, small=False):
    """
    split_lines(List) -> List
    
    Given a list of pixels, splits the pixels into a list of lines of text
    """
    
    # get the vertical line splits
    if not small:
        line_splits = get_splits(pixels, True, False)
    else:
        line_splits = get_splits(pixels, True, False, True)
    
    # iterate through line splits, and create a list of lines
    lines = []
    for i in range(0, len(line_splits), 2):
        start = line_splits[i]
        end = line_splits[i+1]
        temp_line = []
        
        for row in range(start, end):
            temp_row = []
            for col in range(len(pixels[row])):
                temp_row.append(pixels[row][col])
            
            temp_line.append(temp_row)
        
        lines.append(temp_line)
    
    return lines
    
    

def split_chars(pixels):
    """
    split_chars(List) -> List
    
    Given a list of pixels, splits the pixels horizontally into a list of 
    individual characters
    """
    
    # get the horizontal line splits
    line_splits = get_splits(pixels, False, True, False)
    
    # iterate through line_splits, and create a list of characters
    characters = []
    for i in range(0, len(line_splits), 2):
        start = line_splits[i]
        end = line_splits[i+1]
        temp_char = []
        
        for row in range(len(pixels)):
            temp_row = []
            for col in range(start, end):
                temp_row.append(pixels[row][col])
                
            temp_char.append(temp_row)
        
        characters.append(temp_char)
    
    return characters 



def get_splits(pixels, vert=False, horz=False, small=False):
    """
    get_vert_splits(List) -> List
    
    Given a list of pixels, returns a list, where each even index is a row # 
    which is non-white, and occurs directly after a white row, and every odd 
    index is the row # which is the first occurence of a white row after the  
    row # of the index prior 
    """
    non_white = []
    
    if vert:
        # iterate through each row in pixels, to find non-white rows
        for row in range(len(pixels)):
            
            not_white = 0
            for col in range(len(pixels[row])):
                # add 1 to not_white for each non-white pixel in the row
                if pixels[row][col] != (255,255,255):
                    not_white += 1
            
            # if not_white != 0 (there are non-white pixels in the row)
            # add row to the list of non-white rows
            if not_white != 0:
                non_white.append(row)
    
    elif horz:
        # iterate through each col in pixels, to find non-white cols
        for col in range(len(pixels[0])):
            
            not_white = 0
            for row in range(len(pixels)):
                # add 1 to not_white for each non-white pixel in the col
                if pixels[row][col] != (255,255,255):
                    not_white += 1
            
            # if not_white != 0 (there are non-white pixels in the col)
            # add row to the list of non-white cols
            if not_white != 0:
                non_white.append(col)
        
    
    # create a new list (line_splits), where each even index is a row # which
    # is non-white, and occurs directly after a white row, and every odd index
    # is the row # which is the first occurence of a white row after the row # 
    # of the index prior
    line_splits = [non_white[0]]
    for i in range(1, len(non_white)):
        if non_white[i]-1 != non_white[i-1]:
            line_splits.extend([non_white[i-1]+1, non_white[i]])
            
    line_splits.append(non_white[-1]+1)
    
    if vert and not small:
        #find the average line size
        sum1 = 0
        counter1 = 0
        for i in range(0, len(line_splits), 2):
            sum1 += line_splits[i+1]-line_splits[i]-1
            counter1 += 1
        
        avg = sum1/counter1
        
        # if a line is less than half the average, add it to the line afterwards
        # since it may be the dot of a lower-case 'i' (for example)
        for i in range(0, len(line_splits), 2):
            if line_splits[i+1]-line_splits[i]-1 < avg/2:
                line_splits[i+1] = -1
        
        temp = [line_splits[0]]
        for i in range(1, len(line_splits)-1, 2):
            if line_splits[i] != -1:
                temp.append(line_splits[i])
                temp.append(line_splits[i+1])
        
        temp.append(line_splits[-1])
        line_splits = temp[:]   
    
    return line_splits 



def add_spaces(line, chars):
    """
    add_spaces(List) -> List
    
    Given a list of pixels for a line of text, determines the positions where
    there are spaces
    """
    
    splits = get_splits(line, False, True)

    # find the distances of each space
    dists = []
    for i in range(0,len(splits),2):
        if i == 0:
            dists.append(splits[i])
        else:
            dists.append(splits[i]-splits[i-1])
    
    # find the average distance
    sum_dists = 0
    for dist in dists:
        sum_dists += dist
    avg = sum_dists/len(dists)
    
    # find the splits where there likely is a space
    spaces = []
    for i in range(len(dists)):
        if dists[i]/avg > 1.25:
            spaces.append(i)
    
    # add the spaces to the chars in the line
    new_chars = []
    for i in range(len(chars)):
        if i in spaces and i != 0:
            new_chars.append(-1)         
        new_chars.append(chars[i])
               
    return new_chars
            
        
    
def strip(pixels):
    """
    strip(List) -> List
    
    Removes excess white lines at the top and bottom of a given list of pixels
    """
    
    start = -1
    end = -1
    new_pixels = []
    found = False
    
    # iterate through each row, and check if each row is non-white
    for row in range(len(pixels)):
        not_white = 0
        for col in range(len(pixels[row])):
            if pixels[row][col] != (255,255,255):
                not_white += 1
        
        # if the row is the first non-white row, set it to be the start point 
        if not found and not_white > 0:
            start = row
            found = True
    
    found = False
    # now, iterate through the rows in reverse, to find the last non-white row
    for row in range(len(pixels)-1, -1, -1):
        not_white = 0
        for col in range(len(pixels[row])):
            if pixels[row][col] != (255,255,255):
                not_white += 1
        
        # if the row is non-white, set that row to be the end point
        if not found and not_white > 0:
            end = row+1
            found = True
    
    # get the rows from start to end
    for row in range(start, end):
        new_pixels.append(pixels[row])
    
    return new_pixels    
    
    

def scale(pixels, height, width):
    """
    scale(List, Nat, Nat) -> List
    
    Given a list of pixels, adjusts it such that its dimensions are the
    specified width and height
    """
    
    # constant for future comparisons
    bw = [(0,0,0), (255,255,255)]
    
    # while the image is too small, increase its size
    while len(pixels) < height or len(pixels[0]) < width:
        pixels = increase_size(pixels)
    
    # find the dimensions of the rectangles to be compressed to
    # individual pixels
    heights = apportion(len(pixels), height)
    widths = apportion(len(pixels[0]), width)
    
    new_pixels = []
    for i in range(len(heights)-1):
        temp_row = []
        for ii in range(len(widths)-1):
            
            # collect all the pixels in the 'rectangle'
            bw_counter = [0,0]
            for row in range(heights[i], heights[i+1]):
                for col in range(widths[ii], widths[ii+1]):
                    if pixels[row][col] == (0,0,0):
                        bw_counter[0] += 1
                    else:
                        bw_counter[1] += 1
            
            # add the dominant colour in the 'rectangle' to the new row
            temp_row.append(bw[bw_counter.index(max(bw_counter))])
        
        # add the new row to the new image
        new_pixels.append(temp_row)
    
    return new_pixels



def rem_double_chars(chars):
    """
    rem_double_chars(List) -> List
    
    Given a list of chars, splits chars which are predicted to be an image of
    two chars as opposed to one
    """
    
    # find the average width of characters on the line
    sum_widths = 0
    counter = 0
    for i in range(len(chars)):
        if chars[i] != -1:
            sum_widths += len(chars[i][0])
            counter += 1
    avg = sum_widths/counter
    
    new_chars = []
    for i in range(len(chars)):
        
        # check if the given character is suspiciously wide, and is not a space
        if chars[i] != -1 and len(chars[i][0])/avg > 1.5:
            
            # if so, check the columns near the middle
            split = -1
            mid = len(chars[i][0])//2
            for col in range(mid-5, mid+5):
                path = False
                for row in range(1, len(chars[i])-1):
                    
                    # if there is a black pixel, check to see if it connected
                    if chars[i][row][col] == (0,0,0):
                        if chars[i][row][col+1] == (0,0,0) or chars[i][row+1][col+1] == (0,0,0) or chars[i][row-1][col+1] == (0,0,0):
                            path = True
                
                # if a column only has unconnected black pixels, this should be
                # the split point
                if not path:
                    split = col
            
            if split != -1:
                # if a split point has been found, separate the image into
                # two new characters
                char1 = []
                char2 = []
                for row in range(len(chars[i])):
                    char1.append(chars[i][row][:split+1])
                    char2.append(chars[i][row][split+1:])
            
                new_chars.extend([char1,char2])
            
            else:
                new_chars.append(chars[i])
        else:
            new_chars.append(chars[i])
    
    return new_chars

# -----------------------------------------------------------------



# Miscellaneous functions
# -----------------------------------------------------------------         
def apportion(num, div):
    
    # determine the two possible numbers in the list of divisors
    small = num//div
    large = (num//div)+1
    
    # add the small divisor to the list (and remove it from num), until
    # the remainder can be finished using the large divisor
    divs = [0]
    while num != 0:
        if (div-len(divs)+1)*large == num:
            divs.append(large+divs[-1])
            num -= large
        
        else:
            divs.append(small+divs[-1])
            num -= small
    
    return divs



def show_image(pixels, red=False, save=False):
    """
    show_image(List, Bool, Bool) -> None
    
    Shows the image corresponding to the given list of pixels. If red is True,
    then every white pixel in pixels is replaced with a red pixel, otherwise
    each pixel is unaltered
    """
    
    # create a new image, with the dimensions of pixels
    img = Image.new("RGB", (len(pixels[0]), (len(pixels))))
    
    # set each pixel in the new image to its corresponding pixel in pixels
    # if red is True, each white pixel in pixels is replaced with a red pixel
    for row in range(len(pixels)):
        for col in range(len(pixels[row])):
            if red and pixels[row][col] == (255,255,255):
                img.putpixel((col,row), (255,0,0))
            else:
                img.putpixel((col,row), pixels[row][col])
    
    #either save or show the image 
    if save != False:
        img.save(save)
    
    else:
        img.show()



def show_outline(coords):
    im = Image.new("RGB", (500, 500))
    
    for row in range(500):
        for col in range(500):
            if [col,row] in coords:
                im.putpixel((col,row), (0,0,0))
            else:
                im.putpixel((col,row), (255,255,255))
    
    im.show()



def save_default_chars(alphabet):
    """
    save_default_chars(Image) -> None
    
    Given an image of an alphabet, in order a-z from left to right,
    saves an image of each character to the folder this program is in
    """
    
    letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",".",","]
    
    # create a black and white version of the image, and split it into lines
    pixels = black_and_white(increase_size(get_pixels(alphabet)))
    lines = split_lines(pixels)
    
    # find each letter on each line, and add it to a list of chars
    chars = []
    for line in lines:
        line_text = split_chars(line)
        for char in line_text:
            if char != -1:
                chars.append(strip(char))
    
    # iterate through this list of chars, and save them
    for i in range(len(chars)):
        
        # create a new, blank image
        im = Image.new("RGB", (len(chars[i][0]), len(chars[i])))
        
        # set each pixel in this image to the corresponding pixel of the char
        for row in range(len(chars[i])):
            for col in range(len(chars[i][row])):
                im.putpixel((col, row), chars[i][row][col])
        
        # save this new image
        if letters[i].islower() or not letters[i].isalpha():
            im.save("char_{}.png".format(letters[i]))
        else:
            im.save("char__{}.png".format(letters[i]))

# -----------------------------------------------------------------  



# Functions for Character Recognition
# -----------------------------------------------------------------  

def library(letters=False, method="squares"):
    """
    library() -> List
    
    Generates a list of the characteristics for the given method of each 
    character with an image file in the same directory
    """
    
    if method != "squares" and method != "outline":
        print("Given method is not permitted.\nPermitted methods are: outline, squares")
        return []
    
    # create default table of characters if necessary
    if not letters:
        letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",".",","]
        
    lib = []
    
    # open the image file of every letter
    for letter in letters:
        if letter.islower() or not letter.isalpha():
            im = "char_{}.png".format(letter)
        else:
            im = "char__{}.png".format(letter)
        
        # get the attributes of the given letter
        out = []
        pixels = strip(black_and_white(increase_size(get_pixels(im))))
        
        if method == "outline":
            pixels = scale(pixels, 200, 200)
            out = outline(pixels)
        
            # find the dimensions of the 'hole' in the letter, if there is one
            hole = find_hole(out)
            
            # add the information to the library
            lib.append([letter, hole, out])
        
        else:
            lib.append([letter, get_squares(pixels)])
    
    return lib



def get_text(img, lib, method='squares'):
    """
    get_text(Str) -> Str
    
    Given the name of an image, returns the corresponding text
    """
    
    # get black and white version of the image
    str1 = ""
    pixels = get_pixels(img)
    pixels = increase_size(pixels)
    pixels = black_and_white(pixels)
    
    # split the lines of text
    lines = split_lines(pixels)
    for i in range(len(lines)):
                
        # get the spaces within the line, and recognize the characters
        chars = split_chars(lines[i])
        chars = add_spaces(lines[i], chars)
        chars = rem_double_chars(chars)
        
        # find the average size of characters in the line
        avg = 0
        counter = 0
        for char in chars:
            if char != -1:
                avg += len(char)*len(char[0])
                counter += 1
        avg = avg/counter
        
        # iterate through each character, and add it to the string
        counter = 0
        for ii in range(len(chars)):
            char = chars[ii]
            if char != -1:
                char = strip(char)
            str1 += closest_match(char, lib, avg, method)
                
        # add a new line where necessary
        if i != len(lines)-1:
            str1 += "\n"
    
    # return the string
    return str1



def closest_match(pixels, lib, avg, method="squares"):    
    """
    closest_match(List, List, Num) -> Str
    
    Given a list of pixels of a unknown character, and a library of attributes
    for known characters, outputs the known character which most resembles the
    unknown character. Permitted methods are "squares" and "outline"
    """
    
    # check if the character should be a space
    if pixels == -1:
        return " "
    
    # check if the character is too small, and should be ignored
    elif len(pixels)*len(pixels[0]) < avg/10:
        return ""
    
    # otherwise, attempt to find its closest match, using the given method
    
    if method == "outline":
        # scale the unknown character to match the library
        pixels = scale(pixels, 200, 200)
        
        # find the outline, then sample it
        pixels = outline(pixels) 
        n = 200
        for i in range(len(pixels)):
            if len(pixels[i]) < n:
                n = len(pixels[i])-1
        
        hole = find_hole(pixels)
        pixels2 = pixels[:]
        pixels2.reverse()
        
        for i in range(len(pixels)):
            pixels[i] = sample(pixels[i], n)
        
        # now sample each relevant character in the library 
        chars = []
        scores = []
        for item in lib:
            if hole == item[1]:
                chars.append(item[0])
                diff = 0
                for i in range(len(pixels)):
                    sample2 = sample(item[2][i], n)
                    diff += distance(pixels[i], sample2)
                scores.append(diff)
        
        char = chars[scores.index(min(scores))]
    
    elif method == "squares":
        
        # get the squares for the pixels
        squares = get_squares(pixels)
        
        # find its closest match using the squares of known characters
        chars = []
        scores = []
        for item in lib:
            chars.append(item[0])
            diff = 0
            for i in range(len(squares)):
                diff += (squares[i]-item[1][i])**2
            scores.append(diff)
            
        char = chars[scores.index(min(scores))]
    
    return char



def distance(c1, c2):
    """
    distance(List, List) -> Num
    
    Returns the cartesian distance between two lists of points
    """
    dist = 0
    
    for i in range(len(c1)):
        dist += (((c1[i][0]-c2[i][0])**2) + ((c1[i][1]-c2[i][1])**2))**0.5
    
    return dist



# Method 1 for recognizing characters
# -----------------------------------------------------------------  

def get_squares(pixels):
    """
    get_squares(List) -> List
    
    Given a list of pixels, returns the % of black pixels in 25 equal sized
    sections of the list
    """
    
    # scale the images, so the squares can be evenly sized
    pixels = scale(pixels, len(pixels)*5, len(pixels[0])*5)
    heights = apportion(len(pixels), 5)
    widths = apportion(len(pixels[0]), 5)
    
    # iterate through each segment, and find the % of black pixels in each
    squares = []
    for i in range(len(heights)-1):
        for ii in range(len(widths)-1):
            
            bp = 0
            counter = 0
            for row in range(heights[i], heights[i+1]):
                for col in range(widths[i], widths[i+1]):
                    if pixels[row][col] == (0,0,0):
                        bp += 1
                    counter += 1
                    
            squares.append(bp/counter) 
    
    return squares



# Method 2 for recognizing characters
# -----------------------------------------------------------------  

def outline(pixels):    
    """
    outline(List) -> List
    
    Returns a list of points which represent a list of coordinates for the
    two largest shapes (or one if there is only one sufficiently large shape)
    for a given list of pixels
    """
    
    # create a one pixel "buffer" surrounding the image
    trow = [(255,255,255)]*(len(pixels[0])+2)
    new_pixels = []
    new_pixels.append(trow)
    for row in range(len(pixels)):
        new_row = [(255,255,255)]
        new_row.extend(pixels[row])
        new_row.append((255,255,255))
        new_pixels.append(new_row)
    new_pixels.append(trow)
    pixels = new_pixels[:]
        
    out = []
    
    # iterate through every pixel, and if the pixel is black and has a white
    # pixel adjacent, it is likely to be a coordinate for the outline of the
    # list of pixels, so append it to out
    for row in range(1,len(pixels)-1):
        for col in range(1,len(pixels[row])-1):
            if pixels[row][col] == (0,0,0):
                if pixels[row][col+1] != (0,0,0) or pixels[row][col-1] != (0,0,0) or pixels[row-1][col] != (0,0,0) or pixels[row+1][col] != (0,0,0) or pixels[row-1][col-1] != (0,0,0) or pixels[row+1][col+1] != (0,0,0):
                    out.append([col,row])
    
    # find all the different shapes in out, using path
    orig = out[:]
    outlines = []
    while out != []:
        tpath = [out[0]]
        out = out[1:]
        temp = path(tpath[-1], out)
        
        while temp != None:
            tpath.append(temp)
            out.remove(temp)
            temp = path(tpath[-1], out)
            
        outlines.append(tpath)
    
    # find the two largest shapes
    two_shapes = []
    longest = [-1,-1]
    for outl in outlines:
        if len(outl) > longest[1]:
            longest = [outl, len(outl)]
    two_shapes.append(longest[0])
    outlines.remove(longest[0])
    
    if outlines != []:
        longest = [-1,-1]
        for outl in outlines:
            if len(outl) > longest[1]:
                longest = [outl, len(outl)]
        
        # if the second shape is big enough, keep it   
        if longest[1] > len(two_shapes[0])/10:
            two_shapes.append(longest[0])
    
    # return the outlines of the two largest shapes
    return two_shapes



def path(c, coords):
    """
    path(List, List) -> List or None
    
    Given a coordinate (c), and a list of coordinates (coords), returns
    a coordinate in coords if it can be reached by (c) or none otherwise
    """
    
    # directions (c) can travel to reach a coordinate
    modifs = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,2],[1,2],
              [2,2],[2,1],[2,0],[2,-1],[2,-2],[1,-2],[0,-2],[-1,-2],[-2,-2],
              [-2,-1],[-2,0],[-2,1],[-2,2],[-1,2],[0,3],[1,3],[2,3],[3,3],[3,2],
              [3,1],[3,0],[3,-1],[3,-2],[3,-3],[2,-3],[1,-3],[0,-3],[-1,-3],
              [-2,-3],[-3,-3],[-3,-2],[-3,-1],[-3,0],[-3,1],[-3,2],[-3,3]]
    
    # check if any of these paths lead to coordinates in coords
    for mod in modifs:
        if [c[0]+mod[0],c[1]+mod[1]] in coords:
            # if so, return the coordinate
            return [c[0]+mod[0],c[1]+mod[1]] 



def sample(coords, n):
    """
    sample(List, Nat) -> List
    
    Samples n points from coords, spaced evenly, and returns the
    sampled points in a list
    """
    
    # find the indeces
    ind = apportion(len(coords)-1, n)
    
    new_coords = []
    for index in ind:
        
        # ensure points are not sampled twice
        if coords[index] not in new_coords:
            new_coords.append(coords[index])
    
    return new_coords



def find_hole(out):
    """
    out(List) -> Nat
    
    Given an outline, returns the location of the hole in the character
    """
    
    # NOTES
    # 0 -> no hole
    # 1 -> hole in lower half
    # 2 -> hole in middle
    # 3 -> hole in upper half
    
    # set default to be 'no hole'
    hole = 0
    
    # find the max and min y coords
    if len(out) > 1:
        maxy = -1
        miny = -1
        for c in out[1]:
            if c[1] > maxy:
                maxy = c[1]
            elif c[1] < miny or miny == -1:
                miny = c[1]
        
        maxy2 = -1
        for c in out[0]:
            if c[1] > maxy2:
                maxy2 = c[1]      
        
        # check if the max and min are near the top, the bottom, or in the middle
        if miny > 100:
            hole = 1
        elif maxy < 100:
            hole = 3
        else:
            hole = 2 
            
    return hole



# Main function for simplified use
# ----------------------------------------------------------------- 
def user_interface():
    
    main_choice = input("Select an option:\n1. Save Default Characters\n2. Find Image Text\nSelection: ")
    while main_choice != "1" and main_choice != "2":
        main_choice = input("Invalid Selection!\n\nSelect an option:\n1. Save Default Characters\n2. Find Image Text\nSelection: ")
    
    if int(main_choice) == 1:
        save_default_chars(input("Please enter the path to the image of a library: "))
    
    else:
        des_method = input("Please enter the character recogniction method you would like to use (outline or squares): ")
        while method != "outline" and method != "squares":
            des_method = input("Please enter the character recogniction method you would like to use (outline or squares): ")
        
        text = get_text(input("Please enter the path to the image file you would like to translate into plain text: "), library(method=des_method), des_method)
        print("This is the text we found:\n{}".format(text))

user_interface()
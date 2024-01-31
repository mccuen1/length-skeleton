from PIL import Image
import cell
import math
from collections import deque

BLACK = (0, 0, 0)

class Cell:
    def __init__(self) -> None:
        self.color = BLACK
        # store the index of boundary and length to the boundary
        self.minimal_geodesics = []
        self.minimal_distance = math.inf
        self.is_boundary = False
        self.inside = True
        self.visited = False
        self.is_length_skeleton = False
        self.minimal_paths = []

    # i donnow
    def set_color(self, color):
        self.color = color

    def calc_inside(self):
        # converts to greyscale 
        r, g, b = self.color
        greyscale = int(0.33*r + 0.33*g + 0.33*b)
        # sets IF_BOUNDARY and INSIDE
        if greyscale <= 100:
            self.is_boundary = True
            self.inside = False
        ## ADD IF NOT INSIDE BUT NOT BOUNDARY


    # for debugging purposes
    def __repr__(self):
        return f"minimal geodesics: {self.minimal_geodesics} \ndistance: {self.minimal_distance} \n paths: {self.minimal_paths}"
    

# MAIN SEARCH ALGORITHM
def BFS(start_i, start_j, pixel_grid):
    start_pixel = pixel_grid[start_i][start_j]
    ## CHANGE TO DOUBLE ENDED QUEUE
    queue = deque([])
    distance_queue = deque([])
    pathway_queue = deque([])

    queue.append((start_i, start_j))
    distance_queue.append(0)
    pathway_queue.append([])
    start_pixel.visited = True
    ROOT_TWO = 1.4142

    while queue:
        i, j = queue.popleft()
        dist = distance_queue.popleft()
        pathway = pathway_queue.popleft()
        

        current_pixel = pixel_grid[i][j]
        current_pixel.visited = True

        # adds to current minimal geodesics list
        # if len(current_pixel.minimal_geodesics) >= 1:
        #     dist += current_pixel.minimal_distance

        #     if dist < start_pixel.minimal_distance:
        #         # shallow copy of a set
        #         start_pixel.minimal_geodesics = set(current_pixel.minimal_geodesics)
        #         start_pixel.minimal_distance = dist

        #     elif dist == start_pixel.minimal_distance:
        #         for index in current_pixel.minimal_geodesics:
        #             start_pixel.minimal_geodesics.add(index)

        #     continue
            
        # stop searching if you are past the minimum distance

        # PATHWAY REACHES BOUNDARY
        if current_pixel.is_boundary:
            if dist < start_pixel.minimal_distance:
                start_pixel.minimal_geodesics = [(i, j)]
                start_pixel.minimal_distance = dist
                start_pixel.minimal_paths = [pathway]
                
            elif dist == start_pixel.minimal_distance:
                start_pixel.minimal_geodesics.append((i, j))
                start_pixel.minimal_paths.append(pathway)
            continue

        adjacent = [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]
        diagonal = [(i+1, j+1), (i+1, j-1), (i-1, j+1), (i-1, j-1)]
        
        for index in adjacent:
            _i, _j = index
            if not pixel_grid[_i][_j].visited and index not in queue:
                queue.append(index)
                distance_queue.append(dist+1)
                new_path = pathway + [index]
                pathway_queue.append(new_path)

        for index in diagonal:
            _i, _j = index
            if not pixel_grid[_i][_j].visited and index not in queue:
                queue.append(index)
                distance_queue.append(dist+ROOT_TWO)
                new_path = pathway + [index]
                pathway_queue.append(new_path)

    # clears the search for the next node
    for i in range(len(pixel_grid)):
        for j in range(len(pixel_grid[0])):
            pixel_grid[i][j].visited = False


def distance(index1, index2):
    x, y = index1
    _x, _y = index2
    return math.sqrt((x - _x)**2 + (y - _y)**2)

def run_search(pixel_grid, width, height):
    for i in range(width):
        for j in range(height):
            if pixel_grid[i][j].inside:
                #print(f"At {i}, {j}")
                BFS(i, j, pixel_grid)


def two_unique_lists(main_list, other_lists):
    
    last_index = main_list[-1]
    
    for sublist in other_lists:
        mainset = set(main_list)
        subset = set(sublist)
        # 1.5 is the cutoff because it is slightly greater than ROOT TWO
        if mainset & subset == set() and distance(last_index, sublist[-1]) > 1.5:
            return True
    
    return False

def set_length_skeleton(pixel_grid, width, height):
    for i in range(width):
        for j in range(height):
            current = pixel_grid[i][j]
        
            for k in range(len(current.minimal_paths)):
                if k+1 < len(current.minimal_paths):
                    if two_unique_lists(current.minimal_paths[k], current.minimal_paths[k+1::]):
                        current.is_length_skeleton = True
                        break


    # def check_inbetween():
    # # for inbetween points
    #     neighbor_indeces = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
    #     for i in range(width):
    #         for j in range(height):
    #             if pixel_grid[i][j].inside:
    #                 for index in neighbor_indeces:
    #                     _i, _j = index
    #                     main_pixel = pixel_grid[i][j]
    #                     other_pixel = pixel_grid[i+_i][j+_j]
    #                     if not main_pixel.is_boundary and not other_pixel.is_length_skeleton:
    #                         if main_pixel.minimal_distance == other_pixel.minimal_distance:
    #                             if distance(main_pixel.minimal_geodesics[0], other_pixel.minimal_geodesics[0]) >= 2:
    #                                 main_pixel.is_length_skeleton = True

    
    # check_inbetween()


def process_image(img_name):
    # opens image -> 
    #   creates pixel map -> 
    #       gets data of image
    input_image = Image.open(rf"images//{img_name}.png").convert('RGB')
    pixel_map = input_image.load()
    width, height = input_image.size
    # initializes grid
    pixel_grid = [[Cell() for i in range(height)] for j in range(width)]
    
    # INITIALIZATION
    for i in range(width):
        for j in range(height):
            r, g, b = input_image.getpixel((i, j))
            pixel_grid[i][j].set_color((r, g, b))
            pixel_grid[i][j].calc_inside()
    
    run_search(pixel_grid, width, height)
    # for i in range(20):
    #     BFS(4, i, pixel_grid)
    set_length_skeleton(pixel_grid, width, height)

    # SET THE FINAL COLORS
    for i in range(width):
        for j in range(height):
            if pixel_grid[i][j].is_length_skeleton:
                pixel_map[i, j] = (255, 0, 0)
            else:
                pixel_map[i, j] = pixel_grid[i][j].color

    input_image.save("target//length_skeleton", format="png")
    input_image.show()

if __name__ == "__main__":
    process_image("debug_ellipse")
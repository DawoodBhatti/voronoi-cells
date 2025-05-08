from math import ceil, sqrt
from numpy import zeros, empty

# calculate the delauney triangulation of a dataset given the voronoi cells
# as this 'should' be faster than recalculating the delauney set from scratch

class quadrant:
    def __init__(self, length=0, midpoint=None):
        if length > 0:
            self.length = length
        else:
            self.length = 0

        if midpoint is None: 
            self.midpoint = (0,0)
        else:
            self.midpoint = midpoint
            
        self.neighbours = []
        self.contained_points = []


#TODO: might want to reconsider objects for each point? 
# instead implement some container within the quadrant class?
class point:
    def __init__(self):
        non_boundary_edges = 0 
        neighbours = []


# divide grid into quandrants, each with some midpoint, to fill some bounding rectangle or square
def generate_quadrants(voronoi_data):
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    quad_length = 0
    quadrants = []    
    
    # find min and max x and y to determine bounding rectangle and use the shortest length for quadrant
    for cells in voronoi_data:
        for (x,y) in cells:
            
            if x < min_x:
                min_x = x
            elif x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            elif y > max_y:
                max_y = y
    
    # use shortest side / sqrt of number of points to calculate length of quadrant squares (might need scaling)
    scaling = 2
    quad_length = min([(max_x - min_x), (max_y - min_y)]) / round(sqrt(len(voronoi_data)))
    quad_length = quad_length * scaling
    num_rows = ceil((max_x - min_x)/quad_length) 
    num_cols = ceil((max_y - min_y)/quad_length)
    
    # offsets to match to our bounding rect/square as well as centering for overlaps
    x_offset = min_x
    x_offset -= ((quad_length * num_rows) - (max_x - min_x)) / 2
    y_offset = min_y
    #(max_y - min_y) / 2
    y_offset -= ((quad_length * num_cols) - (max_y - min_y)) / 2
    
    # initialise and create quadrants 
    quadrants = empty((num_rows, num_cols), quadrant)
    for r in range(num_rows):
        for c in range(num_cols):
            q = quadrant(quad_length, 
                         ((r * quad_length) + quad_length/2 + x_offset  ,
                          (c * quad_length) + quad_length/2 + y_offset )
                          )
    
            quadrants[r][c] = q
            
            # find all possible neighbouring quadrants, including diagonally adjacent
            for i in range(r-1, r+2, 1):
                for j in range(c-1, c+2, 1):
                    # store valid neighbour rows and columns 
                    if i >= 0 and i <= num_rows and j >= 0 and j <= num_cols:
                        # excluding this quadrant
                        if i == r and j == c:
                            pass
                        else:
                            q.neighbours.append((i,j))
    
    return quadrants
    
    
# loop over each point:
    # loop over each quadrant
        # if the distance from the point to the quadrant midpoint is less than length of quadrant
        # TODO: there might be an even quicker way to calculate this with some rounded division? i.e. divide the x and y coordinates and pull out the integer to find the cube bin it belongs in
            #  add point to that quadrant's list
    
            # calculate the number of neighbours of point i.e.  number of non boundary edges:
                # the corner points can be spotted easily as can edge pieces


# loop over each quadrant
    # loop over each point inside quadrant
            # loop over each edge (i.e. sets of vertices)
                # while number of neighbours != number of non-boundary edges:
                    # loop over each quadrant starting with closest to point 
                    # (quadrants could be retrieved with a generator?)
                        # loop over each point in that quandrant
                            # loop over each edge in point:
                                # if match then add to neighbours array and remaining matches -= 1
                                    # also add the reverse match to the neighbours array of other point 

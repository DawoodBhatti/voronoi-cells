from math import ceil, sqrt
from numpy import zeros, empty
from collections import OrderedDict


# calculate the delauney triangulation of a dataset given the voronoi cells
# as this conversion should(?) be faster than recalculating the delauney set from scratch
# will only work if the bounding shape is a quadrilateral
    
# divide grid into square quandrants, each with some midpoint, to fill some bounding rectangle or square
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
    
    # offsets to match to bottom left of bounding rect/square as well as centering for overlaps
    x_offset = min_x
    x_offset -= ((quad_length * num_rows) - (max_x - min_x)) / 2
    y_offset = min_y
    y_offset -= ((quad_length * num_cols) - (max_y - min_y)) / 2
    
    # initialise and create quadrants 
    quadrants = empty((num_rows, num_cols), quadrant)
    for r in range(num_rows):
        for c in range(num_cols):
            q = quadrant(quad_length, 
                         ((r * quad_length) + quad_length/2 + x_offset  ,
                          (c * quad_length) + quad_length/2 + y_offset ),
                         position=(r,c)
                          )
    
            quadrants[r][c] = q
            
            # find all possible neighbouring quadrants, including diagonally adjacent
            for i in range(r-1, r+2, 1):
                for j in range(c-1, c+2, 1):
                    # store valid neighbour rows and columns 
                    if i >= 0 and i <= num_rows-1 and j >= 0 and j <= num_cols-1:
                        # excluding this quadrant
                        if i == r and j == c:
                            pass
                        else:
                            q.neighbours.append((i,j))
    
    return quadrants


class quadrant:
    def __init__(self, length=0, midpoint=None, position=None):
        if length > 0:
            self.length = length
        else:
            self.length = 0

        if midpoint is None: 
            self.midpoint = (0,0)
        else:
            self.midpoint = midpoint
        
        #the (i,j) position of this quadrant within the grid where (0,0) starts at bottom left
        self.position = position
        
        #store neighbouring quadrants as list of tuples
        self.neighbours = []
        
        #capture voronoi cells that fall in midpoint
        self.contained_cells = []


class cell_conversion:
    """ convert from voronoi set to delauney set.
    
        each voronoi cell stored in a list represented by a cell number (0,1,2,3,4... etc)
        with associated properties (midpoints, edges, neighbours, etc) also stored in lists
        
        access properties of nth voronoi cell using cell number and the relevant list
        
        class auto calculates these properties as well as delauney points on init
        
        use return_delauney() to return a list of plottable triangles 
        
        """
    def __init__(self, voronoi_cells, quadrants, seed_points):
        self.seed_points = seed_points
        self.cell_number = [n for n in range(len(voronoi_cells))]
        self.cells = voronoi_cells
        self.cell_neighbours = [[] for n in range(len(voronoi_cells))]
        self.cell_unmatched_edges = []
        self.quadrants = quadrants
        
        #calculate delauney triangles on class initialisation
        self.calculate_properties()
        self.calculate_delauney()
        print("bing ching")
    
    
    # return seed point co-ords of nth voronoi cell (x,y) 
    def get_seed_point(self, n):
        return self.seed_points[n]

    
    # determine and store properties of voronoi cells as needed for delauney conversion:
    #   - the number of non boundary edges of the cell
    #   - the quadrant which voronoi cell belongs to
    def calculate_properties(self):
        #boundaries (assumed quadrilateral) are found through min and max x and y coords of cell vertices
        flattened = [coords for cells in self.cells for coords in cells] # Convert to standard Python list
        x_coords = [coords[0] for coords in flattened]
        y_coords = [coords[1] for coords in flattened]
        x_coords.sort()
        y_coords.sort()
        
        x_max = x_coords[-1]
        x_min = x_coords[0]
        y_max = y_coords[-1]
        y_min = y_coords[0]
        
        #loop through cells
        for i in self.cell_number:
            self.calculate_non_boundary_edges(i, x_max, x_min, y_max, y_min)
            self.calculate_voronoi_quadrant(i, self.quadrants)
            
    
    # determine how many edges cell, i, shares with other cells, not including the bounding quadrilateral (defined by x_max, x_min, y_max, y_min)
    def calculate_non_boundary_edges(self, i, x_max, x_min, y_max, y_min):
        edge_number = len(self.cells[i])
            
        #loop through each edge, i.e. creating co-ordinate pairs and join last point with the first
        boundary_edges = 0
        for j in range(len(self.cells[i])):
                        
            vertex1=self.cells[i][j]
            if j<len(self.cells[i])-1:
                vertex2 = self.cells[i][j+1]
            elif j ==len(self.cells[i])-1:
                vertex2 = self.cells[i][0]
                                
            #given a pair of vertices (x1,y1) and (x2,y2) we determine if they are edge pieces
            #by taking an average and testing if one or both of these x,y co-ordinates is the same as any of our x/y max/min points 
            
            avg_x = (vertex1[0] + vertex2[0]) / 2
            avg_y = (vertex1[1] + vertex2[1]) / 2
            
            #if we find a partial match we have at least one boundary edge
            if avg_x == x_max or avg_x == x_min or avg_y == y_max or avg_y == y_min:
                boundary_edges = 1
                
            #if we find a corner we therefore 2 boundary edges
            if ((vertex1[0] == x_max and vertex1[1] == y_max) or 
                (vertex1[0] == x_max and vertex1[1] == y_min) or
                (vertex1[0] == x_min and vertex1[1] == y_max) or
                (vertex1[0] == x_min and vertex1[1] == y_min)):
                boundary_edges = 2
                break
            
        #print("cell: ", i, " has this many unmatched edges: ", edge_number - boundary_edges)
        
        non_boundary_edges = (edge_number - boundary_edges)
        self.cell_unmatched_edges.append(non_boundary_edges)
        

    # given a cell's seed point calculate which quadrant (u,v) it falls in
    # and append voronoi cell number to that quadrant's list of contained points
    def calculate_voronoi_quadrant(self, i, quadrants):
        quadrant_length = quadrants[0][0].length
        
        x=self.get_seed_point(i)[0] 
        y=self.get_seed_point(i)[1] 
        u = 0
        v = 0
        
        quadrant_min_x = quadrants[0][0].midpoint[0] + quadrants[0][0].length/2
        quadrant_max_x = quadrants[-1][-1].midpoint[0] - quadrants[0][0].length/2
        quadrant_min_y = quadrants[0][0].midpoint[1] + quadrants[0][0].length/2
        quadrant_max_y = quadrants[-1][-1].midpoint[1] - quadrants[0][0].length/2


        #to avoid partial quadrant offset problem we manually determine first and last buckets
        if x < quadrant_min_x:
            u = 0
        elif x > quadrant_max_x:
            u = -1
        #and remainder divide can be used to determine intermediary quadrants
        else:
            u = 1 + int((x - quadrant_min_x) // quadrant_length)             

        #to avoid partial quadrant  problem we manually determine first and last buckets
        if y < quadrant_min_y:
            v = 0
        elif y > quadrant_max_y:
            v = -1
        #and remainder divide can be used to determine intermediary quadrants
        else:
            v = 1 + int((y - quadrant_min_y) // quadrant_length) 
        
        quadrants[u][v].contained_cells.append(i)
        
    
    # map the set of voronoi cells to an equivalent set of delauney triangles by finding and connecting the seed points of neighbouring voronoi cells
    def calculate_delauney(self):

        # loop over all voronoi cells
        for cols in self.quadrants:    
            for q in cols:
                for i in q.contained_cells:
                    
                    #define edges of voronoi cell as a pair of vertices
                    #to match edges with neighbouring cells
                    for j in range(0,len(self.cells[i])):
                        vertex1=self.cells[i][j]
                        if j<len(self.cells[i])-1:
                            vertex2 = self.cells[i][j+1]
                        elif j == len(self.cells[i])-1:
                            vertex2 = self.cells[i][0]

                        #loop over the neighbouring quadrants (including quadrant which contains cell "i")
                        loop_quadrants = [q.position]+q.neighbours
                        
                        for (x,y) in loop_quadrants:
                            quadrant = self.quadrants[x][y]
                            
                            if self.cell_unmatched_edges[i] == 0:
                                break                              
                            
                            for c in quadrant.contained_cells:
                                #avoid comparing voronoi cell to itself
                                if i == c:
                                    pass
                                #avoid comparing voronoi cell to existing neighbours
                                elif i in (self.cell_neighbours[c]):
                                    pass
                                else:
                                    #scan neighbour's vertices to look for a match
                                    for s in range(0,len(self.cells[c])):
                                        nvertex1=self.cells[c][s]
                                        if s<len(self.cells[c])-1:
                                            nvertex2 = self.cells[c][s+1]
                                        elif s == len(self.cells[c])-1:
                                            nvertex2 = self.cells[c][0]

                                        #on match update info for both cells i and c
                                        if ((vertex1 == nvertex1 and vertex2 == nvertex2) or
                                            (vertex1 == nvertex2 and vertex2 == nvertex1)):

                                            #update class info for both matches
                                            self.cell_neighbours[i].append(c)
                                            self.cell_neighbours[c].append(i)
                                            self.cell_unmatched_edges[i]-=1
                                            self.cell_unmatched_edges[c]-=1
                                            
                                            #nothing more to be found between these two 
                                            break
                                        else:
                                            pass
                
                
    #converts list of cell neighbours into plottable co-ordinates representing
    #triangular seedpoint joins between neighbouring voronoi cells
    def return_delauney_points(self):
        neighbours = self.cell_neighbours.copy()
        delauney_set = []
        seen_triangles = OrderedDict() # maintains insertion order
    
        # find sets of 3 neighbouring cells
        for i in range(len(neighbours)):
            matches = []
            cell_neighbours = neighbours[i]
    
            for j in cell_neighbours:
                if i != j:
                    for k in neighbours[j]:
                        if i != k:
                            for l in neighbours[k]:
                                if i == l:
                                    triangle = tuple(sorted((i, j, k)))
                                    if triangle not in seen_triangles:
                                        seen_triangles[triangle] = True
                                        matches.append(triangle)
                    
            delauney_set.extend(matches) # preserve loop order
    
        # replace the numbers in delauney_set with the seedpoints of these cells
        for i, elements in enumerate(delauney_set):
            v1, v2, v3 = elements
            delauney_set[i] = [self.seed_points[v1], self.seed_points[v2], self.seed_points[v3]]
    
        return delauney_set
    


def run_delauney(voronoi_data, seed_points):
    
    quadrants = generate_quadrants(voronoi_data)
    
    #calculate voronoi cell properties (their quadrant and number of non-boundary cell edges)
    conversion = cell_conversion(voronoi_data, quadrants, seed_points)
    
    #calculate delauney triangles
    delauney_triangles = conversion.return_delauney_points()
    
    #i think the quadrants generate fine
    
    #i think the sorting of points into quadrants is wrong?
    
    return quadrants, delauney_triangles




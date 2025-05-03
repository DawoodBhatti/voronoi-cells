
#steps for voronoi cells

#create a boundary box around the co-ordinates finding the min and max x and y vals
#add some width padding to boundary box

#for P in points :
        
    #set cell = to boundary box
    # for Q in points, except Q == P: 
        
        # create perpendicular bisector between Q and P
        # break cell into line segments and check for intersections between eeach line segment and bisector
        # if we find two intersections then create a new cell:
            #store the first and second intersections and the vertices of the cell after those respective points
            # if P is not in the new cell, then create the cell by reversing the order:
                # etc etc
            # cell = new cell
           
           
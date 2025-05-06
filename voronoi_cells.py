from distributions import PointGenerator
from voronoi_algorithm import VoronoiGenerator

def generate_voronoi_cells(x_range, y_range, num_points, offset_x=0, offset_y=0, distribution_method="halton", bounding_shape="rectangle", custom_shape=None):
    """
    Generate Voronoi cells using a specified point distribution method and bounding shape.

    Parameters:
        x_range (int): Width of the area to spawn points in.
        y_range (int): Height of the area to spawn points in.
        num_points (int): Number of points to generate for Voronoi cells.
        offset_x (int, optional): Adjust output positions horizontally. Default is 0.
        offset_y (int, optional): Adjust output positions vertically. Default is 0.
        distribution_method (str, optional): Method to generate seed points.
            Options: "halton", "fibonacci", "poisson", "random". Default is "halton".
        bounding_shape (str, optional): Type of bounding shape.
            Options: "rectangle", "circle", "triangle", "custom". Default is "rectangle".
        custom_shape (list, optional): List of (x, y) tuples for a custom bounding shape.
    
    Returns:
        tuple: (voronoi_cells, seed_points) where:
            voronoi_cells is a list of Voronoi cell vertex sets.
            seed_points is the list of seed points used for generation.
    """

    # Step 1: Instantiate the PointGenerator with specified parameters
    point_generator = PointGenerator(x_range, y_range, num_points)

    # Step 2: Choose a distribution method
    distributions = {
        "halton": point_generator.halton_samples,
        "fibonacci": point_generator.fibonacci_spiral,
        "poisson": point_generator.poisson_disk_samples,
        "random": point_generator.random_distribution
    }
    
    seed_points = distributions.get(distribution_method, point_generator.halton_samples)()

    # Step 3: Instantiate VoronoiGenerator with selected bounding shape
    voronoi = VoronoiGenerator(seed_points, bounding_shape=bounding_shape, custom_shape=custom_shape)

    # Step 4: Apply an optional offset
    offset_cells = voronoi.apply_offset(dx=offset_x, dy=offset_y)

    # Step 5: Convert dictionary format to list of vertices
    formatted_cells = voronoi.dictionary_to_list(offset_cells)

    return formatted_cells, seed_points
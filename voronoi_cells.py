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

    # Instantiate the PointGenerator with specified parameters
    point_generator = PointGenerator(x_range, y_range, num_points, offset_x, offset_y)

    # Choose a distribution method
    distributions = {
        "halton": point_generator.halton_samples,
        "fibonacci": point_generator.fibonacci_spiral,
        "fibonacci_segments": point_generator.fibonacci_spiral_segments,
        "poisson": point_generator.poisson_disk_samples,
        "random": point_generator.random_distribution
    }
    
    seed_points = distributions.get(distribution_method, distributions[distribution_method])()

    # Instantiate VoronoiGenerator with selected bounding shape
    voronoi = VoronoiGenerator(seed_points, bounding_shape=bounding_shape, custom_shape=custom_shape)

    # Convert dictionary format to list of vertices
    formatted_cells = voronoi.dictionary_to_list(voronoi.voronoi_cells()) 

    return formatted_cells, seed_points
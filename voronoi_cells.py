import math
import random


def compute_intersection(p1, p2, f):
    """Compute the intersection between a segment (p1→p2) and the line f(x, y) = 0."""
    f1, f2 = f(p1[0], p1[1]), f(p2[0], p2[1])
    if f1 == f2:
        return p2
    t = f1 / (f1 - f2)
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


def clip_polygon(polygon, f):
    """Clip a polygon by a half-plane using Sutherland-Hodgman algorithm."""
    if not polygon:
        return []
    clipped = []
    n = len(polygon)
    for i in range(n):
        curr, next_pt = polygon[i], polygon[(i + 1) % n]
        inside_curr, inside_next = f(curr[0], curr[1]) >= 0, f(next_pt[0], next_pt[1]) >= 0

        if inside_curr and inside_next:
            clipped.append(next_pt)
        elif inside_curr and not inside_next:
            clipped.append(compute_intersection(curr, next_pt, f))
        elif not inside_curr and inside_next:
            inter = compute_intersection(curr, next_pt, f)
            clipped.append(inter)
            clipped.append(next_pt)

    # Ensure shape is closed before returning
    if clipped and clipped[0] != clipped[-1]:
        clipped.append(clipped[0])

    return clipped


def compute_voronoi_cell(p, points, bounding_polygon):
    """Compute the Voronoi cell for point p using perpendicular bisectors."""
    cell = bounding_polygon[:]
    for q in points:
        if p == q:
            continue
        mx, my = (p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0
        normal = (p[0] - q[0], p[1] - q[1])
        def half_plane(x, y, mx=mx, my=my, normal=normal):
            return (x - mx) * normal[0] + (y - my) * normal[1]
        cell = clip_polygon(cell, half_plane)
    return cell


def voronoi_cells(points, padding=50):
    """Compute Voronoi cells and return dictionary."""
    min_x, max_x = min(p[0] for p in points) - padding, max(p[0] for p in points) + padding
    min_y, max_y = min(p[1] for p in points) - padding, max(p[1] for p in points) + padding
    bounding_polygon = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]
    
    cells = {p: compute_voronoi_cell(p, points, bounding_polygon) for p in points}
    return cells


def apply_offset(voronoi_cells, dx=0, dy=0):
    """Apply an (x, y) offset to all Voronoi cells."""
    return { (p[0] + dx, p[1] + dy): [(v[0] + dx, v[1] + dy) for v in vertices] for p, vertices in voronoi_cells.items() }


def remove_duplicate_vertices(cell):
    """Remove duplicate or near-identical vertices."""
    cleaned_cell = []
    for v in cell:
        rounded_v = (round(v[0], 2), round(v[1], 2))
        if rounded_v not in cleaned_cell:
            cleaned_cell.append(rounded_v)
    return cleaned_cell


def dictionary_to_list(cells_dict):
    """Convert dictionary into list-of-lists format while ensuring vertices are tuples."""
    result = []
    
    for p, vertices in cells_dict.items():
        cleaned_vertices = remove_duplicate_vertices(vertices)  # Ensure duplicate removal
        result.append([tuple(vertex) for vertex in cleaned_vertices])  # Convert vertices to tuples
    
    return result


def generate_voronoi_cells(x_range=500, y_range=500, num_points=100, offset_x=0, offset_y=0):
    """
    Generate Voronoi cells within a defined range, applying optional offsets.
    
    Parameters:
    - `x_range` : Width of the area to spawn points in.
    - `y_range` : Height of the area to spawn points in.
    - `num_points` : Number of points to generate for Voronoi cells.
    - `offset_x`, `offset_y` (optional) : Adjust output positions.

    Returns:
    - A tuple containing:
      1. A list of Voronoi cells, structured as [[(vertex1), (vertex2), ...], ...]
      2. A list of original seed points used for Voronoi generation
    """

    # Generate random points within the specified range
    sample_points = [(random.randint(0, x_range), random.randint(0, y_range)) for _ in range(num_points)]

    # Compute Voronoi Cells with Padding
    cells = voronoi_cells(sample_points, padding=50)

    # Apply Offset (if specified)
    adjusted_cells = apply_offset(cells, dx=offset_x, dy=offset_y)

    # Convert to List Format with Fixes
    voronoi_cells_list = dictionary_to_list(adjusted_cells)

    return voronoi_cells_list, sample_points


def get_seed_points(x_range=500, y_range=500, num_points=100):
    """
    Generate only the seed points for Voronoi cells.

    Parameters:
    - `x_range` : Width of the area to spawn points in.
    - `y_range` : Height of the area to spawn points in.
    - `num_points` : Number of points to generate.

    Returns:
    - A list of seed points [(x1, y1), (x2, y2), ...]
    """
    return [(random.randint(0, x_range), random.randint(0, y_range)) for _ in range(num_points)]


# --- Example Usage ---
if __name__ == "__main__":
    voronoi_data, seed_points = generate_voronoi_cells(x_range=1000, y_range=1000, num_points=50, offset_x=-500, offset_y=-300)
    
    print("Seed Points:")
    print(seed_points[:5])  # Print first few seed points
    
    print("\nVoronoi Cells:")
    for cell in voronoi_data[:5]:
        print(cell)

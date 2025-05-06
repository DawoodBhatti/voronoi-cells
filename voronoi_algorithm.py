import numpy as np

class VoronoiGenerator:
    def __init__(self, points, padding=50, bounding_shape="rectangle", custom_shape=None):
        """
        Initialize VoronoiGenerator.

        Parameters:
        - points: List of seed points.
        - padding: Extra space around bounding box.
        - bounding_shape: "rectangle", "circle", "triangle", or "custom".
        - custom_shape: List of (x, y) tuples defining a custom bounding region.
        """
        self.points = points
        self.padding = padding
        self.bounding_shape = bounding_shape.lower()  # Normalize input
        self.custom_shape = custom_shape  # Stores user-defined polygon


    def compute_intersection(self, p1, p2, f):
        """Compute intersection with a clipping boundary."""
        f1, f2 = f(p1[0], p1[1]), f(p2[0], p2[1])
        if f1 == f2:
            return p2
        t = f1 / (f1 - f2)
        return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


    def clip_polygon(self, polygon, f):
        """Clip a polygon using a half-plane."""
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
                clipped.append(self.compute_intersection(curr, next_pt, f))
            elif not inside_curr and inside_next:
                inter = self.compute_intersection(curr, next_pt, f)
                clipped.append(inter)
                clipped.append(next_pt)

        return clipped


    def compute_voronoi_cell(self, p, bounding_region):
        """Compute the Voronoi cell for a given point."""
        cell = bounding_region[:]
        for q in self.points:
            if p == q:
                continue
            mx, my = (p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0
            normal = (p[0] - q[0], p[1] - q[1])
            def half_plane(x, y, mx=mx, my=my, normal=normal):
                return (x - mx) * normal[0] + (y - my) * normal[1]
            cell = self.clip_polygon(cell, half_plane)
        return cell


    def voronoi_cells(self):
        """Compute Voronoi cells based on bounding shape."""
        
        if self.bounding_shape == "rectangle":
            min_x, max_x = min(p[0] for p in self.points) - self.padding, max(p[0] for p in self.points) + self.padding
            min_y, max_y = min(p[1] for p in self.points) - self.padding, max(p[1] for p in self.points) + self.padding
            bounding_region = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]
        
        elif self.bounding_shape == "circle":
            center_x = sum(p[0] for p in self.points) / len(self.points)
            center_y = sum(p[1] for p in self.points) / len(self.points)
            radius = max(self.padding, max(np.linalg.norm(np.array(p) - np.array((center_x, center_y))) for p in self.points))

            num_sides = 32  # Approximate circle as a polygon
            bounding_region = [
                (center_x + radius * np.cos(2 * np.pi * i / num_sides),
                 center_y + radius * np.sin(2 * np.pi * i / num_sides))
                for i in range(num_sides)
            ]

        elif self.bounding_shape == "triangle":
            min_x, max_x = min(p[0] for p in self.points), max(p[0] for p in self.points)
            min_y, max_y = min(p[1] for p in self.points), max(p[1] for p in self.points)

            bounding_region = [
                ((min_x + max_x) / 2, min_y - self.padding),  # Top vertex
                (min_x - self.padding, max_y + self.padding),  # Left vertex
                (max_x + self.padding, max_y + self.padding)   # Right vertex
            ]

        elif self.bounding_shape == "custom":
            if not self.custom_shape or len(self.custom_shape) < 3:
                raise ValueError("Custom shape must be a list of at least 3 (x, y) points.")
            bounding_region = self.custom_shape  # Use user-defined polygon

        else:
            raise ValueError(f"Unsupported bounding shape: {self.bounding_shape}")

        # Compute Voronoi cells
        return {p: self.compute_voronoi_cell(p, bounding_region) for p in self.points}


    def remove_duplicate_vertices(self, cell):
        """Remove duplicate or near-identical vertices."""
        cleaned_cell = []
        for v in cell:
            rounded_v = (round(v[0], 2), round(v[1], 2))
            if rounded_v not in cleaned_cell:
                cleaned_cell.append(rounded_v)
        return cleaned_cell


    def dictionary_to_list(self, cells_dict):
        """Convert dictionary format into a list of vertex sets."""
        return [
            [tuple(vertex) for vertex in self.remove_duplicate_vertices(vertices)]
            for vertices in cells_dict.values()
        ]

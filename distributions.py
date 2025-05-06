import numpy as np
import random
import math

class PointGenerator:
    def __init__(self, x_range, y_range, num_points):
        self.x_range = x_range
        self.y_range = y_range
        self.num_points = num_points


    def fibonacci_spiral(self):
        """Generate Fibonacci spiral points."""
        phi = (1 + np.sqrt(5)) / 2  # Golden Ratio
        max_radius = min(self.x_range / 2, self.y_range / 2)

        sample_points = [
            (
                max_radius * np.sqrt(i / self.num_points) * np.cos(2 * np.pi * i / phi),
                max_radius * np.sqrt(i / self.num_points) * np.sin(2 * np.pi * i / phi)
            )
            for i in range(self.num_points)
        ]

        return sample_points


    def halton_sequence(self, index, base):
        """Generate a Halton sequence value."""
        result = 0
        f = 1.0 / base
        while index > 0:
            result += f * (index % base)
            index //= base
            f /= base
        return result


    def halton_samples(self):
        """Generate Halton sequence points."""
        return [(self.halton_sequence(i+1, 2) * self.x_range, 
                 self.halton_sequence(i+1, 3) * self.y_range) for i in range(self.num_points)]


    def poisson_disk_samples(self, min_dist=20):
        """Generate Poisson-disk distributed points."""
        points = []
        while len(points) < self.num_points:
            candidate = (random.uniform(0, self.x_range), random.uniform(0, self.y_range))
            if all(math.dist(candidate, p) >= min_dist for p in points):
                points.append(candidate)
        return points
    
    
    def random_distribution(self):
        """Generate completely random points within the given range."""
        return [(random.uniform(0, self.x_range), random.uniform(0, self.y_range)) for _ in range(self.num_points)]
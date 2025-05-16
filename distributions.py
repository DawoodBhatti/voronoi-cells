import numpy as np
import random
import math

class PointGenerator:
    def __init__(self, x_range, y_range, num_points, offset_x=0, offset_y=0):
        """Initialize point generator with optional offsets."""
        self.x_range = x_range
        self.y_range = y_range
        self.num_points = num_points
        self.offset_x = offset_x
        self.offset_y = offset_y


    def apply_offset(self, points):
        """Applies offset to all generated points."""
        return [(x + self.offset_x, y + self.offset_y) for x, y in points]


    def fibonacci_spiral(self):
        """Generate Fibonacci spiral points."""
        
        #fibonacci is centered without any offsets
        self.offset_x = 0
        self.offset_y = 0
        
        phi = (1 + np.sqrt(5)) / 2  # Golden Ratio
        max_radius = min(self.x_range / 2, self.y_range / 2)

        sample_points = [
            (
                max_radius * np.sqrt(i / self.num_points) * np.cos(2 * np.pi * i / phi),
                max_radius * np.sqrt(i / self.num_points) * np.sin(2 * np.pi * i / phi)
            )
            for i in range(self.num_points)
        ]

        return self.apply_offset(sample_points)  # Apply offset here


    def fibonacci_spiral_segments(self, n=33):
        """Return every nth point from the Fibonacci spiral sequence"""
        points = self.fibonacci_spiral()
        return [ points[i] for i in range(0,len(points)) if i%n == 0 ]
        
        
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
        sample_points = [(self.halton_sequence(i+1, 2) * self.x_range, 
                          self.halton_sequence(i+1, 3) * self.y_range) for i in range(self.num_points)]
        return self.apply_offset(sample_points)  # Apply offset


    def poisson_disk_samples(self, min_dist=20):
        """Generate Poisson-disk distributed points."""
        points = []
        while len(points) < self.num_points:
            candidate = (random.uniform(0, self.x_range), random.uniform(0, self.y_range))
            if all(math.dist(candidate, p) >= min_dist for p in points):
                points.append(candidate)
        
        return self.apply_offset(points)  # Apply offset


    def random_distribution(self):
        """Generate completely random points."""
        sample_points = [(random.uniform(0, self.x_range), random.uniform(0, self.y_range)) for _ in range(self.num_points)]
        return self.apply_offset(sample_points)  # Apply offset

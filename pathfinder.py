# pathfinder.py

import math
from itertools import permutations


class Pathfinder:
    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        #Calculates distance using the gps data
        earth_radius = 6371000  # meters

        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1_rad)
            * math.cos(lat2_rad)
            * math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return earth_radius * c

    def calculate_path_distance(self, start_position, path):
        """
        Calculate the total distance of one complete route.
        """
        total_distance = 0.0
        current_lat, current_lon = start_position

        for tree_lat, tree_lon in path:
            total_distance += self.haversine_distance(current_lat,current_lon,tree_lat,tree_lon)
            current_lat, current_lon = tree_lat, tree_lon

        return total_distance

    def shortest_path(self, start_position, tree_positions):
        #This checks every possible path between all trees for shortest possible route. Note that this means that the processing power increases with the factorial
        #4 trees would be 4!=24 paths to check, 10 trees would be 10!= 3,628,800 paths I believe.
        if start_position is None:
            return [], 0.0

        if not tree_positions:
            return [], 0.0

        best_path = None
        best_distance = float("inf")

        for candidate_path in permutations(tree_positions):
            distance = self.calculate_path_distance(
                start_position,
                candidate_path
            )

            if distance < best_distance:
                best_distance = distance
                best_path = candidate_path

        return list(best_path), best_distance

    @staticmethod
    def bearing_degrees(lat1, lon1, lat2, lon2):
        #Returns: 0   = North ,270 = West
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        dlon_rad = math.radians(lon2 - lon1)

        y = math.sin(dlon_rad) * math.cos(lat2_rad)

        x = (
            math.cos(lat1_rad) * math.sin(lat2_rad)
            - math.sin(lat1_rad)
            * math.cos(lat2_rad)
            * math.cos(dlon_rad)
        )

        bearing = math.degrees(math.atan2(y, x))

        return (bearing + 360.0) % 360.0

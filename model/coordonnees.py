import math


import math

class Coordonnee:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"Coordonnee ({self.latitude}, {self.longitude})"

    def __eq__(self, other):
        return (self.latitude == other.latitude and self.longitude == other.longitude)

    def __ne__(self, other):
        return not self.__eq__(other)

    def distance(self, other):
        # --- Distance de Haversine en kilomètres ---
        R = 6371.0  # rayon moyen de la Terre en km
        lat1 = math.radians(self.latitude)
        lon1 = math.radians(self.longitude)
        lat2 = math.radians(other.latitude)
        lon2 = math.radians(other.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c



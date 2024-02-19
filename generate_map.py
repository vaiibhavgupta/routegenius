import random, folium

from shapely.affinity import translate
from shapely.geometry import LineString

from generate_route import get_osrm_route

def apply_offset(coords, offset):
    """
    Applies an offset to a line of coordinates.
    coords: list of (lat, lon) tuples representing the route.
    offset: tuple representing the offset in lat and lon.
    Returns a list of (lat, lon) tuples representing the offset route.
    """
    line = LineString(coords)
    offset_line = translate(line, offset[0], offset[1])
    
    return list(offset_line.coords)

def generate_hex_color():
    """Generates a random hex color code."""
    return "#{:06x}".format(random.randint(0, 0x9F9F9F))

def main(path_coordinates, optimized):

    if optimized:
        m = folium.Map(location=path_coordinates[0], zoom_start=12)
        offset_amount = 0.0001  # Small offset to apply to each route

        for i in range(len(path_coordinates) - 1):
            origin = path_coordinates[i]
            destination = path_coordinates[i+1]

            route = get_osrm_route(origin, destination)
            offset_route = apply_offset(route, (i * offset_amount, i * offset_amount))
            
            folium.PolyLine(offset_route, color=generate_hex_color(), weight=5, opacity=1).add_to(m)
            folium.Marker(origin, popup=i+1).add_to(m)

            m.save('optimized_route.html')
    else:
        m = folium.Map(location=path_coordinates[0], zoom_start=12)
        for i in range(len(path_coordinates)):
            folium.Marker(path_coordinates[i], popup=i+1).add_to(m)

        m.save('unoptimized_route.html')
    
    return None
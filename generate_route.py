import requests, polyline

def get_osrm_route(start, end, server_url='http://router.project-osrm.org'):
    """
    Fetches a route from an OSRM server.
    start: tuple of (lat, lon) for the starting point
    end: tuple of (lat, lon) for the ending point
    server_url: URL of the OSRM server
    Returns a list of (lon, lat) tuples representing the route.
    """
    # Construct the request URL
    coords = f"{start[1]},{start[0]};{end[1]},{end[0]}"
    url = f"{server_url}/route/v1/driving/{coords}?overview=full&geometries=polyline"
    
    # Make the request
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("OSRM server error")
    data = response.json()
    
    # Extract the route geometry and decode it using the polyline library
    route_geometry = data['routes'][0]['geometry']
    route_coords = polyline.decode(route_geometry)  # Decode the polyline
    
    # OSRM returns coordinates in (lon, lat) format, so they need to be inverted for folium
    route_coords = [(lon, lat) for lon, lat in route_coords]
    
    return route_coords
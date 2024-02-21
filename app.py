import random, streamlit as st
import streamlit.components.v1 as components

import generate_map, optimize_route

def load_html_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

st.set_page_config(layout="wide")
st.title('RouteGenius')

# Ensure the initial setup of the session state variables
if 'original_path_coordinates' not in st.session_state:
    st.session_state.original_path_coordinates = []

if 'count' not in st.session_state:
    st.session_state.count = 1

# Function to add latitude and longitude input fields
def add_lat_lon_input(key, default_lat=0.0, default_lon=0.0):
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input('Latitude', key=f'lat_{key}', value=default_lat)
    with col2:
        lon = st.number_input('Longitude', key=f'lon_{key}', value=default_lon)
    return lat, lon

# Dynamically create input fields based on count and prefill with existing values
def display_input_fields():
    for n in range(st.session_state.count):
        default_lat, default_lon = (0.0, 0.0)
        if n < len(st.session_state.original_path_coordinates):
            default_lat, default_lon = st.session_state.original_path_coordinates[n]
        lat, lon = add_lat_lon_input(n, default_lat, default_lon)
        # Update the session state with the current input values
        if lat == lon == 0:
            continue
        if n >= len(st.session_state.original_path_coordinates):
            st.session_state.original_path_coordinates.append([lat, lon])
        else:
            st.session_state.original_path_coordinates[n] = [lat, lon]

# Display the current input fields
display_input_fields()

# Button to add more input fields
_, col_add = st.columns([0.9, 1])
with col_add:
    if st.button("+ Add more"):
        st.session_state.count += 1
        st.experimental_rerun()  # Force Streamlit to rerun the script

if len(st.session_state.original_path_coordinates) != 0:
    generate_map.main(st.session_state.original_path_coordinates, False)
    st.session_state.optimized_path_coordinates = optimize_route.main(st.session_state.original_path_coordinates)
    generate_map.main(st.session_state.optimized_path_coordinates, True)

# Button to toggle optimization
_, col_opt = st.columns([11.9, 1])

with col_opt:
    show_optimized = st.button('Optimize Route')

if len(st.session_state.original_path_coordinates) != 0:
    if show_optimized:
        html_file_path = 'optimized_route.html'
        html_content = load_html_file(html_file_path)
    else:
        html_file_path = 'unoptimized_route.html'
        html_content = load_html_file(html_file_path)

else:
    if show_optimized:
        html_file_path = 'optimized_route_default.html'
        html_content = load_html_file(html_file_path)
        st.success('Optimized route calculated!')
    else:
        html_file_path = 'unoptimized_route_default.html'
        html_content = load_html_file(html_file_path)


# Display the Folium map in the Streamlit app
components.html(html_content, height=600)
st.write('Developed by RouteGenius')

st.markdown('---')

# List of fun facts
fun_facts = [
    "Route optimization not only saves time and fuel, but it also reduces wear and tear on vehicles and can significantly decrease carbon emissions. This is why logistics companies invest heavily in advanced algorithms to optimize delivery routes.",
    "The Traveling Salesman Problem, a classic algorithmic problem focused on optimization of routes, has been studied in mathematics since the 18th century and is still relevant in logistics today.",
    "Dynamic routing, which involves adjusting routes in real-time based on traffic conditions, weather, and other factors, can lead to a 10-30% reduction in drive time and fuel consumption.",
    "GPS technology, combined with route optimization algorithms, can help reduce the number of miles driven by delivery vehicles by up to 20%, leading to a significant reduction in operational costs."
]

# Initialize session state
if 'index' not in st.session_state:
    st.session_state.index = random.randint(0, len(fun_facts) - 1)

# Display the current fun fact
st.write(fun_facts[st.session_state.index])
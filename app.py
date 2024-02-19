import random, pydeck as pdk, streamlit as st
import streamlit.components.v1 as components

import generate_map, optimize_route

# Function to load map in streamlit app
def load_html_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to add latitude and longitude input fields
def add_lat_lon_input(key):
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input('Latitude', key=f'lat_{key}')
    with col2:
        lon = st.number_input('Longitude', key=f'lon_{key}')
    return lat, lon

st.session_state.original_path_coordinates = [
    [36.131687, -86.668823], # BNA
    [36.183021, -86.886495], # John C. Tune Airport
    [36.206800, -86.690000], # Opry
    [36.160485, -86.778630], # Apple Store
    [36.144051, -86.800949], # Vanderbilt
]

# Streamlit application
st.set_page_config(layout="wide")  # Use the full page width
st.title('RouteGenius')

# # Initialize the session state for count if it does not exist
# if 'count' not in st.session_state:
#     st.session_state.count = 1

# # Display the current input fields and add button
# with st.form("lat_lon_form"):
#     for n in range(st.session_state.count):
#         new_lat, new_lon = add_lat_lon_input(n)
#         st.session_state.original_path_coordinates.append([new_lat, new_lon])
    
#     # Button to add more input fields
#     if st.form_submit_button("+ Add more"):
#         st.session_state.count += 1


generate_map.main(st.session_state.original_path_coordinates, False)
st.session_state.optimized_path_coordinates = optimize_route.main(st.session_state.original_path_coordinates)
generate_map.main(st.session_state.optimized_path_coordinates, True)


# Button to toggle optimization
_, _, _, _, _, _, _, _, _, col = st.columns(10)

with col:
    show_optimized = st.button('Optimize Route')

if show_optimized:
    html_file_path = 'optimized_route.html'
    html_content = load_html_file(html_file_path)
    st.success('Optimized route calculated!')
else:
    html_file_path = 'unoptimized_route.html'
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
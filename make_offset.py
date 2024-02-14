import open3d as o3d
import numpy as np
import pandas as pd

def calculate_distances_and_coordinates(mesh, station_spacing):
    # Convert mesh vertices to NumPy array
    vertices = np.asarray(mesh.vertices)

    # Filter vertices with x > 0
    vertices_positive_x = vertices[vertices[:, 0] > 0]

    # Calculate distances from midship (x = 0)
    distances = np.abs(vertices_positive_x[:, 0])

    # Adjust distances based on station spacing
    num_stations = int(np.ceil(np.max(vertices[:, 0]) / station_spacing))
    adjusted_distances = distances.repeat(num_stations).reshape(-1, num_stations)

    # Create coordinates with adjusted distances
    coordinates = vertices_positive_x.repeat(num_stations, axis=0)
    coordinates[:, 0] = adjusted_distances.flatten()

    return adjusted_distances.flatten(), coordinates

def save_distances_and_coordinates_to_csv(distances, coordinates, output_file):
    # Create station labels
    stations = np.linspace(0, np.max(coordinates[:, 0]), len(distances))

    df = pd.DataFrame({'NO.': stations})

    # Add waterline data
    waterlines = ['W.L'] * len(stations)
    df['W.L'] = waterlines

    # Add distance values
    for i in range(len(distances)):
        # Get rounded coordinates
        rounded_coordinates = np.round(coordinates[coordinates[:, 0] == distances[i], 1:], decimals=2).flatten()
        
        # Extend rounded coordinates if necessary
        if len(rounded_coordinates) < len(stations) - 1:
            rounded_coordinates = np.concatenate([rounded_coordinates, np.zeros(len(stations) - 1 - len(rounded_coordinates))])
        
        df[str(distances[i])] = rounded_coordinates

    # Save DataFrame to CSV
    df.to_csv(output_file, index=False)

def main():
    # Load STL file
    stl_file_path = "example_hull.stl"
    mesh = o3d.io.read_triangle_mesh(stl_file_path)

    # Define station spacing
    max_x_value = np.max(np.asarray(mesh.vertices)[:, 0])  # Convert vertices to NumPy array
    station_spacing = max_x_value / 20  # Divide by 20 for 20 stations

    # Calculate distances and coordinates
    distances, coordinates = calculate_distances_and_coordinates(mesh, station_spacing)

    # Save distances and coordinates to CSV
    output_csv_file = "distances_and_coordinates.csv"
    save_distances_and_coordinates_to_csv(distances, coordinates, output_csv_file)

if __name__ == "__main__":
    main()

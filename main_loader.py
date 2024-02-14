import open3d as o3d
import numpy as np
import pandas as pd

def calculate_distances_and_coordinates(mesh):
    # Get vertices of the mesh
    vertices = np.asarray(mesh.vertices)

    # Calculate midpoint of the mesh
    midpoint = np.mean(vertices, axis=0)

    # Calculate distances from the midpoint
    distances = np.linalg.norm(vertices - midpoint, axis=1)

    # Calculate coordinates of each point
    coordinates = vertices - midpoint

    return distances, coordinates

def save_distances_and_coordinates_to_csv(distances, coordinates, output_file):
    # Create a DataFrame to store distances and coordinates
    df = pd.DataFrame({
        'X_coordinate': coordinates[:, 0],
        'Y_coordinate': coordinates[:, 1],
        'Z_coordinate': coordinates[:, 2],
        'Distance_from_midpoint': distances
    })

    # Save DataFrame to CSV
    df.to_csv(output_file, index=False)

def main():
    # Load STL file
    stl_file_path = "example_hull.stl"
    mesh = o3d.io.read_triangle_mesh(stl_file_path)

    # Calculate distances and coordinates
    distances, coordinates = calculate_distances_and_coordinates(mesh)

    # Save distances and coordinates to CSV
    output_csv_file = "distances_and_coordinates_from_midpoint.csv"
    save_distances_and_coordinates_to_csv(distances, coordinates, output_csv_file)

if __name__ == "__main__":
    main()

import open3d as o3d
import numpy as np
import pandas as pd

def load_and_filter_coordinates(mesh, midship_x):
    vertices = np.asarray(mesh.vertices)

    # Filter out vertices with x coordinate less than 0
    filtered_vertices = vertices[vertices[:, 0] >= 0]

    # Calculate coordinates of each point relative to midship
    coordinates = filtered_vertices - [midship_x, 0, 0]

    return coordinates

def save_coordinates_to_csv(coordinates, output_file):
    df = pd.DataFrame({
        'X_coordinate': coordinates[:, 0],
        'Y_coordinate': coordinates[:, 1],
        'Z_coordinate': coordinates[:, 2]
    })

    # Save DataFrame to CSV
    df.to_csv(output_file, index=False)

def main():
    # Load STL file
    stl_file_path = "example_hull.stl"
    mesh = o3d.io.read_triangle_mesh(stl_file_path)

    # Define midship X coordinate
    midship_x = 0

    # Load and filter coordinates
    coordinates = load_and_filter_coordinates(mesh, midship_x)

    # Save coordinates to CSV
    output_csv_file = "half_offset.csv"
    save_coordinates_to_csv(coordinates, output_csv_file)

if __name__ == "__main__":
    main()

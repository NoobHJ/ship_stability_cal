import open3d as o3d
import pandas as pd

def visualize_points_from_csv(csv_file):
    # Load data from CSV
    df = pd.read_csv(csv_file)

    # Extract coordinates
    coordinates = df[['X_coordinate', 'Y_coordinate', 'Z_coordinate']].values

    # Create a point cloud
    points = o3d.geometry.PointCloud()
    points.points = o3d.utility.Vector3dVector(coordinates)

    # Visualize the point cloud
    o3d.visualization.draw_geometries([points])

def main():
    # csv_file = "half_offset.csv"
    csv_file = "distances_and_coordinates.csv"
    visualize_points_from_csv(csv_file)

if __name__ == "__main__":
    main()

import numpy as np
#from mpl_toolkits import mplot3d  # noqa: F401
import pyk4a
from pyk4a import Config, PyK4A


def save_point_cloud_ply(points, colors, filename):
    num_points = len(points)
    
    with open(filename, 'w') as f:
        # Header schrijven
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("element vertex {}\n".format(num_points))
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")
        
        # Punten en kleuren schrijven
        for i in range(num_points):
            x, y, z = points[i]
            r, g, b = colors[i]
            f.write("{:.4f} {:.4f} {:.4f} {} {} {}\n".format(x, y, z, r, g, b))


def main():
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.RES_720P,
            camera_fps=pyk4a.FPS.FPS_15, #was FPS_5 
            depth_mode=pyk4a.DepthMode.WFOV_UNBINNED,  #Resolutie voor de diepte was WFOV_2X2BINNED
            synchronized_images_only=True,
        )
    )
    k4a.start()

    # Getters en setters direct ophalen en instellen op het apparaat
    k4a.whitebalance = 4500
    assert k4a.whitebalance == 4500
    k4a.whitebalance = 4510
    assert k4a.whitebalance == 4510
    
    # Wacht op een capture met diepte- en kleurinformatie
    while True:
        capture = k4a.get_capture()
        if np.any(capture.depth) and np.any(capture.color):
            break
            
    points = capture.depth_point_cloud.reshape((-1, 3))
    colors = capture.transformed_color[..., (2, 1, 0)].reshape((-1, 3))

    # Sla de puntenwolk op als een .ply-bestand
    save_point_cloud_ply(points, colors, 'C:/Users/jutta/OneDrive - Windesheim Office365/Perron038/EindAssesment/test.ply')

    k4a.stop()
    

if __name__ == "__main__":
    main()

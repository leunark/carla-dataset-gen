import numpy as np

class Projection:

    @staticmethod
    def project_to_camera(points: np.ndarray, K: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Calculate 2D projections of multiple 3D coordinates. 
        Points must be in already in camera coordinate system.
        Returns image position x,y and depth"""
        # Store original shape
        original_shape = points.shape
        
        # Reshape to (-1, 3)
        points = points.reshape(-1, 3)
        
        # Change from UE4's coordinate system to "standard"
        # (x, y, z) -> (y, -z, x)
        points = points[:, [1, 2, 0]]
        points[:, 1] *= -1
        
        # Project 3D->2D using the camera matrix
        points_img = np.dot(K, points.T).T

        # Normalize with the depth value of x but use the absolute value 
        # to ensure it won't be mirrored for objects behind the camera
        points_img[:, :2] /= np.abs(points_img[:, 2:3])

        points_img = points_img.reshape(original_shape)
        
        return points_img[..., :2].astype(int), points_img[..., 2]

    @staticmethod
    def build_projection_matrix(w: int, h: int, fov: float):
        focal = w / (2.0 * np.tan(fov * np.pi / 360.0))
        K = np.identity(3)
        K[0, 0] = K[1, 1] = focal
        K[0, 2] = w / 2.0
        K[1, 2] = h / 2.0
        return K

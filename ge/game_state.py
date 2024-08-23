from raylibpy import *

class GameState:
    def __init__(self):
        self.window_settings = {
            "width": 1920,
            "height": 1080,
            "title": "Isometric",
            "target_fps": 144,
        }

        self.camera = Camera3D(
            Vector3(10.0, 10.0, 10.0),
            Vector3(0.0, 0.0, 0.0),
            Vector3(0.0, 1.0, 0.0),
            45.0,
            CameraProjection.CAMERA_ORTHOGRAPHIC
        )

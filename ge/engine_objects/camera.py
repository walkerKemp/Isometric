from raylibpy import *
from typing import Optional 
from ge.game_state import GameState
from ge.engine_object import EngineObject

class EngineCamera(EngineObject):
    def __init__(self, game_state: 'GameState', parent: Optional['EngineObject']):
        super().__init__(game_state, parent)

        self.camera_3d = Camera3D(
            Vector3(100.0, 100.0, 100.0),
            Vector3(0.0, 0.0, 0.0),
            Vector3(0.0, 1.0, 0.0),
            90.0,
            CameraProjection.CAMERA_ORTHOGRAPHIC
        )

        self.camera_2d = Camera2D(
            Vector2(100.0, 100.0),
            Vector2(0.0, 0.0),
            0.0, 1.0
        )

    def on_update(self, delta_time: float):
        left = 1 if self.game_state.input_manager.get_key_state("camera-left")["key-down"] else 0
        right = 1 if self.game_state.input_manager.get_key_state("camera-right")["key-down"] else 0
        down = 1 if self.game_state.input_manager.get_key_state("camera-down")["key-down"] else 0
        up = 1 if self.game_state.input_manager.get_key_state("camera-up")["key-down"] else 0

        movement_dir = Vector2(left - right, down - up)

        # if self.game_state.input_manager.get_key_state("camera-left")["key-down"]:
        #     self.camera_3d.position.x -= 128.0 * delta_time
        #     self.camera_3d.target.x -= 128.0 * delta_time

        # if self.game_state.input_manager.get_key_state("camera-right")["key-down"]:
        #     self.camera_3d.position.x += 128.0 * delta_time
        #     self.camera_3d.target.x += 128.0 * delta_time

        # if self.game_state.input_manager.get_key_state("camera-down")["key-down"]:
        #     self.camera_3d.position.z += 128.0 * delta_time
        #     self.camera_3d.target.z += 128.0 * delta_time

        # if self.game_state.input_manager.get_key_state("camera-up")["key-down"]:
        #     self.camera_3d.position.z -= 128.0 * delta_time
        #     self.camera_3d.target.z -= 128.0 * delta_time




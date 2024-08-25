from raylibpy import *
from typing import TYPE_CHECKING, Optional
import random
from ge.engine_object import EngineObject
from ge.game_state import GameState

class IsometricGrid(EngineObject):
    def __init__(self, game_state: 'GameState', parent: Optional['EngineObject']):
        super().__init__(game_state, parent)
        self.cube_data = []
        self.tile_size = 32
        self._tile_size_vector3 = Vector3(self.tile_size, self.tile_size, self.tile_size)

        for i in range(1):
            for j in range(1):
                position = Vector3(i * self.tile_size, 0, j * self.tile_size)
                color = Color(*[random.randint(0, 255) for _ in range(3)], 255)
                self.cube_data.append((position, color))

    def is_on_screen(self, camera: 'Camera3D', position: 'Vector3') -> bool:
        return True

    def on_render_3d(self, camera: 'Camera3D'):
        for cube_data in self.cube_data:
            position, color = cube_data

            if self.is_on_screen(camera, position):
                draw_cube_v(position, self._tile_size_vector3, color)

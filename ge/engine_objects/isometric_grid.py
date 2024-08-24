from raylibpy import *
from typing import Optional
import random
from ge.engine_object import EngineObject
from ge.game_state import GameState

class IsometricGrid(EngineObject):
    def __init__(self, game_state: 'GameState', parent: Optional['EngineObject']):
        super().__init__(game_state, parent)
        self.cube_data = []
        self.tile_size = 4
        self._tile_size_vector3 = Vector3(self.tile_size, self.tile_size, self.tile_size)

        for i in range(10):
            for j in range(10):
                self.cube_data.append(
                    (
                        Vector3(
                            i * self.tile_size,
                            0,
                            j * self.tile_size,
                        ),
                        Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
                    )
                )

    def on_render_3d(self):
        for cube_data in self.cube_data:
            draw_cube_v(cube_data[0], self._tile_size_vector3, cube_data[1])
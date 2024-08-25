from raylibpy import *
from ge.game_state import GameState
from ge.engine_object import EngineObject
from ge.engine_objects.isometric_grid import IsometricGrid
from ge.engine_objects.camera import EngineCamera
import math

class RootObject(EngineObject):
    def __init__(self, game_state: 'GameState'):
        super().__init__(game_state, None)

        self.global_camera = EngineCamera(game_state, self)

        self.children.append(self.global_camera)
        self.children.append(IsometricGrid(game_state, self))

def run_game():
    game_state = GameState()
    root_object = RootObject(game_state)

    init_window(
        game_state.window_settings["width"],
        game_state.window_settings["height"],
        game_state.window_settings["title"]
    )

    set_target_fps(game_state.window_settings["target_fps"])
    # toggle_fullscreen()

    while not window_should_close():
        frame_time = get_frame_time()

        begin_drawing()
        clear_background(BLACK)

        begin_mode3d(root_object.global_camera.camera_3d)
        root_object._on_render_3d(root_object.global_camera.camera_3d)
        draw_grid(128, 4)
        end_mode3d()

        begin_mode2d(root_object.global_camera.camera_2d)
        root_object._on_render(root_object.global_camera.camera_2d)
        end_mode2d()

        root_object._on_render_ui()

        draw_fps(4, 4)
        end_drawing()

        root_object._on_update(frame_time)

    close_window()
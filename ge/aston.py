from raylibpy import *
from ge.game_state import GameState
from ge.engine_object import EngineObject

class RootObject(EngineObject):
    def __init__(self, game_state: 'GameState'):
        super().__init__(game_state, None)

    def on_render(self):
        draw_text("test data", 32, 32, 26, WHITE)
        draw_cube(
            Vector3(0.0, 0.0, 0.0),
            2.0, 2.0, 2.0, WHITE
        )

def run_game():
    game_state = GameState()
    root_object = RootObject(game_state)

    init_window(
        game_state.window_settings["width"],
        game_state.window_settings["height"],
        game_state.window_settings["title"]
    )

    set_target_fps(game_state.window_settings["target_fps"])
    toggle_fullscreen()

    while not window_should_close():
        begin_drawing()
        begin_mode3d(game_state.camera)

        root_object._on_render()

        clear_background(BLACK)
        end_mode3d()


        draw_fps(4, 4)
        end_drawing()

        root_object._on_update()

    close_window()
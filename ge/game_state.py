from raylibpy import *
from ge.input import InputManager

class GameState:
    def __init__(self):
        self.window_settings = {
            "width": 1920,
            "height": 1080,
            "title": "Isometric",
            "target_fps": 144,
        }

        self.input_manager = InputManager()


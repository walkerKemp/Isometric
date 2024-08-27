from raylibpy import *

class Input:
    def __init__(self):
        self.key_bindings = {
            "player-left": KEY_A,
            "player-right": KEY_D,
            "player-up": KEY_W,
            "player-down": KEY_S,
        }

    def get_movement_input(self) -> Vector2:
        left = 1.0 if is_key_down(self.key_bindings["player-left"]) else 0.0
        right = 1.0 if is_key_down(self.key_bindings["player-right"]) else 0.0
        up = 1.0 if is_key_down(self.key_bindings["player-up"]) else 0.0
        down = 1.0 if is_key_down(self.key_bindings["player-down"]) else 0.0

        return Vector2(right - left, down - up)

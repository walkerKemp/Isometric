from raylibpy import *
from typing import Dict

class InputManager:
    def __init__(self):
        self.key_bindings = {
            "camera-left": KEY_A,
            "camera-right": KEY_D,
            "camera-up": KEY_W,
            "camera-down": KEY_S,
        }

    def get_key_state(self, binding: str) -> Dict[str, bool]:
        letter = self.key_bindings.get(binding, None)
        if letter == None:
            return None

        return {
            "key-down": is_key_down(letter),
            "key-pressed": is_key_pressed(letter),
            "key-released": is_key_released(letter),
            "key-up": is_key_up(letter),
        }

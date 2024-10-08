from raylibpy import *

def lerp(a: float, b: float, c: float) -> float:
    return a + c * (b - a)

def lerp_vector2(a: Vector2, b: Vector2, c: float) -> Vector2:
    return Vector2(
        lerp(a.x, b.x, c),
        lerp(a.y, b.y, c)
    )

_iota_counter = 0
def _iota(reset=False):
    global _iota_counter
    if reset:
        _iota_counter = 0
    _iota_counter += 1
    return _iota_counter - 1
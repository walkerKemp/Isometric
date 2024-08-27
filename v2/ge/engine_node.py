from ge.aston_math import *
from typing import Optional, List, Dict
from raylibpy import *
import os

_iota_counter = 0
def _iota(reset=False):
    global _iota_counter
    if reset:
        _iota_counter = 0
    _iota_counter += 1
    return _iota_counter - 1

class EngineNode:
    # if parent is none than this is the root object, all children will have a parent
    def __init__(self, game_state: dict[str, any], parent: Optional['EngineNode'], *_args, **_kwargs):
        self._id = None
        self.parent: Optional['EngineNode'] = parent
        self.children: Dict[int, 'EngineNode'] = {}
        self._children_pointer = 0
        self.game_state  = game_state

        self.position: Vector2 = _kwargs.get("position", Vector2())
        self.velocity: Vector2 = _kwargs.get("velocity", Vector2())
        self.size: Vector2 = _kwargs.get("size", Vector2())
        self.default_physics: bool = _kwargs.get("default_physics", False)

        self._position_lock_target: Optional['EngineNode'] = None

    def with_node(self, node: 'EngineNode') -> 'EngineNode':
        self.children[self._children_pointer] = node
        node._id = self._children_pointer
        self._children_pointer += 1
        node.parent = self
        return self

    def on_render_ui(self):
        return None

    def on_render(self, camera: Camera2D):
        return None
    
    def on_update(self, delta_time: float):
        return None
    
    def _on_render_ui(self):
        self.on_render_ui()

        for _id, child in self.children.items():
            child._on_render_ui()
    
    def _on_render(self, camera: Camera2D):
        self.on_render(camera)
        
        for _id, child in self.children.items():
            child._on_render(camera)

    def _on_update(self, delta_time: float):
        self.on_update(delta_time)

        if self.default_physics:
            pass

        if self._position_lock_target != None:
            self.position = self._position_lock_target.position

        for _id, child in self.children.items():
            child._on_update(delta_time)

    def lock_node_position(self, other: 'EngineNode'):
        self._position_lock_target = other

class CameraNode(EngineNode):
    def __init__(self, game_state: dict['str', any], parent: Optional['EngineNode'], *_args, **_kwargs):
        self.camera = _kwargs.get("camera", Camera2D())
        self.lock_on_target: Optional['EngineNode'] = _kwargs.get("lock_on_target", None)
        super().__init__(game_state, parent, *_args, **_kwargs)

    def on_update(self, delta_time: float):
        if self.lock_on_target is None:
            return None
        
        target_center = self.lock_on_target.position + (self.lock_on_target.size / 2)
        
        self.camera.target = lerp_vector2(self.camera.target, target_center, 0.03)

class BackgroundNode(EngineNode):
    def __init__(self, game_state: dict['str', any], parent: Optional['EngineNode'], *_args, **_kwargs):
        self.tile_size = 128

        super().__init__(game_state, parent, *_args, **_kwargs, size=Vector2(self.tile_size, self.tile_size))
    
    def on_render(self, camera: Camera2D):
        window_size = Vector2(
            self.game_state["width"],
            self.game_state["height"]
        )

        squares_horizontal = int(window_size.x / self.tile_size) + 1
        squares_vertical = int(window_size.y / self.tile_size) + 1

        alpha_high = 180
        alpha_low = 100

        for i in range(squares_horizontal):
            for j in range(squares_vertical):
                alpha = alpha_high if i % 2 == 0 else alpha_low
                if j % 2 == 1:
                    alpha = alpha_high if i % 2 == 1 else alpha_low

                color = Color(
                    69, 40, 60, alpha
                )

                draw_rectangle(i * self.tile_size, j * self.tile_size, self.tile_size, self.tile_size, color)

class PlayerNode(EngineNode):
    def __init__(self, game_state: Dict[str, any], parent: Optional['EngineNode'], *_args, **_kwargs):
        self.movement_speed = 256.0
        super().__init__(game_state, parent, *_args, **_kwargs)
    
    def on_render(self, camera: Camera2D):
        draw_rectangle_v(self.position, self.size, WHITE)

    def on_update(self, delta_time: float):
        movement_vector: Vector2 = self.game_state['input'].get_movement_input()
        movement_vector.normalize()
        movement_vector *= self.movement_speed * delta_time

        self.position += movement_vector

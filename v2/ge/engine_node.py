from ge.aston_util import *
from ge.input import SELECTION_MODE
from typing import Optional, List, Dict
from raylibpy import *
import os

class Timer:
    def __init__(self, delta_time_total: float):
        self.delta_time_counter = 0.0
        self.delta_time_total = delta_time_total
        self.is_complete: bool = False
        self.is_enabled = True

    @property
    def percent_complete(self) -> float:
        return self.delta_time_counter / self.delta_time_total

    def on_update(self, delta_time: float):
        if self.is_enabled:
            self.delta_time_counter += delta_time
        self.is_complete = self.delta_time_counter >= self.delta_time_total

    def start(self):
        self.is_enabled = True

    def stop(self):
        self.is_enabled = False

    def reset(self):
        self.delta_time_counter = 0
        self.is_complete = False

class EngineNode:
    # if parent is none than this is the root object, all children will have a parent
    def __init__(self, game_state: dict[str, any], parent: Optional['EngineNode'], *_args, **_kwargs):
        self._id = None
        self.parent: Optional['EngineNode'] = parent
        self.children: Dict[int, 'EngineNode'] = {}
        self._children_pointer = 0
        self.timers: Dict[int, 'Timer'] = {}
        self.game_state  = game_state

        self.position: Vector2 = _kwargs.get("position", Vector2())
        self.velocity: Vector2 = _kwargs.get("velocity", Vector2())
        self.acceleration: Vector2 = _kwargs.get("acceleration", Vector2())
        self.size: Vector2 = _kwargs.get("size", Vector2())
        self.default_physics: bool = _kwargs.get("default_physics", False)
        self.friction: float = _kwargs.get("friction", 0.5)
        self.max_velocity: float = _kwargs.get("max_velocity", 10.0)

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
        for _id, timer in self.timers.items():
            timer.on_update(delta_time)

        self.on_update(delta_time)

        if self.default_physics:
            self.velocity += self.acceleration
            self.position += self.velocity

            if abs(self.acceleration.x) < 0.1:
                self.velocity.x *= self.friction

            if abs(self.acceleration.y) < 0.1:
                self.velocity.y *= self.friction

            self.acceleration = Vector2()

            if self.velocity.length > self.max_velocity:
                self.velocity = self.velocity.normalize() * self.max_velocity

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
        super().__init__(game_state, parent, *_args, **_kwargs)

        self.max_speed = 512.0
        self.acceleration_speed = 128.0
        self.selection_radius = 384.0
        self.selection_location: Vector2 = Vector2()

        self.timers["zip-timer"] = Timer(1.0)
        self.timers["zip-timer"].start()
    
    def on_render(self, camera: Camera2D):
        draw_rectangle_v(self.position - (self.size / 2), self.size, WHITE)

        if self.game_state["input"].selection_mode == SELECTION_MODE.GAME:
            selection_radius_color = Color(255, 255, 255, 100)
            selection_color = Color(128, 128, 128, 100)
            if is_mouse_button_down(MOUSE_BUTTON_RIGHT):
                zip_location = self.get_zip_location(camera)

                draw_circle(zip_location.x, zip_location.y, 16, selection_color)
                draw_circle_lines(self.position.x, self.position.y, self.selection_radius, selection_radius_color)

    def on_update(self, delta_time: float):
        movement_vector: Vector2 = self.game_state['input'].get_movement_input()
        movement_vector.normalize()

        self.acceleration = movement_vector * self.acceleration_speed * delta_time

        if self.game_state["input"].selection_mode == SELECTION_MODE.GAME:
            if self.timers["zip-timer"].is_complete and is_mouse_button_released(MOUSE_BUTTON_RIGHT):
                zip_location = self.get_zip_location(self.game_state["global-camera"])
                self.position = zip_location
                self.timers["zip-timer"].reset()

    def get_zip_location(self, camera: Camera2D) -> Vector2:
        selection_location = get_mouse_position()
        relative_location = get_screen_to_world2d(selection_location, camera)
        difference = self.position - relative_location

        if difference.length > self.selection_radius:
            closest = self.position - (self.position - relative_location).normalize() * self.selection_radius
            return closest
        else:
            return relative_location



from ge.aston_math import *
from typing import Optional, List, Dict
from raylibpy import *
import os


class EngineNode:
    # if parent is none than this is the root object, all children will have a parent
    def __init__(self, game_state: dict[str, any], parent: Optional['EngineNode'], *_args, **_kwargs):
        self.parent: Optional['EngineNode'] = parent
        self.children: Dict['EngineNode'] = {}
        self._children_pointer = 0
        self.game_state  = game_state

        self.position: Vector2 = _kwargs.get("position", Vector2())
        self.desired_position: Vector2 = self.position

        self.velocity: Vector2 = _kwargs.get("velocity", Vector2())

        self.default_physics = _kwargs.get("default_physics", False)
        self._position_lock_target: Optional['EngineNode'] = None

        self.approach_speed = _kwargs.get("approach_speed", 0.3)

    def add_node(self, node: 'EngineNode') -> 'EngineNode':
        self.children[self._children_pointer] = node
        self._children_pointer += 1
        node.parent = self
        return self

    def on_render_ui(self):
        return None

    def on_render(self):
        return None
    
    def on_render_3d(self):
        return None
    
    def on_update(self, delta_time: float):
        return None
    
    def _on_render(self):
        self.on_render()
        
        for _id, child in self.children.items():
            child._on_render()

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


class PlayerNode(EngineNode):
    def __init__(self, game_state: dict['str', 'str'], parent: Optional['EngineNode'], *_args, **_kwargs):
        super().__init__(game_state, parent, *_args, **_kwargs)

    def on_update(self, delta_time: float):
        movement = self.game_state["input"].get_movement_input() * delta_time * 100.0
        self.velocity = movement * self.approach_speed

class AnimationNode(EngineNode):
    def __init__(self, game_state: dict['str', 'str'], parent: Optional['EngineNode'], animation_folder: str, *_args, **_kwargs):
        super().__init__(game_state, parent, *_args, **_kwargs)

        self.key_frames = []
        for file in os.listdir(animation_folder):
            self.key_frames.append(load_texture(os.path.join(animation_folder, file)))

        
        self.frame_index = 0
        self.frame_index_max = len(self.key_frames)

        assert(self.frame_index_max > 0, "test")

        if game_state["debug"]:
            print(f"Animation loaded with {self.frame_index_max} frames.")

        self.frame_rate = 1.0 / 3.0
        self.frame_time = 0.0

        self.width = self.key_frames[0].width
        self.height = self.key_frames[1].height
        self.scale = 1

    def on_render(self):
        centered_position = Vector2(
            self.position.x - self.width / 2,
            self.position.y - self.height / 2
        )

        key_frame = self.key_frames[self.frame_index]

        draw_texture_ex(
            key_frame,
            centered_position,
            0,
            self.scale,
            WHITE
        )

        if self.game_state["debug"]:
            draw_circle(self.position.x, self.position.y, 2, GREEN)

    def on_update(self, delta_time: float):
        self.frame_time += delta_time
        if self.frame_time > self.frame_rate:
            self.frame_index = (self.frame_index + 1) % self.frame_index_max
            self.frame_time = 0.0


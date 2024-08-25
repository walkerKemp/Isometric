from typing import Optional, List
from raylibpy import *
import os

class GameState:
    pass

class EngineNode:
    # if parent is none than this is the root object, all children will have a parent
    def __init__(self, game_state: 'GameState', parent: Optional['EngineNode'], *_args, **_kwargs):
        self.parent: Optional['EngineNode'] = parent
        self.children: List['EngineNode'] = []
        self.game_state: 'GameState' = game_state

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
        
        for child in self.children:
            child._on_render()

    def _on_update(self, delta_time: float):
        self.on_update(delta_time)

        for child in self.children:
            child._on_update(delta_time)

class PlayerNode(EngineNode):
    pass

class AnimationNode(EngineNode):
    def __init__(self, game_state: 'GameState', parent: Optional['EngineNode'], animation_folder: str):
        super().__init__(game_state, parent)

        self.key_frames = []
        for file in os.listdir(animation_folder):
            self.key_frames.append(load_texture(os.path.join(animation_folder, file)))

        self.frame_index = 0
        self.frame_index_max = len(self.key_frames)

        self.frame_rate = 1.0 / 3.0
        self.frame_time = 0.0

    def on_render(self):
        draw_texture(self.key_frames[self.frame_index], 32, 32, WHITE)

    def on_update(self, delta_time: float):
        self.frame_time += delta_time
        if self.frame_time > self.frame_rate:
            self.frame_index = (self.frame_index + 1) % self.frame_index_max
            self.frame_time = 0.0


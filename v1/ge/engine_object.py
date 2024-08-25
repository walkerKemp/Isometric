from ge.game_state import GameState
from typing import TYPE_CHECKING, Optional, List, Callable
from uuid import uuid4
from raylibpy import *

if TYPE_CHECKING:
    from aston import RootObject

def _generate_id():
    return str(uuid4())

class EngineObject:
    # if parent is none than this is the root object, all children will have a parent
    def __init__(self, game_state: 'GameState', parent: Optional['EngineObject'], *_args, **_kwargs):
        self._id: str = _generate_id()
        self.parent: Optional['EngineObject'] = parent
        self.children: List['EngineObject'] = []
        self.game_state: 'GameState' = game_state

    def on_render_ui(self):
        return None

    def on_render(self, camera: 'Camera2D'):
        return None
    
    def on_render_3d(self, camera: 'Camera3D'):
        return None
    
    def on_update(self, delta_time: float):
        return None
    
    def _on_render_ui(self):
        self.on_render_ui()

        for child in self.children:
            child._on_render_ui()

    def _on_render(self, camera: 'Camera2D'):
        self.on_render(camera)
        
        for child in self.children:
            child._on_render(camera)

    def _on_render_3d(self, camera: 'Camera3D'):
        self.on_render_3d(camera)

        for child in self.children:
            child._on_render_3d(camera)

    def _on_update(self, delta_time: float):
        self.on_update(delta_time)

        for child in self.children:
            child._on_update(delta_time)

    @property
    def head(self) -> 'RootObject':
        if self.parent == None:
            return self
        
        return self.parent.head

    # TODO: implement
    def find(self, _id: str) -> Optional['EngineObject']:
        return None
    
    # TODO: implement
    def find_where(self, func: Callable[['EngineObject'], bool]) -> Optional['EngineObject']:
        return None 
    
    # TODO: implement
    def find_all_where(self, func: Callable[['EngineObject'], bool]) -> List['EngineObject']:
        return []
    

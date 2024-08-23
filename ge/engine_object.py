from ge.game_state import GameState
from typing import Optional, List, Callable
from uuid import uuid4

def _generate_id():
    return str(uuid4())

class EngineObject:
    # if parent is none than this is the root object, all children will have a parent
    def __init__(self, game_state: 'GameState', parent: Optional['EngineObject'], *_args, **_kwargs):
        self._id: str = _generate_id()
        self.parent: Optional['EngineObject'] = parent
        self.children: List['EngineObject'] = []
        self.game_state: 'GameState' = game_state

    def on_render(self):
        return None
    
    def on_update(self):
        return None

    def _on_render(self):
        self.on_render()
        
        for child in self.children:
            child._on_render()

    def _on_update(self):
        self.on_update()

        for child in self.children:
            child._on_update()

    # TODO: implement
    def find(self, _id: str) -> Optional['EngineObject']:
        return None
    
    # TODO: implement
    def find_where(self, func: Callable[['EngineObject'], bool]) -> Optional['EngineObject']:
        return None 
    
    # TODO: implement
    def find_all_where(self, func: Callable[['EngineObject'], bool]) -> List['EngineObject']:
        return []
    

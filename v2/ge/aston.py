from raylibpy import *
from ge.engine_node import EngineNode, AnimationNode

def run_game():
    window_data = {
        "width": 1920,
        "height": 1080,
        "title": "Isometric",
        "target-fps": 144
    }

    init_window(
        window_data["width"],
        window_data["height"],
        window_data["title"]
    )

    set_config_flags(FLAG_VSYNC_HINT)
    toggle_fullscreen()

    root_node = EngineNode(window_data, None)
    animation_node = AnimationNode(window_data, root_node, "assets/idle")
    root_node.children.append(animation_node)

    while not window_should_close():
        frame_time = get_frame_time()
        root_node._on_update(frame_time)

        begin_drawing()
        clear_background(WHITE)

        root_node._on_render()

        draw_fps(4, 4)
        end_drawing()

    close_window()
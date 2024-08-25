from raylibpy import *
from ge.engine_node import EngineNode, AnimationNode, PlayerNode

def run_game():
    window_data = {
        "width": 1920,
        "height": 1080,
        "title": "Isometric",
        "target-fps": 144,
        "debug": False
    }

    init_window(
        window_data["width"],
        window_data["height"],
        window_data["title"],
    )

    set_config_flags(FLAG_VSYNC_HINT)
    toggle_fullscreen()

    global_camera = Camera2D(Vector2(), Vector2(), 0.0, 1.0)


    root_node = EngineNode(window_data, None)
    player_node = PlayerNode(window_data, root_node, position=Vector2(400, 400))
    animation_node = AnimationNode(window_data, root_node, "assets/idle")
    animation_node.lock_node_position(player_node)

    root_node.add_node(player_node.add_node(animation_node))

    while not window_should_close():
        frame_time = get_frame_time()
        root_node._on_update(frame_time)

        begin_drawing()
        begin_mode2d(global_camera)
        clear_background(WHITE)

        root_node._on_render()

        draw_fps(4, 4)
        end_mode2d()
        end_drawing()

    close_window()
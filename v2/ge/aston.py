from raylibpy import *
from ge.engine_node import EngineNode, BackgroundNode, PlayerNode, CameraNode
from ge.input import Input

def run_game():
    window_data = {
        "width": 1920,
        "height": 1080,
        "title": "Isometric",
        "target-fps": 144,
        "debug": False,
        "input": Input()
    }

    init_window(
        window_data["width"],
        window_data["height"],
        window_data["title"],
    )

    set_config_flags(FLAG_VSYNC_HINT)
    toggle_fullscreen()

    global_camera = Camera2D(Vector2(window_data["width"] / 2, window_data["height"] / 2), Vector2(), 0.0, 1.0)

    root_node = EngineNode(window_data, None)
    camera_node = CameraNode(window_data, root_node, camera=global_camera)
    background_node = BackgroundNode(window_data, root_node)
    player_node = PlayerNode(window_data, root_node, size=Vector2(32, 32))

    camera_node.lock_on_target = player_node

    root_node.with_node(camera_node).with_node(background_node).with_node(player_node)

    while not window_should_close():
        frame_time = get_frame_time()
        root_node._on_update(frame_time)

        begin_drawing()
        begin_mode2d(global_camera)
        clear_background(BLACK)

        root_node._on_render(global_camera)
        end_mode2d()

        root_node._on_render_ui()

        draw_fps(4, 4)
        end_drawing()

    close_window()
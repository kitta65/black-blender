import contextlib
import bpy
import addon_utils


@contextlib.contextmanager
def text_area():
    area = bpy.context.workspace.screens[0].areas[0]
    original_type = area.type
    area.type = "TEXT_EDITOR"

    try:
        yield area
    finally:
        area.type = original_type


@contextlib.contextmanager
def new_text(area=bpy.types.Area):
    space = area.spaces[0]  # active space
    if not isinstance(space, bpy.types.SpaceTextEditor):
        raise Exception("unnexpected space type")

    bpy.ops.text.new()
    text = space.text

    try:
        yield text
    finally:
        bpy.ops.text.unlink()


def main():
    # prepare
    addon_utils.enable("myaddon")
    bpy.ops.black_blender.install()

    # execute operator
    input_str = "import bpy \n"
    expected_str = "import bpy\n"
    with (
        text_area() as area,
        bpy.context.temp_override(area=area),
        new_text(area) as text,
    ):
        text.from_string(input_str)
        bpy.ops.black_blender.format()
        actual_str = text.as_string()

    # assertion
    if actual_str != expected_str:
        raise Exception("not formatted!")


if __name__ == "__main__":
    main()

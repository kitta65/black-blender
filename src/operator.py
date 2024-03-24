import importlib
import subprocess
import sys
from typing import Final

import bpy

if "exception" in locals():
    importlib.reload(exception)
else:
    from . import exception

# return items
# https://docs.blender.org/api/current/bpy_types_enum_items/operator_return_items.html
CANCELLED: Final[str] = "CANCELLED"
FINISHED: Final[str] = "FINISHED"

# report items
# https://docs.blender.org/api/current/bpy_types_enum_items/wm_report_items.html
INFO: Final[str] = "INFO"
ERROR: Final[str] = "ERROR"

PYTHON_EXECUTABLE = sys.executable


class BLACK_WRAPPER_OT_InstallBlack(bpy.types.Operator):
    bl_idname = "black_wrapper.install_black"
    bl_label = "install latest Black"
    bl_description = "install latest Black"

    def execute(self, _):
        try:
            subprocess.run([PYTHON_EXECUTABLE, "-m", "ensurepip"], check=True)
        except subprocess.CalledProcessError:
            self.report({ERROR}, "failed to execute ensurepip")
            return {CANCELLED}

        try:
            subprocess.run(
                [PYTHON_EXECUTABLE, "-m", "pip", "install", "--upgrade", "black"],
                check=True,
            )
        except subprocess.CalledProcessError:
            self.report({ERROR}, "failed to install Black")
            return {CANCELLED}

        self.report({INFO}, "Black was installed successfully")
        return {FINISHED}


class BLACK_WRAPPER_OT_Format(bpy.types.Operator):
    bl_idname = "black_wrapper.format"
    bl_label = "Run Black"
    bl_description = "Format Python script using Black"
    bl_options = {"UNDO"}

    def execute(self, context):
        for area in context.window.screen.areas:
            if area.type != "TEXT_EDITOR":
                continue

            space = area.spaces[0]  # active space
            if not isinstance(space, bpy.types.SpaceTextEditor):
                continue

            text = space.text
            try:
                formatted = format(text.as_string())
            except exception.BlackWrapperException:
                self.report({ERROR}, "failed to format")
                return {CANCELLED}

            text.from_string(formatted)

            with context.temp_override(area=area):
                bpy.ops.text.jump(1)  # needed to refresh
            break  # several text editors may be open, but format only first one

        return {FINISHED}


def format(text: str) -> str:
    try:
        import black
    except:
        raise exception.BlackWrapperException()

    return black.format_str(text, mode=black.FileMode())
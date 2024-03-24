import bpy
import subprocess
import sys

PYTHON_EXECUTABLE = sys.executable


class BLACK_WRAPPER_OT_InstallBlack(bpy.types.Operator):
    bl_idname = "black_wrapper.install_black"
    bl_label = "install or update black"
    bl_description = "install or update black"

    def execute(self, _):
        self.report({"INFO"}, "install black")
        try:
            subprocess.run([PYTHON_EXECUTABLE, "-m", "ensurepip"], check=True)
        except subprocess.CalledProcessError:
            self.report({"ERROR"}, "failed to execute ensurepip")
            return {"CANCELLED"}

        try:
            subprocess.run(
                [PYTHON_EXECUTABLE, "-m", "pip", "install", "--upgrade", "black"],
                check=True,
            )
        except subprocess.CalledProcessError:
            self.report({"ERROR"}, "failed to install Black")
            return {"CANCELLED"}

        self.report({"INFO"}, "Black was installed successfully")
        return {"FINISHED"}

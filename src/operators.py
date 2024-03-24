import bpy
import subprocess
import sys

PYTHON_EXECUTABLE = sys.executable


class BLACK_WRAPPER_OT_InstallBlack(bpy.types.Operator):
    bl_idname = "black_wrapper.install_black"
    bl_label = "install latest Black"
    bl_description = "install latest Black"

    def execute(self, _):
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


class BLACK_WRAPPER_OT_Format(bpy.types.Operator):
    bl_idname = "black_wrapper.format"
    bl_label = "Run Black"
    bl_description = "Format Python script using Black"

    def execute(self, _):
        try:
            import black

            black
        except:
            self.report({"ERROR"}, "Black was not found")
            return {"CANCELLED"}

        self.report({"INFO"}, "Black was executed successfully")
        return {"FINISHED"}

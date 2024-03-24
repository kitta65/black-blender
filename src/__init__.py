import importlib
import bpy

if "operators" in locals():
    importlib.reload(operators)
else:
    from . import operators

bl_info = {
    "name": "Black",
    "author": "kitta65",
    "version": (0, 0, 1),
    "blender": (4, 0, 0),
    "location": "TEXT Editor > Format > Run Black",
    "description": "Format Python script using Black",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/kitta65/black-blender",
    "tracker_url": "https://github.com/kitta65/black-blender/issues",
    "category": "Development",
}


class BLACK_WRAPPER_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, _):
        layout = self.layout
        layout.operator(
            operators.BLACK_WRAPPER_OT_InstallBlack.bl_idname, icon="CONSOLE"
        )


def menu(cls, _):
    cls.layout.separator()
    cls.layout.operator(operators.BLACK_WRAPPER_OT_Format.bl_idname, icon="SCRIPT")


classes = [
    operators.BLACK_WRAPPER_OT_InstallBlack,
    operators.BLACK_WRAPPER_OT_Format,
    BLACK_WRAPPER_Preferences,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.TEXT_MT_format.append(menu)


def unregister():
    bpy.types.TEXT_MT_format.remove(menu)

    for c in reversed(classes):
        bpy.utils.unregister_class(c)

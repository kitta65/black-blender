import importlib
import bpy

if "operator" in locals():
    importlib.reload(operator)
else:
    from . import operator

bl_info = {
    "name": "Black Blender",
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


class BLACK_BLENDER_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, _):
        layout = self.layout
        layout.operator(
            operator.BLACK_BLENDER_OT_Install.bl_idname, icon="CONSOLE"
        )


def menu(cls, _):
    cls.layout.separator()
    cls.layout.operator(operator.BLACK_BLENDER_OT_Format.bl_idname, icon="SCRIPT")


classes = [
    operator.BLACK_BLENDER_OT_Install,
    operator.BLACK_BLENDER_OT_Format,
    BLACK_BLENDER_Preferences,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.TEXT_MT_format.append(menu)


def unregister():
    bpy.types.TEXT_MT_format.remove(menu)

    for c in reversed(classes):
        bpy.utils.unregister_class(c)

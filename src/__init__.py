import bpy

from .operators import BLACK_WRAPPER_OT_InstallBlack

bl_info = {
    "name": "Black",
    "author": "kitta65",
    "version": (0, 0, 1),
    "blender": (4, 0, 0),
    "location": "TODO",
    "description": "Format Python script using Black",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/kitta65/black-blender",
    "tracker_url": "https://github.com/kitta65/black-blender/issues",
    "category": "Development",
}

class BLACK_WRAPPER_OT_Format(bpy.types.Operator):
    bl_idname = "black_wrapper.format"
    bl_label = "Format"
    bl_description = "Format Python script using Black"

    def execute(self, _):
        try:
            import black
            black
        except:
            self.report({"ERROR"}, "failed to import black")
            return {"CANCELLED"}

        self.report({"INFO"}, "Black was executed successfully")
        return {"FINISHED"}

class BLACK_WRAPPER_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, _):
        layout = self.layout
        layout.operator(BLACK_WRAPPER_OT_InstallBlack.bl_idname, icon="COMMUNITY")


def menu(cls, _):
    cls.layout.separator()
    cls.layout.operator(BLACK_WRAPPER_OT_Format.bl_idname, icon="COMMUNITY")


classes = [
    BLACK_WRAPPER_OT_InstallBlack,
    BLACK_WRAPPER_OT_Format,
    BLACK_WRAPPER_Preferences,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.VIEW3D_MT_edit_mesh.append(menu)


def unregister():
    bpy.types.VIEW3D_MT_edit_mesh.remove(menu)

    for c in reversed(classes):
        bpy.utils.unregister_class(c)

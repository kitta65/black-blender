import importlib
import bpy

# https://blenderartists.org/t/how-to-reload-add-on-code/1202715/6
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
        layout.operator(operator.BLACK_BLENDER_OT_Install.bl_idname, icon="CONSOLE")


def menu(cls, _):
    cls.layout.separator()
    cls.layout.operator(operator.BLACK_BLENDER_OT_Format.bl_idname, icon="SCRIPT")


classes = [
    operator.BLACK_BLENDER_OT_Install,
    operator.BLACK_BLENDER_OT_Format,
    BLACK_BLENDER_Preferences,
]

keymaps = []


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.TEXT_MT_format.append(menu)

    # https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html#keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name="Run Black", space_type="TEXT_EDITOR")
        kmi = km.keymap_items.new(
            operator.BLACK_BLENDER_OT_Format.bl_idname,
            "F",
            "PRESS",
            ctrl=True,
            shift=True,
        )
        keymaps.append((km, kmi))


def unregister():
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)
    keymaps.clear()

    bpy.types.TEXT_MT_format.remove(menu)

    for c in reversed(classes):
        bpy.utils.unregister_class(c)

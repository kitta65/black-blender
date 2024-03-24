import bpy
import bmesh
import random

bl_info = {
    "name": "Thanos",
    "author": "kitta65",
    "version": (0, 0, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Mesh > Thanos",
    "description": "Wipe out half of the vertices / edges / faces",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/kitta65/thanos-blender",
    "tracker_url": "https://github.com/kitta65/thanos-blender/issues",
    "category": "Sample",
}


class THANOS_OT_SnapFingers(bpy.types.Operator):
    bl_idname = "thanos.snap_fingers"
    bl_label = "Thanos"
    bl_description = "Wipe out half of the vertices / edges / faces"
    bl_options = {"UNDO"}

    def execute(self, context):
        modes = ["VERTS", "EDGES", "FACES_ONLY"]
        bools = context.scene.tool_settings.mesh_select_mode
        mode = [m for b, m in zip(bools, modes) if b][0]

        me = context.object.data
        bm = bmesh.from_edit_mesh(me)

        match mode:
            case "VERTS":
                all = bm.verts
            case "EDGES":
                all = bm.edges
            case "FACES_ONLY":
                all = bm.faces

        selection = [x for x in all if x.select]
        half = random.sample(selection, len(selection) // 2)
        bmesh.ops.delete(bm, geom=half, context=mode)
        bmesh.update_edit_mesh(me)
        bm.free()

        return {"FINISHED"}


def menu(cls, _):
    cls.layout.separator()
    cls.layout.operator(THANOS_OT_SnapFingers.bl_idname, icon="COMMUNITY")


classes = [THANOS_OT_SnapFingers]


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.VIEW3D_MT_edit_mesh.append(menu)


def unregister():
    bpy.types.VIEW3D_MT_edit_mesh.remove(menu)

    for c in reversed(classes):
        bpy.utils.unregister_class(c)
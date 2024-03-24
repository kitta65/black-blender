import bpy
import addon_utils


def main():
    addon_utils.enable("myaddon")

    # prepare
    bpy.ops.black_blender.install()

    # TODO test formatter


if __name__ == "__main__":
    main()

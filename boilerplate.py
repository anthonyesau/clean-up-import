import bpy

class boilerplate_operator(bpy.types.Operator):
    """A boilerplate operator"""
    bl_idname = ""
    bl_label = ""

    def execute(self, context):
        return


class boilerplate_panel(bpy.types.Panel):
    """A boilerplate panel"""
    bl_idname = ""
    bl_label = ""
    bl_description = ""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AE Utilz"

    def draw(self, context):
        


def register():
    bpy.utils.register_class(boilerplate_operator)
    bpy.utils.register_class(boilerplate_panel)

def unregister():
    bpy.utils.unregister_class(boilerplate_panel)
    bpy.utils.unregister_class(boilerplate_operator)

if __name__ == "__main__":
    register()
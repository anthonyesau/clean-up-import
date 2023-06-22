import bpy

class CustomPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_custom_panel"
    bl_label = "Clean Up Import"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Clean Up Import"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("custom.merge_duplicate_materials", text="Merge Duplicate Materials")
        row = layout.row()
        row.operator("custom.merge_duplicate_images", text="Merge Duplicate Images")
        row = layout.row()
        row.operator("custom.delete_camera", text="Delete Camera(s) 'CINEMA_4D_Editor'")
        row = layout.row()
        row.operator("custom.delete_def_vw_lights", text="Delete default lights from VW")
        row = layout.row()
        row.operator("custom.clean_vw_img_names", text="Clean VW image names")
        row = layout.row()
        row.operator("custom.relink_packed_images", text="Relink Images")
        row = layout.row()
        row.operator("custom.relink_color_and_transparency_images", text="Relink Color and Transparency Images")
        row = layout.row()
        row.operator("custom.correct_gamma", text="Correct Gamma of Materials")


def register():
    bpy.utils.register_class(CustomPanel)

def unregister():
    bpy.utils.unregister_class(CustomPanel)


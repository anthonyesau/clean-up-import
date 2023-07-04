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
        row.operator("custom.connect_alpha", text="Connect alpha from Img node")
        row = layout.row()
        row.operator("custom.set_img_node_srgb", text="Set image nodes to sRGB")
        row = layout.row()
        row.operator("custom.set_alpha_blend_mode", text="Set alpha blend mode")
        row = layout.row()
        row.operator("custom.correct_gamma", text="Correct Gamma of Materials")
        row = layout.row()
        row.operator("custom.format_vw_area_lights", text="Format Area Lights")
        row = layout.row()
        row.operator("custom.dissolve_top_vw_empties", text="Dissolve top VW empties")
        row = layout.row()
        row.operator("custom.enable_auto_smooth", text="Enable Auto Smooth")
        row = layout.row()
        row.operator("object.resequence_names", text="Resequence Object Names")


def register():
    bpy.utils.register_class(CustomPanel)

def unregister():
    bpy.utils.unregister_class(CustomPanel)


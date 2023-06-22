import bpy

class CorrectGamma(bpy.types.Operator):
    bl_idname = "custom.correct_gamma"
    bl_label = "Correct gamma of colors for materials of selected objects."
    bl_description = "Correct gamma of colors for materials of selected objects."

    def execute(self, context):

        # create list of all materials applied to selected objects
        materialList = []
        for obj in bpy.context.selected_objects:
            for slot in obj.material_slots:
                if slot.material:
                    materialList.append(slot.material)

        # remove duplicates from material list
        materialList = list(set(materialList))

        # go through all materials in list and gamma correct the base color and viewport color
        for material in materialList:
            base_color = material.node_tree.nodes["Principled BSDF"].inputs[0].default_value
            for i in range(4):
                gamma_corrected_color_channel = base_color[i]**2.2
                material.node_tree.nodes["Principled BSDF"].inputs[0].default_value[i] = gamma_corrected_color_channel
                material.diffuse_color[i] = gamma_corrected_color_channel
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CorrectGamma)

def unregister():
    bpy.utils.unregister_class(CorrectGamma)

import bpy

# Only works on Principled BSDF shaders at the moment
# Does not do anything for glass or transparent shaders

class SetAlphaBlendModeOperator(bpy.types.Operator):
    bl_idname = "custom.set_alpha_blend_mode"
    bl_label = "Set alpha blend mode of transparent materials"
    bl_description = "Set alpha blend mode of transparent materials"

    def execute(self, context):
        # Find all materials with node connected to alpha input of Principled BSDF shader
        materials = [mat for mat in bpy.data.materials if mat.node_tree and mat.node_tree.nodes.get('Principled BSDF') and mat.node_tree.nodes['Principled BSDF'].inputs.get('Alpha') and mat.node_tree.nodes['Principled BSDF'].inputs['Alpha'].is_linked]

        # Set blend mode and shadow mode for each material
        for material in materials:
            material.blend_method = 'HASHED'
            material.shadow_method = 'HASHED'

        return {'FINISHED'}


def register():
    bpy.utils.register_class(SetAlphaBlendModeOperator)


def unregister():
    bpy.utils.unregister_class(SetAlphaBlendModeOperator)


if __name__ == "__main__":
    register()

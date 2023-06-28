import bpy

class ConnectAlphaOperator(bpy.types.Operator):
    bl_idname = "custom.connect_alpha"
    bl_label = "Connect Alpha"
    bl_description = "Finds the image texture node attached to base color and connects its alpha."
    
    @classmethod
    def poll(cls, context):
        return context.selected_objects != []

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            for slot in obj.material_slots:
                material = slot.material
                if material:
                    if material.node_tree.nodes.get("Principled BSDF") and material.node_tree.nodes["Principled BSDF"].inputs.get("Base Color"):
                        if material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].is_linked:
                            baseTexture = material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].links[0].from_node
                            alphaTexture = material.node_tree.nodes["Principled BSDF"].inputs.get("Alpha").links[0].from_node if material.node_tree.nodes["Principled BSDF"].inputs.get("Alpha") and material.node_tree.nodes["Principled BSDF"].inputs["Alpha"].is_linked else None
                                
                            if baseTexture.type == "TEX_IMAGE" and alphaTexture and alphaTexture.type == "TEX_IMAGE":
                                if baseTexture.image == alphaTexture.image and baseTexture.image.file_format == 'PNG':
                                    material.node_tree.links.new(material.node_tree.nodes["Principled BSDF"].inputs["Alpha"], alphaTexture.outputs["Alpha"])
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ConnectAlphaOperator)

def unregister():
    bpy.utils.unregister_class(ConnectAlphaOperator)
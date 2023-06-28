import bpy

class SetImgNodeSRGBOperator(bpy.types.Operator):
    bl_idname = "custom.set_img_node_srgb"
    bl_label = "Set image nodes in textures to sRGB."
    bl_description = "Set image nodes in textures to sRGB."

    # The beginnings of functionality to choose between processing all materials in the file
    # and limiting it to the materials of the selected objects is here
    # But it currently isn't fully implemented so it defaults to all materials
    # A checkbox UI element or some selection method is needed

    process_all_materials: bpy.props.BoolProperty(
        name="Process All Materials",
        description="Process all materials in the Blender file instead of just the selected objects.",
        default=True
    )

    def execute(self, context):
        if self.process_all_materials:
            # Loop over all materials in the Blender file
            for material in bpy.data.materials:
                if material.node_tree:
                    # Loop over each node in the material node tree
                    for node in material.node_tree.nodes:
                        # Check if the node is an image texture node
                        if node.type == "TEX_IMAGE":
                            # Set the color space to sRGB
                            node.image.colorspace_settings.name = "sRGB"
        else:
            # Get the selected objects
            selected_objects = bpy.context.selected_objects

            # Loop over each selected object
            for obj in selected_objects:
                # Loop over each material slot of the object
                for material_slot in obj.material_slots:
                    # Get the material of the material slot
                    material = material_slot.material

                    if material.node_tree:
                        # Loop over each node in the material node tree
                        for node in material.node_tree.nodes:
                            # Check if the node is an image texture node
                            if node.type == "TEX_IMAGE":
                                # Set the color space to sRGB
                                node.image.colorspace_settings.name = "sRGB"

        print("Color space changed to sRGB for all image texture nodes.")

        return {'FINISHED'}

def register():
    bpy.utils.register_class(SetImgNodeSRGBOperator)
    

def unregister():
    bpy.utils.unregister_class(SetImgNodeSRGBOperator)
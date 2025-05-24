import bpy

# Iterate through all the materials in the scene
for material in bpy.data.materials:
    # Check if the material has a node tree
    if material.node_tree:
        # Get the material output node
        material_output = material.node_tree.nodes.get('Material Output')
        
        # Get all the nodes in the material node tree
        nodes = material.node_tree.nodes
        # Iterate through all the nodes
        for node in nodes:
            # Check if the node is an image texture node
            if node.type == 'TEX_IMAGE':
                # Check if the image file path contains "Model graphics"
                if "Model graphics" in node.image.filepath:
                    # Get the Principled BSDF node connected to the image texture
                    principled_bsdf = node.outputs['Color'].links[0].to_node
                    # Set the specular value to 0.5
                    principled_bsdf.inputs['Specular'].default_value = 0.5
                    # Set the roughness value to 0.25
                    principled_bsdf.inputs['Roughness'].default_value = 0.25
                    # Break the loop to skip to the next material
                    break
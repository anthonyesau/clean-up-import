import bpy

class ExtractVWDesignLayers(bpy.types.Operator):
    """Reorganize imported Vectorworks geometry"""
    bl_idname = "custom.extract_vw_design_layers"
    bl_label = "Extract VW Design Layers"

    def execute(self, context):
        def clearParent(child):    
            # Save the transform matrix before de-parenting
            matrixcopy = child.matrix_world.copy()
            
            # Clear the parent
            child.parent = None
            
            # Restore child's location / rotation / scale
            child.matrix_world = matrixcopy

        def move_to_collection(obj, target_collection):
            # Unlink the object from its current collections
            for coll in obj.users_collection:
                coll.objects.unlink(obj)

            # Link the object to the target collection
            target_collection.objects.link(obj)

            # Recursively move all children to the same target collection
            for child in obj.children:
                move_to_collection(child, target_collection)

        def move_children_to_collection(obj, parent_collection):
            # Check if the object is an empty
            if obj.type == 'EMPTY':
                # Create a new collection with the same name as the empty if it doesn't exist
                collection_name = obj.name
                new_collection = bpy.data.collections.get(collection_name)
                if not new_collection:
                    new_collection = bpy.data.collections.new(collection_name)
                    parent_collection.children.link(new_collection)
                
                # Iterate through the children of the empty
                for child in obj.children:
                    # Unparent the child while preserving its transforms
                    clearParent(child)

                    move_to_collection(child, new_collection)

                # Remove the empty from the scene
                bpy.data.objects.remove(obj, do_unlink=True)

        # Find all objects with names starting with "Vectorworks_"
        vwScenes = [obj for obj in bpy.data.objects if obj.type == 'EMPTY' and obj.name.startswith("Vectorworks_")]
        
        # Loop through all the children of the vwScenes empties and clear parent and keep transforms
        for individualVWScene in vwScenes:
            # Assume the first collection of the Vectorworks scene is the parent collection
            parent_collection = individualVWScene.users_collection[0] if individualVWScene.users_collection else bpy.context.scene.collection

            for objectGrouping in individualVWScene.children:
                if objectGrouping.name == "Geometry":
                    for designLayer in objectGrouping.children:
                        move_children_to_collection(designLayer, parent_collection)
                    bpy.data.objects.remove(objectGrouping, do_unlink=True)
                else:
                    move_children_to_collection(objectGrouping, parent_collection)
            bpy.data.objects.remove(individualVWScene, do_unlink=True)
            
        bpy.ops.ed.undo_push()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ExtractVWDesignLayers)

def unregister():
    bpy.utils.unregister_class(ExtractVWDesignLayers)

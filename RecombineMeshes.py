import bpy

class RecombineMeshes(bpy.types.Operator):
    """Combine sibling meshes that are all children of the same empty parent"""
    bl_idname = "custom.recombine_meshes"
    bl_label = "RecombineMeshes"

    def execute(self, context):

        def join_meshes_under_empty(empty):
            # Check if all children of the empty are mesh objects
            mesh_children = [child for child in empty.children if child.type == 'MESH']
            if len(mesh_children) != len(empty.children):
                # Skip this empty if there are non-mesh children or another empty
                return

            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')

            # Select all mesh children
            for child in mesh_children:
                child.select_set(True)

            # Set the first mesh child as the active object
            bpy.context.view_layer.objects.active = mesh_children[0]

            # Join the selected mesh objects
            bpy.ops.object.join()

            # The joined object is now a single mesh.
            joined_mesh = bpy.context.active_object
            
            # Rename the new joined mesh
            joined_mesh.name = empty.name + "_joined"
            
            # Set the joined_mesh mesh data-block name to match joined_mesh.name
            joined_mesh.data.name = joined_mesh.name



            # Store the original world matrix
            original_matrix_world = joined_mesh.matrix_world.copy()

            # Clear the current parent while keeping transformation
            joined_mesh.parent = None
            joined_mesh.matrix_parent_inverse.identity()

            # Set the parent to the empty's parent
            joined_mesh.parent = empty.parent

            # Adjust the object's world matrix to match the original matrix
            joined_mesh.matrix_world = original_matrix_world

            # Delete the empty
            bpy.data.objects.remove(empty, do_unlink=True)

        # Get the selected objects to operate on
        selected_objects = bpy.context.selected_objects

        # Switch to Object Mode
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT')

        # Create a list to fill with the empty objects
        empties = []

        for obj in selected_objects:
            if obj.type == 'EMPTY':
                # Check if all children of the empty are mesh objects
                mesh_chil = [child for child in obj.children if child.type == 'MESH']
                if len(mesh_chil) == len(obj.children):
                    empties.append(obj)

        for empty in empties:
            join_meshes_under_empty(empty)

        bpy.ops.ed.undo_push() # Try to enable undo for this operation. Not sure it works...
        return {'FINISHED'}

def register():
    bpy.utils.register_class(RecombineMeshes)

def unregister():
    bpy.utils.unregister_class(RecombineMeshes)

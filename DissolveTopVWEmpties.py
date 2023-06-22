import bpy

class DissolveTopVWEmpties(bpy.types.Operator):
    """Clear the parent and keep the transform for all objects with name starting with 'Vectorworks_'"""
    bl_idname = "custom.dissolve_top_vw_empties"
    bl_label = "Dissolve top VW empties"

    def execute(self, context):
        def clearParent(child):    
            # Save the transform matrix before de-parenting
            matrixcopy = child.matrix_world.copy()
            
            # Clear the parent
            child.parent = None
            
            # Restore childs location / rotation / scale
            child.matrix_world = matrixcopy
        
        # find all objects with names starting with "Vectorworks_"
        empties = [obj for obj in bpy.data.objects if obj.type == 'EMPTY' and obj.name.startswith("Vectorworks_")]
        
        # loop through all the children of the empties and clear parent and keep transforms
        for empty in empties:
            for child in empty.children:
                clearParent(child)
                if child.type == "EMPTY":
                    for childChild in child.children:
                        clearParent(childChild)
                    # remove the empty object
                    bpy.data.objects.remove(child, do_unlink=True)
            
            # remove the empty object
            bpy.data.objects.remove(empty, do_unlink=True)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(DissolveTopVWEmpties)

def unregister():
    bpy.utils.unregister_class(DissolveTopVWEmpties)

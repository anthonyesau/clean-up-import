import bpy

class DeleteVWLights(bpy.types.Operator):
    bl_idname = "custom.delete_def_vw_lights"
    bl_label = "Delete default lights from VW"
    bl_description = "Delete default lights from VW."

    def execute(self, context):
        # Search for objects with names starting with "Ambient_Omni_Light"
        light_names = [obj.name for obj in bpy.data.objects if obj.type == 'LIGHT' and obj.name.startswith("Ambient_Omni_Light")]

        # Remove all objects with the found names
        for light_name in light_names:
            bpy.data.objects.remove(bpy.data.objects[light_name], do_unlink=True)

        # Search for objects with names starting with "Default_Infinite_Light"
        light_names = [obj.name for obj in bpy.data.objects if obj.type == 'LIGHT' and obj.name.startswith("Default_Infinite_Light")]

        # Remove all objects with the found names
        for light_name in light_names:
            bpy.data.objects.remove(bpy.data.objects[light_name], do_unlink=True)
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(DeleteVWLights)

def unregister():
    bpy.utils.unregister_class(DeleteVWLights)
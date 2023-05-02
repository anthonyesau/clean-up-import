import bpy

bl_info = {
   "name": "Clean Up Import",
   "version": (0, 4),
   "blender": (3, 5, 0)
}

class CustomPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_custom_panel"
    bl_label = "Clean Up Import"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Clean Up Import"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("custom.merge_duplicate_textures", text="Merge Duplicate Textures")
        row = layout.row()
        row.operator("custom.delete_camera", text="Delete Camera(s) 'CINEMA_4D_Editor'")
        row = layout.row()
        row.operator("custom.delete_vw_lights", text="Delete generic lights imported from VW")

class MergeDuplicateTexturesOperator(bpy.types.Operator):
    bl_idname = "custom.merge_duplicate_textures"
    bl_label = "Merge Duplicate Textures"
    bl_description = "Merge texName, texName.001, texName.002, et cetera."

    def execute(self, context):
        print("----- Merge Duplicate Textures -----")

        # make a list of all material names
        mat_list = [x.name for x in bpy.data.materials]

        # go through all materials
        for mat in bpy.data.materials:
            # check if last three characters are numbers
            if mat.name[-3:].isnumeric():

                # check if material without number extension exists
                if mat.name[:-4] in mat_list:

                    # find indices of numbered material and material w/o number
                    index_clean = mat_list.index(mat.name[:-4])
                    index_wrong = mat_list.index(mat.name)

                    # remap the duplicate to the one without number extension            
                    mat.user_remap(bpy.data.materials[index_clean].id_data)

        return {'FINISHED'}

class DeleteCameraOperator(bpy.types.Operator):
    bl_idname = "custom.delete_camera"
    bl_label = "Delete Camera(s) 'CINEMA_4D_Editor'"
    bl_description = "Delete Camera(s) 'CINEMA_4D_Editor'."

    def execute(self, context):
        print("----- Delete Camera(s) with Object Name 'CINEMA_4D_Editor' -----")

        # find all camera objects with the given name pattern
        camera_objs = [obj for obj in bpy.data.objects if obj.type == 'CAMERA' and obj.name.startswith("CINEMA_4D_Editor")]

        # delete each camera object if it exists
        for camera_obj in camera_objs:
            bpy.data.objects.remove(camera_obj, do_unlink=True)

        return {'FINISHED'}

class DeleteVWLights(bpy.types.Operator):
    bl_idname = "custom.delete_vw_lights"
    bl_label = "Delete generic lights imported from VW"
    bl_description = "Delete generic lights imported from VW."

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
    bpy.utils.register_class(CustomPanel)
    bpy.utils.register_class(MergeDuplicateTexturesOperator)
    bpy.utils.register_class(DeleteCameraOperator)
    bpy.utils.register_class(DeleteVWLights)

def unregister():
    bpy.utils.unregister_class(CustomPanel)
    bpy.utils.unregister_class(MergeDuplicateTexturesOperator)
    bpy.utils.unregister_class(DeleteCameraOperator)
    bpy.utils.register_class(DeleteVWLights)

if __name__ == "__main__":
    register()

import bpy
import os
from bpy_extras.io_utils import ImportHelper 
from bpy.types import Operator
from bpy.props import CollectionProperty
from bpy.props import StringProperty, BoolProperty

bl_info = {
   "name": "Clean Up Import",
   "version": (0, 8),
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
        row.operator("custom.delete_def_vw_lights", text="Delete default lights from VW")
        row = layout.row()
        row.operator("custom.clean_vw_img_names", text="Clean VW image names")
        row = layout.row()
        row.operator("custom.open_filebrowser", text="Remove Pack then Link")
        row = layout.row()
        row.operator("custom.correct_gamma", text="Correct Gamma of Textures")
        

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

class CleanVWImageNames(bpy.types.Operator):
    bl_idname = "custom.clean_vw_img_names"
    bl_label = "Clean up Vectorworks Image Names."
    bl_description = "Clean up Vectorworks Image Names."

    # ----- Clean up Vectorworks Image Names -----

    # TODO: 

    def execute(self, context):

        print("----- Clean up Vectorworks image names -----")

        # Create a list of prefixes to clean up
        vw_tex_substrings = ["NNA#3_", "NNA#2_", " Color", ".001"]

        for image in bpy.data.images:

            # replace instances of the substrings in image file names and paths
            for vw_tex_substring in vw_tex_substrings:
                
                # changing filepath_raw and filepath are not ultimately needed
                # so they are not run in case the replace command goes awry on the full file path
                
                # print(image.filepath_raw)
                # image.filepath_raw = image.filepath_raw.replace(vw_tex_substring, "")
                # print(image.filepath_raw)
                
                # print(image.filepath)
                # image.filepath = image.filepath.replace(vw_tex_substring, "")
                # print(image.filepath)
                
                print(image.name)
                image.name = image.name.replace(vw_tex_substring, "")
                print(image.name)
        
        return {'FINISHED'}


class RemovePack_OpenFilebrowser(Operator, ImportHelper): 
    bl_idname = "custom.open_filebrowser" 
    bl_label = "Open the file browser" 
    bl_description = "Swap the selected images for packed images."
    
    filter_glob: StringProperty(
        default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp',
        options={'HIDDEN'}
    )
    
    files : CollectionProperty(type=bpy.types.PropertyGroup) # Stores properties
    
    def execute(self, context): 
        
        """Do something with the selected file(s)."""
                        
        directory = os.path.dirname(self.filepath)
        externalFileNames = []
        externalFileNamesWithExtension = []
        for f in self.files:
            print(os.path.join(directory, f.name)) #get filepath properties from collection pointer
            externalFileNamesWithExtension.append(f.name)
            externalFileNames.append(os.path.splitext(f.name)[0])

        
        # Loop through Blender's images
        for image in bpy.data.images:
            # Check if image filename (w/o extension) is in the directory
            if os.path.splitext(image.name)[0] in externalFileNames:
                # Check if exact match of extension exists
                if image.name in externalFileNamesWithExtension:
                    index = externalFileNamesWithExtension.index(image.name)
                else:
                    index = externalFileNames.index(os.path.splitext(image.name)[0])
                fileName = externalFileNamesWithExtension[index]
                image.filepath = os.path.join(directory, fileName)
                image.filepath_raw = os.path.join(directory, fileName)
                image.name = fileName
                if image.packed_file:  
                    # Remove pack
                    image.unpack(method='REMOVE')
                image.update()
                
                
        return {'FINISHED'}


class CorrectGamma(bpy.types.Operator):
    bl_idname = "custom.correct_gamma"
    bl_label = "Correct gamma of colors for textures of selected objects."
    bl_description = "Correct gamma of colors for textures of selected objects."

    def execute(self, context):

        for obj in bpy.context.selected_objects:
            for slot in obj.material_slots:
                if slot.material:
                    base_color = slot.material.node_tree.nodes["Principled BSDF"].inputs[0].default_value
                    for i in range(4):
                        gamma_corrected_color_channel = base_color[i]**2.2
                        slot.material.node_tree.nodes["Principled BSDF"].inputs[0].default_value[i] = gamma_corrected_color_channel
                        slot.material.diffuse_color[i] = gamma_corrected_color_channel
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CustomPanel)
    bpy.utils.register_class(MergeDuplicateTexturesOperator)
    bpy.utils.register_class(DeleteCameraOperator)
    bpy.utils.register_class(DeleteVWLights)
    bpy.utils.register_class(CleanVWImageNames)
    bpy.utils.register_class(RemovePack_OpenFilebrowser)
    bpy.utils.register_class(CorrectGamma)

def unregister():
    bpy.utils.unregister_class(CustomPanel)
    bpy.utils.unregister_class(MergeDuplicateTexturesOperator)
    bpy.utils.unregister_class(DeleteCameraOperator)
    bpy.utils.unregister_class(DeleteVWLights)
    bpy.utils.unregister_class(CleanVWImageNames)
    bpy.utils.unregister_class(RemovePack_OpenFilebrowser)
    bpy.utils.unregister_class(CorrectGamma)

if __name__ == "__main__":
    register()

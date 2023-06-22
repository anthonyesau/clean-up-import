import bpy

class CleanVWImageNames(bpy.types.Operator):
    bl_idname = "custom.clean_vw_img_names"
    bl_label = "Clean up Vectorworks Image Names."
    bl_description = "Clean up Vectorworks image names like NNA#2_."

    # ----- Clean up Vectorworks Image Names -----

    def execute(self, context):

        print("----- Clean up Vectorworks image names -----")

        # Create a list of prefixes to clean up
        vw_tex_substrings = ["NNA#3_", "NNA#2_"]

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


def register():
    bpy.utils.register_class(CleanVWImageNames)

def unregister():
    bpy.utils.unregister_class(CleanVWImageNames)        
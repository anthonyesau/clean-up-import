import bpy

class MergeDuplicateMaterialsOperator(bpy.types.Operator):
    bl_idname = "custom.merge_duplicate_materials"
    bl_label = "Merge Duplicate Materials"
    bl_description = "Merge texName.001, texName.002, et cetera to texName."

    def execute(self, context):
        print("----- Merge Duplicate Materials -----")

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
                else:
                    # change image name to index of image without number extension
                    mat.name = mat.name[:-4]

        return {'FINISHED'}

def register():
    bpy.utils.register_class(MergeDuplicateMaterialsOperator)

def unregister():
    bpy.utils.unregister_class(MergeDuplicateMaterialsOperator)

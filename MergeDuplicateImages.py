import bpy

class MergeDuplicateImagesOperator(bpy.types.Operator):
    bl_idname = "custom.merge_duplicate_images"
    bl_label = "Merge Duplicate Images"
    bl_description = "Merge imageName.001, imageName.002, et cetera to imageName."

    def execute(self, context):
        print("----- Merge Duplicate Images -----")

        # make a list of all image names
        img_list = [x.name for x in bpy.data.images]

        # go through all images
        for img in bpy.data.images:
            # check if last three characters are numbers
            if img.name[-3:].isnumeric():
                # Display alert popup

                # check if image without number extension exists
                if img.name[:-4] in img_list:
                    
                    # find indices of numbered image and image w/o number
                    index_clean = img_list.index(img.name[:-4])
                    index_wrong = img_list.index(img.name)

                    # remap the duplicate to the one without number extension            
                    img.user_remap(bpy.data.images[index_clean].id_data)
                
                else:
                    # change image name to index of image without number extension
                    img.name = img.name[:-4]

        return {'FINISHED'}

def register():
    bpy.utils.register_class(MergeDuplicateImagesOperator)

def unregister():
    bpy.utils.unregister_class(MergeDuplicateImagesOperator)
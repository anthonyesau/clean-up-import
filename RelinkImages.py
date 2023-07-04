import bpy
from bpy.props import StringProperty, CollectionProperty, EnumProperty
from bpy_extras.io_utils import ImportHelper
import os

class RelinkImagesWithSuffixResolverOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "custom.relink_images_with_suffix_resolver" 
    bl_label = "Relink Images"
    bl_description = "Select files on disk to relink to image assets within Blender. Resolves additional suffixes assets may have."
    
    filter_glob: StringProperty(
        default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp',
        options={'HIDDEN'}
    )
    
    files: CollectionProperty(type=bpy.types.PropertyGroup)  # Stores properties
    
    rel_path_options = [
        ("RELATIVE", "Relative", ""),
        ("ABSOLUTE", "Absolute", "")
    ]
    
    rel_path: EnumProperty(
        items=rel_path_options,
        name="File Path",
        description="Choose whether to use relative or absolute file paths",
        default="RELATIVE"
    )
     
    def execute(self, context): 
        """Do something with the selected file(s)."""
        directory = os.path.dirname(self.filepath)
        externalFileNames = []
        externalFileNamesWithExtension = []
        externalFileNamesBeginnings = []
        
        for f in self.files:
            print(os.path.join(directory, f.name)) #get filepath properties from collection pointer
            externalFileNamesWithExtension.append(f.name)
            externalFileNames.append(os.path.splitext(f.name)[0])
            externalFileNamesBeginnings.append(f.name.split(' ', 1)[0])

        suffixes = None
        # suffixes = [" Color", " Transparency"]

        # Loop through Blender's images
        for image in bpy.data.images:
            # Establish starting values for variables
            index = None
            internalFileNameTrimmed = None
            internalFileNameWithExtension = os.path.basename(image.filepath)
            internalFileName = os.path.splitext(internalFileNameWithExtension)[0]
            # Identify the beginning of the file name (see elif around line 78)
            # internalFileNameBeginning = internalFileName.split(' ', 1)[0]

            # If specific suffixes are not defined, try to match any suffixes
            if suffixes == None:
                try:
                    internalFileNameTrimmed = internalFileName[:internalFileName.rfind(' ')]
                except ValueError:
                    internalFileNameTrimmed = None
            else: 
                for suffix in suffixes:
                    if internalFileName.endswith(suffix):
                        internalFileNameTrimmed = internalFileName[:-len(suffix)]

            # Check if image filename (w/o extension) is in the directory
            if internalFileName in externalFileNames:
                # Check if exact match of extension exists
                if image.name in externalFileNamesWithExtension:
                    index = externalFileNamesWithExtension.index(image.name)
                else:
                    index = externalFileNames.index(internalFileName)
            # Check if image filename (w/o suffix) is in the directory
            elif internalFileNameTrimmed != None and internalFileNameTrimmed in externalFileNames:
                index = externalFileNames.index(internalFileNameTrimmed)
            # Check if the beginning of the file name matches
            # elif internalFileNameBeginning in externalFileNamesBeginnings:
            #     index = externalFileNamesBeginnings.index(internalFileNameBeginning)

            if index != None:
                fileName = externalFileNamesWithExtension[index]
                filepath = os.path.join(directory, fileName)

                if self.rel_path == "RELATIVE":
                    filepath = bpy.path.relpath(filepath)

                # If the external file has already been relinked, use that same image asset
                try:
                    # Check if the image exists
                    existingImageAsset = bpy.data.images[fileName[:64]] # filenames are limited to 64 characters
                    if existingImageAsset.filepath == filepath:
                        image.user_remap(existingImageAsset.id_data)

                # Relink the internal image to the external image
                except KeyError:
                    image.filepath = filepath
                    image.filepath_raw = filepath
                        
                    image.name = fileName
                    if image.packed_file:
                        # Remove pack
                        image.unpack(method='REMOVE')
                image.update()

        return {'FINISHED'}

class AEUtilzPanel(bpy.types.Panel):
    bl_label = "Image Asset MGMT"
    bl_idname = "VIEW3D_PT_clean_up_import"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AE Utilz"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("custom.relink_images_with_suffix_resolver", text="Relink Images with Suffix Resolver")

def register():
    bpy.utils.register_class(RelinkImagesWithSuffixResolverOperator)
    bpy.utils.register_class(AEUtilzPanel)


def unregister():
    bpy.utils.unregister_class(RelinkImagesWithSuffixResolverOperator)
    bpy.utils.unregister_class(AEUtilzPanel)


if __name__ == "__main__":
    register()
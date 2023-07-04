import bpy
from bpy.props import StringProperty, CollectionProperty, EnumProperty
from bpy_extras.io_utils import ImportHelper
import os

class RelinkColorAndTransparencyImages(bpy.types.Operator, ImportHelper):
    bl_idname = "custom.relink_color_and_transparency_images" 
    bl_label = "Relink Color and Transparency Images"
    bl_description = "Same as Relink Images plus handling of separate color and transparent images that should be relinked to a single file."
    
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
            internalFileNameBeginning = internalFileName.split(' ', 1)[0]

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
            elif internalFileNameBeginning in externalFileNamesBeginnings:
                index = externalFileNamesBeginnings.index(internalFileNameBeginning)

            if index != None:
                fileName = externalFileNamesWithExtension[index]
                filepath = os.path.join(directory, fileName)
                
                if self.rel_path == "RELATIVE":
                    rel_filepath = bpy.path.relpath(filepath)
                    image.filepath = rel_filepath
                    image.filepath_raw = rel_filepath
                else:
                    image.filepath = filepath
                    image.filepath_raw = filepath
                    
                image.name = fileName
                if image.packed_file:
                    # Remove pack
                    image.unpack(method='REMOVE')
                image.update()

        return {'FINISHED'}

#-------------------------------------------------------------------------------
class AEUtilzPanel(bpy.types.Panel):
    bl_label = "Image Asset MGMT"
    bl_idname = "VIEW3D_PT_clean_up_import"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AE Utilz"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("custom.relink_color_and_transparency_images", text="Relink Color and Transparency Images")

#-------------------------------------------------------------------------------
def register():
    bpy.utils.register_class(RelinkColorAndTransparencyImages)
    bpy.utils.register_class(CleanUpImportPanel)


def unregister():
    bpy.utils.unregister_class(RelinkColorAndTransparencyImages)
    bpy.utils.unregister_class(CleanUpImportPanel)


if __name__ == "__main__":
    register()
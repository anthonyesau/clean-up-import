import bpy
from bpy.props import StringProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper
import os

class RelinkPackedImages(bpy.types.Operator, ImportHelper): 
    bl_idname = "custom.relink_packed_images" 
    bl_label = "" 
    bl_description = "Select image files to relink existing images (packed or otherwise)."
    
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

def register():
    bpy.utils.register_class(RelinkPackedImages)

def unregister():
    bpy.utils.unregister_class(RelinkPackedImages)

import bpy
from bpy.props import StringProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper
import os


class RelinkColorAndTransparencyImages(bpy.types.Operator, ImportHelper): 
    bl_idname = "custom.relink_color_and_transparency_images" 
    bl_label = "" 
    bl_description = "Same as Relink Images plus handling of separate color and transparent images that should be relinked to a single file."
    
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
        externalFileNamesBeginnings = []
        for f in self.files:
            print(os.path.join(directory, f.name)) #get filepath properties from collection pointer
            externalFileNamesWithExtension.append(f.name)
            externalFileNames.append(os.path.splitext(f.name)[0])
            externalFileNamesBeginnings.append(f.name.split(' ', 1)[0])

        suffixes = None
        # suffixes = [" Color", " Transparency"]

        # Get or create a new text block
        text_block = bpy.data.texts.get("MyTextBlock")
        if text_block is None:
            text_block = bpy.data.texts.new("MyTextBlock")
        else:
            text_block.clear()

        # Loop through Blender's images
        for image in bpy.data.images:
            
            # Establish starting values for variables
            index = None
            internalFileNameTrimmed = None
            internalFileNameWithExtension = os.path.basename(image.filepath)
            internalFileName = os.path.splitext(internalFileNameWithExtension)[0]
            internalFileNameBeginning = internalFileName.split(' ', 1)[0]

            # Debug output
            # #----------------------
            # # Set the contents of the text block
            # message = "internalFileName: " + str(internalFileName)
            # message += "\ninternalFileNameTrimmed: " + str(internalFileNameTrimmed)
            # message += "\ninternalFileNameBeginning: " + str(internalFileNameBeginning)
            # #-----------------------

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
                    # Debug output
                    # message += "\nMatch of externalFileNamesWithExtension: " + internalFileName
                    # message += "\nExternal image name: " + image.name
                else:
                    index = externalFileNames.index(internalFileName)
                    # Debug output
                    # message += "\nMatch of internalFileName: " + internalFileName
                    # message += "\nExternal image name: " + image.name

            # Check if image filename (w/o suffix) is in the directory
            elif internalFileNameTrimmed != None and internalFileNameTrimmed in externalFileNames:
                index = externalFileNames.index(internalFileNameTrimmed)

                # message += "\nMatch of internalFileNameTrimmed: " + internalFileNameTrimmed
                # message += "\nExternal image name: " + image.name

            elif internalFileNameBeginning in externalFileNamesBeginnings:
                index = externalFileNamesBeginnings.index(internalFileNameBeginning)
                # Debug output
                # message += "\nMatch of internalFileNameBeginning: " + internalFileNameBeginning
                # message += "\nExternal image name: " + image.name
            
            # Debug output
            # #----------------------
            # existing_contents = text_block.as_string()
            # text_block.from_string(existing_contents + "\n" + "\n" + message)
            # #----------------------

            if index != None: 
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
    bpy.utils.register_class(RelinkColorAndTransparencyImages)

def unregister():
    bpy.utils.unregister_class(RelinkColorAndTransparencyImages)

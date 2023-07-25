import bpy
import os
from bpy.types import Operator
from bpy.props import StringProperty

class BatchRenameImagesOperator(Operator):
    bl_label = "Batch rename images..."
    bl_idname = "object.replace_string"
    bl_description = "Find and replace text within image names and filenames. Part of AE Utilz."
    
    replace_src: StringProperty(name="Find", default="old_string")
    replace_dst: StringProperty(name="Replace with", default="new_string")
    
    def execute(self, context):
        # Loop through all images
        for image in bpy.data.images:
            # Get the filename from the full filepath
            file_name = os.path.basename(image.filepath)
            
            # Replace string in Image.name
            if self.replace_src in image.name:
                image.name = image.name.replace(self.replace_src, self.replace_dst)
            
            # Replace string in Image.filepath
            if self.replace_src in file_name:
                file_name = file_name.replace(self.replace_src, self.replace_dst)
                image.filepath = os.path.join(os.path.dirname(image.filepath), file_name)
            
            # Replace string in Image.filepath_raw
            if self.replace_src in file_name:
                file_name = file_name.replace(self.replace_src, self.replace_dst)
                image.filepath_raw = os.path.join(os.path.dirname(image.filepath_raw), file_name)
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "replace_src")
        layout.prop(self, "replace_dst")

def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(BatchRenameImagesOperator.bl_idname)

def register():
    bpy.utils.register_class(BatchRenameImagesOperator)
    bpy.types.TOPBAR_MT_edit.append(menu_func)

def unregister():
    bpy.utils.unregister_class(BatchRenameImagesOperator)
    bpy.types.TOPBAR_MT_edit.remove(menu_func)

if __name__ == "__main__":
    register()
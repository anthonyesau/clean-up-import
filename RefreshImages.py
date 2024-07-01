import bpy

# Define the operator to refresh linked images
class refresh_linked_images(bpy.types.Operator):
    """Update linked images to reflect the latest files on disk"""
    bl_idname = "object.refresh_linked_images"
    bl_label = "Refresh Linked Images"

    def execute(self, context):
        # Loop through all images in the Blender file
        for img in bpy.data.images:
            # Check if the image is not packed
            if not img.packed_file:
                # Reload the image
                img.reload()
                print(f'Reloaded image: {img.filepath}')
            else:
                print(f'Image is packed and will not be reloaded: {img.name}')
        return {'FINISHED'}

class refresh_linked_images_panel(bpy.types.Panel):
    """Creates a Panel in the AE Utilz sidebar"""
    bl_idname = "OBJECT_PT_refresh_images_panel"
    bl_label = "Refresh Linked Images"
    bl_description = "Reload all non-packed images"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AE Utilz"
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.operator("object.refresh_linked_images", text="Refresh Linked Images")

def register():
    bpy.utils.register_class(refresh_linked_images)
    bpy.utils.register_class(refresh_linked_images_panel)

def unregister():
    bpy.utils.unregister_class(refresh_linked_images)
    bpy.utils.unregister_class(refresh_linked_images_panel)

if __name__ == "__main__":
    register()

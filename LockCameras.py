import bpy

# Toggle function to lock/unlock camera properties
def toggle_camera_lock(self, context):
    # Get all camera objects in the scene
    cameras = [obj for obj in bpy.context.scene.objects if obj.type == 'CAMERA']

    # Loop through each camera object
    for camera in cameras:
        # Toggle the lock properties
        camera.lock_location[0] = not camera.lock_location[0]
        camera.lock_location[1] = not camera.lock_location[1]
        camera.lock_location[2] = not camera.lock_location[2]
        camera.lock_rotation[0] = not camera.lock_rotation[0]
        camera.lock_rotation[1] = not camera.lock_rotation[1]
        camera.lock_rotation[2] = not camera.lock_rotation[2]
        camera.lock_scale[0] = not camera.lock_scale[0]
        camera.lock_scale[1] = not camera.lock_scale[1]
        camera.lock_scale[2] = not camera.lock_scale[2]

# Operator class for the button
class CAMERA_OT_lock_toggle(bpy.types.Operator):
    bl_idname = "object.camera_lock_toggle"
    bl_label = "Toggle Camera Lock"
    
    def execute(self, context):
        toggle_camera_lock(self, context)
        return {'FINISHED'}

# Panel class to display the button in the 3D viewport
class CAMERA_PT_lock_toggle_panel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_camera_lock_toggle_panel"
    bl_label = "Camera Lock Toggle"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Add the toggle button
        layout.operator("object.camera_lock_toggle", text="Toggle Lock")

# Register the operator and panel classes
def register():
    bpy.utils.register_class(CAMERA_OT_lock_toggle)
    bpy.utils.register_class(CAMERA_PT_lock_toggle_panel)

def unregister():
    bpy.utils.unregister_class(CAMERA_OT_lock_toggle)
    bpy.utils.unregister_class(CAMERA_PT_lock_toggle_panel)

# Main function to run the script
if __name__ == "__main__":
    register()
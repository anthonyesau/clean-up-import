import bpy

class DeleteVWCameraOperator(bpy.types.Operator):
    bl_idname = "custom.delete_camera"
    bl_label = "Delete Camera(s) 'CINEMA_4D_Editor'"
    bl_description = "Delete Camera(s) 'CINEMA_4D_Editor'."

    def execute(self, context):
        print("----- Delete Camera(s) with Object Name 'CINEMA_4D_Editor' -----")

        # find all camera objects with the given name pattern
        camera_objs = [obj for obj in bpy.data.objects if obj.type == 'CAMERA' and obj.name.startswith("CINEMA_4D_Editor")]

        # delete each camera object if it exists
        for camera_obj in camera_objs:
            bpy.data.objects.remove(camera_obj, do_unlink=True)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(DeleteVWCameraOperator)

def unregister():
    bpy.utils.unregister_class(DeleteVWCameraOperator)

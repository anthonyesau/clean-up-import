import bpy

class EnableAutoSmooth(bpy.types.Operator):
    bl_idname = "custom.enable_auto_smooth"
    bl_label = "Enable Auto Smooth"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Get all selected mesh objects
        selected_objects = context.selected_objects
        mesh_objects = [obj for obj in selected_objects if obj.type == 'MESH']

        # Enable use_auto_smooth for each mesh object
        for obj in mesh_objects:
            context.view_layer.objects.active = obj
            obj.data.use_auto_smooth = True
            
        return {'FINISHED'}

def register():
    bpy.utils.register_class(EnableAutoSmooth)

def unregister():
    bpy.utils.unregister_class(EnableAutoSmooth)

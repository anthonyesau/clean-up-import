import bpy
import re

class ResequenceObjectNames(bpy.types.Operator):
    bl_idname = "object.resequence_names"
    bl_label = "Resequence Object Names"
    bl_description = "Fixes sequential numbering of names for selected objects."

    @classmethod
    def poll(cls, context):
        return context.selected_objects != []

    def execute(self, context):
        def get_suffix(text):
            match = re.search(r'\d+(.\d+)?$', text)
            return float(match.group()) if match else -1

        selected_objs = bpy.context.selected_objects
        obj_names = [obj.name for obj in selected_objs]

        temp_suffix = "_temp"
        for obj in selected_objs:
            obj.name += temp_suffix

        obj_names.sort(key=get_suffix)

        for i in range(len(obj_names)):
            obj = bpy.data.objects[obj_names[i] + temp_suffix]
            suffix = str(i+1)
            obj_names[i] = re.sub(r'\d+(.\d+)?$', suffix, obj_names[i])
            new_name = re.sub(r'\d+(.\d+)?$', suffix, obj_names[i])
            obj.name = new_name
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ResequenceObjectNames)

def unregister():
    bpy.utils.unregister_class(ResequenceObjectNames)

if __name__ == "__main__":
    register()
    
# To use the operator, select the objects you want to re-sequence and run it from the "Object" menu or the search bar.

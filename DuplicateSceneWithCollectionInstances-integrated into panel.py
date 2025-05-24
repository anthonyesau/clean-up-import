import bpy


def create_scene_with_collections(self, context):
    # Store the current scene and active collection
    current_scene = bpy.context.scene
    active_collection = bpy.context.collection

    # Create a new scene and copy settings of the current scene
    new_scene = bpy.data.scenes.new(name="NewScene")
    new_scene.render.image_settings.file_format = current_scene.render.image_settings.file_format 
    new_scene.render.resolution_x = current_scene.render.resolution_x 
    new_scene.render.resolution_y = current_scene.render.resolution_y 

    # Loop through all collections
    for collection in bpy.data.collections:
        # Skip the active collection
        if collection is not active_collection:
            # Create an instance of the collection in the NewScene
            instance = new_scene.collection.children.link(collection.copy())
            instance.instance_type = 'COLLECTION'
        else:
            # # Duplicate and link the active collection as a linked duplicate
            # link_collection = bpy.data.collections.new(name=active_collection.name + "_Link")
            # new_scene.collection.children.link(link_collection)
            # for obj in active_collection.objects:
            #     link_collection.objects.link(obj)

class AddCollectionSceneOperator(bpy.types.Operator):
    bl_idname = "scene.create_with_collections"
    bl_label = "Create Scene with Collections"

    def execute(self, context):
        create_scene_with_collections(self, context)
        return {'FINISHED'}

# Add the custom operator to a panel in the viewport
class OBJECT_PT_CustomPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AE Utilz"
    bl_context = "objectmode"
    bl_label = "Create New Scene"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('scene.create_with_collections')
        

def register():
    bpy.utils.register_class(AddCollectionSceneOperator)
    bpy.utils.register_class(OBJECT_PT_CustomPanel)


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_CustomPanel)
    bpy.utils.unregister_class(AddCollectionSceneOperator)


if __name__ == "__main__":
    register()
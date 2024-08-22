import bpy
from datetime import datetime

# Define the operator
class SetRenderOutputOperator(bpy.types.Operator):
    """Set the render output path"""
    bl_idname = "render.set_output_path"
    bl_label = "Set to current datetime"

    def execute(self, context):
        # Call the function to set the render output path
        set_render_output(context)
        return {'FINISHED'}

# Define the panel
class RenderOutputPanel(bpy.types.Panel):
    """Panel to set the render output path"""
    bl_idname = "RENDER_PT_output_path"
    bl_label = "Render Output Path"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AE Utilz"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Input field for the base path
        layout.prop(scene, "base_render_path")

        # Button to update the output path
        layout.operator("render.set_output_path", text="Set to current datetime")


def set_render_output(context):
    scene = context.scene
    base_path = scene.base_render_path

    # Get current date and time in the desired format: YYYY-MM-DD_HH_MM_SS
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H.%M.%S")

    # Construct the full output path
    output_path = base_path + timestamp + "/"

    # Set the render output path for all scenes in Blender
    for scene in bpy.data.scenes:
        scene.render.filepath = output_path

        # Update the base path for all File Output nodes in the compositor
        node_tree = scene.node_tree
        if node_tree:
            for node in node_tree.nodes:
                if node.type == 'OUTPUT_FILE':
                    node.base_path = output_path


def register():
    bpy.utils.register_class(SetRenderOutputOperator)
    bpy.utils.register_class(RenderOutputPanel)
    bpy.types.Scene.base_render_path = bpy.props.StringProperty(
        name="Base Output Path",
        description="Base path for rendering output files",
        default="//renders/",
        subtype='DIR_PATH'
    )


def unregister():
    bpy.utils.unregister_class(RenderOutputPanel)
    bpy.utils.unregister_class(SetRenderOutputOperator)
    del bpy.types.Scene.base_render_path


if __name__ == "__main__":
    register()
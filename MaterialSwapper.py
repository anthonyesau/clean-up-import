import bpy

class MaterialSwapperPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Material Swapper"
    bl_idname = "OBJECT_PT_material_swap_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Clean Up Import"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row1 = layout.row()
        row1.prop(scene, "swap_from_material", text="Swap From Material", icon='MATERIAL')  # Add icon and label

        row2 = layout.row()
        row2.prop(scene, "swap_to_material", text="Swap To Material", icon='MATERIAL')

        row3 = layout.row()
        row3.prop(scene, "swap_on_selected_only", text="Swap on Selected Only")
        row3.prop(scene, "add_fake_user", text="Protect Removed Material (Add Fake User)")  # Add checkbox

        row4 = layout.row()
        row4.prop(scene, "swap_material_link", text="Swap Material Link")

        row5 = layout.row()
        row5.operator("object.swap_materials", text="Swap")

class MaterialSwapperOperator(bpy.types.Operator):
    """Swap materials from one to another"""
    bl_idname = "object.swap_materials"
    bl_label = "Swap Materials"

    def execute(self, context):
        scene = context.scene
        swap_from_material = scene.swap_from_material
        swap_to_material = scene.swap_to_material
        swap_on_selected_only = scene.swap_on_selected_only
        swap_material_link = scene.swap_material_link
        add_fake_user = scene.add_fake_user

        if add_fake_user:
            swap_from_material.use_fake_user = True  # Set use_fake_user property to True

        if swap_on_selected_only:
            # Swap materials only on selected objects
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':
                    for slot in obj.material_slots:
                        if slot.material == swap_from_material:
                            if swap_material_link == "OBJECT":
                                slot.link = "OBJECT"  # Link material to the object
                            elif swap_material_link == "DATA":
                                slot.link = "DATA"  # Link material to the data
                            slot.material = swap_to_material
        else:
            # Swap materials on all objects in the scene
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    for slot in obj.material_slots:
                        if slot.material == swap_from_material:
                            if swap_material_link == "OBJECT":
                                slot.link = "OBJECT"  # Link material to the object
                            elif swap_material_link == "DATA":
                                slot.link = "DATA"  # Link material to the data
                            slot.material = swap_to_material

        # Update UI choice boxes
        scene.swap_from_material = swap_to_material
        scene.swap_to_material = swap_from_material

        return {'FINISHED'}

bpy.types.Scene.swap_from_material = bpy.props.PointerProperty(name="Swap From Material", type=bpy.types.Material)
bpy.types.Scene.swap_to_material = bpy.props.PointerProperty(name="Swap To Material", type=bpy.types.Material)
bpy.types.Scene.swap_material_link = bpy.props.EnumProperty(
        items=[("OBJECT", "Link to Object", "Link the material slot to the object"),
               ("DATA", "Link to Data", "Link the material slot to the data"),
               ("NO_CHANGE", "No Change", "Leave the material slot as it currently exists")],
        name="Swap Material Link"
    )
bpy.types.Scene.add_fake_user = bpy.props.BoolProperty(
    name="Add Fake User",
    description="Add a fake user to Swap From Material",
    default=False,
)

def register():
    bpy.utils.register_class(MaterialSwapperPanel)
    bpy.utils.register_class(MaterialSwapperOperator)
    bpy.types.Scene.swap_on_selected_only = bpy.props.BoolProperty(
        name="Swap on selected objects only",
        description="Swap materials on selected objects only",
        default=False,
    )

def unregister():
    bpy.utils.unregister_class(MaterialSwapperPanel)
    bpy.utils.unregister_class(MaterialSwapperOperator)
    del bpy.types.Scene.swap_on_selected_only

if __name__ == "__main__":
    register()
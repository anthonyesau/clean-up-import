import bpy
from mathutils import Vector, Euler

class FormatVWAreaLights(bpy.types.Operator):
    bl_idname = "custom.format_vw_area_lights"
    bl_label = "Set lights to match the location and size of their associated geometry."
    bl_description = "Set lights to match the location and size of their associated geometry."


    def execute(self, context):

        # Iterate through all objects in the scene
        for obj in bpy.context.scene.objects:
            
            # Check if the object name starts with "Area_Light"
            if obj.type == 'LIGHT' and obj.name.startswith("Area_Light"):

                # Loop through each child object of the light
                for child in obj.children:        
                    if child.type == 'MESH':
                        
                        # Clear parent and keep transformation
                        child.select_set(True)
                        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                        bpy.ops.object.transform_apply(scale=True)
                        # Set the scale of the Area light to 1
                        obj.scale = (1, 1, 1)


                        # Select child object to set mode
                        bpy.context.view_layer.objects.active = child
                        
                        # Convert existing geometry to quads
                        bpy.ops.object.mode_set(mode='EDIT')
                        bpy.ops.mesh.select_all(action='SELECT')
                        bpy.ops.mesh.tris_convert_to_quads()
                        bpy.ops.object.mode_set(mode='OBJECT')

                        mesh = child.data
                        face = child.data.polygons[0]
                        center = face.center
                        normal = face.normal

                        # Move the light object "obj" to the center of the first face
                        obj.location = child.matrix_world @ center 

                        # Get the vertex coordinates of the polygon
                        vertices = [mesh.vertices[i].co for i in face.vertices]

                        # Compute the length of each edge of the polygon
                        edgeLengths = [(vertices[i]-vertices[i-1]).length for i in range(len(vertices))]

                        # Compute the dimensions of the rectangle that encloses the polygon
                        faceWidth = edgeLengths[0]
                        faceHeight = edgeLengths[1]

                        # Set the light object to an Area light type
                        obj.data.type = 'AREA'

                        # Set the size of the area light to match the dimensions of "child"
                        obj.data.shape = 'RECTANGLE'
                        obj.data.size = faceWidth
                        obj.data.size_y = faceHeight
                        
                        # Calculate new rotation from normal
                        rotation = normal.to_track_quat('-Z', 'Y').to_euler()
                        
                        # Convert both rotations to a Quaternion
                        old_quat = child.rotation_euler.to_quaternion()
                        new_quat = rotation.to_quaternion()

                        # Add the two quaternions together
                        final_quat = new_quat @ old_quat

                        # Convert the final quaternion back to a Euler rotation and assign
                        obj.rotation_euler = final_quat.to_euler()

                        child.name = obj.name + " Geometry"

        return {'FINISHED'}

def register():
    bpy.utils.register_class(FormatVWAreaLights)

def unregister():
    bpy.utils.unregister_class(FormatVWAreaLights)

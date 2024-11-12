import bpy

from . import utils as ut


class OSC_OT_create_arkit_shapekeys(bpy.types.Operator):
    """Create AR Kit shapekeys for selected object(s)"""
    bl_idname = "nodeosc.create_arkit_shapekeys"
    bl_label = "Create AR Kit shapekeys"

    @classmethod
    def poll(cls, context):
        return context.selected_objects or context.active_object

    def execute(self, context):

        object_list = [context.active_object]
        object_list.extend(context.selected_objects)

        for obj in object_list:

            shape_k = obj.data.shape_keys

            # Basis shapekey if needed
            if not shape_k:
                obj.shape_key_add(
                    name="Basis",
                    from_mix=False,
                )
                shape_k = obj.data.shape_keys

            # AR Kit shapekeys
            for k in ut.arkit_keys:

                # Check if key exists
                try:
                    shape_k.key_blocks[k]

                # Create if needed
                except KeyError:
                    obj.shape_key_add(
                        name=k,
                        from_mix=False,
                    )

        self.report({'INFO'}, "Shape keys created")

        return {'FINISHED'}

def register():
    bpy.utils.register_class(OSC_OT_create_arkit_shapekeys)

def unregister():
    bpy.utils.unregister_class(OSC_OT_create_arkit_shapekeys)

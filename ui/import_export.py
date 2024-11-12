import bpy


def export_menu_func(self, context):
    self.layout.operator(
        "nodeosc.export_config",
        text="Node OSC config (.json)",
    )

def import_menu_func(self, context):
    self.layout.operator(
        "nodeosc.import_config",
        text="Node OSC config (.json)",
    )

def register():
    bpy.types.TOPBAR_MT_file_export.append(export_menu_func)
    bpy.types.TOPBAR_MT_file_import.append(import_menu_func)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(export_menu_func)
    bpy.types.TOPBAR_MT_file_import.append(import_menu_func)

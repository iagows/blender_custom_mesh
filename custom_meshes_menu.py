import bpy
import os
import json

# Class to represent a Blender file
class BlenderFile:
    def __init__(self, label, file_name):
        self.label = label
        self.file_name = file_name

# Class to represent a Blender menu
class BlenderMenu:
    def __init__(self, label, base_path, blender_files):
        self.label = label
        self.base_path = base_path
        self.blender_files = blender_files

# Function to read the JSON file and create Blender menus
def load_blender_menus_from_json(json_path):
    with open(os.path.expanduser(json_path), 'r') as f:
        data = json.load(f)
    
    menus = []
    for menu_data in data['menu']:
        files = [BlenderFile(label=f['label'], file_name=f['file']) for f in menu_data['files']]
        menu = BlenderMenu(label=menu_data['label'], base_path=os.path.expanduser(menu_data['path']), blender_files=files)
        menus.append(menu)
    
    return menus

# Load Blender menus from the specified JSON file
blender_menus = load_blender_menus_from_json("~/.config/custom_assets.json")

# Class to add objects from a .blend file
class AddObjectsFromBlend(bpy.types.Operator):
    bl_idname = "mesh.add_objects_from_blend"
    bl_label = "Add Objects from File"

    blend_file_path: bpy.props.StringProperty()  # Path to the .blend file

    def execute(self, context):
        # Load all objects from the .blend file
        with bpy.data.libraries.load(self.blend_file_path) as (data_from, data_to):
            data_to.objects = data_from.objects  # Load all objects

        # Link loaded objects to the current scene
        for obj in data_to.objects:
            if obj is not None:
                context.collection.objects.link(obj)

        return {'FINISHED'}

# Function to create a submenu for each Blender menu
def create_blender_menu(menu):
    class DynamicBlenderMenu(bpy.types.Menu):
        bl_label = menu.label  # Set the menu label dynamically
        bl_idname = f"OBJECT_MT_{menu.label.lower()}_menu"  # Create a unique ID for the menu

        def draw(self, context):
            layout = self.layout
            for blender_file in menu.blender_files:
                add_operator(layout, blender_file.label, os.path.join(menu.base_path, f"{blender_file.file_name}.blend"))

    return DynamicBlenderMenu

# Helper function to add operators to the menu
def add_operator(layout, text, blend_file):
    operator = layout.operator(AddObjectsFromBlend.bl_idname, text=text, icon='MESH_CUBE')
    operator.blend_file_path = blend_file

# Function to add the custom meshes menu with submenus
class OBJECT_MT_custom_meshes(bpy.types.Menu):
    bl_label = "Custom Meshes"
    bl_idname = "OBJECT_MT_custom_meshes"

    def draw(self, context):
        layout = self.layout
        
        # Add each dynamic menu under "Custom Meshes"
        for menu in blender_menus:
            layout.menu(f"OBJECT_MT_{menu.label.lower()}_menu")  # Add each dynamic menu

# Register the classes and menus
def register():
    bpy.utils.register_class(AddObjectsFromBlend)
    
    # Register each dynamic menu based on the BlenderMenus defined above
    for menu in blender_menus:
        dynamic_menu_class = create_blender_menu(menu)
        bpy.utils.register_class(dynamic_menu_class)

    bpy.utils.register_class(OBJECT_MT_custom_meshes)  # Register the Custom Meshes menu
    
    # Add Custom Meshes menu to the mesh add menu
    bpy.types.VIEW3D_MT_mesh_add.append(lambda self, context: self.layout.menu(OBJECT_MT_custom_meshes.bl_idname))  

def unregister():
    bpy.utils.unregister_class(AddObjectsFromBlend)
    
    # Unregister each dynamic menu
    for menu in blender_menus:
        dynamic_menu_class = create_blender_menu(menu)
        bpy.utils.unregister_class(dynamic_menu_class)

    bpy.utils.unregister_class(OBJECT_MT_custom_meshes)  # Unregister the Custom Meshes menu
    
    # Remove Custom Meshes menu from the mesh add menu
    bpy.types.VIEW3D_MT_mesh_add.remove(lambda self, context: self.layout.menu(OBJECT_MT_custom_meshes.bl_idname))  

# Addon information
bl_info = {
    "name": "Addon Custom Meshes",
    "blender": (4, 0, 0),  # Minimum Blender version (4.0 or higher)
    "category": "Object",
    "description": "Adds objects from .blend files to the mesh add menu.",
    "author": "Iago Alves",
    "version": (1, 1, 0),
    "support": 'COMMUNITY',
    "tracker_url": "https://github.com/iagows/blender_custom_mesh/issues",
    "website": "https://github.com/iagows/blender_custom_mesh",
}

if __name__ == "__main__":
    register()

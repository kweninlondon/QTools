import bpy
import os

bl_info = {
    "name": "QTools",
    "author": "Quentin Vien",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "location": "View3D > Sidebar > QTools",
    "description": "Dynamically loads and runs scripts from a folder",
    "warning": "",
    "category": "Development",
}

# Blender property to store user settings
class QToolsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__  # Use module name as identifier

    script_folder: bpy.props.StringProperty(
        name="Script Folder",
        default="/Users/quentinvien/Documents/QTools_Scripts",
        subtype="DIR_PATH"
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Set the directory where your scripts are stored:")
        layout.prop(self, "script_folder")

# Blender property to store user input for texture path
class QToolsProperties(bpy.types.PropertyGroup):
    texture_path: bpy.props.StringProperty(name="Texture Folder", default="", subtype="DIR_PATH")

class QTOOLS_PT_main_panel(bpy.types.Panel):
    """Creates a Panel in the 3D view sidebar"""
    bl_label = "QTools"
    bl_idname = "QTOOLS_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "QTools"

    def draw(self, context):
        layout = self.layout
        props = context.scene.qtools_props

        # Get the script folder from add-on preferences
        preferences = bpy.context.preferences.addons[__name__].preferences
        script_folder = preferences.script_folder

        # layout.label(text="Scripts Folder:")
        # layout.prop(preferences, "script_folder")  # Editable field in panel

        # Ensure script folder exists
        if not os.path.exists(script_folder):
            layout.label(text="Folder not found!")
            return

        layout.label(text="Scripts:")
        scripts = [f for f in os.listdir(script_folder) if f.endswith(".py")]
        if not scripts:
            layout.label(text="No scripts found!")
            return

        for script in scripts:
            if script == "change_texture_path.py":  # Add UI for texture path
                layout.prop(props, "texture_path")  # Input field for path
                op = layout.operator("qtools.run_texture_script", text="Run Texture Script")
                op.script_name = script
            else:
                op = layout.operator("qtools.run_script", text=script)
                op.script_name = script

class QTOOLS_OT_RunScript(bpy.types.Operator):
    """Operator to execute a script"""
    bl_idname = "qtools.run_script"
    bl_label = "Run Script"

    script_name: bpy.props.StringProperty()

    def execute(self, context):
        # Get script folder from preferences
        preferences = bpy.context.preferences.addons[__name__].preferences
        script_folder = preferences.script_folder
        script_path = os.path.join(script_folder, self.script_name)

        print(f"🟢 Executing script: {script_path}")  # Debug message

        try:
            script_globals = {"__name__": "__main__"}  # Define an isolated execution scope
            with open(script_path) as file:
                exec(compile(file.read(), script_path, 'exec'), script_globals)

            print(f"✅ Successfully executed: {self.script_name}")
            self.report({'INFO'}, f"Executed: {self.script_name}")

        except Exception as e:
            print(f"❌ Error executing: {self.script_name} - {e}")
            self.report({'ERROR'}, f"Failed: {self.script_name} - {e}")

        return {'FINISHED'}

class QTOOLS_OT_RunTextureScript(bpy.types.Operator):
    """Operator to run change_texture_path.py with user input"""
    bl_idname = "qtools.run_texture_script"
    bl_label = "Run Texture Path Script"

    script_name: bpy.props.StringProperty()

    def execute(self, context):
        # Get script folder from preferences
        preferences = bpy.context.preferences.addons[__name__].preferences
        script_folder = preferences.script_folder
        script_path = os.path.join(script_folder, self.script_name)
        texture_path = context.scene.qtools_props.texture_path

        if not texture_path:
            self.report({'ERROR'}, "Please enter a texture folder path!")
            return {'CANCELLED'}

        try:
            exec(compile(open(script_path).read(), script_path, 'exec'), globals(), locals())
            self.report({'INFO'}, f"Executed: {self.script_name} with path: {texture_path}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed: {self.script_name} - {e}")

        return {'FINISHED'}

def register():
    bpy.utils.register_class(QToolsPreferences)  # Register add-on preferences
    bpy.utils.register_class(QTOOLS_PT_main_panel)
    bpy.utils.register_class(QTOOLS_OT_RunScript)
    bpy.utils.register_class(QTOOLS_OT_RunTextureScript)
    bpy.utils.register_class(QToolsProperties)
    bpy.types.Scene.qtools_props = bpy.props.PointerProperty(type=QToolsProperties)

def unregister():
    bpy.utils.unregister_class(QToolsPreferences)
    bpy.utils.unregister_class(QTOOLS_PT_main_panel)
    bpy.utils.unregister_class(QTOOLS_OT_RunScript)
    bpy.utils.unregister_class(QTOOLS_OT_RunTextureScript)
    bpy.utils.unregister_class(QToolsProperties)
    del bpy.types.Scene.qtools_props

if __name__ == "__main__":
    register()

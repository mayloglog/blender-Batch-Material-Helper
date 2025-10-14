bl_info = {
    "name": "Batch Material Helper",
    "author": "maylog",
    "version": (1, 0, 3),  
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Material",
    "description": "Batch adjust material and BSDF properties for selected objects, including emission, coat, sheen, transmission, subsurface, and custom split normals clearing",
    "category": "Material",
}

import bpy
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import FloatProperty, FloatVectorProperty, BoolProperty, EnumProperty

# Define PropertyGroup to hold all properties
class BatchMaterialProperties(PropertyGroup):
    # BSDF Properties
    batch_base_color: FloatVectorProperty(
        name="Base Color",
        description="Base color for Principled BSDF",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0, 1.0),
        size=4
    )
    use_base_color: BoolProperty(
        name="Use Base Color",
        description="Apply Base Color to selected objects",
        default=False
    )
    batch_metallic_value: FloatProperty(
        name="Metallic",
        description="Value to set for metallic property",
        default=0.0,
        min=0.0,
        max=1.0
    )
    use_metallic: BoolProperty(
        name="Use Metallic",
        description="Apply Metallic to selected objects",
        default=False
    )
    batch_roughness_value: FloatProperty(
        name="Roughness",
        description="Value to set for roughness property",
        default=0.5,
        min=0.0,
        max=1.0
    )
    use_roughness: BoolProperty(
        name="Use Roughness",
        description="Apply Roughness to selected objects",
        default=False
    )
    batch_ior_value: FloatProperty(
        name="IOR",
        description="Value to set for IOR property",
        default=1.45,
        min=1.0,
        max=1000.0
    )
    use_ior: BoolProperty(
        name="Use IOR",
        description="Apply IOR to selected objects",
        default=False
    )
    batch_alpha_value: FloatProperty(
        name="Alpha",
        description="Value to set for alpha property",
        default=1.0,
        min=0.0,
        max=1.0
    )
    use_alpha: BoolProperty(
        name="Use Alpha",
        description="Apply Alpha to selected objects",
        default=False
    )
    batch_ior_level_value: FloatProperty(
        name="IOR Level",
        description="Value to set for IOR Level property",
        default=0.5,
        min=0.0,
        max=1.0
    )
    use_ior_level: BoolProperty(
        name="Use IOR Level",
        description="Apply IOR Level to selected objects",
        default=False
    )
    batch_emission_color: FloatVectorProperty(
        name="Emission Color",
        description="Emission color for Principled BSDF",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0, 1.0),
        size=4
    )
    use_emission_color: BoolProperty(
        name="Use Emission Color",
        description="Apply Emission Color to selected objects",
        default=False
    )
    batch_emission_strength: FloatProperty(
        name="Emission Strength",
        description="Value to set for emission strength property",
        default=0.0,
        min=0.0
    )
    use_emission_strength: BoolProperty(
        name="Use Emission Strength",
        description="Apply Emission Strength to selected objects",
        default=False
    )
    batch_coat_weight: FloatProperty(
        name="Coat Weight",
        description="Value to set for coat weight property",
        default=0.0,
        min=0.0,
        max=1.0
    )
    use_coat_weight: BoolProperty(
        name="Use Coat Weight",
        description="Apply Coat Weight to selected objects",
        default=False
    )
    batch_sheen_weight: FloatProperty(
        name="Sheen Weight",
        description="Value to set for sheen weight property",
        default=0.0,
        min=0.0,
        max=1.0
    )
    use_sheen_weight: BoolProperty(
        name="Use Sheen Weight",
        description="Apply Sheen Weight to selected objects",
        default=False
    )
    batch_transmission_weight: FloatProperty(
        name="Transmission Weight",
        description="Value to set for transmission weight property",
        default=0.0,
        min=0.0,
        max=1.0
    )
    use_transmission_weight: BoolProperty(
        name="Use Transmission Weight",
        description="Apply Transmission Weight to selected objects",
        default=False
    )
    batch_subsurface_weight: FloatProperty(
        name="Subsurface Weight",
        description="Value to set for subsurface weight property",
        default=0.0,
        min=0.0,
        max=1.0
    )
    use_subsurface_weight: BoolProperty(
        name="Use Subsurface Weight",
        description="Apply Subsurface Weight to selected objects",
        default=False
    )
    # New: Clear Custom Split Normals
    use_clear_custom_split_normals: BoolProperty(
        name="Clear Custom Split Normals Data",
        description="Clear custom split normals data for selected objects",
        default=False
    )
    # Material Settings
    batch_render_method: EnumProperty(
        name="Render Method",
        description="Surface render method for materials",
        items=[
            ('DITHERED', "Dithered", "Render surface with dithered transparency"),
            ('BLENDED', "Blended", "Render surface with blended transparency")
        ],
        default='DITHERED'
    )
    use_render_method: BoolProperty(
        name="Use Render Method",
        description="Apply Render Method to selected objects",
        default=False
    )
    batch_displacement_method: EnumProperty(
        name="Displacement Method",
        description="Displacement method for materials",
        items=[
            ('BUMP', "Bump", "Use bump mapping only"),
            ('DISPLACEMENT', "Displacement", "Use true displacement"),
            ('BOTH', "Displacement and Bump", "Use both displacement and bump")
        ],
        default='BUMP'
    )
    use_displacement_method: BoolProperty(
        name="Use Displacement Method",
        description="Apply Displacement Method to selected objects",
        default=False
    )
    batch_backface_culling: BoolProperty(
        name="Backface Culling (Camera)",
        description="Enable backface culling for camera",
        default=False
    )
    use_backface_culling: BoolProperty(
        name="Use Backface Culling (Camera)",
        description="Apply Backface Culling (Camera) to selected objects",
        default=False
    )
    batch_backface_culling_shadow: BoolProperty(
        name="Backface Culling (Shadow)",
        description="Enable backface culling for shadows",
        default=False
    )
    use_backface_culling_shadow: BoolProperty(
        name="Use Backface Culling (Shadow)",
        description="Apply Backface Culling (Shadow) to selected objects",
        default=False
    )
    batch_backface_culling_lightprobe: BoolProperty(
        name="Backface Culling (Lightprobe)",
        description="Enable backface culling for lightprobe volume",
        default=False
    )
    use_backface_culling_lightprobe: BoolProperty(
        name="Use Backface Culling (Lightprobe)",
        description="Apply Backface Culling (Lightprobe) to selected objects",
        default=False
    )
    batch_transparent_shadow: BoolProperty(
        name="Raytrace Transmission",
        description="Enable transparent shadows in raytracing",
        default=False
    )
    use_transparent_shadow: BoolProperty(
        name="Use Raytrace Transmission",
        description="Apply Raytrace Transmission to selected objects",
        default=False
    )
    # Viewport Display
    batch_diffuse_color: FloatVectorProperty(
        name="Diffuse Color",
        description="Viewport display color",
        subtype='COLOR',
        default=(0.8, 0.8, 0.8, 1.0),
        size=4
    )
    use_diffuse_color: BoolProperty(
        name="Use Diffuse Color",
        description="Apply Diffuse Color to viewport display",
        default=False
    )
    batch_display_metallic: FloatProperty(
        name="Display Metallic",
        description="Viewport display metallic value",
        default=0.0,
        min=0.0,
        max=1.0
    )
    use_display_metallic: BoolProperty(
        name="Use Display Metallic",
        description="Apply Metallic to viewport display",
        default=False
    )
    batch_display_roughness: FloatProperty(
        name="Display Roughness",
        description="Viewport display roughness value",
        default=0.5,
        min=0.0,
        max=1.0
    )
    use_display_roughness: BoolProperty(
        name="Use Display Roughness",
        description="Apply Roughness to viewport display",
        default=False
    )

class MATERIAL_OT_batch_material_helper(Operator):
    """Batch set material and BSDF properties for selected objects"""
    bl_idname = "material.batch_material_helper"
    bl_label = "Batch Material Helper"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.app.version < (2, 93, 0):
            self.report({'WARNING'}, "Emission, Coat, Sheen, Transmission, and Subsurface properties require Blender 2.93 or higher")
            return {'CANCELLED'}

        props = context.scene.batch_material_props
        # BSDF Properties
        base_color = props.batch_base_color
        metallic_value = props.batch_metallic_value
        roughness_value = props.batch_roughness_value
        ior_value = props.batch_ior_value
        alpha_value = props.batch_alpha_value
        ior_level_value = props.batch_ior_level_value
        emission_color = props.batch_emission_color
        emission_strength = props.batch_emission_strength
        coat_weight = props.batch_coat_weight
        sheen_weight = props.batch_sheen_weight
        transmission_weight = props.batch_transmission_weight
        subsurface_weight = props.batch_subsurface_weight
        # Material Settings
        render_method = props.batch_render_method
        displacement_method = props.batch_displacement_method
        backface_culling = props.batch_backface_culling
        backface_culling_shadow = props.batch_backface_culling_shadow
        backface_culling_lightprobe = props.batch_backface_culling_lightprobe
        transparent_shadow = props.batch_transparent_shadow
        # Viewport Display
        diffuse_color = props.batch_diffuse_color
        display_metallic = props.batch_display_metallic
        display_roughness = props.batch_display_roughness

        selected_objects = context.selected_objects
        
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected!")
            return {'CANCELLED'}

        applied_properties = []
        for obj in selected_objects:
            # New: Clear Custom Split Normals Data
            if props.use_clear_custom_split_normals:
                try:
                    # Store the active object
                    prev_active = context.active_object
                    # Set the current object as active
                    context.view_layer.objects.active = obj
                    # Switch to object mode if necessary
                    if obj.mode != 'OBJECT':
                        bpy.ops.object.mode_set(mode='OBJECT')
                    # Clear custom split normals
                    bpy.ops.mesh.customdata_custom_splitnormals_clear()
                    applied_properties.append("Custom Split Normals Cleared")
                    # Restore the previous active object
                    context.view_layer.objects.active = prev_active
                except Exception as e:
                    self.report({'WARNING'}, f"Failed to clear custom split normals for {obj.name}: {e}")
            
            if obj.material_slots:  # Support all object types with material slots
                for mat_slot in obj.material_slots:
                    material = mat_slot.material
                    if material:
                        # Material Settings (independent of BSDF)
                        if props.use_render_method:
                            material.surface_render_method = render_method
                            applied_properties.append(f"Render Method={render_method}")
                        if props.use_displacement_method:
                            material.displacement_method = displacement_method
                            applied_properties.append(f"Displacement Method={displacement_method}")
                        if props.use_backface_culling:
                            material.use_backface_culling = backface_culling
                            applied_properties.append(f"Backface Culling (Camera)={backface_culling}")
                        if props.use_backface_culling_shadow:
                            material.use_backface_culling_shadow = backface_culling_shadow
                            applied_properties.append(f"Backface Culling (Shadow)={backface_culling_shadow}")
                        if props.use_backface_culling_lightprobe:
                            material.use_backface_culling_lightprobe_volume = backface_culling_lightprobe
                            applied_properties.append(f"Backface Culling (Lightprobe)={backface_culling_lightprobe}")
                        if props.use_transparent_shadow:
                            material.use_transparent_shadow = transparent_shadow
                            applied_properties.append(f"Raytrace Transmission={transparent_shadow}")
                        # Viewport Display
                        if props.use_diffuse_color:
                            material.diffuse_color = diffuse_color
                            applied_properties.append(f"Diffuse Color={diffuse_color[:3]}")
                        if props.use_display_metallic:
                            material.metallic = display_metallic
                            applied_properties.append(f"Display Metallic={display_metallic}")
                        if props.use_display_roughness:
                            material.roughness = display_roughness
                            applied_properties.append(f"Display Roughness={display_roughness}")
                        # BSDF Properties
                        if material.use_nodes:
                            node_tree = material.node_tree
                            principled_node = next((node for node in node_tree.nodes if node.type == 'BSDF_PRINCIPLED'), None)
                            if principled_node:
                                if props.use_base_color:
                                    principled_node.inputs['Base Color'].default_value = base_color
                                    applied_properties.append(f"Base Color={base_color[:3]}")
                                if props.use_metallic:
                                    principled_node.inputs['Metallic'].default_value = metallic_value
                                    applied_properties.append(f"Metallic={metallic_value}")
                                if props.use_roughness:
                                    principled_node.inputs['Roughness'].default_value = roughness_value
                                    applied_properties.append(f"Roughness={roughness_value}")
                                if props.use_ior:
                                    principled_node.inputs['IOR'].default_value = ior_value
                                    applied_properties.append(f"IOR={ior_value}")
                                if props.use_alpha:
                                    principled_node.inputs['Alpha'].default_value = alpha_value
                                    applied_properties.append(f"Alpha={alpha_value}")
                                if props.use_ior_level:
                                    try:
                                        if 'IOR Level' in principled_node.inputs:
                                            principled_node.inputs['IOR Level'].default_value = ior_level_value
                                        else:
                                            principled_node.inputs[13].default_value = ior_level_value
                                        applied_properties.append(f"IOR Level={ior_level_value}")
                                    except (KeyError, IndexError):
                                        self.report({'WARNING'}, "IOR Level input not found in some materials!")
                                if props.use_emission_color:
                                    try:
                                        principled_node.inputs[27].default_value = emission_color
                                        applied_properties.append(f"Emission Color={emission_color[:3]}")
                                    except (KeyError, IndexError):
                                        self.report({'WARNING'}, "Emission Color input not found in some materials!")
                                if props.use_emission_strength:
                                    try:
                                        principled_node.inputs[28].default_value = emission_strength
                                        applied_properties.append(f"Emission Strength={emission_strength}")
                                    except (KeyError, IndexError):
                                        self.report({'WARNING'}, "Emission Strength input not found in some materials!")
                                if props.use_coat_weight:
                                    try:
                                        principled_node.inputs[19].default_value = coat_weight
                                        applied_properties.append(f"Coat Weight={coat_weight}")
                                    except (KeyError, IndexError):
                                        self.report({'WARNING'}, "Coat Weight input not found in some materials!")
                                if props.use_sheen_weight:
                                    try:
                                        principled_node.inputs[24].default_value = sheen_weight
                                        applied_properties.append(f"Sheen Weight={sheen_weight}")
                                    except (KeyError, IndexError):
                                        self.report({'WARNING'}, "Sheen Weight input not found in some materials!")
                                if props.use_transmission_weight:
                                    try:
                                        principled_node.inputs[18].default_value = transmission_weight
                                        applied_properties.append(f"Transmission Weight={transmission_weight}")
                                    except (KeyError, IndexError):
                                        self.report({'WARNING'}, "Transmission Weight input not found in some materials!")
                                if props.use_subsurface_weight:
                                    try:
                                        principled_node.inputs[8].default_value = subsurface_weight
                                        applied_properties.append(f"Subsurface Weight={subsurface_weight}")
                                    except (KeyError, IndexError):
                                        self.report({'WARNING'}, "Subsurface Weight input not found in some materials!")
        
        if applied_properties:
            self.report({'INFO'}, f"Applied to selected objects: {', '.join(applied_properties)}")
        else:
            self.report({'WARNING'}, "No properties selected to apply!")
            return {'CANCELLED'}
        
        return {'FINISHED'}

class VIEW3D_PT_batch_material_helper(Panel):
    """Panel to batch adjust material and BSDF properties for selected objects"""
    bl_label = "Batch Material Helper"
    bl_idname = "VIEW3D_PT_batch_material_helper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Material"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.batch_material_props

        layout.label(text="Adjust Material Properties (Selected)")
        col = layout.column(align=True)
        col.label(text="BSDF Properties")
        row = col.row()
        row.prop(props, "use_base_color", text="")
        row.prop(props, "batch_base_color", text="Base Color")
        row = col.row()
        row.prop(props, "use_metallic", text="")
        row.prop(props, "batch_metallic_value", text="Metallic")
        row = col.row()
        row.prop(props, "use_roughness", text="")
        row.prop(props, "batch_roughness_value", text="Roughness")
        row = col.row()
        row.prop(props, "use_ior", text="")
        row.prop(props, "batch_ior_value", text="IOR")
        row = col.row()
        row.prop(props, "use_alpha", text="")
        row.prop(props, "batch_alpha_value", text="Alpha")
        row = col.row()
        row.prop(props, "use_ior_level", text="")
        row.prop(props, "batch_ior_level_value", text="IOR Level")
        row = col.row()
        row.prop(props, "use_emission_color", text="")
        row.prop(props, "batch_emission_color", text="Emission Color")
        row = col.row()
        row.prop(props, "use_emission_strength", text="")
        row.prop(props, "batch_emission_strength", text="Emission Strength")
        row = col.row()
        row.prop(props, "use_coat_weight", text="")
        row.prop(props, "batch_coat_weight", text="Coat Weight")
        row = col.row()
        row.prop(props, "use_sheen_weight", text="")
        row.prop(props, "batch_sheen_weight", text="Sheen Weight")
        row = col.row()
        row.prop(props, "use_transmission_weight", text="")
        row.prop(props, "batch_transmission_weight", text="Transmission Weight")
        row = col.row()
        row.prop(props, "use_subsurface_weight", text="")
        row.prop(props, "batch_subsurface_weight", text="Subsurface Weight")

        col = layout.column(align=True)
        col.label(text="Material Settings")
        row = col.row()
        row.prop(props, "use_render_method", text="")
        row.prop(props, "batch_render_method", text="Render Method")
        row = col.row()
        row.prop(props, "use_displacement_method", text="")
        row.prop(props, "batch_displacement_method", text="Displacement Method")
        row = col.row()
        row.prop(props, "use_backface_culling", text="")
        row.prop(props, "batch_backface_culling", text="Backface Culling (Camera)")
        row = col.row()
        row.prop(props, "use_backface_culling_shadow", text="")
        row.prop(props, "batch_backface_culling_shadow", text="Backface Culling (Shadow)")
        row = col.row()
        row.prop(props, "use_backface_culling_lightprobe", text="")
        row.prop(props, "batch_backface_culling_lightprobe", text="Backface Culling (Lightprobe)")
        row = col.row()
        row.prop(props, "use_transparent_shadow", text="")
        row.prop(props, "batch_transparent_shadow", text="Raytrace Transmission")

        col = layout.column(align=True)
        col.label(text="Viewport Display")
        row = col.row()
        row.prop(props, "use_diffuse_color", text="")
        row.prop(props, "batch_diffuse_color", text="Diffuse Color")
        row = col.row()
        row.prop(props, "use_display_metallic", text="")
        row.prop(props, "batch_display_metallic", text="Metallic")
        row = col.row()
        row.prop(props, "use_display_roughness", text="")
        row.prop(props, "batch_display_roughness", text="Roughness")

        # New: Clear Custom Split Normals Section
        col = layout.column(align=True)
        col.label(text="Mesh Properties")
        row = col.row()
        row.prop(props, "use_clear_custom_split_normals", text="Clear Custom Split Normals Data")

        layout.operator("material.batch_material_helper", text="Apply to Selected Objects")

def register():
    try:
        bpy.utils.register_class(BatchMaterialProperties)
        bpy.utils.register_class(MATERIAL_OT_batch_material_helper)
        bpy.utils.register_class(VIEW3D_PT_batch_material_helper)
        
        # Register PropertyGroup to Scene
        bpy.types.Scene.batch_material_props = bpy.props.PointerProperty(type=BatchMaterialProperties)
        print("Batch Material Helper: Properties registered successfully")
    except Exception as e:
        print(f"Batch Material Helper: Registration failed - {e}")

def unregister():
    try:
        bpy.utils.unregister_class(MATERIAL_OT_batch_material_helper)
        bpy.utils.unregister_class(VIEW3D_PT_batch_material_helper)
        bpy.utils.unregister_class(BatchMaterialProperties)
        
        # Remove PropertyGroup
        if hasattr(bpy.types.Scene, 'batch_material_props'):
            del bpy.types.Scene.batch_material_props
        print("Batch Material Helper: Properties unregistered successfully")
    except Exception as e:
        print(f"Batch Material Helper: Unregistration failed - {e}")

if __name__ == "__main__":
    register()
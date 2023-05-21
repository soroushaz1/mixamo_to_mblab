bl_info = {
    "name": "Mixamo to MB-Lab Retarget",
    "author": "Soroush Amel Zendedel",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > Tool Shelf > Mixamo to MB-Lab Retarget",
    "description": "Retarget Mixamo animations to MB-Lab rig using Simple Retarget addon",
    "warning": "You should install and enable Simple Retarget addon to use this addon",
    "wiki_url": "",
    "category": "Object",
}

import bpy

bone_mapping = [
    ('mixamorig:Spine', 'spine01'),
    ('mixamorig:Spine1', 'spine02'),
    ('mixamorig:Spine2', 'spine03'),
    ('mixamorig:Neck', 'neck'),
    ('mixamorig:Head', 'head'),
    ('mixamorig:LeftShoulder', 'clavicle_L'),
    ('mixamorig:LeftArm', 'upperarm_L'),
    ('mixamorig:LeftForeArm', 'lowerarm_L'),
    ('mixamorig:LeftHand', 'hand_L'),
    ('mixamorig:LeftHandIndex1', 'index00_L'),
    ('mixamorig:LeftHandIndex2', 'index01_L'),
    ('mixamorig:LeftHandIndex3', 'index02_L'),
    ('mixamorig:LeftHandIndex4', 'index03_L'),
    ('mixamorig:LeftHandIndex1', 'middle00_L'),
    ('mixamorig:LeftHandIndex2', 'middle01_L'),
    ('mixamorig:LeftHandIndex3', 'middle02_L'),
    ('mixamorig:LeftHandIndex4', 'middle03_L'),
    ('mixamorig:LeftHandIndex1', 'pinky00_L'),
    ('mixamorig:LeftHandIndex2', 'pinky01_L'),
    ('mixamorig:LeftHandIndex3', 'pinky02_L'),
    ('mixamorig:LeftHandIndex4', 'pinky03_L'),
    ('mixamorig:LeftHandIndex1', 'ring00_L'),
    ('mixamorig:LeftHandIndex2', 'ring01_L'),
    ('mixamorig:LeftHandIndex3', 'ring02_L'),
    ('mixamorig:LeftHandIndex4', 'ring03_L'),
    ('mixamorig:LeftHandThumb1', 'thumb01_L'),
    ('mixamorig:LeftHandThumb2', 'thumb02_L'),
    ('mixamorig:LeftHandThumb3', 'thumb03_L'),
    ('mixamorig:RightShoulder', 'clavicle_R'),
    ('mixamorig:RightArm', 'upperarm_R'),
    ('mixamorig:RightForeArm', 'lowerarm_R'),
    ('mixamorig:RightHand', 'hand_R'),
    ('mixamorig:RightHandIndex1', 'index00_R'),
    ('mixamorig:RightHandIndex2', 'index01_R'),
    ('mixamorig:RightHandIndex3', 'index02_R'),
    ('mixamorig:RightHandIndex4', 'index03_R'),
    ('mixamorig:RightHandIndex1', 'middle00_R'),
    ('mixamorig:RightHandIndex2', 'middle01_R'),
    ('mixamorig:RightHandIndex3', 'middle02_R'),
    ('mixamorig:RightHandIndex4', 'middle03_R'),
    ('mixamorig:RightHandIndex1', 'pinky00_R'),
    ('mixamorig:RightHandIndex2', 'pinky01_R'),
    ('mixamorig:RightHandIndex3', 'pinky02_R'),
    ('mixamorig:RightHandIndex4', 'pinky03_R'),
    ('mixamorig:RightHandIndex1', 'ring00_R'),
    ('mixamorig:RightHandIndex2', 'ring01_R'),
    ('mixamorig:RightHandIndex3', 'ring02_R'),
    ('mixamorig:RightHandIndex4', 'ring03_R'),
    ('mixamorig:RightHandThumb1', 'thumb01_R'),
    ('mixamorig:RightHandThumb2', 'thumb02_R'),
    ('mixamorig:RightHandThumb3', 'thumb03_R'),
    ('mixamorig:LeftUpLeg', 'thigh_L'),
    ('mixamorig:LeftLeg', 'calf_L'),
    ('mixamorig:LeftFoot', 'foot_L'),
    ('mixamorig:LeftToeBase', 'toes_L'),
    ('mixamorig:RightUpLeg', 'thigh_R'),
    ('mixamorig:RightLeg', 'calf_R'),
    ('mixamorig:RightFoot', 'foot_R'),
    ('mixamorig:RightToeBase', 'toes_R'),
]


def shift_select_objects(object_names):
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    
    first_object = True
    
    for obj_name in object_names:
        obj = bpy.data.objects.get(obj_name)
        
        if obj is not None:
            if first_object:
                # Set the first object as the active object
                bpy.context.view_layer.objects.active = obj
                first_object = False
                
            # Select the object
            obj.select_set(True)
        else:
            print(f"Error: Object '{obj_name}' not found in the scene")

def deselect_all():
    for obj in bpy.context.selected_objects:
        obj.select_set(False)

def select_and_activate(obj):
    deselect_all()
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

mixamo_armature_name = ""
mblab_armature_name = ""

class MIXAMO_OT_mblab_retarget(bpy.types.Operator):
    bl_idname = "object.mixamo_mblab_retarget"
    bl_label = "Mixamo to MB-Lab Retarget"
    bl_description = "Select the Mixamo armature then select the MB-Lab armature"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mixamo_armature = bpy.context.selected_objects[0]
        mblab_armature = bpy.context.selected_objects[1]
        mixamo_armature_name = mixamo_armature.name
        mblab_armature_name = mblab_armature.name

        if mixamo_armature.type != 'ARMATURE' or mblab_armature.type != 'ARMATURE':
            self.report({'ERROR'}, 'Please select Mixamo armature and MB-Lab armature')
            return {'CANCELLED'}
        
        # Set the mb-lab armature to T-pose
        mblab_armature.rest_pose = 't-pose'
        bpy.ops.pose.select_all(action='SELECT')
        bpy.ops.simpleretarget.set_rest_pose_with_object()

        bpy.ops.object.posemode_toggle()

        # Apply the rotation for mixamo_armature
        select_and_activate(bpy.data.objects.get(mixamo_armature_name))
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        shift_select_objects([mblab_armature_name, mixamo_armature_name])
        mixamo_armature = bpy.context.selected_objects[0]
        mblab_armature = bpy.context.selected_objects[1]

        bpy.ops.object.posemode_toggle()

        # Unlock mb-lab pelvis location properties
        mblab_armature.pose.bones['pelvis'].lock_location[0] = False
        mblab_armature.pose.bones['pelvis'].lock_location[1] = False
        mblab_armature.pose.bones['pelvis'].lock_location[2] = False

        # Deselect all bones
        bpy.ops.pose.select_all(action='DESELECT')

        # Retarget root
        mixamo_armature.data.bones['mixamorig:Hips'].select = True
        mixamo_armature.data.bones.active = mixamo_armature.data.bones['mixamorig:Hips']
        mblab_armature.data.bones['pelvis'].select = True
        mblab_armature.data.bones.active = mblab_armature.data.bones['pelvis']
        bpy.ops.simpleretarget.retarget_root()
        bpy.ops.pose.select_all(action='DESELECT')

        # Retarget other bones
        for mixamo_bone_name, mblab_bone_name in bone_mapping:
            mixamo_bone = mixamo_armature.data.bones.get(mixamo_bone_name)
            mblab_bone = mblab_armature.data.bones.get(mblab_bone_name)
            
            if mixamo_bone is not None and mblab_bone is not None:
                mixamo_bone.select = True
                mixamo_armature.data.bones.active = mixamo_bone

                mblab_bone.select = True
                mblab_armature.data.bones.active = mblab_bone

                bpy.ops.simpleretarget.retarget_bone()
                
                bpy.ops.pose.select_all(action='DESELECT')

        bpy.ops.object.posemode_toggle()

        return {'FINISHED'}

class MIXAMO_PT_mblab_retarget(bpy.types.Panel):
    bl_label = "Mixamo to MB-Lab Retarget"
    bl_idname = "MIXAMO_PT_mblab_retarget"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Retarget"

    def draw(self, context):
        layout = self.layout
        layout.operator(MIXAMO_OT_mblab_retarget.bl_idname)


def register():
    bpy.utils.register_class(MIXAMO_OT_mblab_retarget)
    bpy.utils.register_class(MIXAMO_PT_mblab_retarget)


def unregister():
    bpy.utils.unregister_class(MIXAMO_OT_mblab_retarget)
    bpy.utils.unregister_class(MIXAMO_PT_mblab_retarget)



if __name__ == "__main__":
    register()

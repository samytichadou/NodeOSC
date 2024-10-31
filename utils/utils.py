import bpy

dataDirectionItems = {
    ("INPUT", "Input", "Receive the OSC message from somewhere else", "IMPORT", 0),
    ("OUTPUT", "Output", "Send the OSC message from this node", "EXPORT", 1),
    ("BOTH", "Both", "Send and Reveive this OSC message", "FILE_REFRESH", 2),
    ("PHIZIN", "Phiz Input", "Receive OSC message from Phiz Mocap source", "MESH_MONKEY", 3),
}

dataNodeDirectionItems = {
    ("INPUT", "Input", "Receive the OSC message from somewhere else", "IMPORT", 0),
    ("OUTPUT", "Output", "Send the OSC message from this node", "EXPORT", 1),
}

nodeDataTypeItems = {
    ("LIST", "List", "Expects List", "IMPORT", 0),
    ("SINGLE", "Single", "Expects single value", "IMPORT", 1),
}

nodeTypeItems = {
    ("NONE", 0),
    ("AN", 1),
    ("SORCAR", 2),
}

arkit_keys = [
        "browInnerUp",
        "browDownLeft",
        "browDownRight",
        "browOuterUpLeft",
        "browOuterUpRight",
        "eyeLookUpLeft",
        "eyeLookUpRight",
        "eyeLookDownLeft",
        "eyeLookDownRight",
        "eyeLookInLeft",
        "eyeLookInRight",
        "eyeLookOutLeft",
        "eyeLookOutRight",
        "eyeBlinkLeft",
        "eyeBlinkRight",
        "eyeSquintLeft",
        "eyeSquintRight",
        "eyeWideLeft",
        "eyeWideRight",
        "cheekPuff",
        "cheekSquintLeft",
        "cheekSquintRight",
        "noseSneerLeft",
        "noseSneerRight",
        "mouthFunnel",
        "mouthPucker",
        "mouthRollUpper",
        "mouthRollLower",
        "mouthShrugUpper",
        "mouthShrugLower",
        "mouthClose",
        "mouthSmileLeft",
        "mouthSmileRight",
        "mouthFrownLeft",
        "mouthFrownRight",
        "mouthDimpleLeft",
        "mouthDimpleRight",
        "mouthUpperUpLeft",
        "mouthUpperUpRight",
        "mouthLowerDownLeft",
        "mouthLowerDownRight",
        "mouthPressLeft",
        "mouthPressRight",
        "mouthStretchLeft",
        "mouthStretchRight",
        "mouthLeft",
        "mouthRight",
        "jawOpen",
        "jawForward",
        "jawLeft",
        "jawRight",
        "tongueOut",
    ]

def sorcarTreeUpdate():
    bpy.context.scene.nodeosc_SORCAR_needsUpdate = True

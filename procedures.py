import bpy
from easybpy import *
import os

################################################################
'''
List of procedures to be executed
'''
################################################################


def link_switcher(node_group_name: object, node_from: str, node_to: str) -> None:
    node_group = bpy.data.node_groups.get(node_group_name)

    point1 = node_group.nodes[node_from]
    point2 = node_group.nodes[node_to]

    create_node_link(point1.outputs[0], point2.inputs[0])


# def get_active_camera() -> object:
#     return bpy.context.scene.camera


def BSDF_baker_switcher(node_group_name: str, switch: bool) -> None:
    if switch:
        link_switcher(node_group_name,
                      "OutPreviewBakerData", "OutPreview")
    else:
        link_switcher(node_group_name, "OutPreviewBSF", "OutPreview")


def Albedo(node_group_name: str, save_path: str, file_base_name: str) -> None:

    bpy.context.scene.view_settings.view_transform = 'Standard'
    bpy.context.scene.view_settings.look = 'None'
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'

    link_switcher(node_group_name, "TargetAlbedo", "TargetSwitcher")

    bpy.data.materials["Baker.BGPlanes"].node_tree.nodes["Group"].inputs[0].default_value = 0
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.data.scenes["TrimTextures/"].render.filepath = save_path + \
        "\\" + file_base_name + "+Albedo"
    bpy.context.scene.use_nodes = True  # PPSharpen

    bpy.data.scenes["TrimTextures/"].node_tree.nodes["Filter.001"].inputs[0].default_value = 0.250

    bpy.ops.render.render(write_still=True)

    bpy.data.scenes["TrimTextures/"].node_tree.nodes["Filter.001"].inputs[0].default_value = 0


def ORM(node_group_name: str, save_path: str, file_base_name: str) -> None:

    bpy.context.scene.view_settings.view_transform = 'Raw'
    bpy.context.scene.view_settings.look = 'None'
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'

    link_switcher(node_group_name, "TargetORM", "TargetSwitcher")

    bpy.context.scene.eevee.gtao_distance = 0.1

    bpy.data.materials["Baker.BGPlanes"].node_tree.nodes["Group"].inputs[0].default_value = 0
    bpy.context.scene.render.image_settings.color_mode = 'RGB'
    bpy.data.scenes["TrimTextures/"].render.filepath = save_path + \
        "\\" + file_base_name + "+ORM"
    bpy.context.scene.use_nodes = False  # PPSharpen

    bpy.ops.render.render(write_still=True)


def Normal(node_group_name: str, save_path: str, file_base_name: str) -> None:

    bpy.context.scene.view_settings.view_transform = 'Raw'
    bpy.context.scene.view_settings.look = 'None'
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'

    link_switcher(node_group_name, "TargetNormol", "TargetSwitcher")

    bpy.data.materials["Baker.BGPlanes"].node_tree.nodes["Group"].inputs[0].default_value = 1
    bpy.context.scene.render.image_settings.color_mode = 'RGB'
    bpy.data.scenes["TrimTextures/"].render.filepath = save_path + \
        "\\" + file_base_name + "+Normal"
    bpy.context.scene.use_nodes = False  # PPSharpen

    bpy.ops.render.render(write_still=True)

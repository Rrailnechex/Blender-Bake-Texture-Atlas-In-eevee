import os
import bpy
# from easybpy import *

bl_info = {
    "name": "Pipline - Bake Texture Atlas",
    "author": "Rrailnechex",
    "version": (0, 0, 2),
    "blender": (3, 3, 0),
    "description": "bake trim textures to my pipline",
    "location": "View3D > Properties > Bake TA",
    "warning": "",
    "doc_url": "https://github.com/Rrailnechex/Blender-Bake-Texture-Atlas-In-eevee",
    "category": "Render",
    "support": "EXPERIMENTAL",
    # "support": 'COMMUNITY',

}

# TODO: handle render settings properly
# TODO: create authomatick setup for bg plane and BGPlane() material
# TODO: create authomatick setup for Main sheder and MAinShader() material
# TODO: create packed addon
# TODO: add ability to bake anything in eevee. Convert mesh to UV > create new attributes to store original world position, normals, etc > bake


################################################################
# Vars

bpy.types.Scene.node_group_name = bpy.props.StringProperty(
    name="Master shader",
    description="Enter The Master shader name",
    default="Baker.MainShader()",
)

################################################################
# UI


class BAKER_TA_main_panel(bpy.types.Panel):
    bl_label = "Pipline - Bake Texture Atlas"
    bl_idname = 'PIPLINE_BAKE_TA'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Pipline - Bake Texture Atlas"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.label(text="Guide")
        row = layout.row()
        row.label(
            text="    0. Enter Main Shader name, so script can svitch connection in it an render different passes")
        row = layout.row()
        row.label(
            text="    1. Select camera(s), so each of them will be rendered and saved to default folder")
        row = layout.row()
        row.label(
            text='    2. Set camera`s name to TA name, so each image will have base name + postfix')
        row = layout.row()
        row.label(text='    3. Bake')
        row = layout.row()
        layout.prop(scene, "node_group_name")
        row = layout.row()
        row.operator("shader.render_multiple_ta",
                     text="Bake texture atlases")


'''Work only as installed addon
class ProgressBar():

    ammount_of_rander_cycles = len(bpy.context.selected_objects) * 3
    progressbar_one_unit = int(100 / ammount_of_rander_cycles)

    def show_progress_bar(context):
        wm = context.window_manager
        wm.progress_begin(0, 100)  # Set the range of the progress bar (0-100)
        wm.progress_update(0)  # Initialize the progress bar

    def hide_progress_bar(context):
        wm = context.window_manager
        wm.progress_end()  # Close the progress bar
        bpy.ops.wm.progress_update(ProgressBar.progressbar_one_unit)
'''
################################################################
# Button action


class RENDER_OT_MULTIPLE_TA(bpy.types.Operator):
    bl_label = "Bake texture atlases"
    bl_idname = 'shader.render_multiple_ta'

    def execute(self, context):

        # ProgressBar.show_progress_bar(context)

        Baker.performe_baking(self)

        # ProgressBar.hide_progress_bar(context)

        return {'FINISHED'}


############################
# Bake handlers
class Baker():

    global node_group_name
    # global save_path

    node_group_name = bpy.context.scene.node_group_name

    def BSDF_baker_switcher(node_group_name: str, switch: bool) -> None:
        if switch:
            procedures.link_switcher(node_group_name,
                                     "OutPreviewBakerData", "OutPreview")
        else:
            procedures.link_switcher(
                node_group_name, "OutPreviewBSF", "OutPreview")

    """ def do_in_bake_mode(func):
        # enter_bake_mode
        Baker.BSDF_baker_switcher(node_group_name, True)

        func()

        # exit_bake_mode
        Baker.BSDF_baker_switcher(node_group_name, False)
    """

    def bake_selected_cameras(node_group_name, save_path):

        cameras_names_to_render = bpy.context.selected_objects

        for i in range(len(cameras_names_to_render)):

            cam = cameras_names_to_render[i]
            bpy.context.scene.camera = cam
            file_base_name = bpy.context.scene.camera.name

            procedures.Albedo(node_group_name, save_path, file_base_name)
            procedures.ORM(node_group_name, save_path, file_base_name)
            procedures.Normal(node_group_name, save_path, file_base_name)

    def performe_baking(self):
        # enter_bake_mode
        Baker.BSDF_baker_switcher(node_group_name, True)
        oroginal_save_path = os.path.dirname(
            bpy.context.scene.render.filepath)

        Baker.bake_selected_cameras(node_group_name, oroginal_save_path)

        # exit_bake_mode
        Baker.BSDF_baker_switcher(node_group_name, False)


############################
# Bake scenarious
class procedures():

    def link_switcher(node_group_name: object, node_from: str, node_to: str) -> None:
        node_group = bpy.data.node_groups.get(node_group_name)

        point1 = node_group.nodes[node_from]
        point2 = node_group.nodes[node_to]

        def create_node_link(point1, point2):
            links = point1.id_data.links
            return links.new(point1, point2)

        create_node_link(point1.outputs[0], point2.inputs[0])

    def BSDF_baker_togler(node_group_name: str, switch: bool) -> None:
        if switch:
            procedures.link_switcher(node_group_name,
                                     "OutPreviewBakerData", "OutPreview")
        else:
            procedures.link_switcher(
                node_group_name, "OutPreviewBSF", "OutPreview")

    def Albedo(node_group_name: str, save_path: str, file_base_name: str) -> None:

        bpy.context.scene.render.image_settings.color_depth = '8'
        bpy.context.scene.eevee.use_gtao = False

        bpy.context.scene.view_settings.view_transform = 'Standard'
        bpy.context.scene.view_settings.look = 'None'
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'

        procedures.link_switcher(
            node_group_name, "TargetAlbedo", "TargetSwitcher")

        bpy.data.materials["Baker.BGPlanes"].node_tree.nodes["Group"].inputs[0].default_value = 0
        bpy.context.scene.render.image_settings.color_mode = 'RGBA'
        bpy.data.scenes["TrimTextures/"].render.filepath = save_path + \
            "\\" + file_base_name + "+Albedo"
        bpy.context.scene.use_nodes = True  # PPSharpen

        bpy.data.scenes["TrimTextures/"].node_tree.nodes["Filter.001"].inputs[0].default_value = 0.250

        bpy.ops.render.render(write_still=True)

        bpy.data.scenes["TrimTextures/"].node_tree.nodes["Filter.001"].inputs[0].default_value = 0

    def ORM(node_group_name: str, save_path: str, file_base_name: str) -> None:

        bpy.context.scene.render.image_settings.color_depth = '8'
        bpy.context.scene.eevee.use_gtao = False

        bpy.context.scene.view_settings.view_transform = 'Raw'
        bpy.context.scene.view_settings.look = 'None'
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'

        procedures.link_switcher(
            node_group_name, "TargetORM", "TargetSwitcher")

        bpy.context.scene.eevee.gtao_distance = 0.1

        bpy.data.materials["Baker.BGPlanes"].node_tree.nodes["Group"].inputs[0].default_value = 0
        bpy.context.scene.render.image_settings.color_mode = 'RGB'
        bpy.data.scenes["TrimTextures/"].render.filepath = save_path + \
            "\\" + file_base_name + "+ORM"
        bpy.context.scene.use_nodes = False  # PPSharpen

        bpy.ops.render.render(write_still=True)

    def Normal(node_group_name: str, save_path: str, file_base_name: str) -> None:

        bpy.context.scene.render.image_settings.color_depth = '16'
        bpy.context.scene.eevee.use_gtao = False

        bpy.context.scene.view_settings.view_transform = 'Raw'
        bpy.context.scene.view_settings.look = 'None'
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'

        procedures.link_switcher(
            node_group_name, "TargetNormol", "TargetSwitcher")

        bpy.data.materials["Baker.BGPlanes"].node_tree.nodes["Group"].inputs[0].default_value = 1
        bpy.context.scene.render.image_settings.color_mode = 'RGB'
        bpy.data.scenes["TrimTextures/"].render.filepath = save_path + \
            "\\" + file_base_name + "+Normal"
        bpy.context.scene.use_nodes = False  # PPSharpen

        bpy.ops.render.render(write_still=True)


################################################################
# Registration
_classes = [BAKER_TA_main_panel,
            RENDER_OT_MULTIPLE_TA,
            ]


def register():
    bpy.utils.register_class(BAKER_TA_main_panel)
    bpy.utils.register_class(RENDER_OT_MULTIPLE_TA)

    # for cls in _classes:
    #     bpy.utils.register_class(cls)


def unregister():
    bpy.utils.unregister_class(BAKER_TA_main_panel)
    bpy.utils.unregister_class(RENDER_OT_MULTIPLE_TA)

    # for cls in _classes:
    #     bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

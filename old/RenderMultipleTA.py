import bpy
from easybpy import *
import os
from RenderTextureAtlas import render_fullTA

# get_objects()
# select_all_cameras()
# get_collection()

cameras_names_to_render = so()


def RenderMultipleTA(cameras_names_to_render):
    for i in range(len(cameras_names_to_render)):
        render_fullTA(cameras_names_to_render[i])

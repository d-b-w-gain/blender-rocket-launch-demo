"""
Blender rocket launch demo generator.

Run from Blender's Python console or with:
blender --python scripts/rocket_launch_demo.py
"""

import bpy


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def create_scene():
    clear_scene()

    # TODO: Build procedural rocket, launch animation, smoke/exhaust effects,
    # camera, lighting, and render settings from the reference material.


if __name__ == "__main__":
    create_scene()

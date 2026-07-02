"""
Blender rocket launch demo generator.

Run from the project root with:
& "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Blender\\blender.exe" --python scripts\\rocket_launch_demo.py
"""

import os
from pathlib import Path

import bpy
from mathutils import Vector


def find_project_root():
    candidates = []

    env_root = os.environ.get("BLENDER_ROCKET_PROJECT_ROOT")
    if env_root:
        candidates.append(Path(env_root).expanduser().resolve())

    script_path = Path(__file__).resolve()
    candidates.extend(script_path.parents)
    candidates.extend(Path.cwd().resolve().parents)
    candidates.append(Path.cwd().resolve())
    candidates.append(Path.home() / "Documents" / "Projects" / "blender-rocket-launch-demo")

    for candidate in candidates:
        if (
            (candidate / "assets").is_dir()
            and (candidate / "reference").is_dir()
            and (candidate / "scripts").is_dir()
        ):
            return candidate

    raise FileNotFoundError(
        "Could not find the project root. Run this script from the project root, "
        "pass Blender the full path to scripts/rocket_launch_demo.py, or set "
        "BLENDER_ROCKET_PROJECT_ROOT to the project folder."
    )


PROJECT_ROOT = find_project_root()
ASSETS_DIR = PROJECT_ROOT / "assets"
REFERENCE_DIR = PROJECT_ROOT / "reference"
RENDERS_DIR = PROJECT_ROOT / "renders"
CACHE_DIR = RENDERS_DIR / "cache"
GENERATED_BLEND_PATH = RENDERS_DIR / "rocket_launch_demo.generated.blend"
ROCKET_TEXTURE_DIR = ASSETS_DIR / "rocket" / "blender" / "textures"

FRAME_START = 1
LAUNCH_FRAME = 40
FRAME_END = 200
ROCKET_LAUNCH_HEIGHT = 90.0
ROCKET_BLEND_OBJECT_NAME = "BezierCurve.002"
DEFAULT_CAMERA_LOCATION = (0.0, -12.0, 6.0)
DEFAULT_CAMERA_ROTATION = (1.109319, 0.0, 0.0)
DEFAULT_LIGHT_LOCATION = (4.0, 1.0, 6.0)
GENERATED_COLLECTIONS = (
    "Rocket",
    "Outward Smoke",
    "Rocket Trail",
    "Lighting",
    "Camera",
    "Render Helpers",
)
ROCKET_ASSET_CANDIDATES = (
    ASSETS_DIR / "rocket" / "blender" / "source" / "Sketchfab_2022_03_01_00_10_13.blend",
    ASSETS_DIR / "rocket" / "Sketchfab_2022_03_01_00_10_13.blend",
    ASSETS_DIR / "rocket" / "rocket.glb",
    ASSETS_DIR / "rocket" / "gltf" / "scene.gltf",
)
ROCKET_MATERIAL_NAME = "Rocket Neutral White"


def ensure_project_paths():
    """Create generated-output folders and validate checked-in inputs."""
    missing_dirs = [path for path in (ASSETS_DIR, REFERENCE_DIR) if not path.exists()]
    if missing_dirs:
        formatted = "\n".join(f"- {path}" for path in missing_dirs)
        raise FileNotFoundError(f"Required project directories are missing:\n{formatted}")

    RENDERS_DIR.mkdir(exist_ok=True)
    CACHE_DIR.mkdir(exist_ok=True)


def resolve_rocket_asset():
    for candidate in ROCKET_ASSET_CANDIDATES:
        if candidate.exists():
            return candidate

    candidates = "\n".join(f"- {path}" for path in ROCKET_ASSET_CANDIDATES)
    raise FileNotFoundError(
        "No rocket asset was found. Download or extract the Sketchfab rocket asset "
        "into one of these expected locations:\n"
        f"{candidates}"
    )


def remove_collection(collection):
    for child in list(collection.children):
        remove_collection(child)
    for obj in list(collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.collections.remove(collection)


def clear_scene():
    for obj in list(bpy.data.objects):
        if obj.type not in {"CAMERA", "LIGHT"}:
            bpy.data.objects.remove(obj, do_unlink=True)

    for collection_name in GENERATED_COLLECTIONS:
        collection = bpy.data.collections.get(collection_name)
        if collection:
            remove_collection(collection)

    for collection in list(bpy.context.scene.collection.children):
        if not collection.objects and not collection.children:
            bpy.data.collections.remove(collection)


def create_collection(name):
    existing = bpy.data.collections.get(name)
    if existing:
        return existing

    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)
    return collection


def create_collections():
    return {name: create_collection(name) for name in GENERATED_COLLECTIONS}


def ensure_default_camera_and_light(collections):
    camera = bpy.data.objects.get("Camera")
    if camera is None:
        bpy.ops.object.camera_add(location=DEFAULT_CAMERA_LOCATION, rotation=DEFAULT_CAMERA_ROTATION)
        camera = bpy.context.object
        camera.name = "Camera"
    bpy.context.scene.camera = camera
    link_object_to_collection(camera, collections["Camera"])

    light = bpy.data.objects.get("Light")
    if light is None:
        bpy.ops.object.light_add(type="POINT", location=DEFAULT_LIGHT_LOCATION)
        light = bpy.context.object
        light.name = "Light"
    link_object_to_collection(light, collections["Lighting"])


def configure_timeline():
    scene = bpy.context.scene
    scene.frame_start = FRAME_START
    scene.frame_end = FRAME_END
    scene.frame_set(FRAME_START)


def configure_render_defaults():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 64
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.fps = 24
    scene.render.filepath = str(RENDERS_DIR / "rocket_launch_demo_")

    scene.view_settings.view_transform = "Filmic"
    scene.view_settings.look = "Medium High Contrast"
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1


def link_object_to_collection(obj, collection):
    if obj.name not in collection.objects:
        collection.objects.link(obj)

    for current_collection in list(obj.users_collection):
        if current_collection != collection:
            current_collection.objects.unlink(obj)


def imported_objects(before_names):
    return [obj for obj in bpy.data.objects if obj.name not in before_names]


def import_blend_object(asset_path, object_name):
    with bpy.data.libraries.load(str(asset_path), link=False) as (source, target):
        if object_name not in source.objects:
            available = "\n".join(f"- {name}" for name in source.objects)
            raise ValueError(
                f"Could not find tutorial rocket object {object_name!r} in {asset_path}.\n"
                f"Available objects:\n{available}"
            )
        target.objects = [object_name]
    return [obj for obj in target.objects if obj]


def import_rocket_asset(asset_path):
    before_names = set(bpy.data.objects.keys())

    if asset_path.suffix.lower() in {".glb", ".gltf"}:
        bpy.ops.import_scene.gltf(filepath=str(asset_path))
        return imported_objects(before_names)

    if asset_path.suffix.lower() == ".blend":
        return import_blend_object(asset_path, ROCKET_BLEND_OBJECT_NAME)

    raise ValueError(f"Unsupported rocket asset format: {asset_path}")


def mesh_world_bounds(objects):
    mesh_objects = [obj for obj in objects if obj.type == "MESH"]
    if not mesh_objects:
        raise ValueError("The rocket asset did not import any mesh objects.")

    points = [
        obj.matrix_world @ Vector(corner)
        for obj in mesh_objects
        for corner in obj.bound_box
    ]
    min_point = Vector((min(point.x for point in points), min(point.y for point in points), min(point.z for point in points)))
    max_point = Vector((max(point.x for point in points), max(point.y for point in points), max(point.z for point in points)))
    return min_point, max_point


def make_neutral_rocket_material():
    material = bpy.data.materials.get(ROCKET_MATERIAL_NAME)
    if material:
        return material

    material = bpy.data.materials.new(ROCKET_MATERIAL_NAME)
    material.diffuse_color = (0.86, 0.84, 0.8, 1.0)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.86, 0.84, 0.8, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.45
    return material


def assign_rocket_material(objects):
    relink_rocket_textures()
    for obj in objects:
        if obj.type == "MESH":
            if not obj.data.materials:
                obj.data.materials.append(make_neutral_rocket_material())
            for slot in obj.material_slots:
                if slot.material and slot.material.name == "main_SMR":
                    slot.material.diffuse_color = (1.0, 1.0, 1.0, 1.0)


def relink_rocket_textures():
    if not ROCKET_TEXTURE_DIR.exists():
        print(f"Rocket texture folder not found, skipping texture relink: {ROCKET_TEXTURE_DIR}")
        return

    for image in bpy.data.images:
        if image.packed_file or not image.filepath:
            continue

        image_path = Path(bpy.path.abspath(image.filepath))
        if image_path.exists():
            continue

        local_path = ROCKET_TEXTURE_DIR / Path(image.filepath).name
        if local_path.exists():
            image.filepath = str(local_path)
            image.reload()
            print(f"Relinked rocket texture: {image.name} -> {local_path}")


def top_level_imported_objects(objects):
    imported = set(objects)
    return [obj for obj in objects if obj.parent not in imported]


def create_rocket_rig(collections, rocket_asset):
    rocket_collection = collections["Rocket"]

    imported = import_rocket_asset(rocket_asset)
    if not imported:
        raise ValueError(f"Rocket asset imported no objects: {rocket_asset}")

    for obj in imported:
        link_object_to_collection(obj, rocket_collection)

    rocket_object = top_level_imported_objects(imported)[0]
    rocket_object["asset_path"] = str(rocket_asset.relative_to(PROJECT_ROOT))

    if rocket_object.parent:
        rocket_object.parent = None

    reset_rocket_transform(rocket_object, imported)
    assign_rocket_material(imported)
    animate_rocket_launch(rocket_object)

    return rocket_object


def reset_rocket_transform(rocket_object, imported):
    bpy.context.view_layer.objects.active = rocket_object
    rocket_object.select_set(True)

    # Mirrors the tutorial's Alt+G, manual upright rotation, and Ctrl+A apply scale/rotation.
    rocket_object.location = (0.0, 0.0, 0.0)
    rocket_object.rotation_euler = (0.0, 0.0, 0.0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)


def animate_rocket_launch(rig):
    rig.location = (0.0, 0.0, 0.0)
    rig.keyframe_insert(data_path="location", frame=LAUNCH_FRAME)

    rig.location.z = ROCKET_LAUNCH_HEIGHT
    rig.keyframe_insert(data_path="location", frame=FRAME_END)

    for fcurve in action_fcurves(rig.animation_data.action):
        if fcurve.data_path != "location":
            continue
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = "BEZIER"
            keyframe.easing = "AUTO"
            keyframe.handle_left_type = "FREE"
            keyframe.handle_right_type = "FREE"

        if fcurve.array_index == 2:
            start, end = fcurve.keyframe_points
            start.handle_left = (LAUNCH_FRAME - 36.0, 0.0)
            start.handle_right = (LAUNCH_FRAME + 70.0, 0.0)
            end.handle_left = (FRAME_END - 28.0, -5.0)
            end.handle_right = (FRAME_END + 42.0, ROCKET_LAUNCH_HEIGHT)


def action_fcurves(action):
    if hasattr(action, "fcurves"):
        return action.fcurves

    fcurves = []
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for channelbag in getattr(strip, "channelbags", []):
                fcurves.extend(channelbag.fcurves)
    return fcurves


def save_generated_file():
    bpy.ops.wm.save_as_mainfile(filepath=str(GENERATED_BLEND_PATH))


def create_scene():
    ensure_project_paths()
    rocket_asset = resolve_rocket_asset()

    clear_scene()
    collections = create_collections()
    ensure_default_camera_and_light(collections)
    configure_timeline()
    configure_render_defaults()
    create_rocket_rig(collections, rocket_asset)
    save_generated_file()

    print(f"Rocket launch demo foundation generated: {GENERATED_BLEND_PATH}")
    print(f"Rocket asset resolved: {rocket_asset}")


if __name__ == "__main__":
    create_scene()

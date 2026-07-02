"""
Blender rocket launch demo generator.

Run from the project root with:
& "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Blender\\blender.exe" --python scripts\\rocket_launch_demo.py
"""

import os
from pathlib import Path, PureWindowsPath

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
ANIMATION_OUTPUT_DIR = RENDERS_DIR / "animation"
HDRI_DIR = ASSETS_DIR / "hdri"
OUTWARD_SMOKE_CACHE_DIR = CACHE_DIR / "outward_smoke"
ROCKET_TRAIL_CACHE_DIR = CACHE_DIR / "rocket_trail"
GENERATED_BLEND_PATH = RENDERS_DIR / "rocket_launch_demo.generated.blend"
ROCKET_TEXTURE_DIR = ASSETS_DIR / "rocket" / "blender" / "textures"
DRY_MEADOW_BACKPLATE_PATH = HDRI_DIR / "dry_meadow_backplate_2k.jpg"

FRAME_START = 1
LAUNCH_FRAME = 40
FRAME_END = 200
ROCKET_LAUNCH_HEIGHT = 90.0
ROCKET_BLEND_OBJECT_NAME = "BezierCurve.002"
OUTWARD_SMOKE_DOMAIN_SIZE = (130.0, 130.0, 55.0)
OUTWARD_SMOKE_DOMAIN_LOCATION = (0.0, 0.0, 27.5)
OUTWARD_SMOKE_INNER_START = 40
OUTWARD_SMOKE_OUTER_START = 50
OUTWARD_SMOKE_STOP = 120
OUTWARD_SMOKE_INNER_VELOCITY = 90.0
OUTWARD_SMOKE_OUTER_VELOCITY = 50.0
OUTWARD_SMOKE_INNER_DOWNWARD_BIAS = -0.18
OUTWARD_SMOKE_OUTER_DOWNWARD_BIAS = -0.28
ROCKET_TRAIL_DOMAIN_SIZE = (50.0, 50.0, 105.0)
ROCKET_TRAIL_DOMAIN_LOCATION = (0.0, 0.0, 52.5)
ROCKET_TRAIL_FIRE_VELOCITY_Z = -200.0
ROCKET_TRAIL_SMOKE_START_VELOCITY_Z = -200.0
ROCKET_TRAIL_SMOKE_SETTLED_VELOCITY_Z = -10.0
ROCKET_TRAIL_SMOKE_VELOCITY_START_FRAME = 70
ROCKET_TRAIL_SMOKE_VELOCITY_SETTLED_FRAME = 80
OUTWARD_SMOKE_DENSITY_MULTIPLIER = 14.0
OUTWARD_SMOKE_ABSORPTION_COLOR = (0.62, 0.62, 0.58, 1.0)
ROCKET_TRAIL_SMOKE_DENSITY_MULTIPLIER = 5.0
ROCKET_TRAIL_FIRE_EMISSION_STRENGTH = 24.0
ROCKET_TRAIL_FIRE_TEMPERATURE = 1450.0
FINAL_CAMERA_LOCATION = (76.0, -122.0, 70.0)
FINAL_CAMERA_TARGET = (0.0, 0.0, 52.0)
FINAL_CAMERA_ORTHO_SCALE = 190.0
FALLBACK_KEY_LIGHT_LOCATION = (-18.0, -26.0, 44.0)
FALLBACK_SUN_ROTATION = (0.75, 0.0, -0.55)
GROUND_SIZE = 170.0
BACKPLATE_DISTANCE = 118.0
RENDER_SAMPLES = 50
RENDER_RESOLUTION = (1920, 1080)
WORLD_STRENGTH = 1.35
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
    ANIMATION_OUTPUT_DIR.mkdir(exist_ok=True)
    CACHE_DIR.mkdir(exist_ok=True)
    OUTWARD_SMOKE_CACHE_DIR.mkdir(exist_ok=True)
    ROCKET_TRAIL_CACHE_DIR.mkdir(exist_ok=True)


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
        bpy.ops.object.camera_add()
        camera = bpy.context.object
        camera.name = "Camera"
    camera.location = FINAL_CAMERA_LOCATION
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = FINAL_CAMERA_ORTHO_SCALE
    camera.data.lens = 45
    camera.data.clip_end = 1000.0
    camera.data.dof.use_dof = True
    camera.data.dof.focus_distance = 120.0
    camera.data.dof.aperture_fstop = 8.0
    look_at(camera, FINAL_CAMERA_TARGET)
    bpy.context.scene.camera = camera
    link_object_to_collection(camera, collections["Camera"])

    light = bpy.data.objects.get("Light")
    if light is None:
        bpy.ops.object.light_add(type="AREA", location=FALLBACK_KEY_LIGHT_LOCATION)
        light = bpy.context.object
        light.name = "Light"
    light.location = FALLBACK_KEY_LIGHT_LOCATION
    light.data.type = "AREA"
    light.data.energy = 800.0
    light.data.size = 18.0
    link_object_to_collection(light, collections["Lighting"])

    sun = bpy.data.objects.get("Fallback Sun")
    if sun is None:
        bpy.ops.object.light_add(type="SUN", rotation=FALLBACK_SUN_ROTATION)
        sun = bpy.context.object
        sun.name = "Fallback Sun"
    sun.rotation_euler = FALLBACK_SUN_ROTATION
    sun.data.energy = 0.7
    link_object_to_collection(sun, collections["Lighting"])


def configure_timeline():
    scene = bpy.context.scene
    scene.frame_start = FRAME_START
    scene.frame_end = FRAME_END
    scene.frame_set(FRAME_START)


def configure_render_defaults():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = RENDER_SAMPLES
    scene.cycles.use_denoising = True
    scene.render.resolution_x = RENDER_RESOLUTION[0]
    scene.render.resolution_y = RENDER_RESOLUTION[1]
    scene.render.fps = 24
    scene.render.filepath = str(ANIMATION_OUTPUT_DIR / "rocket_launch_demo_")
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.compression = 15

    scene.view_settings.view_transform = "Filmic"
    scene.view_settings.look = "High Contrast"
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    configure_world_lighting()


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def configure_world_lighting():
    world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    background = nodes.get("Background")
    if background is None:
        background = nodes.new("ShaderNodeBackground")

    hdri_path = find_hdri_path()
    if hdri_path:
        environment = nodes.new("ShaderNodeTexEnvironment")
        environment.image = bpy.data.images.load(str(hdri_path), check_existing=True)
        world.node_tree.links.new(environment.outputs["Color"], background.inputs["Color"])
        background.inputs["Strength"].default_value = WORLD_STRENGTH
        world["lighting_source"] = str(hdri_path.relative_to(PROJECT_ROOT))
    else:
        background.inputs["Color"].default_value = (0.78, 0.82, 0.86, 1.0)
        background.inputs["Strength"].default_value = 0.8
        world["lighting_source"] = "fallback_world_plus_area_and_sun"


def find_hdri_path():
    if not HDRI_DIR.exists():
        return None
    for pattern in ("*.hdr", "*.exr", "*.png", "*.jpg", "*.jpeg"):
        matches = sorted(HDRI_DIR.glob(pattern))
        if matches:
            return matches[0]
    return None


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

        texture_name = Path(image.filepath).name
        if "\\" in texture_name:
            texture_name = PureWindowsPath(image.filepath).name

        local_path = ROCKET_TEXTURE_DIR / texture_name
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


def create_outward_smoke_setup(collections):
    outward_collection = collections["Outward Smoke"]
    domain = create_outward_smoke_domain(outward_collection)
    flow_objects = create_outward_smoke_flows(outward_collection)
    configure_outward_smoke_domain(domain, outward_collection)
    assign_volume_material(domain, create_outward_smoke_material())
    return domain, flow_objects


def create_outward_smoke_domain(collection):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=OUTWARD_SMOKE_DOMAIN_LOCATION)
    domain = bpy.context.object
    domain.name = "Outward Smoke Domain"
    domain.dimensions = OUTWARD_SMOKE_DOMAIN_SIZE
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    link_object_to_collection(domain, collection)
    return domain


def create_outward_smoke_flows(collection):
    inner_specs = [
        ("Outward Smoke Inner +X", (4.8, 0.0, 2.1), (1.0, 0.0, OUTWARD_SMOKE_INNER_DOWNWARD_BIAS), 3.25),
        ("Outward Smoke Inner -X", (-4.8, 0.0, 2.1), (-1.0, 0.0, OUTWARD_SMOKE_INNER_DOWNWARD_BIAS), 3.25),
        ("Outward Smoke Inner +Y", (0.0, 4.8, 2.1), (0.0, 1.0, OUTWARD_SMOKE_INNER_DOWNWARD_BIAS), 3.25),
        ("Outward Smoke Inner -Y", (0.0, -4.8, 2.1), (0.0, -1.0, OUTWARD_SMOKE_INNER_DOWNWARD_BIAS), 3.25),
    ]
    outer_specs = [
        ("Outward Smoke Outer +X", (13.5, 0.0, 1.7), (1.0, 0.0, OUTWARD_SMOKE_OUTER_DOWNWARD_BIAS), 2.5),
        ("Outward Smoke Outer -X", (-13.5, 0.0, 1.7), (-1.0, 0.0, OUTWARD_SMOKE_OUTER_DOWNWARD_BIAS), 2.5),
        ("Outward Smoke Outer +Y", (0.0, 13.5, 1.7), (0.0, 1.0, OUTWARD_SMOKE_OUTER_DOWNWARD_BIAS), 2.5),
        ("Outward Smoke Outer -Y", (0.0, -13.5, 1.7), (0.0, -1.0, OUTWARD_SMOKE_OUTER_DOWNWARD_BIAS), 2.5),
    ]

    flows = []
    for name, location, direction, radius in inner_specs:
        flow = create_smoke_flow_disc(name, location, direction, radius, collection)
        configure_smoke_flow(flow, OUTWARD_SMOKE_INNER_VELOCITY, OUTWARD_SMOKE_INNER_START)
        flows.append(flow)

    for name, location, direction, radius in outer_specs:
        flow = create_smoke_flow_disc(name, location, direction, radius, collection)
        configure_smoke_flow(flow, OUTWARD_SMOKE_OUTER_VELOCITY, OUTWARD_SMOKE_OUTER_START)
        flows.append(flow)

    return flows


def create_smoke_flow_disc(name, location, direction, radius, collection):
    normal = Vector(direction).normalized()
    rotation = normal.to_track_quat("Z", "Y").to_euler()
    bpy.ops.mesh.primitive_circle_add(
        vertices=64,
        radius=radius,
        fill_type="TRIFAN",
        location=location,
        rotation=rotation,
    )
    flow = bpy.context.object
    flow.name = name
    flow.hide_render = True
    link_object_to_collection(flow, collection)
    return flow


def configure_smoke_flow(flow, normal_velocity, start_frame):
    bpy.context.view_layer.objects.active = flow
    flow.select_set(True)
    bpy.ops.object.modifier_add(type="FLUID")
    modifier = flow.modifiers[-1]
    modifier.name = "Smoke Flow"
    modifier.fluid_type = "FLOW"

    settings = modifier.flow_settings
    settings.flow_type = "SMOKE"
    settings.flow_behavior = "INFLOW"
    settings.flow_source = "MESH"
    settings.use_plane_init = True
    settings.use_initial_velocity = True
    settings.velocity_normal = normal_velocity

    set_flow_enabled(settings, False, start_frame)
    set_flow_enabled(settings, True, start_frame + 1)
    set_flow_enabled(settings, True, OUTWARD_SMOKE_STOP)
    set_flow_enabled(settings, False, OUTWARD_SMOKE_STOP + 1)
    flow.select_set(False)


def set_flow_enabled(settings, enabled, frame):
    settings.use_inflow = enabled
    settings.keyframe_insert(data_path="use_inflow", frame=frame)


def configure_outward_smoke_domain(domain, flow_collection):
    bpy.context.view_layer.objects.active = domain
    domain.select_set(True)
    bpy.ops.object.modifier_add(type="FLUID")
    modifier = domain.modifiers[-1]
    modifier.name = "Outward Smoke Domain"
    modifier.fluid_type = "DOMAIN"

    settings = modifier.domain_settings
    settings.domain_type = "GAS"
    settings.resolution_max = 196
    settings.use_collision_border_bottom = True
    settings.use_adaptive_domain = True
    settings.alpha = 0.7
    settings.beta = 0.7
    settings.use_noise = True
    settings.noise_scale = 1
    settings.noise_strength = 0.6
    settings.cache_type = "MODULAR"
    settings.cache_resumable = True
    settings.cache_frame_start = FRAME_START
    settings.cache_frame_end = FRAME_END
    settings.cache_directory = str(OUTWARD_SMOKE_CACHE_DIR)
    settings.force_collection = flow_collection
    domain.select_set(False)


def create_rocket_trail_setup(collections, rocket_object):
    trail_collection = collections["Rocket Trail"]
    domain = create_rocket_trail_domain(trail_collection)
    fire_flow = create_rocket_trail_flow(
        name="Rocket Trail Fire Flow",
        radius=1.45,
        scale_x=1.35,
        rocket_object=rocket_object,
        collection=trail_collection,
    )
    smoke_flow = create_rocket_trail_flow(
        name="Rocket Trail Smoke Flow",
        radius=1.75,
        scale_x=1.45,
        rocket_object=rocket_object,
        collection=trail_collection,
    )
    configure_rocket_trail_fire_flow(fire_flow)
    configure_rocket_trail_smoke_flow(smoke_flow)
    configure_rocket_trail_domain(domain, trail_collection)
    assign_volume_material(domain, create_rocket_trail_material())
    return domain, fire_flow, smoke_flow


def create_rocket_trail_domain(collection):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=ROCKET_TRAIL_DOMAIN_LOCATION)
    domain = bpy.context.object
    domain.name = "Rocket Trail Domain"
    domain.dimensions = ROCKET_TRAIL_DOMAIN_SIZE
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    link_object_to_collection(domain, collection)
    return domain


def create_rocket_trail_flow(name, radius, scale_x, rocket_object, collection):
    bpy.ops.mesh.primitive_circle_add(
        vertices=64,
        radius=radius,
        fill_type="TRIFAN",
        location=(0.0, 0.0, 0.25),
    )
    flow = bpy.context.object
    flow.name = name
    flow.scale.x = scale_x
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    flow.parent = rocket_object
    flow.hide_render = True
    link_object_to_collection(flow, collection)
    return flow


def configure_rocket_trail_fire_flow(flow):
    settings = add_flow_modifier(flow, "Fire Flow")
    settings.flow_type = "FIRE"
    settings.flow_behavior = "INFLOW"
    settings.flow_source = "MESH"
    settings.use_plane_init = True
    settings.use_initial_velocity = True
    settings.velocity_coord = (0.0, 0.0, ROCKET_TRAIL_FIRE_VELOCITY_Z)


def configure_rocket_trail_smoke_flow(flow):
    settings = add_flow_modifier(flow, "Smoke Flow")
    settings.flow_type = "SMOKE"
    settings.flow_behavior = "INFLOW"
    settings.flow_source = "MESH"
    settings.use_plane_init = True
    settings.use_initial_velocity = True
    settings.velocity_coord = (0.0, 0.0, ROCKET_TRAIL_SMOKE_START_VELOCITY_Z)
    settings.keyframe_insert(
        data_path="velocity_coord",
        frame=ROCKET_TRAIL_SMOKE_VELOCITY_START_FRAME,
    )
    settings.velocity_coord = (0.0, 0.0, ROCKET_TRAIL_SMOKE_SETTLED_VELOCITY_Z)
    settings.keyframe_insert(
        data_path="velocity_coord",
        frame=ROCKET_TRAIL_SMOKE_VELOCITY_SETTLED_FRAME,
    )


def add_flow_modifier(flow, name):
    bpy.context.view_layer.objects.active = flow
    flow.select_set(True)
    bpy.ops.object.modifier_add(type="FLUID")
    modifier = flow.modifiers[-1]
    modifier.name = name
    modifier.fluid_type = "FLOW"
    flow.select_set(False)
    return modifier.flow_settings


def configure_rocket_trail_domain(domain, flow_collection):
    bpy.context.view_layer.objects.active = domain
    domain.select_set(True)
    bpy.ops.object.modifier_add(type="FLUID")
    modifier = domain.modifiers[-1]
    modifier.name = "Rocket Trail Domain"
    modifier.fluid_type = "DOMAIN"

    settings = modifier.domain_settings
    settings.domain_type = "GAS"
    settings.resolution_max = 196
    settings.use_collision_border_bottom = True
    settings.use_adaptive_domain = True
    settings.alpha = -0.5
    settings.beta = -0.5
    settings.use_noise = False
    settings.flame_vorticity = 0.2
    settings.cache_type = "MODULAR"
    settings.cache_resumable = True
    settings.cache_frame_start = FRAME_START
    settings.cache_frame_end = FRAME_END
    settings.cache_directory = str(ROCKET_TRAIL_CACHE_DIR)
    settings.force_collection = flow_collection
    domain.select_set(False)


def create_ground_plane(collections):
    helper_collection = collections["Render Helpers"]
    bpy.ops.mesh.primitive_plane_add(size=GROUND_SIZE, location=(0.0, 0.0, -0.02))
    ground = bpy.context.object
    ground.name = "Launch Field Ground"
    material = bpy.data.materials.new("Launch Field Ground Material")
    material.diffuse_color = (0.28, 0.25, 0.17, 1.0)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.28, 0.25, 0.17, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.86
    ground.data.materials.append(material)
    link_object_to_collection(ground, helper_collection)
    return ground


def create_environment_backplate(collections):
    if not DRY_MEADOW_BACKPLATE_PATH.exists():
        return None

    helper_collection = collections["Render Helpers"]
    camera = bpy.context.scene.camera
    direction = (Vector(FINAL_CAMERA_TARGET) - camera.location).normalized()
    location = Vector(FINAL_CAMERA_TARGET) + direction * BACKPLATE_DISTANCE

    bpy.ops.mesh.primitive_plane_add(size=1.0, location=location)
    backplate = bpy.context.object
    backplate.name = "Dry Meadow Backplate"
    backplate.rotation_euler = (camera.location - backplate.location).to_track_quat("Z", "Y").to_euler()
    aspect = RENDER_RESOLUTION[0] / RENDER_RESOLUTION[1]
    backplate.scale = (FINAL_CAMERA_ORTHO_SCALE * aspect * 0.62, FINAL_CAMERA_ORTHO_SCALE * 0.62, 1.0)

    material = bpy.data.materials.new("Dry Meadow Backplate Material")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    image_node = nodes.new("ShaderNodeTexImage")
    image_node.image = bpy.data.images.load(str(DRY_MEADOW_BACKPLATE_PATH), check_existing=True)
    if bsdf:
        links.new(image_node.outputs["Color"], bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 1.0
    backplate.data.materials.append(material)
    link_object_to_collection(backplate, helper_collection)
    return backplate


def assign_volume_material(domain, material):
    domain.data.materials.clear()
    domain.data.materials.append(material)


def clear_material_nodes(material):
    material.use_nodes = True
    nodes = material.node_tree.nodes
    for node in list(nodes):
        nodes.remove(node)
    return nodes, material.node_tree.links


def create_outward_smoke_material():
    material = bpy.data.materials.new("Outward Smoke Volume")
    material["density_multiplier"] = OUTWARD_SMOKE_DENSITY_MULTIPLIER
    nodes, links = clear_material_nodes(material)

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (520, 0)
    volume = nodes.new("ShaderNodeVolumePrincipled")
    volume.location = (280, 0)
    volume.inputs["Color"].default_value = (0.64, 0.64, 0.6, 1.0)
    volume.inputs["Absorption Color"].default_value = OUTWARD_SMOKE_ABSORPTION_COLOR

    info = nodes.new("ShaderNodeVolumeInfo")
    info.location = (-520, 40)
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-300, 40)
    ramp.color_ramp.elements[0].position = 0.16
    ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    ramp.color_ramp.elements[1].position = 0.78
    ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    density = nodes.new("ShaderNodeMath")
    density.location = (-80, 40)
    density.operation = "MULTIPLY"
    density.inputs[1].default_value = OUTWARD_SMOKE_DENSITY_MULTIPLIER

    links.new(info.outputs["Density"], ramp.inputs["Factor"])
    links.new(ramp.outputs["Color"], density.inputs[0])
    links.new(density.outputs["Value"], volume.inputs["Density"])
    links.new(volume.outputs["Volume"], output.inputs["Volume"])
    return material


def create_rocket_trail_material():
    material = bpy.data.materials.new("Rocket Trail Fire Smoke Volume")
    material["smoke_density_multiplier"] = ROCKET_TRAIL_SMOKE_DENSITY_MULTIPLIER
    material["fire_emission_strength"] = ROCKET_TRAIL_FIRE_EMISSION_STRENGTH
    material["fire_temperature"] = ROCKET_TRAIL_FIRE_TEMPERATURE
    nodes, links = clear_material_nodes(material)

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (700, 0)
    volume = nodes.new("ShaderNodeVolumePrincipled")
    volume.location = (460, 0)
    volume.inputs["Color"].default_value = (0.58, 0.58, 0.55, 1.0)
    volume.inputs["Absorption Color"].default_value = (0.58, 0.58, 0.55, 1.0)
    volume.inputs["Temperature"].default_value = ROCKET_TRAIL_FIRE_TEMPERATURE

    info = nodes.new("ShaderNodeVolumeInfo")
    info.location = (-640, 80)

    smoke_ramp = nodes.new("ShaderNodeValToRGB")
    smoke_ramp.location = (-420, 120)
    smoke_ramp.color_ramp.elements[0].position = 0.18
    smoke_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    smoke_ramp.color_ramp.elements[1].position = 0.86
    smoke_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    smoke_density = nodes.new("ShaderNodeMath")
    smoke_density.location = (-180, 120)
    smoke_density.operation = "MULTIPLY"
    smoke_density.inputs[1].default_value = ROCKET_TRAIL_SMOKE_DENSITY_MULTIPLIER

    fire_ramp = nodes.new("ShaderNodeValToRGB")
    fire_ramp.location = (-420, -140)
    fire_ramp.color_ramp.elements[0].position = 0.38
    fire_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    fire_ramp.color_ramp.elements[1].position = 0.9
    fire_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    fire_strength = nodes.new("ShaderNodeMath")
    fire_strength.location = (-180, -140)
    fire_strength.operation = "MULTIPLY"
    fire_strength.inputs[1].default_value = ROCKET_TRAIL_FIRE_EMISSION_STRENGTH
    blackbody = nodes.new("ShaderNodeBlackbody")
    blackbody.location = (-180, -320)
    blackbody.inputs["Temperature"].default_value = ROCKET_TRAIL_FIRE_TEMPERATURE

    links.new(info.outputs["Density"], smoke_ramp.inputs["Factor"])
    links.new(smoke_ramp.outputs["Color"], smoke_density.inputs[0])
    links.new(smoke_density.outputs["Value"], volume.inputs["Density"])
    links.new(info.outputs["Flame"], fire_ramp.inputs["Factor"])
    links.new(fire_ramp.outputs["Color"], fire_strength.inputs[0])
    links.new(fire_strength.outputs["Value"], volume.inputs["Emission Strength"])
    links.new(blackbody.outputs["Color"], volume.inputs["Emission Color"])
    links.new(volume.outputs["Volume"], output.inputs["Volume"])
    return material


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
    create_ground_plane(collections)
    create_environment_backplate(collections)
    rocket_object = create_rocket_rig(collections, rocket_asset)
    create_outward_smoke_setup(collections)
    create_rocket_trail_setup(collections, rocket_object)
    save_generated_file()

    print(f"Rocket launch demo foundation generated: {GENERATED_BLEND_PATH}")
    print(f"Rocket asset resolved: {rocket_asset}")


if __name__ == "__main__":
    create_scene()

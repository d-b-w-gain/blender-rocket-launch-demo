# Blender Rocket Launch Demo Issues

Backlog goal: faithfully recreate the final rocket launch animation from the reference video, not the tutorial screen recording itself.

Reference video: https://www.youtube.com/watch?v=xjzhd62ZAKg  
Rocket model source from video description: https://sketchfab.com/3d-models/rocket-75d8f8cc8c2b4598b694edfe67e073e8  
Target Blender executable: `C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe`  
Target Blender version: 5.1.2

Faithful does not mean pixel-identical. Fluid simulation seeds, asset versions, HDRI choice, renderer changes, and hardware differences can all change the exact smoke and fire result. The acceptance target is a close recreation of the tutorial's scene, animation timing, smoke structure, flame/trail behavior, camera framing, and rendered look.

## Issue 01: Asset Intake and License Notes

Labels: `asset`, `setup`, `documentation`

Status: blocked on authenticated Sketchfab model download; source/license notes are complete.

### Summary

Prepare the rocket model used by the demo and document where it came from so the Blender script can import it consistently.

### Details

- Use the Sketchfab rocket model linked in the video description unless a replacement asset is intentionally provided.
- Place the asset under `assets/rocket/`.
- Keep the original downloaded package or exported file in that folder.
- Add a short asset note documenting source URL, author if available, license/usage terms, download date, and expected import format.
- Prefer an importable format Blender 5.1.2 supports directly, such as `.blend`, `.fbx`, `.obj`, or `.glb`.

### Acceptance Criteria

- [ ] `assets/rocket/` contains the selected rocket asset.
- [ ] The asset can be opened or imported manually in Blender 5.1.2.
- [ ] The model has its textures or required companion files stored with it.
- [x] A source/license note exists in `assets/rocket/`.
- [x] The intended import file path is recorded for use by `scripts/rocket_launch_demo.py`.

### Progress Notes

- Created `assets/rocket/SOURCE.md`.
- Created `assets/rocket/asset_manifest.json`.
- Saved `assets/rocket/sketchfab_thumbnail.jpg`.
- Official Sketchfab download endpoints returned `401 Unauthorized` without credentials, so the `.blend` model file still needs a manual authenticated download.

### Dependencies

None.

---

## Issue 02: Script Foundation and Project Paths

Labels: `python`, `blender`, `setup`

Status: foundation implemented and validated in Blender 5.1.2.

### Summary

Build the script foundation needed for repeatable scene generation from the project folder.

### Details

- Update `scripts/rocket_launch_demo.py` to run inside Blender 5.1.2.
- Define project paths for `assets/`, `reference/`, `renders/`, and cache/output folders.
- Add scene reset logic that removes default objects and stale generated objects.
- Add collection helpers for rocket, outward smoke, rocket trail, lighting, camera, and render helpers.
- Set the frame range to match the tutorial target, ending at frame 200.
- Add a clear CLI command in comments or README notes:
  `& "C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe" --python scripts\rocket_launch_demo.py`
- Save the generated `.blend` file into the project or `renders/` folder after script execution.

### Acceptance Criteria

- [x] Running the script from Blender creates a clean scene without manual setup.
- [x] The script resolves paths relative to the project folder, not the current working directory.
- [x] Required collections are created with stable names.
- [x] Timeline start/end frames are configured.
- [x] The script saves a generated `.blend` output.
- [x] Missing required assets produce a readable error message.

### Progress Notes

- Added project-root path resolution for `assets/`, `reference/`, `renders/`, and `renders/cache/`.
- Added reusable scene reset and collection helpers for rocket, smoke, trail, lighting, camera, and render helper collections.
- Added frame range, render defaults, asset path validation, and generated `.blend` save output.

### Dependencies

- Issue 01.

---

## Issue 03: Rocket Import and Launch Animation

Labels: `animation`, `asset`, `blender`

Status: tutorial-style rocket append and launch animation implemented; validated in Blender 5.1.2.

### Summary

Import the rocket asset, normalize it in the scene, and recreate the tutorial's launch motion.

### Details

- Import the rocket from `assets/rocket/`.
- Center the rocket at the world origin and orient it vertically.
- Apply or compensate for asset scale and rotation so animation behaves predictably.
- Add a simple white or neutral material override if the imported asset's viewport/material setup is distracting or broken.
- Animate the rocket location:
  - frame 40: rocket at launch position
  - frame 200: rocket approximately 90 Blender units higher
- Shape the Z animation curve so the rocket starts slower and accelerates upward, matching the tutorial's Graph Editor adjustment.

### Acceptance Criteria

- [x] The rocket appears upright and centered at frame 1.
- [x] The rocket begins moving around frame 40.
- [x] The rocket reaches the upper part of the scene by frame 200.
- [x] The motion visibly accelerates rather than easing to a stop.
- [x] The generated scene can be scrubbed in Blender to inspect the animation.

### Progress Notes

- Added Blend/GLB/glTF rocket import support, preferring and preserving the tutorial's appended `.blend` object `BezierCurve.002`.
- Mirrored the tutorial's initial object cleanup: delete the cube, keep the default camera/light, clear location, set the rocket upright, apply scale/rotation, set the `main_SMR` viewport display to white, and relink the downloaded texture folder.
- Added launch keyframes at frames 40 and 200, moving the rocket upward by 90 units.
- Approximated the tutorial's hand-shaped Graph Editor acceleration with scripted Bezier handles.

### Dependencies

- Issue 01.
- Issue 02.

---

## Issue 04: Outward Smoke Domain Setup

Labels: `mantaflow`, `smoke`, `simulation`

### Summary

Create the first gas simulation: the ground-level smoke burst that shoots outward from the rocket base.

### Details

- Create a dedicated `Outward Smoke` collection.
- Add the first gas domain around the launch area, sized similarly to the tutorial's broad domain.
- Add planar circular smoke flow objects around the rocket base.
- Configure flow behavior as inflow and animate use-flow timing:
  - off at frame 40
  - on immediately after launch
  - off again around the tutorial's end point for the base burst
- Configure outward velocity, using the tutorial's high normal velocity target as the starting point.
- Duplicate or place extra flow circles farther from the center to extend the smoke spread.
- Isolate the domain to only use the outward smoke flow collection.
- Configure adaptive domain, bottom collision, cache path, modular cache, and noise settings for later bake.

### Acceptance Criteria

- [ ] The outward smoke domain and flow objects are generated by script.
- [ ] Flow objects are in a dedicated collection and isolated from other simulations.
- [ ] Flow timing matches the tutorial's launch-window behavior.
- [ ] Cache paths for this domain are separate from the rocket trail cache.
- [ ] The domain is ready to bake from the generated `.blend`.

### Dependencies

- Issue 02.
- Issue 03.

---

## Issue 05: Outward Smoke Tuning

Labels: `mantaflow`, `smoke`, `visual-match`

### Summary

Tune the outward smoke simulation to resemble the tutorial's broad ground smoke burst.

### Details

- Bake or preview the outward smoke simulation.
- Compare against these reference frames:
  - `reference/keyframes/frame_05_06-18.jpg`
  - `reference/keyframes/frame_06_08-06.jpg`
  - `reference/keyframes/frame_07_09-54.jpg`
  - `reference/keyframes/frame_08_11-42.jpg`
- Adjust flow positions, rotations, scale, emission timing, and velocity so smoke spreads outward along the ground instead of rising too quickly.
- Tune domain density/heat behavior and noise settings to keep the burst dense but not opaque.

### Acceptance Criteria

- [ ] A baked or previewed outward smoke result exists.
- [ ] Smoke spreads broadly away from the rocket base.
- [ ] Smoke remains near the ground early in the launch.
- [ ] The result is visually compared against the extracted keyframes.
- [ ] Any tuning values changed from the tutorial are documented in comments or notes.

### Dependencies

- Issue 04.

---

## Issue 06: Rocket Trail Domain Setup

Labels: `mantaflow`, `fire`, `smoke`, `simulation`

### Summary

Create the second gas simulation: the vertical rocket exhaust trail with separate fire and smoke flow objects parented to the rocket.

### Details

- Create a dedicated `Rocket Trail` or `Smoke Trail` collection.
- Add a tall gas domain that covers the rocket's vertical path.
- Add planar exhaust flow objects positioned under the rocket engine.
- Parent the flow objects to the rocket so they follow the launch.
- Create separate flow behavior for:
  - fire inflow
  - smoke inflow
- Configure downward initial velocity for the exhaust.
- Animate smoke velocity from a strong downward value early to a gentler value after the first phase, matching the tutorial's frame 70 to 80 transition.
- Isolate this domain to only use the rocket trail flow collection.
- Set a separate modular cache path and end frame 200.

### Acceptance Criteria

- [ ] The rocket trail domain and flow objects are generated by script.
- [ ] Exhaust flow objects follow the rocket during animation.
- [ ] Fire and smoke flows are separate and named clearly.
- [ ] The rocket trail simulation is isolated from outward smoke flows.
- [ ] Cache paths are separate from the outward smoke cache.
- [ ] The domain is ready to bake from the generated `.blend`.

### Dependencies

- Issue 03.
- Issue 04.

---

## Issue 07: Fire and Smoke Trail Materials

Labels: `materials`, `shader`, `rendering`

### Summary

Create volume materials for smoke and fire so baked simulations render like the tutorial.

### Details

- Build a smoke volume material using volume density attributes and a color ramp.
- Use a principled volume-style shader setup appropriate for Blender 5.1.2.
- Add density controls for outward smoke and rocket trail smoke.
- Add fire emission using flame attributes and a blackbody or equivalent color approach.
- Tune fire brightness and smoke density so flame remains visible through the smoke.
- Apply high-contrast color management as in the tutorial.

### Acceptance Criteria

- [ ] Outward smoke renders as dense grey/white volume.
- [ ] Rocket trail smoke renders separately from fire emission.
- [ ] Fire appears bright near the exhaust and inside the lower trail.
- [ ] Smoke density and fire brightness are exposed as script constants.
- [ ] Rendered stills show material changes without manual shader editing.

### Dependencies

- Issue 04.
- Issue 06.

---

## Issue 08: Lighting, Camera, and Render Settings

Labels: `rendering`, `camera`, `lighting`

### Summary

Set up the final scene presentation so the generated demo can be rendered without manual camera or render configuration.

### Details

- Add a ground plane or launch field surface.
- Configure world lighting or an HDRI if one is provided under `assets/hdri/`.
- Add a fallback lighting setup if no HDRI is available.
- Use Cycles for final rendering.
- Configure samples, denoise, resolution, output path, and color management.
- Add a camera view that frames the rocket, ground smoke, and vertical trail similarly to the tutorial's final scene.
- Set output paths under `renders/`.

### Acceptance Criteria

- [ ] A camera exists and is set as the active camera.
- [ ] Frame 1, mid-launch, and frame 200 are all reasonably framed.
- [ ] Cycles, denoise, samples, resolution, and output path are configured.
- [ ] The scene has usable lighting even without an HDRI.
- [ ] Render outputs go under `renders/`.

### Dependencies

- Issue 03.
- Issue 07.

---

## Issue 09: Bake and Validation Renders

Labels: `validation`, `rendering`, `simulation`

### Summary

Bake the simulations, render validation stills, and compare them against the extracted video keyframes.

### Details

- Bake the outward smoke simulation.
- Bake the rocket trail fire/smoke simulation.
- Render stills at representative frames, including early launch, broad smoke spread, mid trail, and final trail.
- Save validation renders under `renders/validation/`.
- Compare renders against the extracted keyframes and contact sheet:
  - `reference/keyframes_contact_sheet.jpg`
  - `reference/keyframes/`
- Record observations and any follow-up tuning needed.

### Acceptance Criteria

- [ ] Both simulations are baked or a clear bake failure is documented.
- [ ] Validation stills exist under `renders/validation/`.
- [ ] Renders are compared to the keyframes, not just checked for script success.
- [ ] The generated `.blend` file can be reopened with baked caches available.
- [ ] A short preview animation path is documented.

### Dependencies

- Issue 05.
- Issue 06.
- Issue 07.
- Issue 08.

---

## Issue 10: Optional Parity Polish

Labels: `polish`, `visual-match`, `optional`

### Summary

Tune the faithful recreation after the first full bake/render pass to get closer to the video's final look.

### Details

- Adjust smoke density, color ramps, and opacity.
- Tune flame brightness, color, and trail length.
- Adjust flow object positions, rotations, sizes, and timings.
- Refine camera distance, lens, and composition.
- Choose or add a closer HDRI/background if needed.
- Tune render samples and resolution for final output quality.
- Update notes with the final settings that produced the best result.

### Acceptance Criteria

- [ ] Final stills are closer to the reference than the first validation pass.
- [ ] Important tuning changes are documented.
- [ ] The final scene remains reproducible from script plus assets.
- [ ] Final render settings are suitable for a full animation render.

### Dependencies

- Issue 09.

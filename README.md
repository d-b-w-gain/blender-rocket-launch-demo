# Blender Rocket Launch Demo

This repository is a reproducibility experiment for turning a Blender rocket
launch tutorial into a working, shareable Blender Python script.

The source tutorial is
[Blender Tutorial - Creating a Rocket Launch Simulation](https://www.youtube.com/watch?v=xjzhd62ZAKg)
by [Blender Made Easy](https://www.youtube.com/@BlenderMadeEasy). This project is
not affiliated with Blender Made Easy; the tutorial remains their work and should
be credited as the creative and instructional reference.

## Goal

The goal is to test how much of the tutorial can be translated into a repeatable
Blender script from the available video, transcript, and sampled keyframes. In
practical terms, the project asks:

- Can the demo be recreated without manually following the video every time?
- Does the tutorial contain enough visible detail to recover the important scene,
  simulation, timing, material, lighting, and render choices?
- Can the result become a useful open-source Blender demo that others can run,
  inspect, adapt, and improve?

The target is not a pixel-perfect copy. Fluid simulations, Blender versions,
asset choices, render hardware, and cache settings can all change the final look.
The target is a script-generated scene that captures the same idea: a rocket
launch with ground smoke, exhaust/fire trail, camera, lighting, and render setup.

## Current State

- `scripts/rocket_launch_demo.py` is the starting Blender Python entry point.
- `reference/transcript.md` contains a cleaned, timestamped transcript from the
  tutorial.
- `reference/keyframes_contact_sheet.jpg` gives a quick visual overview of
  sampled tutorial frames.
- `reference/keyframes/` contains individual sampled frames for visual checking.
- `issues.md` tracks the planned implementation work as a backlog.

## Running the Script

Once implementation begins, run the script from this repository with Blender:

```powershell
& "C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe" --python scripts\rocket_launch_demo.py
```

The script should eventually generate a `.blend` file and validation renders
under `renders/`.

## Project Layout

```text
assets/      Local models, textures, HDRIs, and notes for third-party assets.
reference/   Transcript, keyframes, and other tutorial analysis material.
renders/     Generated renders, validation stills, and Blender output files.
scripts/     Blender Python scripts.
issues.md    Implementation backlog and acceptance criteria.
```

## Attribution

Tutorial reference:
[Blender Tutorial - Creating a Rocket Launch Simulation](https://www.youtube.com/watch?v=xjzhd62ZAKg)
by Blender Made Easy.

If this project uses third-party models, textures, HDRIs, or add-ons later, each
asset should be documented with its source, author, license, and download date
before it is committed.

# CIaC Godot Handoff - 2026-05-28

## Current State

The Godot walking-view project lives at:

`viewer/liminal_ciac`

It has been renamed in the UI/project metadata from Liminal to **CIaC Simulator**. The original external Liminal project should no longer be referenced unless explicitly requested.

## Recent Viewer Changes

- Start menu now supports population selection from 12 to 1500 residents.
- The selected population is exported through the CIaC Python CLI before launch and stored at `user://ciac_selected.world.json`.
- `CiacDistrictLevel.gd` loads the selected manifest first and falls back to the bundled `assets/data/civic_floor_80_v0.world.json`.
- The shared Python world manifest generator now owns population topology logic instead of leaving scaling only in the webview.
- A 1000-resident manifest was generated and validated at `examples/world_manifests/civic_floor_1000_v0.world.json`.
- Godot now honors manifest-generated positions/paths for scaled worlds.
- Building signage/bulletin text was adjusted so side-mounted labels face the correct direction.
- Multi-level buildings now have functional lift call points. Pressing `E` on `LIFT / E` moves between ground and level two.
- Upper slabs, access landings, and visible stair treads were made collidable.

## Key Files Changed

- `ciac/world_manifest.py`
- `examples/world_manifests/civic_floor_80_v0.world.json`
- `examples/world_manifests/civic_floor_1000_v0.world.json`
- `tests/test_world_manifest_export.py`
- `viewer/liminal_ciac/project.godot`
- `viewer/liminal_ciac/scenes/Menu.tscn`
- `viewer/liminal_ciac/scripts/Menu.gd`
- `viewer/liminal_ciac/scripts/Main.gd`
- `viewer/liminal_ciac/scripts/CiacDistrictLevel.gd`
- `viewer/liminal_ciac/scripts/CiacCampusAestheticBuilder.gd`
- `viewer/liminal_ciac/scripts/CiacInteriorPrimitives.gd`
- `viewer/liminal_ciac/scripts/ServiceNodeBuilder.gd`
- `viewer/liminal_ciac/scripts/CiacStructureInteractable.gd`
- `viewer/liminal_ciac/README.md`

## Godot MCP Enhanced Install

Installed at:

`D:\Tools\godot-mcp-enhanced`

Version observed:

`0.15.1`

Codex config updated at:

`C:\Users\james\.codex\config.toml`

Added MCP server:

```toml
[mcp_servers.godot]
command = "node"
args = ["D:\\Tools\\godot-mcp-enhanced\\build\\index.js"]
env = { GODOT_PATH = "E:\\godot\\Godot_v4.6.2-stable_win64_console.exe", DEBUG = "true", ALLOWED_PROJECT_PATHS = "D:\\Projects\\CIaC\\viewer\\liminal_ciac", GODOT_MCP_SANDBOX = "strict" }
```

The optional editor addon was copied into:

`viewer/liminal_ciac/addons/godot_mcp_server`

and enabled in `viewer/liminal_ciac/project.godot`.

After restarting Codex, the new `godot` MCP tools should become available. The current session may not expose them until restart/reload.

## Validation Commands

Run from `D:\Projects\CIaC`:

```powershell
py -3.10 -m unittest discover -s tests -p "test_world_manifest*.py"
py -3.10 -m ciac validate-world examples/world_manifests/civic_floor_80_v0.world.json
py -3.10 -m ciac validate-world examples/world_manifests/civic_floor_1000_v0.world.json
& 'E:\godot\Godot_v4.6.2-stable_win64_console.exe' --headless --path 'D:\Projects\CIaC\viewer\liminal_ciac' --scene res://scenes/Menu.tscn --quit-after 5
& 'E:\godot\Godot_v4.6.2-stable_win64_console.exe' --headless --path 'D:\Projects\CIaC\viewer\liminal_ciac' --scene res://scenes/Main.tscn --quit-after 20
```

Last known result: all passed.

## Next Good Step

After Codex restart, test whether the `godot` MCP server is visible. If available, use it first for read/verify actions:

- read scene structure
- validate scripts/project
- capture screenshots
- query runtime scene tree
- inspect transforms/colliders around signs, entrances, lifts, and upper floors

Avoid widening `ALLOWED_PROJECT_PATHS` unless there is a specific reason.


# CIaC Simulator

This is a Godot 4 walking-view adaptation copied from the local Liminal project and kept inside the CIaC repository.

CIaC remains the source of truth. The start menu can generate a population-specific world manifest, then renders a first-person civic floor walkthrough.

## Run

1. Install Godot 4.2+.
2. Open `viewer/liminal_ciac/project.godot`.
3. Run the main scene.

## Controls

- `WASD`: Move
- `Shift`: Sprint
- `Space`: Jump
- `E`: Inspect the structure or infrastructure node you are looking at
- Mouse wheel: Scroll the active inspection tab
- `Esc` or `Close`: Exit inspection reading mode
- `Esc`: Toggle mouse capture / return to menu
- `R`: Return to the district spawn point

## Current CIaC Behavior

- `scenes/Main.tscn` loads `scenes/CiacDistrictLevel.tscn`.
- `scripts/CiacDistrictLevel.gd` reads the CIaC world manifest and spawns zones, paths, structures, infrastructure nodes, labels, and an inspection panel.
- The start menu can commit a population from 12 to 1500 residents, export a matching CIaC world manifest through the Python CLI, and launch that generated world.
- `scripts/CiacSpatialScale.gd` inflates human-occupied structures to walkable proportions and attaches capacity policy metadata: occupancy, modeled capacity, soft threshold, hard threshold, utilization, status, scaling strategy, recommendation, and research basis.
- Structure scale records now include modeled floor count and vertical program, so buildings can grow upward before the campus blindly replicates footprint.
- The district is arranged like a compact university campus: residential colleges around a quad, a student-union Common House, food/dining buildings, clinic/care, library/studio, and a service edge.
- `scripts/CiacCampusAestheticBuilder.gd` adds the first mature campus aesthetic pass: quad lawns, warmer stone walks, benches, lamp rhythm, tree rows, entry canopies, columns, facade plinths/cornices, window rhythm, and department signage.
- The aesthetic builder now adds multi-level envelopes: upper facades, floor bands, repeated upper windows, stair/elevator cores, balconies, roof parapets, and a common-house roof terrace.
- Floating exterior labels have been replaced with physical campus signage and in-building bulletins. Building names appear on facade sign panels; bulletin surfaces now only say `BULLETIN / E TO READ`, while structure stats, scale state, modules, and evidence are accessed through inspection.
- Multi-level buildings now include clearer upper-floor program massing, floor slabs, front-facing glass stair/lift towers, visible stair treads, handrails, landings, elevator-door cues, balconies, parapets, and roof/upper-level elements.
- `scripts/CommonHouseInteriorBuilder.gd` builds the first real interior vertical slice.
- `scripts/CiacInteriorPrimitives.gd` provides a small reusable kit for walkable floors, walls, fixtures, plaques, and labels.
- Interior fixtures can now be inspectable model objects, not just scenery. Inspectable fixtures show their parent structure, role, model effects, operating notes, linked modules, evidence card, and source summaries.
- The inspection panel now enters a reading mode: movement pauses, the mouse is released, long sections scroll, and content is split into Overview, Scale, Modules, Evidence, and Effects tabs.
- `scripts/ResidentialPodInteriorBuilder.gd` turns residential pods into small residential-college interiors with private retreat rooms, shared lounges, hygiene cores, porch thresholds, and module/source plaques.
- `scripts/QuietStudioInteriorBuilder.gd` turns the quiet studio into a library/studio interior with desks, shelves, rest alcoves, an acoustic divider, and module/source plaques.
- `scripts/FoodCommonsInteriorBuilder.gd` turns the food and protein commons into walkable dining, prep, food-safety, and protein-culture spaces.
- `scripts/CareSocialInteriorBuilder.gd` turns the care room and social commons into walkable care continuity and belonging spaces.
- `scripts/MaintenanceShopInteriorBuilder.gd` turns the maintenance shop into a walkable asset stewardship, repair, tool-library, and spare-parts space.
- `scripts/ServiceNodeBuilder.gd` turns water, energy, sanitation, and risk nodes into physical service stations with visible reserves, controls, safety boundaries, protected kiosks/pavilions, and inspectable module/source plaques.
- `scripts/CiacCampusLifeBuilder.gd`, `scripts/CiacResidentAgent.gd`, and `scripts/CiacResidentAvatar.gd` turn manifest daily events into lightweight animated resident routines: residents start from their home structures, move toward event destinations, idle near task-relevant spaces, and return home as articulated privacy-preserving avatars.
- Water, energy, sanitation, risk, and maintenance boards now display concise telemetry pulled from the manifest, while their inspection records expose the fuller metric fields.
- Structures now display scale/capacity markers in the walking world, and the campus scale board summarizes which nodes are safe to hold, nearing a soft threshold, or require expansion/duplication before the next population increase.
- `scripts/CiacStructureInteractable.gd` connects the first-person interaction loop to CIaC object inspection.
- The original Liminal scripts and assets remain available in this copied project as source material.

## Godot MCP Enhanced

Godot MCP Enhanced is installed locally at `D:\Tools\godot-mcp-enhanced` and registered in `C:\Users\james\.codex\config.toml` as the `godot` MCP server.

The MCP server is configured with:

```toml
[mcp_servers.godot]
command = "node"
args = ["D:\\Tools\\godot-mcp-enhanced\\build\\index.js"]
env = { GODOT_PATH = "E:\\godot\\Godot_v4.6.2-stable_win64_console.exe", DEBUG = "true", ALLOWED_PROJECT_PATHS = "D:\\Projects\\CIaC\\viewer\\liminal_ciac", GODOT_MCP_SANDBOX = "strict" }
```

The project also includes the optional editor addon at `addons/godot_mcp_server`, enabled in `project.godot`. After restarting Codex, the MCP tools can be used for scene reads, script validation, runtime scene-tree inspection, screenshots, and closed-loop Godot verification. Keep the allowlist scoped to this Godot project unless there is a specific reason to widen it.

## Refresh Manifest

From the CIaC repository root:

```powershell
Copy-Item examples\world_manifests\civic_floor_80_v0.world.json viewer\liminal_ciac\assets\data\civic_floor_80_v0.world.json -Force
```

## Not Yet Implemented

- Live sync with the Python viewer server
- Full resident agent routines with real schedule clocks, task completion, indoor fixture targeting, and navigation mesh pathfinding
- Dynamic runtime updates after simulation ticks inside Godot
- Research/promote workflow controls

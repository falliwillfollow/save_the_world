# CIaC Sprint 54 Execution Plan: Civic Floor World MVP

**Plan ID:** `sprint_54_civic_floor_world_mvp_v0_1`  
**Target repo:** `falliwillfollow/save_the_world`  
**Audience:** coding agent / implementation agent  
**Status:** actionable execution plan  
**Primary objective:** Build the first browser-based 3D Civic Floor World from CIaC runtime outputs, with a manifest-driven architecture that can later support Unreal, Blender, and n8n orchestration.

---

## 0. One-Sentence Goal

Create a web-first 3D civic diorama that renders CIaC model outputs as an explorable world, showing life, infrastructure systems, and stress scenarios from the same underlying simulation data.

---

## 1. Product Concept

The 3D world is not a hand-authored art scene.

It is a generated visualization of the CIaC civic floor.

```text
CIaC runtime bundle
  -> world_manifest.json
  -> web 3D viewer
  -> Life Mode / Systems Mode / Stress Mode
  -> future n8n orchestration
  -> future Unreal / Blender pipeline
```

The demo should let a visitor understand:

```text
1. What the civic floor looks like.
2. How the systems work.
3. How people spend their time.
4. What happens under stress.
5. Which assumptions are provisional.
6. Which modules are blocked by review, evidence, law, safety, or consent.
```

---

## 2. Design Philosophy

### 2.1 The world must be generated from model truth

The viewer should not invent civic meaning. It should render a `world_manifest.json` generated from compiled/simulated CIaC outputs.

### 2.2 Stylized first, photoreal later

Use simple proxy geometry first:

```text
boxes
low-poly structures
color-coded zones
paths
billboards / labels
simple animated residents
overlay ribbons / icons
```

Do not spend this sprint on asset polish.

### 2.3 Three synchronized modes

The same world should support three modes:

```text
Life Mode:
  shows people, daily rhythms, creation time, care, food, maintenance, and rest

Systems Mode:
  shows infrastructure overlays for food, water, energy, sanitation, care, labor, governance, risk

Stress Mode:
  shows scenario states, degradations, bottlenecks, failures, and recovery
```

### 2.4 Evidence on click

Every object should eventually be interrogable:

```text
what is this?
what module created it?
what assumptions support it?
what is provisional?
what review is required?
what fails under stress?
```

For v0, click cards can be simple.

---

## 3. Repo Additions

Add these paths:

```text
schemas/world_manifest.schema.json

ciac/world_manifest.py

examples/world_manifests/
  civic_floor_80_v0.world.json

viewer/world3d/
  package.json
  index.html
  src/
    App.jsx
    main.jsx
    world/
      WorldScene.jsx
      WorldManifestLoader.js
      AssetRegistry.js
      layout.js
    components/
      Structure.jsx
      Zone.jsx
      Path.jsx
      ResidentAgent.jsx
      InfrastructureNode.jsx
      OverlayPanel.jsx
      InfoCard.jsx
      ModeSwitcher.jsx
      TimelineScrubber.jsx
      Legend.jsx
    modes/
      LifeMode.jsx
      SystemsMode.jsx
      StressMode.jsx
    styles/
      app.css
    assets/
      proxy/
        README.md

docs/
  civic_floor_world_mvp.md

n8n/
  workflow_specs/
    civic_floor_world_build_pipeline.md
    civic_floor_scenario_snapshot_pipeline.md
    asset_gap_pipeline.md
```

If the repo already has preferred locations for web viewer code, adapt paths but preserve the separation:

```text
world manifest schema
Python exporter
sample committed manifest
web 3D viewer
n8n workflow specs
docs
```

---

## 4. New Artifact: World Manifest

### 4.1 Purpose

The world manifest is the 3D viewer contract.

It converts CIaC runtime/capability/node outputs into a renderable scene.

The viewer should need no Python knowledge and no internal simulator knowledge.

### 4.2 Manifest shape

Create `schemas/world_manifest.schema.json`.

Minimum required top-level fields:

```json
{
  "kind": "CivicFloorWorldManifest",
  "version": "v0",
  "world_id": "civic_floor_80_v0",
  "generated_at": "ISO_TIMESTAMP_OR_NULL",
  "source": {},
  "population": {},
  "scale": {},
  "modules": [],
  "zones": [],
  "structures": [],
  "paths": [],
  "infrastructure_nodes": [],
  "residents": [],
  "daily_events": [],
  "scenario_states": [],
  "overlays": {},
  "evidence_cards": [],
  "warnings": [],
  "failures": [],
  "unknowns": []
}
```

### 4.3 Schema details

#### `source`

```json
{
  "runtime_bundle_path": "string-or-null",
  "simulation_id": "string-or-null",
  "profile_id": "string-or-null",
  "provisional": true
}
```

#### `population`

```json
{
  "residents": 80,
  "households": 40,
  "active_scale_slider_value": 80
}
```

#### `scale`

```json
{
  "scale_class": "micro_commons|village_block|multi_block_district|town_city_layer|regional_membrane",
  "recommended_unit_size": 80,
  "implied_village_blocks": 1,
  "scaling_mode": "seed|minimal|single_node|replicated_nodes|federated_layers",
  "active_layers": [
    "village_block"
  ]
}
```

#### `modules`

Each active module:

```json
{
  "module_id": "food.hybrid_food_commons.v0_1",
  "pattern_id": "hybrid_food_commons",
  "tier": "floor_systems|operating_systems|capacity_systems|meta_systems",
  "status": "spec_only|contract_defined|pattern_implemented|simulation_connected|viewer_connected|scenario_tested|promotion_blocked",
  "review_status": "not_reviewed|review_required|reviewed|blocked",
  "provisional": true
}
```

#### `zones`

Spatial areas.

```json
{
  "id": "zone_common_core",
  "type": "common_core|residential|food|water|energy|sanitation|maintenance|care|social|mobility|green_space|service_edge",
  "label": "Common Core",
  "position": {"x": 0, "y": 0, "z": 0},
  "size": {"x": 20, "y": 1, "z": 20},
  "color_token": "common_core",
  "module_refs": ["housing.dignified_village_block.v0_1"],
  "evidence_card_id": "evidence_common_core"
}
```

#### `structures`

Renderable buildings or objects.

```json
{
  "id": "structure_common_house",
  "type": "common_house",
  "label": "Common House",
  "position": {"x": 0, "y": 0, "z": 0},
  "rotation": {"x": 0, "y": 0, "z": 0},
  "size": {"x": 12, "y": 4, "z": 8},
  "asset_key": "proxy_common_house",
  "module_refs": [
    "housing.dignified_village_block.v0_1",
    "social_cultural_commons.belonging_without_coercion.v0_1"
  ],
  "systems": ["food", "social", "governance"],
  "state": {
    "status": "normal|warning|degraded|failed|unknown",
    "occupancy": 12
  },
  "evidence_card_id": "evidence_common_house"
}
```

#### `paths`

```json
{
  "id": "path_pod_1_to_common_house",
  "type": "primary_access|secondary_social|service|emergency|garden",
  "label": "Pod 1 to Common House",
  "points": [
    {"x": -20, "y": 0, "z": 10},
    {"x": -8, "y": 0, "z": 4},
    {"x": 0, "y": 0, "z": 0}
  ],
  "accessibility": {
    "accessible": true,
    "grade_status": "unknown|modeled|review_required"
  },
  "module_refs": ["mobility_access.pedestrian_first_access_commons.v0_1"],
  "evidence_card_id": "evidence_primary_paths"
}
```

#### `infrastructure_nodes`

```json
{
  "id": "node_solar_battery",
  "type": "energy|water|food|sanitation|maintenance|care|governance|risk",
  "label": "Solar + Critical Battery",
  "position": {"x": 24, "y": 0, "z": -12},
  "asset_key": "proxy_solar_battery",
  "module_refs": ["energy.critical_load_energy_commons.v0_1"],
  "metrics": {
    "critical_load_runtime_hours": 72,
    "status": "provisional"
  },
  "evidence_card_id": "evidence_solar_battery"
}
```

#### `residents`

Residents are archetypal routine agents, not simulated real people.

```json
{
  "id": "resident_artist_01",
  "archetype": "artist|caregiver|elder|student|maintenance_steward|food_steward|researcher|child|visitor",
  "label": "Artist",
  "home_structure_id": "structure_residential_pod_1",
  "daily_profile_id": "day_artist_balanced",
  "privacy": "archetype_only",
  "position": {"x": -20, "y": 0, "z": 8}
}
```

#### `daily_events`

```json
{
  "id": "event_artist_garden_shift",
  "resident_id": "resident_artist_01",
  "time": "09:00",
  "duration_minutes": 90,
  "type": "commons_labor|passion_time|care|rest|social|learning|maintenance|food|governance",
  "label": "Garden commons shift",
  "location_id": "structure_greenhouse",
  "module_refs": ["food.hybrid_food_commons.v0_1", "labor_time.life_burden_ledger.v0_1"],
  "visual": {
    "animation_hint": "walk_work_idle",
    "icon": "garden"
  }
}
```

#### `scenario_states`

```json
{
  "id": "scenario_grid_outage_72h",
  "label": "72-Hour Grid Outage",
  "type": "energy_outage",
  "timeline": [
    {
      "timestep": 0,
      "label": "Outage begins",
      "affected_objects": ["node_solar_battery", "structure_common_house"],
      "overlays": {
        "energy": {"critical_load_status": "protected"}
      },
      "warnings": []
    }
  ],
  "status": "modeled|placeholder|not_available"
}
```

#### `overlays`

```json
{
  "food": {
    "enabled": true,
    "status": "provisional",
    "summary": "Hybrid Food Commons active"
  },
  "water": {},
  "energy": {},
  "labor_time": {},
  "governance": {},
  "risk_resilience": {}
}
```

#### `evidence_cards`

```json
{
  "id": "evidence_common_house",
  "title": "Common House",
  "summary": "Shared third place, dining, social, and governance interface.",
  "module_refs": [
    "housing.dignified_village_block.v0_1",
    "social_cultural_commons.belonging_without_coercion.v0_1"
  ],
  "assumptions": [
    "Common space ratio is provisional.",
    "Architectural/code review required."
  ],
  "review_required": [
    "building code",
    "accessibility",
    "fire/life safety"
  ],
  "status": "provisional"
}
```

---

## 5. Python Exporter

### 5.1 Add file

```text
ciac/world_manifest.py
```

### 5.2 Responsibilities

```text
- Load runtime bundle or simulation output.
- Extract population, scale, modules, capabilities, resource states.
- Generate a deterministic proxy spatial layout.
- Create zones, structures, paths, infrastructure nodes, resident archetypes, daily events, overlays, evidence cards.
- Validate against world_manifest.schema.json.
- Write JSON output.
```

### 5.3 CLI entry

Add a CLI route if the project has a CLI dispatcher.

Suggested command:

```bash
py -3.10 -m ciac export-world \
  --runtime examples/generated/webapp_runtime_bundle.json \
  --output examples/world_manifests/civic_floor_80_v0.world.json \
  --population 80
```

If existing CLI naming differs, adapt.

### 5.4 Exporter functions

```python
def build_world_manifest(runtime_bundle: dict, population: int | None = None) -> dict:
    ...

def infer_scale(population: int) -> dict:
    ...

def build_proxy_layout(population: int, scale: dict, modules: list[dict]) -> dict:
    ...

def build_zones(layout: dict, runtime_bundle: dict) -> list[dict]:
    ...

def build_structures(layout: dict, runtime_bundle: dict) -> list[dict]:
    ...

def build_paths(layout: dict, runtime_bundle: dict) -> list[dict]:
    ...

def build_infrastructure_nodes(layout: dict, runtime_bundle: dict) -> list[dict]:
    ...

def build_resident_archetypes(population: int) -> list[dict]:
    ...

def build_daily_events(residents: list[dict], layout: dict, runtime_bundle: dict) -> list[dict]:
    ...

def build_overlays(runtime_bundle: dict) -> dict:
    ...

def build_evidence_cards(world_objects: dict, runtime_bundle: dict) -> list[dict]:
    ...
```

### 5.5 Deterministic proxy layout

Do not solve procedural urban design yet.

Use a simple stable radial/courtyard layout for population 80.

Suggested positions:

```text
Common house:       center
Food commons:       center-east
Care room:          center-west
Social/cultural:    center-north
Maintenance shop:   service edge southeast
Water node:         service edge southwest
Energy node:        service edge south
Sanitation/waste:   service edge east
Greenhouse/garden:  north/east
Residential pods:   four pods around common core
Paths:              radial + loop
```

For larger populations, replicate clusters around a district spine, but v0 can still visualize only one representative block plus layer badges.

### 5.6 Deterministic resident archetypes

For v0, generate around 12 visible residents for any population.

They represent archetypes, not every resident.

```text
artist
elder
caregiver
student/apprentice
maintenance steward
food steward
researcher/maker
child
governance steward
visitor
water/energy steward
resting resident
```

Do not render 1500 individuals.

### 5.7 Privacy

The manifest must never include real residents or personal info.

Set:

```json
"privacy": "archetype_only"
```

---

## 6. Web 3D Viewer

### 6.1 Tech direction

Use a lightweight web 3D stack.

Recommended:

```text
Vite
React
React Three Fiber
@react-three/drei
three
```

If the repo already has a viewer frontend, add `world3d` as a standalone sub-view or package.

### 6.2 Viewer modes

Implement three modes:

```text
Life
Systems
Stress
```

Use a mode switcher.

#### Life Mode

Show:

```text
resident archetypes
daily movement
common meals
garden shifts
workshop work
studio/passion time
rest / quiet space
social/cultural events
```

Minimum for v0:

```text
static agents + simple path interpolation + event labels
```

#### Systems Mode

Show overlays:

```text
food
water
energy
sanitation
maintenance
care
governance
labor_time
risk_resilience
```

Minimum for v0:

```text
color-coded structures
icons
right-side overlay panel with selected system summary
```

#### Stress Mode

Show scenario selector.

For v0, support placeholder scenario states from manifest.

```text
normal
grid outage
water contamination
illness wave
drought
financial shock
```

Minimum for v0:

```text
change colors/status labels
show warnings/failures panel
show affected infrastructure nodes
```

---

## 7. Asset Registry

### 7.1 Add file

```text
viewer/world3d/src/world/AssetRegistry.js
```

### 7.2 Purpose

Map civic object types to either:

```text
proxy geometry component
future glTF asset path
icon
color token
default size
```

### 7.3 Example

```javascript
export const ASSET_REGISTRY = {
  common_house: {
    component: "box",
    color: "#d9b26f",
    defaultSize: [12, 4, 8],
    icon: "house"
  },
  residential_pod: {
    component: "box",
    color: "#d8d2c4",
    defaultSize: [10, 3, 8],
    icon: "bed"
  },
  greenhouse: {
    component: "box",
    color: "#9ad18b",
    defaultSize: [10, 3, 5],
    icon: "leaf"
  },
  solar_battery: {
    component: "box",
    color: "#f2d16b",
    defaultSize: [6, 2, 4],
    icon: "energy"
  }
}
```

Use semantic colors, not final art.

---

## 8. UI Requirements

### 8.1 Layout

The 3D viewer page should contain:

```text
top-left: title + population + scale class
top-center: mode switcher
top-right: scenario selector / timeline
left panel: legend / active overlays
right panel: selected object info card
bottom: time scrubber or daily timeline
```

### 8.2 Click behavior

Clicking any object should show:

```text
label
type
module refs
status
summary
assumptions
review required
warnings/failures if any
```

### 8.3 Hover behavior

Show lightweight label.

### 8.4 Camera

Basic orbit controls.

Defaults:

```text
camera elevated and angled
target center common house
zoom limits
pan enabled
```

### 8.5 Accessibility

Even as a prototype:

```text
keyboard-accessible mode buttons
visible labels
no meaning conveyed only by color
reduced motion toggle if possible
```

---

## 9. Sample World Manifest

Add committed sample:

```text
examples/world_manifests/civic_floor_80_v0.world.json
```

This should be generated from the exporter, but it can initially be produced from a fixture if no runtime bundle is committed.

It must validate against:

```text
schemas/world_manifest.schema.json
```

It should include:

```text
population 80
scale_class village_block
4 residential pods
common house
food commons
protein commons / duckweed greenhouse
water node
energy node
sanitation/waste node
maintenance workshop
care room
social/cultural space
mobility paths
12 resident archetypes
normal day daily events
one stress scenario placeholder
evidence cards
```

---

## 10. n8n Workflow Specs

Do not implement live n8n integration in code during this sprint unless very easy.

Add markdown workflow specs.

### 10.1 `n8n/workflow_specs/civic_floor_world_build_pipeline.md`

Workflow:

```text
Manual Trigger or GitHub Push
  -> Run CIaC validation
  -> Run CIaC simulation / export runtime
  -> Export world manifest
  -> Validate world manifest schema
  -> Build viewer/world3d
  -> Publish preview artifact or static site
  -> Create GitHub issue on failure
  -> Notify user
```

Include expected inputs:

```yaml
population: 80
scenario: normal
runtime_bundle_path: examples/generated/webapp_runtime_bundle.json
publish_target: local|github_pages|netlify|vercel|s3
```

Expected outputs:

```yaml
world_manifest_path:
viewer_build_path:
preview_url:
validation_status:
warnings:
failures:
```

### 10.2 `n8n/workflow_specs/civic_floor_scenario_snapshot_pipeline.md`

Workflow:

```text
Manual Trigger
  -> Select population
  -> Select scenario
  -> Run scenario export
  -> Generate world manifest scenario state
  -> Capture key states
  -> Generate markdown summary
  -> Create shareable scenario card
```

### 10.3 `n8n/workflow_specs/asset_gap_pipeline.md`

Workflow:

```text
World manifest generated
  -> Compare asset_key values against asset registry
  -> Identify missing assets
  -> Create GitHub issues
  -> Assign labels: proxy-needed, gltf-needed, blender-needed, unreal-later
  -> Optional AI-generated asset brief
  -> Human approval
```

### 10.4 Why n8n matters

Add this note:

```text
n8n is the orchestration layer, not the renderer. It coordinates validated CIaC artifacts, human approvals, asset gaps, publishing, and scenario snapshots.
```

---

## 11. Tests

Add tests for the Python/export side.

### 11.1 `tests/test_world_manifest_schema.py`

Cases:

```text
sample manifest validates
missing top-level kind fails
missing structures fails
invalid scale class fails
```

### 11.2 `tests/test_world_manifest_export.py`

Cases:

```text
build_world_manifest returns required top-level keys
population 80 gives village_block
manifest includes common_house
manifest includes at least one residential pod
manifest includes evidence cards
manifest includes resident archetypes
manifest includes overlays
```

### 11.3 `tests/test_world_manifest_privacy.py`

Cases:

```text
resident entries are archetype-only
no real names required
no health status exposed
no private financial fields
```

### 11.4 Existing test suite

Must still pass:

```bash
py -3.10 -m unittest discover -s tests
py -3.10 -m ciac validate patterns
```

If there is a generic validation command for schemas or examples, add world manifest validation to it.

---

## 12. Validation Commands

Add one or both:

```bash
py -3.10 -m ciac validate-world examples/world_manifests/civic_floor_80_v0.world.json
```

or:

```bash
py -3.10 -m ciac validate examples/world_manifests
```

Use whichever matches repo conventions.

---

## 13. Build Commands for Viewer

Inside `viewer/world3d`:

```bash
npm install
npm run dev
npm run build
```

If repo already has root-level package management, adapt.

### `package.json` scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

---

## 14. Minimal React Component Structure

### `App.jsx`

Responsibilities:

```text
load manifest
hold selected mode
hold selected object
hold selected scenario
render panels
render WorldScene
```

### `WorldScene.jsx`

Responsibilities:

```text
render zones
render structures
render paths
render infrastructure nodes
render residents
apply mode-specific overlays
handle click selection
```

### `LifeMode.jsx`

Responsibilities:

```text
derive visible daily events
animate or position residents
show time labels
```

### `SystemsMode.jsx`

Responsibilities:

```text
color infrastructure by selected system
show systems overlay
```

### `StressMode.jsx`

Responsibilities:

```text
apply scenario state status
highlight affected objects
show warnings/failures
```

---

## 15. Rendering Rules

### Structures

Use simple boxes with labels.

### Zones

Use transparent floor planes.

### Paths

Use tubes or flat line meshes.

### Residents

Use small capsule/sphere figures with icon labels. Do not use realistic humans in v0.

### Infrastructure Nodes

Use simple blocks or cylinders with semantic colors.

### Color tokens

Use a simple palette:

```text
housing: warm neutral
food: green
protein: bright green / teal
water: blue
energy: yellow
sanitation: brown/gray
maintenance: orange
care: pink/red
governance: purple
social: lavender
risk: black/red
mobility: slate
```

Do not over-optimize colors.

---

## 16. Mode-Specific Acceptance

### Life Mode done when:

```text
viewer loads sample manifest
resident archetypes visible
daily events visible
at least 3 resident routines shown
common house, food, work, rest, passion time are represented
```

### Systems Mode done when:

```text
clicking system overlay changes highlighted objects
right panel shows selected system summary
objects show module refs
```

### Stress Mode done when:

```text
scenario selector exists
selecting scenario changes object statuses
warnings/failures panel updates
affected objects highlighted
```

---

## 17. Evidence Card Acceptance

Clicking the common house should show:

```text
Common House
module refs
summary
assumptions
review required
status provisional
```

Clicking protein commons should show:

```text
Protein Commons
duckweed / fermentation notes
food safety review required
acceptance gate
input-dependency warning
```

Clicking energy node should show:

```text
Critical Load Energy Commons
critical load runtime if available
battery/fire review required
outage scenario state if active
```

---

## 18. Documentation

Add:

```text
docs/civic_floor_world_mvp.md
```

Include:

```text
purpose
architecture
how world manifest works
how to generate sample manifest
how to run web viewer
how to add asset mappings
what v0 does not prove
future Unreal/Blender/n8n roadmap
```

Add README note:

```markdown
## Civic Floor World MVP

The project now includes an experimental web-first 3D viewer driven by a generated `world_manifest.json`. The viewer renders CIaC outputs as a stylized civic diorama with Life, Systems, and Stress modes. It is a provisional demonstration surface only and does not prove real-world safety, legality, cost, consent, or buildability.
```

---

## 19. Safety / Trust Language

Every viewer should show a visible provisionality note:

```text
This is a provisional civic simulation. It visualizes model assumptions and stress tests. It does not certify real-world safety, legality, affordability, engineering, public health, accessibility, resident consent, or buildability.
```

Do not hide this in docs only.

---

## 20. n8n Integration Boundary

For this sprint, only write workflow specs unless implementing simple local webhooks is trivial.

Future integration should treat n8n as:

```text
orchestration
validation
artifact generation
human approval
publishing
asset-gap tracking
evidence review
scenario snapshot generation
```

Do not make n8n required for the local viewer to run.

---

## 21. Future Unreal / Blender Branch

Document future but do not implement now.

```text
world_manifest.json
  -> Blender asset maturation
  -> Unreal scene generation
  -> cinematic exports
  -> Pixel Streaming / VR later
```

The web viewer is the first public surface.

Unreal is the high-fidelity branch after the data contract proves useful.

---

## 22. Implementation Order

### Phase 1: World Manifest Contract

```text
1. Add schemas/world_manifest.schema.json
2. Add ciac/world_manifest.py
3. Add unit tests for manifest generation and validation
4. Generate sample civic_floor_80_v0.world.json
```

### Phase 2: Viewer Skeleton

```text
1. Create viewer/world3d package
2. Load sample manifest
3. Render zones, structures, paths, infrastructure nodes
4. Add camera controls
5. Add object click panel
```

### Phase 3: Three Modes

```text
1. Life Mode
2. Systems Mode
3. Stress Mode
4. Mode switcher
5. Basic legend
```

### Phase 4: Evidence Cards

```text
1. Build info card
2. Connect object evidence_card_id
3. Show assumptions and review requirements
```

### Phase 5: n8n Specs

```text
1. Add workflow spec markdowns
2. Document future orchestration
```

### Phase 6: Docs and Tests

```text
1. Add docs/civic_floor_world_mvp.md
2. README note
3. Run tests
4. Run viewer build
```

---

## 23. Acceptance Criteria

The sprint is complete when:

```text
1. A valid world_manifest.schema.json exists.
2. ciac/world_manifest.py can generate a sample manifest for population 80.
3. The sample manifest is committed at examples/world_manifests/civic_floor_80_v0.world.json.
4. Tests validate manifest generation and privacy constraints.
5. viewer/world3d loads the sample manifest.
6. Viewer renders a stylized 80-person civic floor world.
7. Viewer supports Life, Systems, and Stress modes.
8. Clicking objects shows evidence cards.
9. At least one stress scenario changes visible object state.
10. n8n workflow spec files exist for build, scenario snapshot, and asset gaps.
11. Existing Python tests still pass.
12. Viewer build succeeds.
13. Documentation explains how to run everything.
14. The viewer displays provisionality / non-certification language.
```

---

## 24. Suggested Commit Plan

```text
commit 1:
  Add world manifest schema and exporter

commit 2:
  Add sample civic_floor_80_v0.world.json and tests

commit 3:
  Add viewer/world3d skeleton and manifest loader

commit 4:
  Render zones, structures, paths, and infrastructure nodes

commit 5:
  Add Life/System/Stress modes and selected object panel

commit 6:
  Add n8n workflow specs

commit 7:
  Add docs and README note

commit 8:
  Polish tests and validation commands
```

---

## 25. Future Work After Sprint 54

Do not implement until Sprint 54 is stable.

```text
1. Generate manifests for slider checkpoints: 15, 80, 150, 300, 730, 1500.
2. Add live viewer-server endpoint for world manifest generation.
3. Add scenario frame export from simulation.
4. Add animated daily routines from labor/time model.
5. Add conventional-life comparison world.
6. Add screenshot/video capture pipeline.
7. Add GitHub Pages or static deploy workflow.
8. Add n8n live workflows.
9. Add glTF asset packs.
10. Add Blender asset maturation.
11. Add Unreal export branch.
12. Add policy/evidence drill-down panel.
13. Add external-region map view.
```

---

## 26. One-Sentence Coding Agent Instruction

Build a manifest-driven, browser-based 3D Civic Floor World MVP that renders CIaC runtime outputs as a stylized explorable settlement with Life, Systems, and Stress modes, while preserving the existing simulator as the source of truth and preparing n8n workflow specs for future artifact orchestration.

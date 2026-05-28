# CIaC Adaptation Notes

This directory is a copied and adapted Godot project derived from `E:\Project\Liminal`.

The original external Liminal project is not modified by this adaptation. CIaC owns this copy under `viewer/liminal_ciac`.

## Architecture

- `project.godot` starts at `scenes/Menu.tscn`.
- The menu launches `scenes/Main.tscn`.
- `Main.tscn` keeps the Liminal player, camera, lighting, loading UI, and environment shell.
- `Main.tscn` now instances `scenes/CiacDistrictLevel.tscn` instead of the original procedural liminal level.
- `CiacDistrictLevel.gd` reads `assets/data/civic_floor_80_v0.world.json` and constructs a manifest-driven district.

## Manifest Rendering

The Godot level currently renders:

- `zones` as translucent floor overlays,
- `paths` as walkable access strips,
- `structures` as colored building volumes,
- `infrastructure_nodes` as service objects,
- `evidence_cards` as source material for the inspection panel,
- `modules` as contained capability summaries.

## Sprint 1-2 Buildout

The first inhabitable pass adds:

- `CiacSpatialScale.gd` for human-scale minimum dimensions by structure type.
- A university/campus layout model:
  - Common House as a student-union commons on the main walk.
  - Residential pods as residential colleges around the quad.
  - Food Commons and Protein Commons as dining/food research buildings near the north walk.
  - Care Room as a campus clinic/wellbeing point.
  - Quiet Studio as a library/studio building.
  - Maintenance, water, energy, and sanitation on a service edge.
- Campus quad, main walk, dining walk, residential walk, and service walk paths.
- Entry pads for non-interior structures.
- A return-to-spawn action on `R`.
- A walkable Common House vertical slice with walls, a doorway, meal commons, kitchen/service counter, governance table, quiet nooks, labels, and inspectable plaques.

## Sprint 3-4 Buildout

The next inhabitable pass adds reusable interior primitives and expands the campus beyond the Common House:

- `CiacInteriorPrimitives.gd` centralizes common walkable building pieces: boxes with collision, open-shell rooms, labels, materials, and inspectable plaques.
- `ResidentialPodInteriorBuilder.gd` models residential pods as residential-college houses rather than replicated abstract blocks:
  - private retreat rooms,
  - shared lounge and resident notice board,
  - hygiene/linen core,
  - porch seating and threshold planter,
  - inspectable module/source plaque.
- `QuietStudioInteriorBuilder.gd` models the quiet studio as a library/studio building:
  - studio desks,
  - reference shelves,
  - rest alcoves,
  - acoustic divider and soft planting buffer,
  - inspectable module/source plaque.

This keeps population growth visually legible: campus structures can become larger and more specific before they become duplicated wholesale.

## Sprint 5-6 Buildout

The next campus pass makes the daily-life and care buildings inhabitable:

- `FoodCommonsInteriorBuilder.gd` gives the food commons a wash/prep run, cooking island, pantry, cold storage, serving rail, shared tables, handwash station, clean/dirty divider, food-safety board, and module/source plaque.
- The same builder gives the protein commons a distinct research/production interior with culture bench, fermentation cabinets, ingredient cold cabinet, process log desk, resident tasting counter, safety board, and module/source plaque.
- `CareSocialInteriorBuilder.gd` gives the care room a reception desk, continuity table, medication continuity cabinet, privacy screen, recovery bench, protocol board, and module/source plaque.
- The same builder gives the social commons an open circle, maker table, materials shelf, story wall, low-stimulus nook, and module/source plaque.
- `CiacSpatialScale.gd` now treats protein commons and social commons as explicit human-occupied building types rather than generic volumes.

This moves the model closer to a campus that can be walked as a civic system: food, care, rest, residence, governance, and study now each have an interior grammar.

## Sprint 7-8 Buildout

The next service-edge pass makes maintenance and infrastructure legible in first person:

- `CiacInteriorPrimitives.gd` now includes a collision-ready cylinder primitive for tanks and vertical service equipment.
- `MaintenanceShopInteriorBuilder.gd` gives the maintenance shop a repair bay, tool library, parts inventory, asset registry board, queue priority rail, steward workbench, PPE locker, and module/source plaque.
- `ServiceNodeBuilder.gd` replaces simple infrastructure blocks with physical stations:
  - water source/reserve tanks, pump/quality canopy, well head, quality bench, reserve gauge, pipe run, and module/source plaque,
  - open solar tables plus a protected energy control kiosk for the battery cabinet, inverter cabinet, critical-load board, cable run, and module/source plaque,
  - sanitation clean/dirty sides, route boards, blackwater safety gate, PPE, handwash, separated waste bins, emergency fallback crate, and module/source plaque,
  - covered risk/governance pavilion with scenario board, dependency map table, decision log bench, and module/source plaque.

This pass is intentionally explanatory rather than photorealistic: a resident, reviewer, or builder should be able to walk the service edge and see what is being tracked, what must be maintained, and where evidence is attached.

## Sprint 9-10 Buildout

The first life pass makes the campus feel inhabited without pretending to be a full agent simulation:

- `CiacDistrictLevel.gd` now records world positions for manifest structures and infrastructure nodes.
- `CiacCampusLifeBuilder.gd` reads `daily_events` from the manifest and places up to twelve lightweight resident routine markers near their event locations.
- `CiacResidentAgent.gd` gives each marker a slow local motion loop so daily routines can be perceived while walking the district.
- Labels above each marker show the routine being represented, such as studio practice, care continuity check, garden commons shift, protected play/rest, or water and energy check.

This is deliberately modest: it is a visual bridge from manifest life events into the embodied world. It does not yet solve schedule execution, pathfinding, indoor task completion, privacy filters, or actual resident simulation.

## Sprint 11-12 Buildout

The interaction pass turns high-signal interior and service fixtures into inspectable model objects:

- `CiacInteriorPrimitives.gd` now provides `fixture_box` and `fixture_cylinder` helpers.
- Fixture records include:
  - parent structure or node,
  - fixture role,
  - linked module refs,
  - inherited evidence card,
  - modeled effects,
  - operating notes.
- `CiacDistrictLevel.gd` renders fixture-specific inspection sections before the shared module/evidence/source chain.
- Major fixtures now answer "why is this here?" while walking:
  - Common House meal, pantry, kitchen, governance, decision, and quiet-boundary fixtures.
  - Residential pod retreat, lounge, notice, and hygiene fixtures.
  - Quiet studio desk, rest, reference, and acoustic fixtures.
  - Food/protein prep, cold-chain, inventory, food-safety, culture, and cabinet fixtures.
  - Care room continuity, medication, privacy, and protocol fixtures.
  - Social commons circle, maker, and story fixtures.
  - Maintenance tool, spare, asset, and PPE fixtures.
  - Water, energy, sanitation, and risk service fixtures.

This shifts the Godot world from a visual proxy toward an embodied model browser: visible objects can carry assumptions, evidence, and model consequences.

## Sprint 13 Inspection UX

The inspection panel now behaves like a reading surface instead of a debug overlay:

- Opening inspection releases the mouse and pauses player movement.
- `Esc` or the panel `Close` button exits inspection and returns to walk mode.
- Long content can be scrolled with the mouse wheel.
- Inspection content is split into tabs:
  - Overview,
  - Modules,
  - Evidence,
  - Effects.
- `Main.gd` now closes an open inspection panel before treating `Esc` as a return-to-menu action.

## Sprint 14 Telemetry Binding

The first spatial-dashboard pass binds manifest telemetry to visible service boards:

- `CiacDistrictLevel.gd` indexes `resource_telemetry.resources` and enriches matching infrastructure nodes before they render.
- `CiacInteriorPrimitives.gd` fixture records inherit parent `metrics`, so inspecting a service board or gauge reveals the same current model fields as the underlying node.
- `ServiceNodeBuilder.gd` displays concise in-world telemetry labels:
  - water current/capacity, net/day, reserve floor, status,
  - energy current/capacity, net/day, reserve floor, critical runtime, status,
  - sanitation capability fields for hygiene access, greywater boundary, waste separation, blackwater path, worker safety, fallback,
  - risk/governance capability status and linked module count.
- `MaintenanceShopInteriorBuilder.gd` displays an asset-board summary with status, module count, occupancy, and critical spare visibility.

This is still a snapshot binding from the manifest, not a live simulation stream. It makes the embodied world truthful to the current compiled model state and prepares the path for runtime tick updates later.

## Sprint 15 Resident Routine Pathing

The resident layer now uses manifest homes and event destinations:

- `CiacCampusLifeBuilder.gd` indexes `residents` by id and joins each `daily_events` record to its resident archetype.
- Each resident route starts near `home_structure_id`, moves toward the event `location_id`, idles near a task-relevant spot, and returns home.
- Task offsets place archetypes closer to meaningful campus destinations:
  - care near the care room,
  - food/commons labor near the food commons,
  - maintenance and learning near the shop,
  - passion/rest near the quiet studio,
  - social/governance near common/social spaces.
- `CiacResidentAgent.gd` now runs a simple home-task-idle-return cycle rather than orbiting a single event point.
- Resident bodies are inspectable. Inspection shows archetype, routine, time, duration, home, destination, privacy mode, linked modules, and notes that the motion is a lightweight visualization rather than full pathfinding.

This makes the world read more like a living campus model: resident behavior is tied to homes, destinations, modules, and privacy assumptions, while still staying honest about what is not yet simulated.

## Sprint 16 Campus Scale and Capacity Overlay

The campus now exposes population scaling pressure instead of silently stretching or duplicating the footprint:

- `CiacSpatialScale.gd` attaches a scale record to every structure with occupancy, modeled capacity, soft threshold, hard threshold, utilization, pass/warn/fail status, preferred scaling strategy, recommendation, and research basis.
- Structures render small in-world scale markers, for example `PASS 12/12` or `WARN 18/35`, so scale pressure is visible while walking.
- A campus scale board near the spawn path summarizes pass/warn/fail counts and points to the next structure needing attention.
- Inspection now includes a `Scale` tab for structures and the scale board.
- The scale policies encode the current research direction:
  - small residential pods should duplicate as a small-house cluster instead of becoming huge halls,
  - common and food nodes can expand before duplicating,
  - care, quiet, and social nodes should preserve low-pressure privacy and acoustic limits,
  - maintenance and service nodes can expand at the service edge while keeping labor visibility explicit.

This is the first pass where the walking world can answer whether population growth should enlarge a structure, add a satellite, or stop for redesign before the next promoted model scale.

## Sprint 17 Campus Aesthetic Pass

The first visual maturity pass makes the district read more like a university campus and less like a blockout:

- `CiacCampusAestheticBuilder.gd` adds a procedural campus kit with lawns, warmer stone walks, benches, lamp posts, tree rows, a founders green, and a service-edge apron.
- Every manifest structure gets a simple architectural layer:
  - limestone plinth,
  - cornice,
  - system-colored facade band,
  - entry canopy,
  - front columns,
  - window rhythm,
  - department signage.
- The common house receives a more formal arcade/paving edge.
- Residential colleges receive garden thresholds.
- Maintenance receives a harder service apron.

This pass deliberately avoids external asset dependence. It establishes campus grammar first so later imported or generated assets have a coherent place to land.

## Sprint 18 Vertical Campus Pass

The campus now has vertical scale instead of reading as a one-story civic village:

- `CiacSpatialScale.gd` assigns modeled floor counts and vertical programs to structure types.
- Building heights now reflect these floor counts:
  - Common House: three levels with public commons, upper assembly/study, and roof terrace.
  - Residential colleges: two levels with ground shared space and upper private retreat rooms.
  - Food, protein, care, quiet, social, and maintenance buildings: two-level civic/support structures.
- `CiacCampusAestheticBuilder.gd` renders upper facade shells, floor bands, repeated upper windows, stair/elevator cores, balconies, roof parapets, and a Common House roof terrace.
- The inspection `Scale` tab now shows floor count and vertical program.

The current pass is primarily exterior and legibility-focused. Ground floors remain the walkable interiors; upper floors are modeled as truthful program envelopes that prepare the world for later accessible stairs, elevators, and second-floor interior scenes.

## Sprint 19 Resident Avatar Pass

The resident layer now uses procedural articulated avatars inspired by the Suburbia voxel NPC approach, implemented natively in Godot inside this repository:

- `CiacResidentAvatar.gd` builds a privacy-preserving person form from simple rigged parts:
  - hip,
  - torso,
  - pelvis,
  - head,
  - hair,
  - arms,
  - forearms,
  - legs,
  - feet,
  - archetype/privacy badge.
- `CiacResidentAgent.gd` now passes locomotion and idle state into the avatar so arms, legs, head, and torso animate during route movement and task idle.
- `CiacCampusLifeBuilder.gd` replaces cylinder residents with articulated avatars while preserving inspectable resident records.
- Palette variation is used for legibility only. It is not demographic modeling.

The Suburbia project was inspected as read-only reference material. No files were copied from or modified in that project.

## Sprint 20 Signage, Bulletins, and Deeper Verticality

The world now moves away from floating annotation text:

- Free-floating building and route labels are suppressed.
- Building names are shown as physical facade signs rather than overhead labels.
- Scale status remains visible as a color strip, while the numeric details move into inspectable in-building bulletins.
- Each human-occupied building receives a bulletin board that carries:
  - scale status,
  - occupancy/capacity,
  - modeled floor count,
  - linked module count,
  - the full inspection tabs when interacted with.
- Bulletin board surfaces now only say `BULLETIN / E TO READ`; detailed stats are available through inspection instead of being painted into the world.
- The welcome text is now a physical board near spawn instead of a floating scene label.

The vertical campus pass also deepens:

- Upper-floor slabs and program volumes make multi-level structures read as inhabited rather than just tall facades.
- Side cores now show alternating stair flights, landings, and elevator-door cues.
- Front-facing glass access towers now make vertical circulation obvious from the quad:
  - stair/lift signage,
  - ground and upper elevator doors,
  - visible stair treads,
  - handrails,
  - upper landings.
- Roof, balcony, parapet, and upper-level elements reinforce that the buildings can scale upward before duplicating across the campus.

## Interaction

`PlayerController.gd` still provides the first-person Liminal movement loop. Looking at a CIaC structure, infrastructure node, or inspectable fixture shows a prompt; pressing `E` opens the inspection panel with modules, status, evidence, review requirements, assumptions, and the first several research sources.

## Refreshing Data

Regenerate CIaC manifests in the main project, then copy the current world manifest into this Godot project:

```powershell
Copy-Item examples\world_manifests\civic_floor_80_v0.world.json viewer\liminal_ciac\assets\data\civic_floor_80_v0.world.json -Force
```

## Boundaries

This is an embodied visualization target. It does not replace the Python model, React diagnostics viewer, n8n research loop, capability policy checks, or source registry. Those remain authoritative.

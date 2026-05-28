extends RefCounted
class_name QuietStudioInteriorBuilder

const P := preload("res://scripts/CiacInteriorPrimitives.gd")
const WALL_T := 0.3
const WALL_H := 3.1
const DOOR_W := 3.2

static func build(level: Node, geometry_root: Node3D, label_root: Node3D, structure: Dictionary, base: Vector3, size: Vector3, color: Color, interactable_script: Script) -> void:
    var root := Node3D.new()
    root.name = str(structure.get("id", "quiet_studio"))
    root.position = base
    geometry_root.add_child(root)

    P.open_shell(root, size, color, WALL_T, WALL_H, DOOR_W)
    _reading_studio(root, level, interactable_script, structure, size)
    _rest_alcoves(root, level, interactable_script, structure, size)
    _library_wall(root, level, interactable_script, structure, size)
    _sensory_buffer(root, level, interactable_script, structure, size)

    P.plaque(root, level, interactable_script, "QuietStudioModulesPlaque", Vector3(-size.x * 0.5 + 0.9, 1.4, size.z * 0.5 - 2.0), structure, "Modules and sources")
    P.bulletin(root, level, interactable_script, "QuietStudioStatusBulletin", Vector3(size.x * 0.5 - 0.68, 1.65, size.z * 0.5 - 2.0), structure, "Studio bulletin")
    P.label(label_root, str(structure.get("label", "Quiet Studio")), base + Vector3(0.0, WALL_H + 0.9, 0.0), 28)
    P.label(label_root, "studio desks", base + Vector3(-3.4, 1.1, -1.6), 20)
    P.label(label_root, "rest alcoves", base + Vector3(4.5, 1.1, 2.7), 20)

static func _reading_studio(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    for index in range(3):
        var z := -size.z * 0.18 + float(index) * 2.1
        P.fixture_box(root, level, interactable_script, "StudioDesk%d" % index, Vector3(-3.8, 0.68, z), Vector3(2.4, 0.32, 0.95), Color(0.45, 0.34, 0.25), structure, "Quiet studio desk %d" % (index + 1), "Passion, learning, and evidence work surface", "labor_time.life_burden_ledger.v0_1", ["represents reclaimed time being usable for study, craft, research, or recovery"], ["Does not assign a required job or productivity obligation."])
        P.box(root, "StudioSeat%d" % index, Vector3(-2.15, 0.42, z), Vector3(0.55, 0.42, 0.55), Color(0.32, 0.46, 0.5), true)
    P.box(root, "SharedWorkTable", Vector3(0.6, 0.72, -2.2), Vector3(3.2, 0.28, 1.65), Color(0.42, 0.31, 0.25), true)

static func _rest_alcoves(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    var alcove_x := size.x * 0.5 - 2.35
    for index in range(2):
        var z := 0.8 + float(index) * 2.4
        P.box(root, "RestDivider%d" % index, Vector3(alcove_x - 1.15, 1.05, z), Vector3(0.14, 1.85, 2.0), Color(0.58, 0.55, 0.5), true)
        P.fixture_box(root, level, interactable_script, "RestBench%d" % index, Vector3(alcove_x, 0.42, z), Vector3(2.0, 0.36, 0.72), Color(0.38, 0.5, 0.48), structure, "Quiet rest alcove %d" % (index + 1), "Recovery and low-stimulation fixture", "labor_time.life_burden_ledger.v0_1", ["makes non-productive recovery time spatially visible"], ["Not a clinical care space."])

static func _library_wall(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.fixture_box(root, level, interactable_script, "LibraryShelves", Vector3(-size.x * 0.5 + 0.75, 1.45, -size.z * 0.5 + 4.6), Vector3(0.9, 2.35, 6.4), Color(0.5, 0.38, 0.27), structure, "Reference shelves", "Evidence and learning commons fixture", "labor_time.life_burden_ledger.v0_1", ["anchors research, learning, and source review in the embodied model"], ["Digital/source registry remains authoritative."])
    P.box(root, "ReferenceShelf", Vector3(0.0, 1.45, -size.z * 0.5 + 0.65), Vector3(size.x - 2.2, 2.2, 0.78), Color(0.5, 0.38, 0.27), true)

static func _sensory_buffer(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.fixture_box(root, level, interactable_script, "AcousticDivider", Vector3(2.0, 1.15, 0.2), Vector3(0.18, 2.1, 5.2), Color(0.52, 0.56, 0.56), structure, "Acoustic divider", "Low-stimulation boundary", "labor_time.life_burden_ledger.v0_1", ["separates active studio work from recovery alcoves"], ["Placeholder for acoustic design, not measured sound performance."])
    P.box(root, "SoftPlantingBuffer", Vector3(0.0, 0.5, size.z * 0.5 - 2.2), Vector3(5.6, 0.8, 0.75), Color(0.28, 0.48, 0.3), true)

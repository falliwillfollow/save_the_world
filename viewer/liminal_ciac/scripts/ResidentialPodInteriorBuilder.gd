extends RefCounted
class_name ResidentialPodInteriorBuilder

const P := preload("res://scripts/CiacInteriorPrimitives.gd")
const WALL_T := 0.3
const WALL_H := 3.15
const DOOR_W := 3.4

static func build(level: Node, geometry_root: Node3D, label_root: Node3D, structure: Dictionary, base: Vector3, size: Vector3, color: Color, interactable_script: Script) -> void:
    var root := Node3D.new()
    root.name = str(structure.get("id", "residential_pod"))
    root.position = base
    root.rotation.y = PI if base.z > 0.0 else 0.0
    geometry_root.add_child(root)

    P.open_shell(root, size, color, WALL_T, WALL_H, DOOR_W)
    _private_rooms(root, level, interactable_script, structure, size)
    _shared_lounge(root, level, interactable_script, structure, size)
    _hygiene_core(root, level, interactable_script, structure, size)
    _threshold_garden(root, size)

    P.plaque(root, level, interactable_script, "ResidentialPodModulesPlaque", Vector3(-size.x * 0.5 + 0.9, 1.4, size.z * 0.5 - 2.2), structure, "Modules and sources")
    P.bulletin(root, level, interactable_script, "ResidentialPodStatusBulletin", Vector3(size.x * 0.5 - 0.68, 1.65, size.z * 0.5 - 2.2), structure, "House bulletin")
    P.label(label_root, str(structure.get("label", "Residential Pod")), base + Vector3(0.0, WALL_H + 0.9, 0.0), 28)
    P.label(label_root, "private retreat rooms", base + _world_from_local(root, Vector3(-size.x * 0.18, 1.05, -size.z * 0.5 + 3.4)), 20)
    P.label(label_root, "shared lounge", base + _world_from_local(root, Vector3(2.0, 1.05, 0.4)), 20)

static func _private_rooms(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    var room_w := maxf((size.x - 2.4) / 4.0, 2.8)
    var room_d := minf(4.8, size.z * 0.34)
    var start_x := -size.x * 0.5 + room_w * 0.5 + 0.8
    var back_z := -size.z * 0.5 + room_d * 0.5 + 0.55
    for index in range(4):
        var room_x := start_x + float(index) * room_w
        P.box(root, "RetreatPartition%d" % index, Vector3(room_x + room_w * 0.5 - 0.06, 1.15, back_z), Vector3(0.12, 2.1, room_d), Color(0.62, 0.58, 0.52), true)
        P.fixture_box(root, level, interactable_script, "RetreatBed%d" % index, Vector3(room_x - room_w * 0.18, 0.42, back_z - 0.8), Vector3(room_w * 0.48, 0.42, 1.65), Color(0.36, 0.5, 0.58), structure, "Private retreat bed %d" % (index + 1), "Private retreat/rest fixture", "housing.dignified_village_block.v0_1", ["shows private recovery capacity inside a residential pod"], ["Represents archetypal privacy capacity, not a final bedroom count."])
        P.box(root, "RetreatDesk%d" % index, Vector3(room_x + room_w * 0.22, 0.58, back_z + 1.0), Vector3(room_w * 0.36, 0.42, 0.8), Color(0.43, 0.32, 0.24), true)
    P.box(root, "RetreatHallThreshold", Vector3(0.0, 0.08, -size.z * 0.5 + room_d + 0.85), Vector3(size.x - 1.8, 0.08, 0.65), Color(0.32, 0.45, 0.43), true)

static func _shared_lounge(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.fixture_box(root, level, interactable_script, "LoungeTable", Vector3(1.9, 0.65, 0.6), Vector3(3.8, 0.28, 1.8), Color(0.44, 0.32, 0.22), structure, "Residential lounge table", "Small-house shared living fixture", "housing.dignified_village_block.v0_1", ["shows a small-group common area distinct from the campus common house"], ["Social use should remain opt-in and low pressure."])
    P.box(root, "LoungeSeatNorth", Vector3(1.9, 0.42, -0.95), Vector3(3.6, 0.36, 0.55), Color(0.32, 0.48, 0.47), true)
    P.box(root, "LoungeSeatSouth", Vector3(1.9, 0.42, 2.05), Vector3(3.6, 0.36, 0.55), Color(0.32, 0.48, 0.47), true)
    P.fixture_box(root, level, interactable_script, "ResidentNoticeBoard", Vector3(size.x * 0.5 - 0.68, 1.7, 0.6), Vector3(0.18, 1.5, 3.2), Color(0.22, 0.3, 0.34), structure, "Resident notice board", "Household-level coordination surface", "housing.dignified_village_block.v0_1", ["makes pod-level coordination visible"], ["Should not become a surveillance or compliance board."])

static func _hygiene_core(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.box(root, "HygieneCoreWall", Vector3(-size.x * 0.5 + 3.2, 1.25, 1.0), Vector3(0.18, 2.4, 4.8), Color(0.68, 0.67, 0.62), true)
    P.fixture_box(root, level, interactable_script, "HygieneCounter", Vector3(-size.x * 0.5 + 1.55, 0.82, 0.6), Vector3(2.2, 0.62, 0.9), Color(0.72, 0.72, 0.68), structure, "Residential hygiene counter", "Pod-level hygiene support fixture", "housing.dignified_village_block.v0_1", ["connects residential dignity to sanitation and daily care assumptions"], ["Final plumbing and accessibility need professional review."])
    P.box(root, "LinenStorage", Vector3(-size.x * 0.5 + 1.0, 1.25, 2.8), Vector3(0.9, 1.9, 1.4), Color(0.52, 0.43, 0.32), true)

static func _threshold_garden(root: Node3D, size: Vector3) -> void:
    P.box(root, "PorchBenchLeft", Vector3(-2.4, 0.36, size.z * 0.5 + 1.4), Vector3(2.2, 0.32, 0.52), Color(0.38, 0.28, 0.2), true)
    P.box(root, "PorchBenchRight", Vector3(2.4, 0.36, size.z * 0.5 + 1.4), Vector3(2.2, 0.32, 0.52), Color(0.38, 0.28, 0.2), true)
    P.box(root, "ResidentPlanter", Vector3(0.0, 0.42, size.z * 0.5 + 2.5), Vector3(4.8, 0.55, 0.7), Color(0.28, 0.48, 0.3), true)

static func _world_from_local(root: Node3D, local: Vector3) -> Vector3:
    return local.rotated(Vector3.UP, root.rotation.y)

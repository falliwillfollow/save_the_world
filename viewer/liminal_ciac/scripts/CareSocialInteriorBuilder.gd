extends RefCounted
class_name CareSocialInteriorBuilder

const P := preload("res://scripts/CiacInteriorPrimitives.gd")
const WALL_T := 0.3
const WALL_H := 3.15
const DOOR_W := 3.6

static func build(level: Node, geometry_root: Node3D, label_root: Node3D, structure: Dictionary, base: Vector3, size: Vector3, color: Color, interactable_script: Script) -> void:
    var root := Node3D.new()
    root.name = str(structure.get("id", "care_social"))
    root.position = base
    root.rotation.y = _rotation_toward_center(base)
    geometry_root.add_child(root)

    P.open_shell(root, size, color, WALL_T, WALL_H, DOOR_W)
    var structure_type := str(structure.get("type", "care_room"))
    if structure_type == "social_cultural":
        _social_commons(root, level, interactable_script, structure, size)
    else:
        _care_room(root, level, interactable_script, structure, size)

    P.plaque(root, level, interactable_script, "CareSocialModulesPlaque", Vector3(-size.x * 0.5 + 0.9, 1.4, size.z * 0.5 - 2.0), structure, "Modules and sources")
    P.bulletin(root, level, interactable_script, "CareSocialStatusBulletin", Vector3(size.x * 0.5 - 0.68, 1.65, size.z * 0.5 - 2.0), structure, "Building bulletin")
    P.label(label_root, str(structure.get("label", "Care Commons")), base + Vector3(0.0, WALL_H + 0.9, 0.0), 28)

static func _care_room(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.box(root, "ReceptionDesk", Vector3(-size.x * 0.5 + 2.0, 0.72, size.z * 0.5 - 3.1), Vector3(2.7, 0.45, 1.0), Color(0.45, 0.34, 0.25), true)
    P.fixture_box(root, level, interactable_script, "CareContinuityTable", Vector3(-1.1, 0.72, -1.4), Vector3(3.3, 0.34, 1.35), Color(0.42, 0.31, 0.25), structure, "Care continuity table", "Opt-in care planning fixture", "care_health.care_health_high_need_meal_illness_support_v0.active", ["represents high-need care coordination and meal/illness support"], ["Resident consent and privacy boundaries must be explicit."])
    P.box(root, "CareSeatA", Vector3(-1.1, 0.42, -2.55), Vector3(2.8, 0.36, 0.5), Color(0.32, 0.48, 0.47), true)
    P.box(root, "CareSeatB", Vector3(-1.1, 0.42, -0.25), Vector3(2.8, 0.36, 0.5), Color(0.32, 0.48, 0.47), true)
    P.fixture_box(root, level, interactable_script, "MedicationContinuityCabinet", Vector3(size.x * 0.5 - 1.0, 1.3, -size.z * 0.5 + 2.5), Vector3(1.1, 2.1, 2.1), Color(0.55, 0.67, 0.72), structure, "Medication continuity cabinet", "Resident-controlled medication continuity fixture", "care_health.care_health_resident_controlled_medication_continuity_kit_v0.active", ["makes medication continuity explicit in the spatial model"], ["Not a prescription, pharmacy, or cold-chain validation."])
    P.fixture_box(root, level, interactable_script, "PrivacyScreen", Vector3(size.x * 0.5 - 3.2, 1.2, 0.6), Vector3(0.16, 2.2, 4.4), Color(0.62, 0.58, 0.55), structure, "Care privacy screen", "Privacy and dignity boundary", "care_health.care_health_high_need_meal_illness_support_v0.active", ["prevents care support from being visually conflated with public monitoring"], ["Privacy protocol remains a governance and consent requirement."])
    P.box(root, "RecoveryBench", Vector3(size.x * 0.5 - 1.7, 0.44, 2.2), Vector3(2.6, 0.38, 0.8), Color(0.38, 0.5, 0.48), true)
    P.fixture_box(root, level, interactable_script, "CareProtocolBoard", Vector3(-size.x * 0.5 + 0.7, 1.75, -size.z * 0.5 + 3.4), Vector3(0.18, 1.6, 3.0), Color(0.22, 0.3, 0.34), structure, "Care protocol board", "Visible care operating protocol", "care_health.care_health_high_need_meal_illness_support_v0.active", ["links care-room fixtures to protocol review and scenario testing"], ["Must avoid exposing private resident information."])

static func _social_commons(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.fixture_box(root, level, interactable_script, "OpenCircleRug", Vector3(0.0, 0.08, -0.2), Vector3(6.4, 0.08, 4.4), Color(0.5, 0.48, 0.58), structure, "Open circle", "Belonging without coercion gathering fixture", "social_cultural_commons.belonging_without_coercion.v0_1", ["supports social connection while remaining non-compulsory"], ["High-, medium-, and low-social-energy alternatives must coexist."])
    for index in range(6):
        var angle := TAU * float(index) / 6.0
        var x := cos(angle) * 3.2
        var z := sin(angle) * 2.2 - 0.2
        P.box(root, "CircleSeat%d" % index, Vector3(x, 0.42, z), Vector3(0.85, 0.36, 0.85), Color(0.32, 0.48, 0.47), true)
    P.fixture_box(root, level, interactable_script, "MakersTable", Vector3(-size.x * 0.5 + 3.0, 0.72, -size.z * 0.5 + 3.0), Vector3(4.0, 0.35, 1.4), Color(0.42, 0.31, 0.25), structure, "Maker table", "Culture and skill-sharing fixture", "social_cultural_commons.belonging_without_coercion.v0_1", ["represents voluntary cultural production and informal learning"], ["Must not become required labor."])
    P.box(root, "MaterialsShelf", Vector3(-size.x * 0.5 + 0.8, 1.35, -size.z * 0.5 + 4.8), Vector3(0.9, 2.0, 3.4), Color(0.5, 0.38, 0.27), true)
    P.fixture_box(root, level, interactable_script, "StoryWall", Vector3(size.x * 0.5 - 0.7, 1.8, -1.0), Vector3(0.18, 1.7, 5.0), Color(0.22, 0.3, 0.34), structure, "Story wall", "Shared meaning and history fixture", "social_cultural_commons.belonging_without_coercion.v0_1", ["makes belonging and shared identity inspectable without reducing it to resource flow"], ["Needs explicit opt-out and anti-capture norms."])
    P.box(root, "LowStimulusNook", Vector3(size.x * 0.5 - 2.2, 0.44, size.z * 0.5 - 3.2), Vector3(2.5, 0.38, 0.8), Color(0.38, 0.5, 0.48), true)

static func _rotation_toward_center(base: Vector3) -> float:
    if absf(base.x) >= absf(base.z):
        if base.x < 0.0:
            return PI * 0.5
        return -PI * 0.5
    if base.z > 0.0:
        return PI
    return 0.0

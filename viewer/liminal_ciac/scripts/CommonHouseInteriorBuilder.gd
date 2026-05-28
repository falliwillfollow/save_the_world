extends RefCounted
class_name CommonHouseInteriorBuilder

const P := preload("res://scripts/CiacInteriorPrimitives.gd")
const WALL_T := 0.32
const WALL_H := 3.25
const DOOR_W := 4.4

static func build(level: Node, geometry_root: Node3D, label_root: Node3D, structure: Dictionary, base: Vector3, size: Vector3, color: Color, interactable_script: Script) -> void:
    var root := Node3D.new()
    root.name = str(structure.get("id", "common_house"))
    root.position = base
    geometry_root.add_child(root)

    _box(root, "Floor", Vector3(0.0, 0.05, 0.0), Vector3(size.x, 0.1, size.z), Color(0.58, 0.53, 0.45), true)
    _box(root, "BackWall", Vector3(0.0, WALL_H * 0.5, -size.z * 0.5), Vector3(size.x, WALL_H, WALL_T), color, true)
    _box(root, "LeftWall", Vector3(-size.x * 0.5, WALL_H * 0.5, 0.0), Vector3(WALL_T, WALL_H, size.z), color, true)
    _box(root, "RightWall", Vector3(size.x * 0.5, WALL_H * 0.5, 0.0), Vector3(WALL_T, WALL_H, size.z), color, true)
    _box(root, "FrontWallLeft", Vector3(-(size.x + DOOR_W) * 0.25, WALL_H * 0.5, size.z * 0.5), Vector3((size.x - DOOR_W) * 0.5, WALL_H, WALL_T), color, true)
    _box(root, "FrontWallRight", Vector3((size.x + DOOR_W) * 0.25, WALL_H * 0.5, size.z * 0.5), Vector3((size.x - DOOR_W) * 0.5, WALL_H, WALL_T), color, true)
    _box(root, "HeaderBeam", Vector3(0.0, WALL_H + 0.18, size.z * 0.5), Vector3(size.x, 0.36, WALL_T), color.lightened(0.12), true)
    _box(root, "EntryMat", Vector3(0.0, 0.08, size.z * 0.5 + 1.6), Vector3(5.2, 0.08, 2.6), Color(0.32, 0.45, 0.43), true)

    _meal_area(root, level, interactable_script, structure)
    _kitchen_area(root, level, interactable_script, structure, size)
    _governance_area(root, level, interactable_script, structure, size)
    _quiet_nooks(root, level, interactable_script, structure, size)
    _plaque(root, level, interactable_script, "CommonHouseModulesPlaque", Vector3(-size.x * 0.5 + 1.0, 1.45, size.z * 0.5 - 2.4), structure, "Module + source plaque")
    _plaque(root, level, interactable_script, "CommonHouseEvidencePlaque", Vector3(size.x * 0.5 - 1.0, 1.45, size.z * 0.5 - 2.4), structure, "Evidence plaque")
    P.bulletin(root, level, interactable_script, "CommonHouseStatusBulletin", Vector3(-size.x * 0.5 + 0.9, 1.65, 0.6), structure, "Building bulletin")

    _label(label_root, str(structure.get("label", "Common House")), base + Vector3(0.0, WALL_H + 0.95, 0.0))
    _label(label_root, "meal commons", base + Vector3(-5.5, 1.15, 0.0), 22)
    _label(label_root, "governance table", base + Vector3(6.4, 1.15, -4.8), 22)
    _label(label_root, "quiet nooks", base + Vector3(7.0, 1.15, 4.4), 22)

static func _meal_area(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary) -> void:
    P.fixture_box(root, level, interactable_script, "MealTable", Vector3(-4.8, 0.78, 0.0), Vector3(7.0, 0.28, 2.2), Color(0.48, 0.34, 0.22), structure, "Shared meal table", "Low-pressure common meal fixture", "social_cultural_commons.belonging_without_coercion.v0_1", ["supports shared meals without requiring private household hosting"], ["Represents a social commons feature, not a mandatory gathering point."])
    _box(root, "MealBenchNorth", Vector3(-4.8, 0.48, -1.65), Vector3(7.2, 0.34, 0.55), Color(0.38, 0.28, 0.2), true)
    _box(root, "MealBenchSouth", Vector3(-4.8, 0.48, 1.65), Vector3(7.2, 0.34, 0.55), Color(0.38, 0.28, 0.2), true)

static func _kitchen_area(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.fixture_box(root, level, interactable_script, "KitchenCounter", Vector3(-size.x * 0.5 + 2.4, 0.95, -size.z * 0.5 + 2.2), Vector3(4.2, 1.1, 1.0), Color(0.68, 0.67, 0.62), structure, "Commons kitchen counter", "Shared meal and care support surface", "", ["makes common meal preparation spatially visible"], ["Food safety and staffing assumptions remain review-dependent."])
    P.fixture_box(root, level, interactable_script, "PantryShelf", Vector3(-size.x * 0.5 + 0.75, 1.45, -size.z * 0.5 + 5.0), Vector3(0.9, 2.1, 4.2), Color(0.54, 0.43, 0.32), structure, "Commons pantry shelf", "Visible short-cycle food storage", "", ["shows where shared food inventory would be tracked"], ["Does not replace the dedicated food commons inventory model."])
    _box(root, "ServiceIsland", Vector3(-1.2, 0.82, -size.z * 0.5 + 3.1), Vector3(4.2, 0.8, 1.3), Color(0.62, 0.58, 0.5), true)

static func _governance_area(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.fixture_box(root, level, interactable_script, "GovernanceTable", Vector3(5.9, 0.76, -size.z * 0.5 + 5.6), Vector3(4.8, 0.28, 2.4), Color(0.42, 0.31, 0.25), structure, "Governance table", "Commons decision workspace", "governance.commons_stewardship_protocol.v0_1", ["anchors decision records and resident review conversations"], ["Does not imply meetings are compulsory."])
    P.fixture_box(root, level, interactable_script, "DecisionBoard", Vector3(size.x * 0.5 - 0.7, 1.85, -size.z * 0.5 + 5.6), Vector3(0.25, 1.8, 4.8), Color(0.22, 0.3, 0.34), structure, "Decision board", "Visible governance log", "governance.commons_stewardship_protocol.v0_1", ["makes governance status inspectable in the embodied model"], ["Must not replace transparent records or due-process review."])

static func _quiet_nooks(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    _box(root, "QuietBenchA", Vector3(size.x * 0.5 - 3.4, 0.48, 2.8), Vector3(3.4, 0.38, 0.8), Color(0.38, 0.5, 0.48), true)
    _box(root, "QuietBenchB", Vector3(size.x * 0.5 - 3.4, 0.48, 5.0), Vector3(3.4, 0.38, 0.8), Color(0.38, 0.5, 0.48), true)
    P.fixture_box(root, level, interactable_script, "PlantingDivider", Vector3(2.0, 1.0, size.z * 0.5 - 3.3), Vector3(0.7, 1.5, 5.2), Color(0.32, 0.48, 0.32), structure, "Quiet nook divider", "Low-stimulation opt-out boundary", "social_cultural_commons.belonging_without_coercion.v0_1", ["supports belonging without requiring high-social-energy participation"], ["Represents a design affordance, not clinical sensory design validation."])

static func _plaque(root: Node3D, level: Node, interactable_script: Script, node_name: String, local_position: Vector3, structure: Dictionary, prompt: String) -> void:
    var body := _box(root, node_name, local_position, Vector3(0.16, 1.25, 2.3), Color(0.95, 0.9, 0.74), true)
    body.set_script(interactable_script)
    var duplicate_value: Variant = structure.duplicate(true)
    var record: Dictionary = {}
    if typeof(duplicate_value) == TYPE_DICTIONARY:
        record = duplicate_value
    record["label"] = "%s - %s" % [str(structure.get("label", "Common House")), prompt]
    body.call("setup", level, "plaque", record)

static func _box(root: Node3D, node_name: String, position: Vector3, size: Vector3, color: Color, has_collision: bool) -> StaticBody3D:
    var body := StaticBody3D.new()
    body.name = node_name
    body.position = position
    root.add_child(body)

    var mesh_instance := MeshInstance3D.new()
    var mesh := BoxMesh.new()
    mesh.size = size
    mesh_instance.mesh = mesh
    mesh_instance.material_override = _material(color)
    body.add_child(mesh_instance)

    if has_collision:
        var collision := CollisionShape3D.new()
        var shape := BoxShape3D.new()
        shape.size = size
        collision.shape = shape
        body.add_child(collision)

    return body

static func _label(label_root: Node3D, text: String, position: Vector3, font_size: int = 30) -> void:
    pass

static func _material(color: Color) -> StandardMaterial3D:
    var mat := StandardMaterial3D.new()
    mat.albedo_color = color
    mat.roughness = 0.86
    return mat
